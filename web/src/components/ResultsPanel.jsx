// Owner: Urooj. Areas, coverage with its CI, Brier score, cache flag.
import { fmtCI, fmtKm2, fmtPct, LABEL_CLASS } from "../lib/format.js";

export default function ResultsPanel({ run, busy }) {
  if (!run) {
    return <p className="text-base text-mute">{busy ? "Computing…" : "Waiting for the first result."}</p>;
  }
  const s = run.stats;
  const short = s.coverage != null && s.coverage < 0.95;

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">
        <Kpi label="Deterministic" value={fmtKm2(s.area_km2.deterministic)} unit="km²" bar="bg-aqua" />
        <Kpi label="Calibrated" value={fmtKm2(s.area_km2.calibrated)} unit="km²" bar="bg-neon" />
        <Kpi label="Truth (1 m)" value={fmtKm2(s.area_km2.truth)} unit="km²" bar="bg-sun" />
        <Kpi
          label="Coverage of truth"
          value={fmtPct(s.coverage)}
          sub={fmtCI(s.coverage_ci).trim()}
          bar={short ? "bg-blush" : "bg-neon"}
        />
      </div>

      {s.coverage == null ? (
        <p className="text-sm text-mute">Coverage is not available for this run (the truth area is empty).</p>
      ) : short ? (
        <p role="alert" className="border-4 border-ink bg-blush p-3 text-sm font-bold text-ink shadow-[4px_4px_0_0_#0d0814]">
          SHORTFALL: coverage is below 95 %. This is reported as a failure, not a pass.
        </p>
      ) : (
        <p className="text-sm text-mute">Coverage is 95 % or higher for this run.</p>
      )}

      <p className="text-sm text-mute">
        Brier score <span className="text-cream">{s.brier}</span> (lower is better
        {s.brier_baseline != null && (
          <>
            ; a forecast with no skill scores <span className="text-cream">{s.brier_baseline}</span>
            {s.brier > s.brier_baseline ? ", so this one is worse than no forecast" : ""}
          </>
        )}
        ).{" "}
        {run.cached ? "From cache." : "Computed now."}
        {busy ? " Updating…" : ""}
      </p>
    </div>
  );
}

function Kpi({ label, value, unit, sub, bar }) {
  return (
    <div className="px-inset relative p-3 pl-5">
      <span className={`absolute inset-y-0 left-0 w-2 ${bar}`} />
      <div className="flex items-start justify-between gap-2">
        <span className="text-xs leading-tight text-mute">{label}</span>
        <span className={`px-chip ${LABEL_CLASS.derived}`}>derived</span>
      </div>
      <div className="mt-2 font-pixel text-base leading-tight text-sun">
        {value}
        {unit && <span className="ml-1 text-[9px] text-mute">{unit}</span>}
      </div>
      {sub && <div className="mt-1 text-xs text-mute">{sub}</div>}
    </div>
  );
}
