// Owner: Urooj. Areas, coverage with its CI, Brier score, cache flag.
import { fmtCI, fmtKm2, fmtPct } from "../lib/format.js";

export default function ResultsPanel({ run, busy }) {
   if (!run) {
    return <p className="text-sm text-slate-500">{busy ? "Computing…" : "Waiting for the first result."}</p>;
  }
  const s = run.stats;
  return (
    <div className="space-y-2 text-sm">
      <div className="grid grid-cols-2 gap-2">
        <Stat label="Deterministic" value={`${fmtKm2(s.area_km2.deterministic)} km²`} />
        <Stat label="Calibrated" value={`${fmtKm2(s.area_km2.calibrated)} km²`} />
        <Stat label="Truth (1 m)" value={`${fmtKm2(s.area_km2.truth)} km²`} />
        <Stat label="Coverage of truth" value={`${fmtPct(s.coverage)}${fmtCI(s.coverage_ci)}`} />
      </div>
      <p className="text-slate-500">
        Brier score {s.brier} (lower is better). {run.cached ? "From cache." : "Computed now."}
        {busy ? " Updating…" : ""}
      </p>
           
         {s.coverage == null ? (
        <p className="text-xs text-slate-500">
          Coverage is not available for this run (the truth area is empty).
        </p>
      ) : s.coverage < 0.95 ? (
        <p className="rounded bg-rose-50 p-2 text-xs font-semibold text-rose-800">
          Shortfall: coverage is below 95 %. This is reported as a failure, not a pass.
        </p>
      ) : (
        <p className="text-xs text-slate-400">Coverage is 95 % or higher for this run.</p>
      )}


    </div>
  );
}

function Stat({ label, value }) {
  return (
    <div className="rounded border border-slate-200 p-2">
      <div className="text-xs text-slate-500">{label}</div>
      <div className="font-semibold">{value}</div>
    </div>
  );
}
