// // Owner: Urooj. Every assumption used in the run, with its label.
// import { LABEL_CLASS } from "../lib/format.js";

// export default function AssumptionsPanel({ assumptions }) {
//   if (!assumptions?.length) return <p className="text-sm text-slate-500">No run yet.</p>;
//   return (
//     <table className="w-full text-sm">
//       <tbody>
//         {assumptions.map((a) => (
//           <tr key={a.name} className="border-b border-slate-200">
//             <td className="py-1 pr-2 font-mono text-xs">{a.name}</td>
//             <td className="py-1 pr-2">{a.value}</td>
//             <td className="py-1">
//               <span className={`rounded px-2 py-0.5 text-xs ${LABEL_CLASS[a.label] ?? ""}`}>{a.label}</span>
//             </td>
//           </tr>
//         ))}
//       </tbody>
//     </table>
//   );
// }

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
  assumed: "border-l-rose-500",
  derived: "border-l-blue-500",
  measured: "border-l-emerald-500",
};
const ORDER = ["assumed", "derived", "measured"];

const pretty = (name) => name.replace(/_/g, " ").replace(/^./, (c) => c.toUpperCase());

export default function AssumptionsPanel({ assumptions }) {
  if (!assumptions?.length) return <p className="text-sm text-slate-500">No run yet.</p>;

  const sorted = [...assumptions].sort((a, b) => ORDER.indexOf(a.label) - ORDER.indexOf(b.label));
  const counts = ORDER.map((l) => ({ l, n: assumptions.filter((a) => a.label === l).length })).filter(
    (c) => c.n > 0
  );

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap gap-2">
        {counts.map(({ l, n }) => (
          <span
            key={l}
            className={`rounded-full px-2.5 py-1 text-[11px] font-semibold uppercase tracking-wide ${LABEL_CLASS[l]}`}
          >
            {n} {l}
          </span>
        ))}
      </div>

      <ul className="grid gap-2 sm:grid-cols-2 xl:grid-cols-3">
        {sorted.map((a) => {
          const info = INFO[a.name];
          return (
            <li
              key={a.name}
              className={`flex items-center justify-between gap-3 rounded-lg border border-slate-200 border-l-4 bg-slate-50 px-3 py-2 ${
                BORDER[a.label] ?? "border-l-slate-300"
              }`}
            >
              <div className="min-w-0">
                <div className="truncate text-sm font-medium text-slate-800">
                  {info?.title ?? pretty(a.name)}
                </div>
                <div className="truncate font-mono text-[10px] text-slate-400">{a.name}</div>
              </div>
              <div className="flex shrink-0 flex-col items-end gap-1">
                <span className="text-sm font-semibold text-slate-900">
                  {a.value}
                  {info?.unit && <span className="ml-1 text-xs font-normal text-slate-500">{info.unit}</span>}
                </span>
                <span
                  className={`rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase ${LABEL_CLASS[a.label] ?? ""}`}
                >
                  {a.label}
                </span>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}