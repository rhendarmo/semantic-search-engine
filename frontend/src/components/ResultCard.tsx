import type { SearchResult } from "@/lib/types";

export default function ResultCard({ result }: { result: SearchResult }) {
  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-zinc-200">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="text-base font-semibold text-zinc-900">
            {result.title}{" "}
            {result.year ? (
              <span className="text-sm font-medium text-zinc-500">
                ({result.year})
              </span>
            ) : null}
          </h3>

          <div className="mt-1 flex flex-wrap gap-2">
            {result.genres?.map((g) => (
              <span
                key={g}
                className="rounded-full bg-zinc-100 px-2.5 py-1 text-xs font-medium text-zinc-700"
              >
                {g}
              </span>
            ))}
          </div>
        </div>

        {/* Similarity score */}
        <div className="shrink-0 rounded-xl bg-zinc-900 px-3 py-2 text-xs font-semibold text-white">
          {Math.round(result.score * 100)}%
        </div>
      </div>

      <p className="mt-3 text-sm leading-relaxed text-zinc-700">
        {result.overview}
      </p>
    </div>
  );
}
