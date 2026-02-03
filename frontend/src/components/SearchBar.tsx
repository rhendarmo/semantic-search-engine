type Props = {
  query: string;
  setQuery: (v: string) => void;
  topK: number;
  setTopK: (v: number) => void;
  onSearch: () => void;
  loading: boolean;
};

export default function SearchBar({
  query,
  setQuery,
  topK,
  setTopK,
  onSearch,
  loading,
}: Props) {
  return (
    <div className="flex flex-col gap-2 sm:flex-row sm:items-center">
      <div className="flex-1">
        <label className="mb-1 block text-xs font-medium text-zinc-700">
          Search movies
        </label>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder='e.g., "mind-bending sci-fi with emotional ending"'
          className="w-full rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm outline-none ring-0 placeholder:text-zinc-400 focus:border-zinc-300 focus:ring-2 focus:ring-zinc-200"
        />
      </div>

      <div className="flex items-end gap-2">
        <div className="w-28">
          <label className="mb-1 block text-xs font-medium text-zinc-700">
            Top
          </label>
          <select
            value={topK}
            onChange={(e) => setTopK(Number(e.target.value))}
            className="w-full rounded-xl border border-zinc-200 bg-white px-3 py-3 text-sm outline-none focus:ring-2 focus:ring-zinc-200"
          >
            <option value={5}>5</option>
            <option value={10}>10</option>
            <option value={15}>15</option>
          </select>
        </div>

        <button
          className="rounded-xl bg-zinc-900 px-4 py-3 text-sm font-medium text-white shadow-sm hover:bg-zinc-800 active:bg-zinc-950 disabled:opacity-60"
          type="button"
          onClick={onSearch}
          disabled={loading || query.trim().length === 0}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>
    </div>
  );
}