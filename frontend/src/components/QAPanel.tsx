type Citation = { ref: string; title: string; movie_id: number };

type Props = {
  question: string;
  setQuestion: (v: string) => void;
  onAsk: () => void;
  loading: boolean;
  answer: string | null;
  error: string | null;
  citations: Citation[];
};

export default function QAPanel({
  question,
  setQuestion,
  onAsk,
  loading,
  answer,
  error,
  citations,
}: Props) {
  return (
    <div className="rounded-2xl bg-white p-4 shadow-sm ring-1 ring-zinc-200">
      <h2 className="text-sm font-semibold text-zinc-800">
        Ask a question (RAG)
      </h2>
      <p className="mt-1 text-xs text-zinc-500">
        Answers are grounded in your retrieved top results and include citations.
      </p>

      <div className="mt-4">
        <label className="mb-1 block text-xs font-medium text-zinc-700">
          Question
        </label>
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder='e.g., "Which of these movies has the most hopeful ending and why?"'
          rows={4}
          className="w-full resize-none rounded-xl border border-zinc-200 bg-white px-3 py-2 text-sm outline-none placeholder:text-zinc-400 focus:ring-2 focus:ring-zinc-200"
        />
      </div>

      <button
        type="button"
        onClick={onAsk}
        disabled={loading || question.trim().length === 0}
        className="mt-3 w-full rounded-xl bg-zinc-900 px-4 py-2.5 text-sm font-medium text-white hover:bg-zinc-800 active:bg-zinc-950 disabled:opacity-60"
      >
        {loading ? "Answering..." : "Answer"}
      </button>

      {error ? (
        <p className="mt-3 text-sm text-red-600">{error}</p>
      ) : null}

      <div className="mt-4 rounded-xl bg-zinc-50 p-3 text-sm text-zinc-700 ring-1 ring-zinc-200">
        <p className="text-xs font-semibold text-zinc-600">Answer</p>

        {answer ? (
          <>
            <p className="mt-2 whitespace-pre-wrap text-sm text-zinc-800">
              {answer}
            </p>

            {citations.length > 0 ? (
              <div className="mt-3">
                <p className="text-xs font-semibold text-zinc-600">Citations</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {citations.map((c) => (
                    <span
                      key={`${c.ref}-${c.movie_id}`}
                      className="rounded-full bg-white px-2.5 py-1 text-xs font-medium text-zinc-700 ring-1 ring-zinc-200"
                      title={`TMDb ID: ${c.movie_id}`}
                    >
                      {c.ref} {c.title}
                    </span>
                  ))}
                </div>
              </div>
            ) : null}
          </>
        ) : (
          <p className="mt-2 text-sm text-zinc-600">
            Ask a question to see a grounded answer here.
          </p>
        )}
      </div>
    </div>
  );
}
