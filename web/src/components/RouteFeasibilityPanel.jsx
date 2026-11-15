// Owner: Urooj. Static finding from reports/route_feasibility.md: do the planner's own routes work on the 1 m truth?
import { useEffect, useState } from "react";
import { fmtPct } from "../lib/format.js";
import { loadRouteFeasibility } from "../lib/api.js";

export default function RouteFeasibilityPanel({ params }) {
  const [data, setData] = useState(undefined); // undefined = loading, null = not available

  useEffect(() => {
    let live = true;
    loadRouteFeasibility().then((d) => live && setData(d));
    return () => {
      live = false;
    };
  }, []);

  if (data === undefined) return <p className="text-base text-mute">Loading…</p>;
  if (!data) return <p className="text-base text-mute">Route feasibility report not available.</p>;

  const match = data.rows.find((r) => r.roughness === params?.roughness && r.confidence === params?.confidence);
  const row = match ?? data.rows.find((r) => r.roughness === data.headline.roughness && r.confidence === data.headline.confidence);
  if (!row) return null;

  return (
    <div className="space-y-3">
      <div className="px-inset relative p-3 pl-5">
        <span className="absolute inset-y-0 left-0 w-2 bg-aqua" />
        <span className="text-xs leading-tight text-mute">Planner routes that work on the 1 m truth</span>
        <div className="mt-2 font-pixel text-base leading-tight text-sun">{fmtPct(row.share)}</div>
        <div className="mt-1 text-xs text-mute">
          {row.feasible} of {row.cells} cells; {row.blocked} blocked, {row.too_slow} too slow
        </div>
      </div>
      <p className="text-sm text-mute">
        Roughness {row.roughness}, confidence {row.confidence}
        {match ? " (your current inputs)" : " (headline setting; your inputs were not in the 9 reported)"}. Area false
        reach for the same setting is {fmtPct(row.area_false_reach)}.
      </p>
      <p className="text-xs text-mute">
        Fixed report, not recomputed from the sliders. One Jezero window, v2 model, linear speed (assumed). No steep
        window run. A planning aid, not flight software.
      </p>
    </div>
  );
}
