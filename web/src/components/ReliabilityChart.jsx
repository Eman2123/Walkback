// Owner: Urooj. Predicted vs observed steep probability per bin. Diagonal = perfect calibration.
export default function ReliabilityChart({ bins }) {
  const W = 300, H = 220, P = 30;
  const x = (v) => P + v * (W - 2 * P);
  const y = (v) => H - P - v * (H - 2 * P);
  const usable = (bins || []).filter((b) => b.n > 0);
  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" role="img" aria-label="Reliability diagram">
      <rect x={P} y={P} width={W - 2 * P} height={H - 2 * P} fill="none" stroke="#cbd5e1" />
      <line x1={x(0)} y1={y(0)} x2={x(1)} y2={y(1)} stroke="#94a3b8" strokeDasharray="4 4" />
      {usable.map((b) => (
        <circle
          key={b.bin}
          cx={x(b.pred)}
          cy={y(b.obs)}
          r={Math.min(9, 3 + Math.sqrt(b.n) / 4)}
          fill="rgba(31,157,85,0.7)"
        >
          <title>{`n=${b.n}, predicted ${b.pred.toFixed(2)}, observed ${b.obs.toFixed(2)}`}</title>
        </circle>
      ))}
      <text x={W / 2} y={H - 6} textAnchor="middle" fontSize="10" fill="#64748b">Predicted P(steep)</text>
      <text x={8} y={H / 2} fontSize="10" fill="#64748b" transform={`rotate(-90 8 ${H / 2})`} textAnchor="middle">
        Observed
      </text>
    </svg>
  );
}
