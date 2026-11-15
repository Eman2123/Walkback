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

const FILL = { assumed: "#ff5d8f", derived: "#4cc9f0" };

export default function ControlPanel({ params, onChange }) {
  const anyChanged = FIELDS.some((f) => params[f.key] !== f.def);

  return (
    <div className="space-y-4">
      {FIELDS.map((f) => {
        const v = params[f.key];
        const pct = ((v - f.min) / (f.max - f.min)) * 100;
        const changed = v !== f.def;
        const id = `ctl-${f.key}`;
        return (
          <div key={f.key} className="border-4 border-ink bg-panel2 p-3 shadow-[inset_3px_3px_0_0_rgba(245,230,200,0.07)]">
            <div className="flex items-start justify-between gap-2">
              <label htmlFor={id} className="font-pixel text-[10px] leading-relaxed text-cream">
                {f.label}
              </label>
              <span className={`px-chip shrink-0 ${LABEL_CLASS[f.tag]}`}>{f.tag}</span>
            </div>
            <p className="mt-1 text-xs leading-tight text-mute">{f.hint}</p>

            <div className="mt-2 flex items-end justify-between">
              <span className="px-inset px-3 py-1 font-pixel text-sm text-sun">
                {v}
                {f.unit && <span className="ml-1 text-[10px] text-mute">{f.unit}</span>}
              </span>
              <span className="flex items-center gap-2 text-xs text-mute">
                {f.key === "budget_s" && <span>= {v / 60} min</span>}
                {changed && <span className="px-chip bg-sun">changed</span>}
              </span>
            </div>

            <input
              id={id}
              type="range"
              className="wb-range mt-3"
              style={{ "--pct": `${pct}%`, "--fill": FILL[f.tag] }}
              min={f.min}
              max={f.max}
              step={f.step}
              value={v}
              onChange={(e) => onChange(f.key, Number(e.target.value))}
            />
            <div className="mt-1 flex justify-between text-xs text-mute">
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
        className="px-btn px-btn-ghost w-full"
      >
        Reset to defaults
      </button>
    </div>
  );
}
