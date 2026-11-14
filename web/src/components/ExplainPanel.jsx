// // Owner: Urooj. Plain-language explanation from the API. Shows the fallback text when the explainer is unavailable.
// export default function ExplainPanel({ onExplain, text, loading, disabled }) {
//   return (
//     <div className="space-y-2">
//       <button
//         type="button"
//         onClick={onExplain}
//         disabled={disabled || loading}
//         className="rounded bg-slate-900 px-3 py-1.5 text-sm text-white disabled:opacity-40"
//       >
//         {loading ? "Explaining…" : "Explain this result"}
//       </button>
//       {text && <p className="text-sm text-slate-700">{text}</p>}
//     </div>
//   );
// }
// Owner: Urooj. Plain-language explanation from the API. Shows the fallback text when the explainer is unavailable.
export default function ExplainPanel({ onExplain, text, loading, disabled }) {
  return (
    <div className="space-y-3">
      <div>
        <h2 className="text-xs font-semibold uppercase tracking-wider text-slate-500">Plain-language summary</h2>
        <p className="mt-1 text-xs text-slate-500">
          An AI assistant explains the stored result above in simple words. It can only use numbers that
          appear in the run. If that check fails, a fallback text is shown instead.
        </p>
      </div>

      <button
        type="button"
        onClick={onExplain}
        disabled={disabled || loading}
        className="flex w-full items-center justify-center gap-2 rounded-md bg-slate-900 px-3 py-2 text-sm font-medium text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {loading && (
          <span
            className="h-3 w-3 animate-spin rounded-full border-2 border-white/40 border-t-white"
            aria-hidden="true"
          />
        )}
        {loading ? "Explaining…" : "Explain this result"}
      </button>

      {text && (
        <div role="status" className="rounded-lg border border-slate-200 bg-slate-50 p-3">
          <p className="mb-1 text-[10px] font-semibold uppercase tracking-wider text-slate-400">
            Explanation
          </p>
          <p className="text-sm leading-relaxed text-slate-700">{text}</p>
        </div>
      )}
    </div>
  );
}




