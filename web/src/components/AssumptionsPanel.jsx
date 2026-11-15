// Owner: Urooj. Every assumption used in the run, with its label.
import { LABEL_CLASS } from "../lib/format.js";

// Friendly names for known keys. Unknown keys fall back to a readable version of the key.
const INFO = {
  walking_speed_mps: { title: "Walking speed on flat ground", unit: "m/s" },
  slope_cutoff_deg: { title: "Slope cutoff", unit: "°" },
  unresolved_roughness: { title: "Unresolved roughness", unit: "" },
  time_budget_s: { title: "Time budget", unit: "s" },
  confidence_threshold: { title: "Confidence threshold", unit: "" },
  grid_cell_m: { title: "Grid cell size", unit: "m" },
};

const BORDER = {
  assumed: "border-l-blush",
  derived: "border-l-aqua",
  measured: "border-l-neon",
};
const ORDER = ["assumed", "derived", "measured"];

const pretty = (name) => name.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase());

export default function AssumptionsPanel({ assumptions }) {
  if (!assumptions?.length) return <p className="text-base text-mute">No run yet.</p>;

  const sorted = [...assumptions].sort((a, b) => ORDER.indexOf(a.label) - ORDER.indexOf(b.label));
  const counts = ORDER.map((l) => ({ l, n: assumptions.filter((a) => a.label === l).length })).filter(
    (c) => c.n > 0
  );

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2">
        {counts.map(({ l, n }) => (
          <span key={l} className={`px-chip ${LABEL_CLASS[l]}`}>
            {n} {l}
          </span>
        ))}
      </div>

      <ul className="grid gap-3 sm:grid-cols-2 xl:grid-cols-3">
        {sorted.map((a) => {
          const info = INFO[a.name];
          return (
            <li
              key={a.name}
              className={`px-inset flex items-center justify-between gap-3 !border-l-8 px-3 py-2 ${
                BORDER[a.label] ?? "border-l-edge"
              }`}
            >
              <div className="min-w-0">
                <div className="truncate text-sm text-cream">{info?.title ?? pretty(a.name)}</div>
                <div className="truncate text-xs text-mute">{a.name}</div>
              </div>
              <div className="flex shrink-0 flex-col items-end gap-1">
                <span className="font-pixel text-[11px] text-sun">
                  {a.value}
                  {info?.unit && <span className="ml-1 text-[9px] text-mute">{info.unit}</span>}
                </span>
                <span className={`px-chip ${LABEL_CLASS[a.label] ?? "bg-edge"}`}>{a.label}</span>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
