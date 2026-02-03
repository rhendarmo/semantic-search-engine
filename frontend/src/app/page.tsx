"use client";

import React, { useState } from "react";
import SearchBar from "@/components/SearchBar";
import ResultCard from "@/components/ResultCard";
import QAPanel from "@/components/QAPanel";
import { searchMovies, askQA } from "@/lib/api";
import type { SearchResult } from "@/lib/types";

export default function HomePage() {
  const [query, setQuery] = useState("space exploration with emotional ending");
  const [topK, setTopK] = useState(10);
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [question, setQuestion] = useState(
  "Which movie in these results is most aligned with space exploration and an emotional ending? Explain briefly."
  );
  const [qaLoading, setQaLoading] = useState(false);
  const [qaError, setQaError] = useState<string | null>(null);
  const [answer, setAnswer] = useState<string | null>(null);
  const [citations, setCitations] = useState<{ ref: string; title: string; movie_id: number }[]>([]);


  async function handleSearch() {
    setLoading(true);
    setError(null);
    try {
      const data = await searchMovies({ query, top_k: topK });
      setResults(data.results);
    } catch (e: any) {
      setError(e?.message ?? "Something went wrong");
    } finally {
      setLoading(false);
    }
  }

  async function handleAsk() {
    setQaLoading(true);
    setQaError(null);
    try {
      // If user hasn't searched yet, do a search first so QA has evidence
      let currentResults = results;
      if (currentResults.length === 0) {
        const data = await searchMovies({ query, top_k: topK });
        currentResults = data.results;
        setResults(currentResults);
      }

      const qa = await askQA({
        question,
        query,     // we use the same search query to retrieve evidence
        top_k: topK,
      });

      setAnswer(qa.answer);
      setCitations(qa.citations ?? []);
    } catch (e: any) {
      setQaError(e?.message ?? "QA failed");
    } finally {
      setQaLoading(false);
    }
  }

  return (
    <main className="mx-auto max-w-6xl p-6">
      {/* Header */}
      <header className="mb-6 flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">
            Semantic Search Engine for Movies
          </h1>
          <p className="mt-1 text-sm text-zinc-600">
            Embedding-based search + QA (TMDb + Sentence Transformers + FastAPI)
          </p>
        </div>
      </header>

      {/* Controls */}
      <section className="mb-6 rounded-2xl bg-white p-4 shadow-sm ring-1 ring-zinc-200">
        <div className="flex flex-col gap-4">
          <SearchBar
            query={query}
            setQuery={setQuery}
            topK={topK}
            setTopK={setTopK}
            onSearch={handleSearch}
            loading={loading}
          />
        </div>

        {error ? (
          <p className="mt-3 text-sm text-red-600">{error}</p>
        ) : null}
      </section>

      {/* Two-column layout */}
      <section className="grid grid-cols-1 gap-6 lg:grid-cols-3">
        {/* Results */}
        <div className="lg:col-span-2">
          <div className="mb-3 flex items-center justify-between">
            <h2 className="text-sm font-semibold text-zinc-800">Results</h2>
            <span className="text-xs text-zinc-500">
              {results.length > 0
                ? `Showing ${results.length} results`
                : "Run a search to see results"}
            </span>
          </div>

          <div className="space-y-3">
            {results.map((r) => (
              <ResultCard key={r.doc_id} result={r} />
            ))}
          </div>
        </div>

        {/* QA Panel */}
        <div className="lg:col-span-1">
          <QAPanel
            question={question}
            setQuestion={setQuestion}
            onAsk={handleAsk}
            loading={qaLoading}
            answer={answer}
            error={qaError}
            citations={citations}
          />
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-10 text-xs text-zinc-500">
        <p>
          Group 10 - Raditya Hendarmo, Teagan White, Gloria Huang, Ernesto Mata, Kyle Biagan
        </p>
      </footer>
    </main>
  );
}