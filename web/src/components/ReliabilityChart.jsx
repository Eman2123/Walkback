// Owner: Urooj. Predicted vs observed steep probability per bin. Diagonal = perfect calibration.
import { LABEL_CLASS } from "../lib/format.js";

export default function ReliabilityChart({ bins }) {
  const usable = (bins || []).filter((b) => b.n > 0);
  if (!usable.length) return <p className="text-base text-mute">No reliability data yet.</p>;

  const W = 320, H = 280, L = 40, R = 12, T = 12, PH = 190;
  const x = (v) => L + v * (W - L - R);
  const y = (v) => T + PH - v * PH;
  const ticks = [0, 0.25, 0.5, 0.75, 1];

  const total = usable.reduce((s, b) => s + b.n, 0);
  const maxN = Math.max(...usable.map((b) => b.n));
  const gap = Math.max(...usable.map((b) => Math.abs(b.pred - b.obs)));
  const barBase = 274, barMax = 24;
  const sq = (n) => Math.round(Math.min(14, 6 + Math.sqrt(n) / 3) / 2) * 2; // square size, even px

  return (
    <div className="space-y-3">
      <svg
        viewBox={`0 0 ${W} ${H}`}
        className="px-inset w-full"
        role="img"
        aria-label="Reliability diagram"
        shapeRendering="crispEdges"
        fontFamily="VT323, monospace"
      >
        {/* Zones above and below the perfect-calibration line */}
        <polygon points={`${x(0)},${y(0)} ${x(1)},${y(1)} ${x(0)},${y(1)}`} fill="#4cc9f0" opacity="0.10" />
        <polygon points={`${x(0)},${y(0)} ${x(1)},${y(1)} ${x(1)},${y(0)}`} fill="#ff5d8f" opacity="0.12" />
        <rect x={L} y={T} width={W - L - R} height={PH} fill="none" stroke="#5b4580" strokeWidth="2" />

        {ticks.map((t) => (
          <g key={t}>
            <line x1={x(t)} y1={T} x2={x(t)} y2={T + PH} stroke="#f5e6c8" strokeOpacity="0.1" />
            <line x1={L} y1={y(t)} x2={W - R} y2={y(t)} stroke="#f5e6c8" strokeOpacity="0.1" />
            <text x={x(t)} y={T + PH + 13} textAnchor="middle" fontSize="13" fill="#b7a6c9">{t}</text>
            <text x={L - 6} y={y(t) + 4} textAnchor="end" fontSize="13" fill="#b7a6c9">{t}</text>
          </g>
        ))}

        <text x={L + 6} y={T + 13} fontSize="13" fill="#4cc9f0">Observed higher than predicted</text>
        <text x={W - R - 6} y={T + PH - 6} textAnchor="end" fontSize="13" fill="#ff5d8f">
          Observed lower than predicted
        </text>

        <line x1={x(0)} y1={y(0)} x2={x(1)} y2={y(1)} stroke="#f5e6c8" strokeWidth="2" strokeDasharray="6 6" />

        {/* Gap from the perfect line to each square */}
        {usable.map((b) => (
          <line
            key={`g${b.bin}`}
            x1={x(b.pred)} y1={y(b.pred)} x2={x(b.pred)} y2={y(b.obs)}
            stroke={b.obs >= b.pred ? "#4cc9f0" : "#ff5d8f"}
            strokeWidth="2"
            opacity="0.8"
          />
        ))}

        <polyline
          points={usable.map((b) => `${x(b.pred)},${y(b.obs)}`).join(" ")}
          fill="none" stroke="#5eea8a" strokeWidth="2" opacity="0.7"
        />
        {usable.map((b) => {
          const s = sq(b.n);
          return (
            <rect
              key={b.bin}
              x={x(b.pred) - s / 2} y={y(b.obs) - s / 2} width={s} height={s}
              fill="#5eea8a" stroke="#0d0814" strokeWidth="2"
            >
              <title>{`n=${b.n}, predicted ${b.pred.toFixed(2)}, observed ${b.obs.toFixed(2)}`}</title>
            </rect>
          );
        })}

        <text x={(L + W - R) / 2} y={T + PH + 28} textAnchor="middle" fontSize="14" fill="#f5e6c8">
          Predicted P(steep)
        </text>
        <text x={10} y={T + PH / 2} fontSize="14" fill="#f5e6c8" transform={`rotate(-90 10 ${T + PH / 2})`} textAnchor="middle">
          Observed
        </text>

        {/* Cells per bin */}
        <text x={L} y={barBase - barMax - 4} fontSize="13" fill="#b7a6c9">Cells per bin</text>
        {usable.map((b) => {
          const h = Math.max(2, Math.round(barMax * Math.sqrt(b.n / maxN)));
          return (
            <rect key={`b${b.bin}`} x={x(b.pred) - 11} y={barBase - h} width="22" height={h} fill="#7d6b93">
              <title>{`${b.n} cells`}</title>
            </rect>
          );
        })}
      </svg>

      <div className="flex flex-wrap gap-2 text-sm">
        <span className="px-inset flex items-center gap-2 px-2.5 py-1.5">
          <span className="text-mute">Cells evaluated</span>
          <strong className="font-normal text-sun">{total.toLocaleString()}</strong>
          <span className={`px-chip ${LABEL_CLASS.derived}`}>derived</span>
        </span>
        <span className="px-inset flex items-center gap-2 px-2.5 py-1.5">
          <span className="text-mute">Largest gap</span>
          <strong className="font-normal text-sun">{gap.toFixed(2)}</strong>
          <span className={`px-chip ${LABEL_CLASS.derived}`}>derived</span>
        </span>
      </div>

      <p className="text-sm leading-tight text-mute">
        Dashed line = perfect calibration. Square size = cells in the bin. A square far from the line is a place
        where the prediction and the 1 m truth disagree.
      </p>
    </div>
  );
}
