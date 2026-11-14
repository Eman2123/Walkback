// Owner: Urooj. Every assumption used in the run, with its label.
import { LABEL_CLASS } from "../lib/format.js";

export default function AssumptionsPanel({ assumptions }) {
  if (!assumptions?.length) return <p className="text-sm text-slate-500">No run yet.</p>;
  return (
    <table className="w-full text-sm">
      <tbody>
        {assumptions.map((a) => (
          <tr key={a.name} className="border-b border-slate-200">
            <td className="py-1 pr-2 font-mono text-xs">{a.name}</td>
            <td className="py-1 pr-2">{a.value}</td>
            <td className="py-1">
              <span className={`rounded px-2 py-0.5 text-xs ${LABEL_CLASS[a.label] ?? ""}`}>{a.label}</span>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
