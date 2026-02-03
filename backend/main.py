from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.ingestion.ingest import ingest_movies
from app.ingestion.transform import transform_raw_to_corpus
from app.core.config import settings
from app.embeddings.build import build_embeddings
from app.search.service import search_movies
from app.search.schemas import SearchRequest
from app.qa.schemas import QARequest
from app.qa.service import answer_question_grounded


app = FastAPI(title="Movie Semantic Search API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://semantic-search-engine-six.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(limit: int = 200, language: str = "en-US"):
    return await ingest_movies(limit=limit, language=language)

@app.post("/transform")
def transform(min_overview_chars: int = 20):
    """
    Transform raw TMDb movie JSONL into a normalized corpus JSONL.
    """
    raw_path = os.path.join(settings.DATA_DIR, "movies_raw.jsonl")
    corpus_path = os.path.join(settings.DATA_DIR, "movies_corpus.jsonl")

    if not os.path.exists(raw_path):
        return {
            "error": "movies_raw.jsonl not found. Run /ingest first.",
            "expected_path": raw_path,
        }

    result = transform_raw_to_corpus(
        raw_path=raw_path,
        corpus_path=corpus_path,
        min_overview_chars=min_overview_chars,
    )
    return result

@app.post("/embed")
def embed(
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    batch_size: int = 32,
    normalize: bool = True,
):
    """
    Build embeddings for the cleaned corpus and persist them to disk.
    """
    corpus_path = os.path.join(settings.DATA_DIR, "movies_corpus.jsonl")

    if not os.path.exists(corpus_path):
        return {
            "error": "movies_corpus.jsonl not found. Run /transform first.",
            "expected_path": corpus_path,
        }

    return build_embeddings(
        corpus_path=corpus_path,
        model_name=model_name,
        batch_size=batch_size,
        normalize=normalize,
    )

@app.post("/search")
def search(req: SearchRequest):
    return search_movies(
        query=req.query,
        top_k=req.top_k,
        model_name=req.model_name,
    )

@app.post("/qa")
def qa(req: QARequest):
    return answer_question_grounded(
        question=req.question,
        query=req.query,
        top_k=req.top_k,
        model_name=req.model_name,
        llm_model=req.llm_model,
    )
