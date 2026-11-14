// Owner: Urooj. Sliders. Each one shows its label: assumed or derived.
import { LABEL_CLASS } from "../lib/format.js";

const FIELDS = [
  { key: "budget_s", label: "Time budget (s)", min: 300, max: 1800, step: 60, tag: "assumed" },
  { key: "speed_mps", label: "Walking speed (m/s, flat)", min: 0.3, max: 1.0, step: 0.05, tag: "assumed" },
  { key: "cutoff_deg", label: "Slope cutoff (deg)", min: 10, max: 30, step: 1, tag: "assumed" },
  { key: "confidence", label: "Confidence threshold", min: 0.5, max: 0.95, step: 0.05, tag: "derived" },
  { key: "roughness", label: "Unresolved roughness", min: 0, max: 1, step: 0.05, tag: "assumed" },
];

export default function ControlPanel({ params, onChange }) {
  return (
    <div className="space-y-4">
      {FIELDS.map((f) => (
        <label key={f.key} className="block text-sm">
          <div className="flex justify-between">
            <span>{f.label}</span>
            <span className="font-mono">{params[f.key]}</span>
          </div>
          <input
            type="range"
            className="w-full"
            min={f.min}
            max={f.max}
            step={f.step}
            value={params[f.key]}
            onChange={(e) => onChange(f.key, Number(e.target.value))}
          />
          <span className={`mt-1 inline-block rounded px-2 py-0.5 text-xs ${LABEL_CLASS[f.tag]}`}>{f.tag}</span>
        </label>
      ))}
    </div>
  );
}
