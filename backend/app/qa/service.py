from typing import Any, Dict, List
import textwrap

from openai import OpenAI

from app.core.config import settings
from app.search.service import search_movies


def _build_context(results: List[Dict[str, Any]], max_chars: int = 9000) -> str:
    """
    Build a compact evidence context from top-K results.
    Keep it short enough to avoid huge token usage.
    """
    chunks = []
    for i, r in enumerate(results, start=1):
        title = r.get("title", "Unknown")
        year = r.get("year")
        genres = r.get("genres") or []
        overview = r.get("overview") or ""
        movie_id = r.get("movie_id")

        chunk = f"""[{i}] {title} ({year if year else "N/A"}) | id={movie_id}
Genres: {", ".join(genres) if genres else "N/A"}
Overview: {overview}
SimilarityScore: {r.get("score")}
"""
        chunks.append(chunk.strip())

    context = "\n\n".join(chunks).strip()
    return context[:max_chars]


def answer_question_grounded(
    question: str,
    query: str,
    top_k: int,
    model_name: str,
    llm_model: str,
) -> Dict[str, Any]:
    """
    1) Retrieve top-K results with embeddings
    2) Ask LLM to answer using ONLY the retrieved evidence
    3) Return answer + citations
    """
    # Retrieve evidence
    search = search_movies(query=query, top_k=top_k, model_name=model_name)
    if "error" in search:
        return {"error": search["error"]}

    results = search["results"]
    context = _build_context(results)

    system_instructions = textwrap.dedent("""
    You are a helpful assistant for a movie semantic search app.
    You MUST answer using only the provided EVIDENCE.
    If the evidence is insufficient, say you don't have enough information.
    Always include citations as [#] referring to the evidence item number(s).
    Keep the answer clear and concise.
    """).strip()

    user_prompt = textwrap.dedent(f"""
    USER QUESTION:
    {question}

    EVIDENCE (top retrieved movies):
    {context}
    """).strip()

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Responses API (recommended for new projects)
    resp = client.responses.create(
        model=llm_model,
        input=[
            {"role": "system", "content": system_instructions},
            {"role": "user", "content": user_prompt},
        ],
    )

    answer_text = resp.output_text

    # Provide simple citation objects for the UI (titles + ids)
    citations = []
    for i, r in enumerate(results, start=1):
        citations.append({
            "ref": f"[{i}]",
            "title": r.get("title"),
            "movie_id": r.get("movie_id"),
        })

    return {
        "question": question,
        "query": query,
        "top_k": top_k,
        "llm_model": llm_model,
        "answer": answer_text,
        "citations": citations,
        "results_used": results,
    }
