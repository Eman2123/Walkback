"""Route feasibility, as registered in PREREGISTRATION.md ("Route feasibility").

EXPLORATORY. For the cells the v2 model calls reachable, walk the planner's own route on the 1 m truth speed field
and report how many of those routes get the crew home within the budget. Changes no default and no registered number.

Usage (repo root):
    PYTHONPATH=src python scripts/route_feasibility.py
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

from walkback.compute import compute_run_v2, speed_field
from walkback.tiles import load_tile
from walkback.validation.route_feasibility import planner_tree, route_feasibility, truth_time_along_tree
from walkback.compute import wilson_ci

BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0}
ROUGHNESS = (0.1, 0.3, 0.5)
CONFIDENCE = (0.5, 0.7, 0.9)
HEADLINE = (0.5, 0.9)
FIELDS = ["roughness", "confidence", "region", "cells", "feasible", "share", "wilson_low", "wilson_high", "blocked",
          "too_slow", "ratio_median", "ratio_p95", "area_false_reach"]


def pct(x):
    return "n/a" if x is None else f"{x * 100:.1f} %"


def num(x):
    return "n/a" if x is None else f"{x:.2f}"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-id", default="jezero-20m")
    ap.add_argument("--out", type=Path, default=Path("reports/route_feasibility.md"))
    ap.add_argument("--csv", type=Path, default=Path("reports/route_feasibility.csv"))
    ap.add_argument("--json", type=Path, default=Path("web/public/route-feasibility.json"))
    args = ap.parse_args()
    tile = load_tile(args.tile_id, args.tile_dir)
    if tile is None:
        raise SystemExit("tile not found")
    hab = (BASE["habitat_row"], BASE["habitat_col"])
    rows = []
    for rough in ROUGHNESS:
        for conf in CONFIDENCE:
            res = compute_run_v2(tile, dict(BASE, confidence=conf, roughness=rough), return_fields=True)
            f = res["_fields"]
            sp = speed_field(f["slope_coarse"], BASE["speed_mps"], BASE["cutoff_deg"])
            T, parent, order = planner_tree(sp, hab, tile.cell_m)
            tt = truth_time_along_tree(speed_field(f["slope_fine"], BASE["speed_mps"], BASE["cutoff_deg"]),
                                       parent, order, hab, tile.cell_m)
            for name in ("calibrated", "deterministic"):
                region = f["cal"] if name == "calibrated" else f["det"]
                r = route_feasibility(region, T, tt, BASE["budget_s"])
                lo, hi = wilson_ci(r["feasible"], r["n"])
                false_reach = None
                if name == "calibrated" and res["stats"]["false_reach"] is not None:
                    false_reach = res["stats"]["false_reach"]
                rows.append({"roughness": rough, "confidence": conf, "region": name, "cells": r["n"],
                             "feasible": r["feasible"], "share": r["share"], "wilson_low": lo, "wilson_high": hi,
                             "blocked": r["blocked"], "too_slow": r["too_slow"], "ratio_median": r["ratio_median"],
                             "ratio_p95": r["ratio_p95"], "area_false_reach": false_reach})

    args.csv.parent.mkdir(parents=True, exist_ok=True)
    with args.csv.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps({
        "tile": tile.label, "profile": "v2", "budget_s": BASE["budget_s"], "speed_mps": BASE["speed_mps"],
        "cutoff_deg": BASE["cutoff_deg"], "headline": {"roughness": HEADLINE[0], "confidence": HEADLINE[1]},
        "rows": [r for r in rows if r["region"] == "calibrated"],
    }, indent=1) + "\n")

    head = next(r for r in rows if (r["roughness"], r["confidence"]) == HEADLINE and r["region"] == "calibrated")
    lines = [
        "# Route feasibility (exploratory)",
        "",
        "Registered in PREREGISTRATION.md before it was run. This does not replace the headline in validation_report.md.",
        "",
        f"Tile: {tile.label}. Model v2, habitat {hab}, budget {BASE['budget_s']} s, speed {BASE['speed_mps']} m/s (assumed), "
        f"cutoff {BASE['cutoff_deg']} deg (assumed). For each cell the model calls reachable, the planner's shortest route "
        "(on the 200 m model) is walked on the 1 m truth. Feasible = the route never enters a truth-impassable cell and takes "
        "no longer than the budget.",
        "",
        "## Headline (roughness 0.5, confidence 0.9, calibrated region)",
        "",
        f"- Planner routes that work on the truth: {head['feasible']} of {head['cells']} ({pct(head['share'])}, "
        f"95 % Wilson {pct(head['wilson_low'])} to {pct(head['wilson_high'])}; cells are spatially correlated, so the interval is optimistic).",
        f"- Failures: {head['blocked']} cross a truth-impassable cell, {head['too_slow']} are too slow.",
        f"- Truth time over planner time: median {num(head['ratio_median'])}, 95th percentile {num(head['ratio_p95'])}.",
        f"- Area view of the same setting: false reach {pct(head['area_false_reach'])}.",
        "",
        "## All settings",
        "",
        "| roughness | confidence | region | cells | feasible | blocked | too slow | truth/planner time (median, p95) | area false reach |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        lines.append(
            f"| {r['roughness']} | {r['confidence']} | {r['region']} | {r['cells']} | {pct(r['share'])} | {r['blocked']} | "
            f"{r['too_slow']} | {num(r['ratio_median'])}, {num(r['ratio_p95'])} | {pct(r['area_false_reach'])} |"
        )
    lines += [
        "",
        "## Limits",
        "",
        "- One 2 km Jezero window, which has almost no steep cells. This says nothing about steep terrain; the steep tiles are not in this repository, so they were not run.",
        "- Linear speed model, an assumption. Truth uses the same speed model on the 1 m data, so this tests the planner's terrain information, not the speed model.",
        "- A planning aid, not flight software. No route is declared safe.",
    ]
    args.out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:14]))


if __name__ == "__main__":
    main()
