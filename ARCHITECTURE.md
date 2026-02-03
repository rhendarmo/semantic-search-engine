# 🏗️ Architecture

This document describes the system architecture for **Movie Semantic Search Engine**: a semantic search + RAG (question answering) web app built on TMDb data, Sentence Transformer embeddings, FastAPI, and a Next.js UI.

---

## 1) High-level Overview

**Goal:** Let users search movies semantically (embeddings + cosine similarity), retrieve Top-K results, and ask grounded questions answered using only retrieved evidence (RAG).

**Core idea:**
- Precompute embeddings for a curated corpus of ~100–500 movie documents
- Serve fast similarity search from an in-memory embedding matrix
- Provide a QA endpoint that retrieves evidence and calls an LLM to generate grounded answers with citations
- Frontend is a thin UI that calls backend APIs and renders results/answers

---

## 2) System Components

### Frontend (Next.js)
- Presents search UI and results list
- Presents QA panel for RAG questions and citations
- Sends requests to backend over HTTP (JSON)

**Key responsibilities**
- User input: query string, Top-K selection
- Display: results with similarity scores and metadata
- QA: question text, answer output, citation chips
- Environment: reads `NEXT_PUBLIC_API_BASE_URL` to locate backend

---

### Backend (FastAPI)
- Ingestion from TMDb API (popular list + details)
- Transformation into clean corpus JSONL
- Embedding creation (Sentence Transformer)
- Search service (cosine similarity)
- QA service (RAG: retrieve → build evidence → call LLM → answer + citations)

**Key responsibilities**
- Provide stable JSON API for the UI
- Cache heavy assets in-process (embedding matrix + doc index + embedding model)
- Keep secrets server-side (TMDb token, OpenAI key)

---

### External Services
- **TMDb API**: Source of movie metadata & overviews
- **OpenAI API**: LLM for grounded QA responses

---

## 3) Data Model

### 3.1 Raw TMDb Record (stored as JSONL)
File: `backend/data/movies_raw.jsonl`  
- One JSON per line
- Direct movie detail responses from TMDb `/movie/{id}`

### 3.2 Normalized Corpus Document
File: `backend/data/movies_corpus.jsonl`  
Each line is a normalized document:

- `doc_id` (string): `movie_{tmdb_id}`
- `movie_id` (int): TMDb movie id
- `title` (string)
- `year` (int|null)
- `genres` (string[])
- `rating` (float|null)
- `vote_count` (int|null)
- `overview` (string)
- `combined_text` (string): the text used for embeddings (title/year/genres/overview/etc.)
- `metadata` (object): extra TMDb fields (language, popularity, release_date, etc.)

**Why `combined_text`?**
- Produces consistent embedding inputs
- Keeps embedding text separate from UI metadata

### 3.3 Embeddings + Index
- `backend/data/embeddings.npy`: `float32` numpy array, shape `(N, D)`
- `backend/data/doc_index.json`: list of metadata aligned to embedding rows

**Normalization**
- Embeddings are stored normalized (`normalize_embeddings=True`)
- Cosine similarity reduces to a dot product: `scores = embeddings @ q`

---

## 4) API Surface

### 4.1 Health
`GET /health`
- Returns `{ "status": "ok" }`

### 4.2 Ingestion
`POST /ingest?limit=200&language=en-US`
- Fetch movie IDs from TMDb “popular” pages
- Fetch details for each ID
- Write to `movies_raw.jsonl`

### 4.3 Transform
`POST /transform?min_overview_chars=20`
- Read `movies_raw.jsonl`
- Normalize into `movies_corpus.jsonl`
- Build `combined_text`

### 4.4 Embedding Build
`POST /embed?model_name=sentence-transformers/all-MiniLM-L6-v2&batch_size=32&normalize=true`
- Load `movies_corpus.jsonl`
- Embed each `combined_text`
- Save `embeddings.npy` and `doc_index.json`

### 4.5 Search
`POST /search`
Body:
```json
{
  "query": "space exploration with emotional ending",
  "top_k": 10,
  "model_name": "sentence-transformers/all-MiniLM-L6-v2"
}
```

Response:
- Top-K results with similarity score, plus metadata used by the UI

### 4.6 QA (RAG)
`POST /qa`
Body:
```json
{
  "question": "Which movie best matches the query and why?",
  "query": "space exploration with emotional ending",
  "top_k": 5,
  "model_name": "sentence-transformers/all-MiniLM-L6-v2",
  "llm_model": "gpt-5.2"
}
```

Response:
- `answer`: grounded response
- `citations`: mapping evidence slots `[1]..[K]` to titles + ids
- `results_used`: the retrieved evidence set

---

## 5) Request Flows

### 5.1 Offline/Build-time Pipeline (index creation)
1. **/ingest** → `movies_raw.jsonl`
2. **/transform** → `movies_corpus.jsonl`
3. **/embed** → `embeddings.npy` + `doc_index.json`

This pipeline is run once during setup or when updating the corpus.

### 5.2 Online Search Flow
1. User enters query in UI
2. UI calls **POST /search**
3. Backend:
   - embeds query
   - computes similarities
   - returns top-K results
4. UI renders result cards

### 5.3 Online QA Flow (RAG)
1. User enters question in UI
2. UI calls **POST /qa**
3. Backend:
   - retrieves top-K evidence via embeddings
   - builds compact evidence context
   - calls LLM
   - returns answer + citations
4. UI renders answer and citation chips

---

## 6) Caching & Performance

### In-process caches (backend)
The backend caches:
- Sentence Transformer model instance
- Embedding matrix loaded from `embeddings.npy`
- Doc index loaded from `doc_index.json`

**Benefit:** Search/QA requests avoid disk reads and repeated model loads.

### Complexity
- Search: `O(N*D)` dot product per request (fast for N~100–10k)
- For larger N, use ANN indexing (FAISS) — see “Scaling”.

---

## 7) Security & Secrets

### Secrets must be server-side only
- `TMDB_API_READ_TOKEN` (backend)
- `OPENAI_API_KEY` (backend)

Frontend environment:
- `NEXT_PUBLIC_API_BASE_URL` is safe to expose (no secrets)

### CORS
Backend allows frontend origin(s) via CORS middleware, e.g.:
- `http://localhost:3000` (dev)
- production domain(s) (Vercel URL)

---

## 8) Deployment Considerations

### Recommended free-tier deployment
- Frontend: Vercel
- Backend: Render (or similar)

**Important**
- Ensure `DATA_DIR` has the embedding artifacts available at runtime:
  - commit `embeddings.npy` + `doc_index.json`, OR
  - generate them during build/startup (more complex)
- Free-tier hosts may sleep → cold starts

---

## 9) Failure Modes & Observability

### Common issues
- Missing env vars: startup failure or 500 errors
- Missing embedding files: `/search` and `/qa` fail until `/embed` is run
- Quota/rate limits: LLM API errors (429)
- CORS misconfig: frontend cannot call backend

### Recommended logging
- Log all endpoint errors with stack traces (server logs)
- Add structured logs for:
  - request IDs
  - query strings (cautiously)
  - latency timings
  - LLM error codes (no secrets)

---

## 10) Scaling Roadmap (Optional Enhancements)

### Search scaling
- Replace brute-force dot product with **FAISS** ANN index
- Store vectors in FAISS, keep doc index aligned
- Add filters (genre/year) via metadata filtering before ANN or after

### QA improvements
- Evidence selection: allow user to pick which movies are used as evidence
- Streaming: stream LLM output to UI (better UX)
- Guardrails: stricter grounding, citation enforcement, refusal on insufficient evidence

### Data growth
- Increase corpus size: ingest multiple TMDb lists (top rated, now playing, upcoming)
- Add periodic re-index job

---

## 11) Environment Variables

### Backend (`backend/.env`)
- `TMDB_API_READ_TOKEN`
- `TMDB_BASE_URL`
- `DATA_DIR`
- `OPENAI_API_KEY`

### Frontend (`frontend/.env.local`)
- `NEXT_PUBLIC_API_BASE_URL`

---

## 12) Notes on Reproducibility

- Index artifacts are deterministic given:
  - corpus input
  - embedding model version
- If the corpus changes, you must rerun:
  - `/transform` → `/embed`
- Keep a record of:
  - embedding model name
  - embedding normalization setting
  - corpus version/date

---

## 13) Diagram (Text)

```
+------------------+        HTTP JSON         +---------------------------+
|   Next.js UI     |  <-------------------->  |      FastAPI Backend      |
|  (localhost:3000)|                         |  (localhost:8000)         |
+------------------+                         +---------------------------+
        |                                               |
        |  /search: query, top_k                        |  Loads embeddings.npy
        |---------------------------------------------->|  Loads doc_index.json
        |                                               |  Embeds query (ST)
        |                                               |  Dot product scores
        |<----------------------------------------------|  Returns top-K results
        |
        |  /qa: question + query + top_k                |  Retrieves evidence
        |---------------------------------------------->|  Builds evidence context
        |                                               |  Calls OpenAI LLM
        |<----------------------------------------------|  Returns answer + citations
        |
        v
  Displays results + answer
```
