"""Solver and directional-speed comparison, as registered in PREREGISTRATION.md
("Solver and directional speed (exploratory, registered 2026-11-15 BEFORE the code or any result)" and its amendment).

EXPLORATORY. It does not replace reports/validation_report.md and it does not change the API default.

For every tile in the tile directory it runs the registered planner model (staircase) and grid200, each with
  solver        dijkstra8 (registered) and dijkstra16 (adds knight moves)
  speed model   linear out (registered), minetti out, minetti back, minetti_cap out, minetti_cap back
over the registered 9 roughness x confidence combinations. Every row is reported, with its difference from the
registered row (dijkstra8, linear, out) of the same planner model, roughness and confidence.

Usage (repo root):
    PYTHONPATH=src python scripts/run_solver_directional.py
"""
import argparse
import csv
import math
from pathlib import Path

import numpy as np

from walkback.compute import NEIGHBOURS, NEIGHBOURS16, compute_run, travel_time
from walkback.tiles import load_tile
from walkback.validation.metrics import block_bootstrap_ci, brier_skill_score

BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0}
ROUGHNESS = (0.1, 0.3, 0.5)
CONFIDENCE = (0.5, 0.7, 0.9)
PLANNERS = [("staircase (registered)", "staircase"), ("grid200", "grid200")]
SOLVERS = ["dijkstra8", "dijkstra16"]
SPEEDS = [("linear", "out"), ("minetti", "out"), ("minetti", "back"), ("minetti_cap", "out"), ("minetti_cap", "back")]
REGISTERED = ("dijkstra8", "linear", "out")
CSV_FIELDS = ["tile", "planner", "solver", "speed_model", "direction", "roughness", "confidence", "cal_km2", "truth_km2",
              "coverage", "wilson_low", "wilson_high", "boot_low", "boot_high", "false_reach", "bss",
              "d_cal_km2", "d_truth_km2", "d_coverage_pts"]


def pct(x):
    return "n/a" if x is None else f"{x * 100:.1f} %"


def ci_text(lo, hi):
    return "n/a" if lo is None or hi is None else f"{pct(lo)} to {pct(hi)}"


def signed(x, nd=3):
    return "n/a" if x is None else f"{x:+.{nd}f}"


def flat_ground_check(cell=20.0, v=0.5, budget=900.0, n=101):
    """Solver bias on flat ground at uniform speed: worst path error and the reach area against the true circle."""
    yy, xx = np.mgrid[0:n, 0:n]
    dist = np.hypot(yy - n // 2, xx - n // 2) * cell
    m = dist > 0
    out = {}
    for name, nb in (("dijkstra8", NEIGHBOURS), ("dijkstra16", NEIGHBOURS16)):
        T = travel_time(np.full((n, n), v), (n // 2, n // 2), cell, nb)
        err = float((T[m] / (dist[m] / v)).max() - 1)
        area = float((T <= budget).sum() * cell * cell / 1e6)
        out[name] = (err, area)
    out["circle"] = math.pi * (budget * v) ** 2 / 1e6
    return out


def run_row(tile, planner, solver, speed, direction, rough, conf):
    params = dict(BASE, confidence=conf, roughness=rough)
    try:
        res = compute_run(tile, params, planner_slope_mode=planner, solver=solver, speed_model=speed,
                          direction=direction, return_fields=True)
    except ValueError as exc:
        return None, str(exc)
    f = res["_fields"]
    obs = f["obs_steep"].astype(float)
    brier_full = float(np.mean((f["p_steep"] - obs) ** 2))
    noskill = float(obs.mean() * (1.0 - obs.mean()))
    return {"stats": res["stats"], "boot": block_bootstrap_ci(f["cal"], f["truth"])[:2],
            "bss": brier_skill_score(brier_full, noskill)}, None


def tile_section(tile, csv_rows):
    lines = [f"## Tile: {tile.label}", "", f"Tile id {tile.tile_id}, cell {tile.cell_m:g} m.", ""]
    for pname, planner in PLANNERS:
        lines += [f"### Planner model: {pname}", "",
                  "Differences are against the registered row of the same planner model, roughness and confidence "
                  "(dijkstra8, linear, out). Area in km2, coverage difference in percentage points.", "",
                  "| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % "
                  "| block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |",
                  "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        notes = []
        reg = {}
        for solver in SOLVERS:
            for speed, direction in SPEEDS:
                for rough in ROUGHNESS:
                    for conf in CONFIDENCE:
                        row, err = run_row(tile, planner, solver, speed, direction, rough, conf)
                        key = (rough, conf)
                        if row is None:
                            lines.append(f"| {solver} | {speed} | {direction} | {rough} | {conf} | not computed |||||||||| ")
                            notes.append(f"{solver} {speed} {direction}, roughness {rough}, confidence {conf}: {err}")
                            continue
                        s = row["stats"]
                        if (solver, speed, direction) == REGISTERED:
                            reg[key] = s
                        base = reg.get(key)
                        d_cal = None if base is None else s["area_km2"]["calibrated"] - base["area_km2"]["calibrated"]
                        d_truth = None if base is None else s["area_km2"]["truth"] - base["area_km2"]["truth"]
                        d_cov = (None if base is None or s["coverage"] is None or base["coverage"] is None
                                 else (s["coverage"] - base["coverage"]) * 100)
                        lines.append(
                            f"| {solver} | {speed} | {direction} | {rough} | {conf} | {s['area_km2']['calibrated']:.3f} "
                            f"| {s['area_km2']['truth']:.3f} | {pct(s['coverage'])} | {ci_text(*s['coverage_ci'])} "
                            f"| {ci_text(*row['boot'])} | {pct(s['false_reach'])} | {row['bss']:+.3f} "
                            f"| {signed(d_cal)} | {signed(d_truth)} | {signed(d_cov, 1)} |")
                        csv_rows.append({
                            "tile": tile.tile_id, "planner": planner, "solver": solver, "speed_model": speed,
                            "direction": direction, "roughness": rough, "confidence": conf,
                            "cal_km2": s["area_km2"]["calibrated"], "truth_km2": s["area_km2"]["truth"],
                            "coverage": s["coverage"], "wilson_low": s["coverage_ci"][0], "wilson_high": s["coverage_ci"][1],
                            "boot_low": row["boot"][0], "boot_high": row["boot"][1], "false_reach": s["false_reach"],
                            "bss": round(row["bss"], 4), "d_cal_km2": d_cal, "d_truth_km2": d_truth,
                            "d_coverage_pts": d_cov})
        lines.append("")
        for n in notes:
            lines.append(f"- not computed, {n}")
        if notes:
            lines.append("")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-ids", nargs="*", help="default: every .npz in the tile directory")
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    args = ap.parse_args()

    ids = args.tile_ids or sorted(p.stem for p in args.tile_dir.glob("*.npz"))
    tiles = [(i, load_tile(i, args.tile_dir)) for i in ids]
    missing = [i for i, t in tiles if t is None]
    if missing:
        raise SystemExit(f"tile(s) not found: {missing}")
    if not tiles:
        raise SystemExit("no tiles to run")

    fg = flat_ground_check()
    lines = [
        "# Solver and directional speed (exploratory, registered before it was run)",
        "",
        "This is not the validation result. The pre-registered headline in validation_report.md is unchanged.",
        "Registered in PREREGISTRATION.md, section \"Solver and directional speed\" and its amendment.",
        "",
        f"Fixed: habitat ({BASE['habitat_row']}, {BASE['habitat_col']}), budget {BASE['budget_s']} s, speed "
        f"{BASE['speed_mps']} m/s (assumed), cutoff {BASE['cutoff_deg']} deg (assumed), 16 realizations, seed 1234.",
        "",
        "Speed models: linear = registered, symmetric. minetti = edge speed times Cs(g)/C(g) from the Minetti et al. 2002 "
        "walking cost (assumed: Earth treadmill, speed inverse to cost, no Mars gravity or suit); it speeds the crew up "
        "on downhill grades (up to about 4 times), which is not a defensible planning speed. minetti_cap = the same with the "
        "factor limited to 1, so uphill penalties only; read this one for a return-time question. direction out = time from "
        "the habitat (registered); back = time from each cell to the habitat, which is the walkback.",
        "",
        "Grades use the planner elevation (200 m blocks drawn on the 20 m grid) for the planner, so the staircase artifact of "
        "the registered model also affects the direction factor, for grid200 as well. The fine elevation is used for the truth.",
        "",
        "Solver check on flat ground at uniform speed (101 x 101 cells, 20 m, 0.5 m/s, 900 s):",
        "",
        "| solver | worst path error | reach area km2 | against the true circle |",
        "|---|---|---|---|",
    ]
    for name in SOLVERS:
        err, area = fg[name]
        lines.append(f"| {name} | {err * 100:+.1f} % | {area:.3f} | {(area / fg['circle'] - 1) * 100:+.1f} % (circle {fg['circle']:.3f}) |")
    lines += ["", "All rows are reported. No row is chosen as the result. A difference between out and back is reported even "
              "when it is zero.", ""]
    csv_rows: list[dict] = []
    for _, tile in tiles:
        lines += tile_section(tile, csv_rows)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "solver_directional.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    with open(args.out_dir / "solver_directional.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(csv_rows)
    print(f"wrote {len(csv_rows)} rows to {args.out_dir}/solver_directional.md and .csv")


if __name__ == "__main__":
    main()
