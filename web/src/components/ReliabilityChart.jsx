// // Owner: Urooj. Predicted vs observed steep probability per bin. Diagonal = perfect calibration.
// export default function ReliabilityChart({ bins }) {
//   const W = 300, H = 220, P = 30;
//   const x = (v) => P + v * (W - 2 * P);
//   const y = (v) => H - P - v * (H - 2 * P);
//   const usable = (bins || []).filter((b) => b.n > 0);
//   return (
//     <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Reliability diagram">
//       <rect x={P} y={P} width={W - 2 * P} height={H - 2 * P} fill="none" stroke="#cbd5e1" />
//       <line x1={x(0)} y1={y(0)} x2={x(1)} y2={y(1)} stroke="#94a3b8" strokeDasharray="4 4" />
//       {usable.map((b) => (
//         <circle
//           key={b.bin}
//           cx={x(b.pred)}
//           cy={y(b.obs)}
//           r={Math.min(9, 3 + Math.sqrt(b.n) / 4)}
//           fill="rgba(31,157,85,0.7)"
//         >
//           <title>{`n=${b.n}, predicted ${b.pred.toFixed(2)}, observed ${b.obs.toFixed(2)}`}</title>
//         </circle>
//       ))}
//       <text x={W / 2} y={H - 6} textAnchor="middle" fontSize="10" fill="#64748b">Predicted P(steep)</text>
//       <text x={8} y={H / 2} fontSize="10" fill="#64748b" transform={`rotate(-90 8 ${H / 2})`} textAnchor="middle">
//         Observed
//       </text>
//     </svg>
//   );
// }


// Owner: Urooj. Predicted vs observed steep probability per bin. Diagonal = perfect calibration.
import { LABEL_CLASS } from "../lib/format.js";

export default function ReliabilityChart({ bins }) {
  const usable = (bins || []).filter((b) => b.n > 0);
  if (!usable.length) return <p className="text-sm text-slate-500">No reliability data yet.</p>;

  const W = 320, H = 270, L = 40, R = 12, T = 12, PH = 190;
  const x = (v) => L + v * (W - L - R);
  const y = (v) => T + PH - v * PH;
  const ticks = [0, 0.25, 0.5, 0.75, 1];

  const total = usable.reduce((s, b) => s + b.n, 0);
  const maxN = Math.max(...usable.map((b) => b.n));
  const gap = Math.max(...usable.map((b) => Math.abs(b.pred - b.obs)));
  const barBase = 262, barMax = 24;

  return (
    <div className="space-y-3">
      <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Reliability diagram">
        {/* Zones above and below the perfect-calibration line */}
        <polygon points={`${x(0)},${y(0)} ${x(1)},${y(1)} ${x(0)},${y(1)}`} fill="#dbeafe" opacity="0.55" />
        <polygon points={`${x(0)},${y(0)} ${x(1)},${y(1)} ${x(1)},${y(0)}`} fill="#ffedd5" opacity="0.7" />
        <rect x={L} y={T} width={W - L - R} height={PH} fill="none" stroke="#cbd5e1" />

        {ticks.map((t) => (
          <g key={t}>
            <line x1={x(t)} y1={T} x2={x(t)} y2={T + PH} stroke="#ffffff" strokeOpacity="0.8" />
            <line x1={L} y1={y(t)} x2={W - R} y2={y(t)} stroke="#ffffff" strokeOpacity="0.8" />
            <text x={x(t)} y={T + PH + 12} textAnchor="middle" fontSize="8" fill="#64748b">{t}</text>
            <text x={L - 5} y={y(t) + 3} textAnchor="end" fontSize="8" fill="#64748b">{t}</text>
          </g>
        ))}

        <text x={L + 6} y={T + 12} fontSize="8" fill="#1d4ed8">Observed higher than predicted</text>
        <text x={W - R - 6} y={T + PH - 6} textAnchor="end" fontSize="8" fill="#c2410c">
          Observed lower than predicted
        </text>

        <line x1={x(0)} y1={y(0)} x2={x(1)} y2={y(1)} stroke="#475569" strokeDasharray="4 4" />

        {/* Gap from the perfect line to each dot */}
        {usable.map((b) => (
          <line
            key={`g${b.bin}`}
            x1={x(b.pred)} y1={y(b.pred)} x2={x(b.pred)} y2={y(b.obs)}
            stroke={b.obs >= b.pred ? "#2563eb" : "#ea580c"}
            strokeWidth="1.5"
            opacity="0.7"
          />
        ))}

        <polyline
          points={usable.map((b) => `${x(b.pred)},${y(b.obs)}`).join(" ")}
          fill="none" stroke="#10b981" strokeWidth="1.5" opacity="0.6"
        />
        {usable.map((b) => (
          <circle
            key={b.bin}
            cx={x(b.pred)} cy={y(b.obs)}
            r={Math.min(9, 3 + Math.sqrt(b.n) / 4)}
            fill="rgba(16,185,129,0.85)" stroke="#047857"
          >
            <title>{`n=${b.n}, predicted ${b.pred.toFixed(2)}, observed ${b.obs.toFixed(2)}`}</title>
          </circle>
        ))}

        <text x={(L + W - R) / 2} y={T + PH + 24} textAnchor="middle" fontSize="9" fill="#475569">
          Predicted P(steep)
        </text>
        <text x={10} y={T + PH / 2} fontSize="9" fill="#475569" transform={`rotate(-90 10 ${T + PH / 2})`} textAnchor="middle">
          Observed
        </text>

        {/* Cells per bin */}
        <text x={L} y={barBase - barMax - 4} fontSize="8" fill="#64748b">Cells per bin</text>
        {usable.map((b) => {
          const h = Math.max(2, barMax * Math.sqrt(b.n / maxN));
          return (
            <rect key={`b${b.bin}`} x={x(b.pred) - 11} y={barBase - h} width="22" height={h} fill="#94a3b8" rx="2">
              <title>{`${b.n} cells`}</title>
            </rect>
          );
        })}
      </svg>

      <div className="flex flex-wrap gap-2 text-xs">
        <span className="flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1.5">
          <span className="text-slate-500">Cells evaluated</span>
          <strong className="text-slate-900">{total.toLocaleString()}</strong>
          <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-semibold uppercase ${LABEL_CLASS.derived}`}>derived</span>
        </span>
        <span className="flex items-center gap-2 rounded-lg border border-slate-200 bg-slate-50 px-2.5 py-1.5">
          <span className="text-slate-500">Largest gap</span>
          <strong className="text-slate-900">{gap.toFixed(2)}</strong>
          <span className={`rounded-full px-1.5 py-0.5 text-[10px] font-semibold uppercase ${LABEL_CLASS.derived}`}>derived</span>
        </span>
      </div>

      <p className="text-xs text-slate-500">
        Dashed line = perfect calibration. Dot size = cells in the bin. A dot far from the line is a place
        where the prediction and the 1 m truth disagree.
      </p>
    </div>
  );
}