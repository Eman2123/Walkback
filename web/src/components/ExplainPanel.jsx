// Owner: Urooj. Plain-language explanation from the API. Shows the fallback text when the explainer is unavailable.
export default function ExplainPanel({ onExplain, text, loading, disabled }) {
  return (
    <div className="space-y-2">
      <button
        type="button"
        onClick={onExplain}
        disabled={disabled || loading}
        className="rounded bg-slate-900 px-3 py-1.5 text-sm text-white disabled:opacity-40"
      >
        {loading ? "Explaining…" : "Explain this result"}
      </button>
      {text && <p className="text-sm text-slate-700">{text}</p>}
    </div>
  );
}
