// // Owner: Urooj. Areas, coverage with its CI, Brier score, cache flag.
// import { fmtCI, fmtKm2, fmtPct } from "../lib/format.js";

// export default function ResultsPanel({ run, busy }) {
//    if (!run) {
//     return <p className="text-sm text-slate-500">{busy ? "Computing…" : "Waiting for the first result."}</p>;
//   }
//   const s = run.stats;
//   return (
//     <div className="space-y-2 text-sm">
//       <div className="grid grid-cols-2 gap-2">
//         <Stat label="Deterministic" value={`${fmtKm2(s.area_km2.deterministic)} km²`} />
//         <Stat label="Calibrated" value={`${fmtKm2(s.area_km2.calibrated)} km²`} />
//         <Stat label="Truth (1 m)" value={`${fmtKm2(s.area_km2.truth)} km²`} />
//         <Stat label="Coverage of truth" value={`${fmtPct(s.coverage)}${fmtCI(s.coverage_ci)}`} />
//       </div>
//       <p className="text-slate-500">
//         Brier score {s.brier} (lower is better). {run.cached ? "From cache." : "Computed now."}
//         {busy ? " Updating…" : ""}
//       </p>
           
//          {s.coverage == null ? (
//         <p className="text-xs text-slate-500">
//           Coverage is not available for this run (the truth area is empty).
//         </p>
//       ) : s.coverage < 0.95 ? (
//         <p className="rounded bg-rose-50 p-2 text-xs font-semibold text-rose-800">
//           Shortfall: coverage is below 95 %. This is reported as a failure, not a pass.
//         </p>
//       ) : (
//         <p className="text-xs text-slate-400">Coverage is 95 % or higher for this run.</p>
//       )}


//     </div>
//   );
// }

// function Stat({ label, value }) {
//   return (
//     <div className="rounded border border-slate-200 p-2">
//       <div className="text-xs text-slate-500">{label}</div>
//       <div className="font-semibold">{value}</div>
//     </div>
//   );
// }
 // Owner: Urooj. Areas, coverage with its CI, Brier score, cache flag.
import { fmtCI, fmtKm2, fmtPct, LABEL_CLASS } from "../lib/format.js";

export default function ResultsPanel({ run, busy }) {
  if (!run) {
    return <p className="text-sm text-slate-500">{busy ? "Computing…" : "Waiting for the first result."}</p>;
  }
  const s = run.stats;
  const short = s.coverage != null && s.coverage < 0.95;

  return (
    <div className="space-y-4 text-sm">
      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Kpi label="Deterministic" value={fmtKm2(s.area_km2.deterministic)} unit="km²" bar="bg-blue-500" />
        <Kpi label="Calibrated" value={fmtKm2(s.area_km2.calibrated)} unit="km²" bar="bg-emerald-500" />
        <Kpi label="Truth (1 m)" value={fmtKm2(s.area_km2.truth)} unit="km²" bar="bg-amber-500" />
        <Kpi
          label="Coverage of truth"
          value={fmtPct(s.coverage)}
          sub={fmtCI(s.coverage_ci).trim()}
          bar={short ? "bg-rose-500" : "bg-emerald-500"}
        />
      </div>

      {s.coverage == null ? (
        <p className="text-xs text-slate-500">Coverage is not available for this run (the truth area is empty).</p>
      ) : short ? (
        <p className="rounded-lg bg-rose-50 p-3 text-xs font-semibold text-rose-800">
          Shortfall: coverage is below 95 %. This is reported as a failure, not a pass.
        </p>
      ) : (
        <p className="text-xs text-slate-500">Coverage is 95 % or higher for this run.</p>
      )}

      <p className="text-xs text-slate-500">
        Brier score {s.brier} (lower is better). {run.cached ? "From cache." : "Computed now."}
        {busy ? " Updating…" : ""}
      </p>
    </div>
  );
}

function Kpi({ label, value, unit, sub, bar }) {
  return (
    <div className="relative overflow-hidden rounded-lg border border-slate-200 bg-slate-50 p-3 pl-4">
      <span className={`absolute inset-y-0 left-0 w-1 ${bar}`} />
      <div className="flex items-center justify-between gap-2">
        <span className="text-xs text-slate-500">{label}</span>
        <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-semibold uppercase ${LABEL_CLASS.derived}`}>
          derived
        </span>
      </div>
      <div className="mt-1 text-xl font-semibold text-slate-900">
        {value}
        {unit && <span className="ml-1 text-xs font-normal text-slate-500">{unit}</span>}
      </div>
      {sub && <div className="text-xs text-slate-500">{sub}</div>}
    </div>
  );
}




