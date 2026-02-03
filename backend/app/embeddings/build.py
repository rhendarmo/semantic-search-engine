import json
import os
from typing import Dict, Any, List, Optional

import numpy as np
from sentence_transformers import SentenceTransformer

from app.core.config import settings


def _path(filename: str) -> str:
    return os.path.join(settings.DATA_DIR, filename)


def load_corpus(corpus_path: str) -> List[Dict[str, Any]]:
    docs = []
    with open(corpus_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            docs.append(json.loads(line))
    return docs


def build_embeddings(
    corpus_path: str,
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
    batch_size: int = 32,
    normalize: bool = True,
) -> Dict[str, Any]:
    """
    Read movies_corpus.jsonl, embed combined_text, and save:
      - embeddings.npy (float32)
      - doc_index.json (list aligned with embeddings rows)

    normalize=True is recommended because it makes cosine similarity simply a dot product later.
    """
    os.makedirs(settings.DATA_DIR, exist_ok=True)

    docs = load_corpus(corpus_path)
    if not docs:
        return {"error": "No documents found in corpus.", "corpus_path": corpus_path}

    texts = [d.get("combined_text", "") for d in docs]
    if any(t.strip() == "" for t in texts):
        # If any document is empty, better to fail now.
        empty_count = sum(1 for t in texts if t.strip() == "")
        return {"error": "Some documents have empty combined_text.", "empty_count": empty_count}

    model = SentenceTransformer(model_name)

    # encode returns a numpy array if convert_to_numpy=True
    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=normalize,
    ).astype(np.float32)

    # Build doc index: keep only fields needed for retrieval + UI
    doc_index = []
    for d in docs:
        doc_index.append(
            {
                "doc_id": d.get("doc_id"),
                "movie_id": d.get("movie_id"),
                "title": d.get("title"),
                "year": d.get("year"),
                "genres": d.get("genres"),
                "rating": d.get("rating"),
                "vote_count": d.get("vote_count"),
                "overview": d.get("overview"),
                "metadata": d.get("metadata", {}),
            }
        )

    embeddings_path = _path("embeddings.npy")
    index_path = _path("doc_index.json")

    np.save(embeddings_path, embeddings)

    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(doc_index, f, ensure_ascii=False, indent=2)

    return {
        "model_name": model_name,
        "normalize_embeddings": normalize,
        "batch_size": batch_size,
        "num_docs": len(doc_index),
        "embedding_dim": int(embeddings.shape[1]),
        "embeddings_file": embeddings_path,
        "doc_index_file": index_path,
    }
