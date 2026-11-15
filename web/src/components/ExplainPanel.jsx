// Owner: Urooj. Plain-language explanation from the API. Shows the fallback text when the explainer is unavailable.
export default function ExplainPanel({ onExplain, text, loading, disabled }) {
  return (
    <div className="space-y-3">
      <div>
        <h2 className="px-title">Plain-language summary</h2>
        <p className="mt-2 text-sm leading-tight text-mute">
          An AI assistant explains the stored result above in simple words. It can only use numbers that
          appear in the run. If that check fails, a fallback text is shown instead.
        </p>
      </div>

      <button type="button" onClick={onExplain} disabled={disabled || loading} className="px-btn w-full">
        {loading ? "Explaining…" : "Explain this result"}
      </button>

      {text && (
        <div role="status" className="px-inset p-3">
          <p className="mb-2 font-pixel text-[8px] uppercase text-mute">Explanation</p>
          <p className="text-base leading-snug text-cream">{text}</p>
        </div>
      )}
    </div>
  );
}
