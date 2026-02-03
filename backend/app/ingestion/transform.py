import json
import os
from typing import Dict, Any, List, Optional

from app.core.config import settings


def _safe_int_year(date_str: Optional[str]) -> Optional[int]:
    if not date_str:
        return None
    # TMDb release_date is usually "YYYY-MM-DD"
    try:
        return int(date_str.split("-")[0])
    except Exception:
        return None


def build_combined_text(movie: Dict[str, Any]) -> str:
    """
    Create the text used for embeddings.
    Keep it consistent and informative, but not too long.
    """
    title = movie.get("title") or movie.get("original_title") or ""
    overview = movie.get("overview") or ""
    genres = movie.get("genres") or []
    genre_names = [g.get("name") for g in genres if isinstance(g, dict) and g.get("name")]
    release_year = _safe_int_year(movie.get("release_date"))

    tagline = movie.get("tagline") or ""
    original_language = movie.get("original_language") or ""

    parts = []
    if title:
        parts.append(f"Title: {title}")
    if release_year:
        parts.append(f"Year: {release_year}")
    if genre_names:
        parts.append("Genres: " + ", ".join(genre_names))
    if tagline:
        parts.append(f"Tagline: {tagline}")
    if original_language:
        parts.append(f"Language: {original_language}")
    if overview:
        parts.append(f"Overview: {overview}")

    return "\n".join(parts).strip()


def transform_raw_to_corpus(
    raw_path: str,
    corpus_path: str,
    min_overview_chars: int = 20,
) -> Dict[str, Any]:
    """
    Read movies_raw.jsonl and write normalized movies_corpus.jsonl.

    - Filters out entries with missing/too-short overview (optional)
    - Creates doc_id, combined_text, and metadata fields
    """
    os.makedirs(settings.DATA_DIR, exist_ok=True)

    total_in = 0
    total_out = 0
    dropped_no_overview = 0

    with open(raw_path, "r", encoding="utf-8") as fin, open(corpus_path, "w", encoding="utf-8") as fout:
        for line in fin:
            line = line.strip()
            if not line:
                continue

            total_in += 1
            movie = json.loads(line)

            overview = (movie.get("overview") or "").strip()
            if len(overview) < min_overview_chars:
                dropped_no_overview += 1
                continue

            movie_id = movie.get("id")
            title = movie.get("title") or movie.get("original_title") or ""
            year = _safe_int_year(movie.get("release_date"))
            genres = movie.get("genres") or []
            genre_names = [g.get("name") for g in genres if isinstance(g, dict) and g.get("name")]

            vote_avg = movie.get("vote_average")
            vote_count = movie.get("vote_count")

            combined_text = build_combined_text(movie)

            doc = {
                "doc_id": f"movie_{movie_id}",
                "movie_id": movie_id,
                "title": title,
                "year": year,
                "genres": genre_names,
                "rating": vote_avg,
                "vote_count": vote_count,
                "overview": overview,
                "combined_text": combined_text,
                "metadata": {
                    "tmdb_id": movie_id,
                    "original_title": movie.get("original_title"),
                    "original_language": movie.get("original_language"),
                    "release_date": movie.get("release_date"),
                    "popularity": movie.get("popularity"),
                },
            }

            fout.write(json.dumps(doc, ensure_ascii=False) + "\n")
            total_out += 1

    return {
        "input_file": raw_path,
        "output_file": corpus_path,
        "read": total_in,
        "written": total_out,
        "dropped_no_overview": dropped_no_overview,
    }
