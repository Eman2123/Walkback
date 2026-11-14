// // Owner: Urooj. Sliders. Each one shows its label: assumed or derived.
// import { LABEL_CLASS } from "../lib/format.js";

// const FIELDS = [
//   { key: "budget_s", label: "Time budget (s)", min: 300, max: 1800, step: 60, tag: "assumed" },
//   { key: "speed_mps", label: "Walking speed (m/s, flat)", min: 0.3, max: 1.0, step: 0.05, tag: "assumed" },
//   { key: "cutoff_deg", label: "Slope cutoff (deg)", min: 10, max: 30, step: 1, tag: "assumed" },
//   { key: "confidence", label: "Confidence threshold", min: 0.5, max: 0.95, step: 0.05, tag: "derived" },
//   { key: "roughness", label: "Unresolved roughness", min: 0, max: 1, step: 0.05, tag: "assumed" },
// ];

// export default function ControlPanel({ params, onChange }) {
//   return (
//     <div className="space-y-4">
//       {FIELDS.map((f) => (
//         <label key={f.key} className="block text-sm">
//           <div className="flex justify-between">
//             <span>{f.label}</span>
//             <span className="font-mono">{params[f.key]}</span>
//           </div>
//           <input
//             type="range"
//             className="w-full"
//             min={f.min}
//             max={f.max}
//             step={f.step}
//             value={params[f.key]}
//             onChange={(e) => onChange(f.key, Number(e.target.value))}
//           />
//           <span className={`mt-1 inline-block rounded px-2 py-0.5 text-xs ${LABEL_CLASS[f.tag]}`}>{f.tag}</span>
//         </label>
//       ))}
//     </div>
//   );
// }

// Owner: Urooj. Sliders. Each one shows its label: assumed or derived.
import { LABEL_CLASS } from "../lib/format.js";

// def must match DEFAULTS in App.jsx. It is used for the "changed" mark and the reset button.
const FIELDS = [
  {
    key: "budget_s", label: "Time budget", unit: "s", min: 300, max: 1800, step: 60, def: 900, tag: "assumed",
    hint: "How long the crew can walk before it must be home.",
  },
  {
    key: "speed_mps", label: "Walking speed", unit: "m/s", min: 0.3, max: 1.0, step: 0.05, def: 0.5, tag: "assumed",
    hint: "Pace on flat ground. It falls as the slope gets steeper.",
  },
  {
    key: "cutoff_deg", label: "Slope cutoff", unit: "°", min: 10, max: 30, step: 1, def: 20, tag: "assumed",
    hint: "Steepest ground the crew will cross. Steeper cells block the route.",
  },
  {
    key: "confidence", label: "Confidence threshold", unit: "", min: 0.5, max: 0.95, step: 0.05, def: 0.9, tag: "derived",
    hint: "How sure a cell must be to count as reachable. Higher is stricter.",
  },
  {
    key: "roughness", label: "Unresolved roughness", unit: "", min: 0, max: 1, step: 0.05, def: 0.5, tag: "assumed",
    hint: "Terrain detail that the coarse map cannot see.",
  },
];

const FILL = { assumed: "#ea580c", derived: "#2563eb" };

export default function ControlPanel({ params, onChange }) {
  const anyChanged = FIELDS.some((f) => params[f.key] !== f.def);

  return (
    <div className="space-y-3">
      {FIELDS.map((f) => {
        const v = params[f.key];
        const pct = ((v - f.min) / (f.max - f.min)) * 100;
        const changed = v !== f.def;
        const id = `ctl-${f.key}`;
        return (
          <div key={f.key} className="rounded-lg border border-slate-200 bg-slate-50 p-3">
            <div className="flex items-start justify-between gap-2">
              <div>
                <label htmlFor={id} className="text-sm font-semibold text-slate-800">
                  {f.label}
                </label>
                <p className="mt-0.5 text-[11px] leading-snug text-slate-500">{f.hint}</p>
              </div>
              <span
                className={`shrink-0 rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide ${LABEL_CLASS[f.tag]}`}
              >
                {f.tag}
              </span>
            </div>

            <div className="mt-3 flex items-baseline justify-between">
              <span className="text-2xl font-semibold text-slate-900">
                {v}
                {f.unit && <span className="ml-1 text-xs font-normal text-slate-500">{f.unit}</span>}
              </span>
              <span className="flex items-center gap-2 text-xs text-slate-500">
                {f.key === "budget_s" && <span>= {v / 60} min</span>}
                {changed && (
                  <span className="rounded bg-amber-100 px-1.5 py-0.5 text-[10px] font-semibold uppercase text-amber-800">
                    changed
                  </span>
                )}
              </span>
            </div>

            <input
              id={id}
              type="range"
              className="wb-range mt-2"
              style={{ "--pct": `${pct}%`, "--fill": FILL[f.tag] }}
              min={f.min}
              max={f.max}
              step={f.step}
              value={v}
              onChange={(e) => onChange(f.key, Number(e.target.value))}
            />
            <div className="mt-1 flex justify-between text-[10px] text-slate-400">
              <span>{f.min}</span>
              <span>{f.max}</span>
            </div>
          </div>
        );
      })}

      <button
        type="button"
        disabled={!anyChanged}
        onClick={() => FIELDS.forEach((f) => onChange(f.key, f.def))}
        className="w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-100 disabled:cursor-not-allowed disabled:opacity-40"
      >
        Reset to defaults
      </button>
    </div>
  );
}