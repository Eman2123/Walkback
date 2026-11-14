// Owner: Urooj. Areas, coverage with its CI, Brier score, cache flag.
import { fmtCI, fmtKm2, fmtPct } from "../lib/format.js";

export default function ResultsPanel({ run, busy }) {
  if (!run) return <p className="text-sm text-slate-500">Click the map to place the habitat.</p>;
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
      <p className="text-xs text-slate-400">Coverage below 95 % is a shortfall, not a pass.</p>
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
