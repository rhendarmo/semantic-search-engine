# 🎬 Movie Semantic Search Engine

A production-ready semantic search web application for movies, built with:

- **FastAPI (Python)** backend
- **Sentence Transformers** for embeddings
- **Cosine similarity search**
- **Next.js (React)** frontend
- **LLM-powered Question Answering (RAG)** using OpenAI
- **TMDb API** as the movie data source

This app allows users to:
- Perform **semantic search** over movies (not keyword search)
- Retrieve **Top-K similar movies**
- Ask **natural language questions** grounded in retrieved results (RAG)
- View **citations** for generated answers

---

## 🧱 Tech Stack

### Backend
- Python 3.10+
- FastAPI
- Sentence Transformers
- NumPy
- OpenAI SDK
- TMDb API

### Frontend
- Node.js 18+
- Next.js (App Router)
- React
- Tailwind CSS

---

## 📂 Project Structure

```
semantic-search-engine/
├── backend/
│   ├── app/
│   │   ├── core/          # config & settings
│   │   ├── ingestion/     # TMDb ingestion + transform
│   │   ├── embeddings/    # embedding builder
│   │   ├── search/        # cosine similarity search
│   │   ├── qa/            # RAG QA logic
│   │
│   ├── data/              # generated data (JSONL, embeddings)
│   ├── main.py            # FastAPI entrypoint
│   ├── .env               # backend environment variables
│
├── frontend/
│   ├── src/
│   │   ├── app/           # Next.js pages
│   │   ├── components/    # UI components
│   │   ├── lib/           # API helpers + types
│   │
│   ├── .env.local         # frontend environment variables
│
└── README.md
```

---

## ✅ Prerequisites

Make sure you have the following installed **before starting**:

### 1️⃣ Python
- **Python 3.10 or 3.11 recommended**
```bash
python --version
```

### 2️⃣ Node.js
- **Node.js 18 or newer**
```bash
node --version
npm --version
```

### 3️⃣ Git
```bash
git --version
```

---

## 🔑 Required API Keys

You will need **two API keys**:

### 1️⃣ TMDb API (Free)
Used to fetch movie data.

- Create an account: https://www.themoviedb.org/
- Generate a **v4 Read Access Token**
- This is free and required

### 2️⃣ OpenAI API (Paid)
Used for the **Question Answering (RAG)** feature.

- Create an API key: https://platform.openai.com/
- Billing must be enabled

---

## 🚀 Local Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/your-username/semantic-search-engine.git
cd semantic-search-engine
```

---

## 🧠 Backend Setup (FastAPI)

### Step 2: Create a Python Virtual Environment
```bash
cd backend
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**
```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

---

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

---

### Step 4: Create Backend Environment File
Create a file:

```
backend/.env
```

Add the following:

```env
TMDB_API_READ_TOKEN=YOUR_TMDB_READ_TOKEN
TMDB_BASE_URL=https://api.themoviedb.org/3
DATA_DIR=./data
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

⚠️ **Never commit this file to GitHub**

---

### Step 5: Run the Backend Server
```bash
uvicorn main:app --reload --port 8000
```

Verify:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health

---

## 📥 Data Preparation (Required Once)

These steps **must be run in order** to prepare the search index.

### Step 6: Ingest Movies from TMDb
In Swagger UI (`/docs`):

**POST** `/ingest`
- `limit`: `120` (or more)

This creates:
```
backend/data/movies_raw.jsonl
```

---

### Step 7: Transform Raw Data
**POST** `/transform`

This creates:
```
backend/data/movies_corpus.jsonl
```

---

### Step 8: Build Embeddings
**POST** `/embed`

This creates:
```
backend/data/embeddings.npy
backend/data/doc_index.json
```

At this point, semantic search is fully ready.

---

## 🖥️ Frontend Setup (Next.js)

### Step 9: Install Frontend Dependencies
```bash
cd ../frontend
npm install
```

---

### Step 10: Create Frontend Environment File
Create:

```
frontend/.env.local
```

Add:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

---

### Step 11: Run the Frontend
```bash
npm run dev
```

Open:
```
http://localhost:3000
```

---

## 🔍 How the App Works

### Semantic Search
1. User enters a natural language query
2. Query is embedded using Sentence Transformers
3. Cosine similarity is computed against precomputed embeddings
4. Top-K movies are returned

### Question Answering (RAG)
1. Top-K movies are retrieved
2. Their content is passed as **evidence**
3. LLM generates a grounded answer
4. Citations are included for transparency

---

## 🧪 Example Queries

**Search**
```
mind-bending sci-fi with emotional ending
```

**QA**
```
Which movie best matches space exploration and an emotional ending? Explain why.
```

---

## ⚠️ Notes & Limitations

- Backend uses **in-memory embedding cache** (fine for ~100–5,000 docs)
- Free deployment services may have **cold starts**
- OpenAI usage incurs cost
- TMDb attribution is required for public deployments

---

## 🛡️ Attribution
> This product uses the TMDB API but is not endorsed or certified by TMDB.

---

## 📌 Next Improvements (Optional)
- FAISS index for large datasets
- Streaming QA responses
- Evidence selection UI
- Hybrid keyword + semantic search
- Authentication

---

## 📄 License
This project is for **educational purposes**.
