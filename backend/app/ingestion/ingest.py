import json
import os
from typing import Dict, List

from app.core.config import settings
from app.tmdb.client import TMDbClient

def ensure_data_dir():
    os.makedirs(settings.DATA_DIR, exist_ok=True)

def jsonl_path(filename: str) -> str:
    return os.path.join(settings.DATA_DIR, filename)

async def ingest_movies(limit: int = 200, language: str = "en-US") -> Dict:
    """
    Fetch 'limit' movies from TMDb Popular list, then fetch details for each movie.
    Save raw detail JSON to data/movies_raw.jsonl.
    """
    ensure_data_dir()

    client = TMDbClient()

    seen_ids = set()
    collected_ids: List[int] = []

    page = 1
    # Collect IDs first (from popular pages)
    while len(collected_ids) < limit:
        data = await client.get_popular_movies_page(page=page, language=language)
        results = data.get("results", [])
        if not results:
            break

        for m in results:
            mid = m.get("id")
            if mid and mid not in seen_ids:
                seen_ids.add(mid)
                collected_ids.append(mid)
                if len(collected_ids) >= limit:
                    break

        page += 1
        if page > 500:  # safety cap
            break

    # Fetch details and write JSONL
    out_file = jsonl_path("movies_raw.jsonl")
    wrote = 0

    with open(out_file, "w", encoding="utf-8") as f:
        for mid in collected_ids:
            details = await client.get_movie_details(movie_id=mid, language=language)
            f.write(json.dumps(details, ensure_ascii=False) + "\n")
            wrote += 1

    return {
        "requested": limit,
        "collected": len(collected_ids),
        "written": wrote,
        "output_file": out_file,
    }
