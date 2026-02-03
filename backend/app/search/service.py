import json
import os
from typing import Any, Dict, List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


# --- Simple in-process cache so we don't reload on every request ---
_CACHE: Dict[str, Any] = {
    "model_name": None,
    "model": None,
    "embeddings": None,   # shape: (N, D), float32, normalized
    "doc_index": None,    # list aligned with embeddings rows
}


def _path(filename: str) -> str:
    return os.path.join(settings.DATA_DIR, filename)


def _load_doc_index(index_path: str) -> List[Dict[str, Any]]:
    with open(index_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_search_assets(model_name: str) -> None:
    """
    Load model + embeddings + doc index into memory (cached).
    Re-load if model_name differs or assets not loaded yet.
    """
    embeddings_path = _path("embeddings.npy")
    index_path = _path("doc_index.json")

    if not os.path.exists(embeddings_path):
        raise FileNotFoundError(f"Missing embeddings file: {embeddings_path}")
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"Missing doc index file: {index_path}")

    need_reload = (
        _CACHE["model"] is None
        or _CACHE["embeddings"] is None
        or _CACHE["doc_index"] is None
        or _CACHE["model_name"] != model_name
    )

    if need_reload:
        _CACHE["model_name"] = model_name
        _CACHE["model"] = SentenceTransformer(model_name)
        _CACHE["embeddings"] = np.load(embeddings_path).astype(np.float32)
        _CACHE["doc_index"] = _load_doc_index(index_path)

        # Basic sanity checks
        emb = _CACHE["embeddings"]
        idx = _CACHE["doc_index"]
        if emb.ndim != 2:
            raise ValueError(f"Embeddings must be 2D, got shape {emb.shape}")
        if len(idx) != emb.shape[0]:
            raise ValueError(
                f"doc_index length ({len(idx)}) must match embeddings rows ({emb.shape[0]})"
            )


def _top_k_indices(scores: np.ndarray, k: int) -> np.ndarray:
    """
    Return indices of top-k scores in descending order.
    Uses argpartition for speed then sorts the small top-k slice.
    """
    k = max(1, min(int(k), scores.shape[0]))
    if k == scores.shape[0]:
        return np.argsort(-scores)

    top = np.argpartition(-scores, kth=k - 1)[:k]
    top_sorted = top[np.argsort(-scores[top])]
    return top_sorted


def search_movies(
    query: str,
    top_k: int = 10,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
) -> Dict[str, Any]:
    """
    Semantic search:
    - embed query (normalized)
    - similarity = dot(query_emb, doc_emb) since both are normalized
    - return top_k docs with scores
    """
    query = (query or "").strip()
    if not query:
        return {"error": "Query is empty."}

    load_search_assets(model_name=model_name)

    model: SentenceTransformer = _CACHE["model"]
    embeddings: np.ndarray = _CACHE["embeddings"]  # (N, D)
    doc_index: List[Dict[str, Any]] = _CACHE["doc_index"]

    # Encode query (normalized to match corpus normalization)
    q = model.encode(
        [query],
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype(np.float32)[0]  # (D,)

    # cosine similarity for normalized vectors = dot product
    scores = embeddings @ q  # (N,)

    top_idx = _top_k_indices(scores, top_k)

    results = []
    for i in top_idx:
        d = doc_index[int(i)]
        results.append(
            {
                "doc_id": d.get("doc_id"),
                "movie_id": d.get("movie_id"),
                "title": d.get("title"),
                "year": d.get("year"),
                "genres": d.get("genres"),
                "rating": d.get("rating"),
                "vote_count": d.get("vote_count"),
                "overview": d.get("overview"),
                "score": float(scores[int(i)]),
            }
        )

    return {
        "query": query,
        "top_k": int(top_k),
        "model_name": model_name,
        "num_docs": int(embeddings.shape[0]),
        "results": results,
    }
