import type { SearchResponse } from "@/lib/types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL;

export async function searchMovies(params: {
  query: string;
  top_k: number;
  model_name?: string;
}): Promise<SearchResponse> {
  if (!API_BASE) {
    throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
  }

  const res = await fetch(`${API_BASE}/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      query: params.query,
      top_k: params.top_k,
      model_name: params.model_name ?? "sentence-transformers/all-MiniLM-L6-v2",
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json();
}

export type QAResponse = {
  question: string;
  query: string;
  top_k: number;
  llm_model: string;
  answer: string;
  citations: { ref: string; title: string; movie_id: number }[];
  results_used: any[];
};

export async function askQA(params: {
  question: string;
  query: string;
  top_k: number;
  model_name?: string;
  llm_model?: string;
}): Promise<QAResponse> {
  if (!API_BASE) throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");

  const res = await fetch(`${API_BASE}/qa`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question: params.question,
      query: params.query,
      top_k: params.top_k,
      model_name: params.model_name ?? "sentence-transformers/all-MiniLM-L6-v2",
      llm_model: params.llm_model ?? "gpt-5.2",
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(`API error ${res.status}: ${text}`);
  }

  return res.json();
}