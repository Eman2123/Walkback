"""Extended validation, as registered in PREREGISTRATION.md ("Extended validation and sub-grid roughness").

EXPLORATORY. It does not replace reports/validation_report.md and it does not change the API default.

For every tile in the tile directory it runs three planner models:
  staircase                 the registered model
  grid200                   slope on the 200 m block grid (exploratory variant)
  grid200 + hurst           grid200 plus sub-grid gradient noise predicted from a scale exponent H (exploratory)
over the registered 9 roughness x confidence combinations (the hurst model has no roughness, so 3 rows), and reports
coverage with a Wilson and a block-bootstrap interval, false reach, Brier, Brier skill score, the reliability of the
reach probability, and coverage against the confidence threshold. Every row is reported.

H is read from reports/scale_effect.md. That file was measured on the same window that is validated, so the hurst
model is IN-SAMPLE; the report says so. Pass --hurst to override.

Usage (repo root):
    PYTHONPATH=src python scripts/run_validation.py
"""
import argparse
import csv
import re
from pathlib import Path

import numpy as np

from walkback.compute import compute_run
from walkback.tiles import load_tile
from walkback.validation.metrics import (
    block_bootstrap_ci,
    brier_skill_score,
    coverage_by_confidence,
    reach_reliability,
    wider_interval,
)

BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0}
ROUGHNESS = (0.1, 0.3, 0.5)
CONFIDENCE = (0.5, 0.7, 0.9)
CURVE_ROUGHNESS = 0.5
MODELS = [
    ("staircase (registered)", {"planner_slope_mode": "staircase", "roughness_mode": "multiplicative"}),
    ("grid200", {"planner_slope_mode": "grid200", "roughness_mode": "multiplicative"}),
    ("grid200 + hurst (in-sample H)", {"planner_slope_mode": "grid200", "roughness_mode": "hurst"}),
]
CSV_FIELDS = ["tile", "model", "roughness", "confidence", "det_km2", "cal_km2", "truth_km2", "coverage",
              "wilson_low", "wilson_high", "boot_low", "boot_high", "false_reach", "brier", "brier_noskill", "bss"]


def pct(x):
    return "n/a" if x is None else f"{x * 100:.1f} %"


def ci_text(lo, hi):
    return "n/a" if lo is None or hi is None else f"{pct(lo)} to {pct(hi)}"


def read_hurst(path: Path) -> float:
    m = re.search(r"\bH = ([0-9]*\.?[0-9]+)", path.read_text(encoding="utf-8"))
    if not m:
        raise SystemExit(f"no 'H = ...' line in {path}; pass --hurst")
    return float(m.group(1))


def run_row(tile, kw, rough, conf, hurst):
    params = dict(BASE, confidence=conf, roughness=0.5 if rough is None else rough)
    extra = {"hurst": hurst} if kw["roughness_mode"] == "hurst" else {}
    try:
        res = compute_run(tile, params, return_fields=True, **kw, **extra)
    except ValueError as exc:
        return None, str(exc)
    s, f = res["stats"], res["_fields"]
    wilson = tuple(s["coverage_ci"])
    boot = block_bootstrap_ci(f["cal"], f["truth"])[:2]
    # Brier and its no-skill value from the unrounded fields: the 4-decimal values in the stats hide small differences
    obs = f["obs_steep"].astype(float)
    brier_full = float(np.mean((f["p_steep"] - obs) ** 2))
    noskill_full = float(obs.mean() * (1.0 - obs.mean()))
    return {
        "stats": s, "fields": f, "wilson": wilson, "boot": boot,
        "brier": brier_full, "noskill": noskill_full, "bss": brier_skill_score(brier_full, noskill_full),
    }, None


def tile_section(tile, hurst, csv_rows):
    cutoff = BASE["cutoff_deg"]
    lines = [f"## Tile: {tile.label}", "", f"Tile id {tile.tile_id}, cell {tile.cell_m:g} m.", ""]
    keep = {}   # model -> fields at the curve setting
    noskill = None
    body = []
    for name, kw in MODELS:
        is_h = kw["roughness_mode"] == "hurst"
        body += [f"### {name}", "",
                 "| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % "
                 "| false reach | Brier | no-skill Brier | Brier skill score |",
                 "|---|---|---|---|---|---|---|---|---|---|---|"]
        notes = []
        for rough in ((None,) if is_h else ROUGHNESS):
            for conf in CONFIDENCE:
                row, err = run_row(tile, kw, rough, conf, hurst)
                rtxt = "n/a" if rough is None else f"{rough}"
                if row is None:
                    body.append(f"| {rtxt} | {conf} | not computed | | | | | | | | |")
                    notes.append(f"roughness {rtxt}, confidence {conf}: {err}")
                    continue
                s = row["stats"]
                noskill = row["noskill"]
                body.append(
                    f"| {rtxt} | {conf} | {s['area_km2']['calibrated']:.3f} | {s['area_km2']['truth']:.3f} "
                    f"| {pct(s['coverage'])} | {ci_text(*row['wilson'])} | {ci_text(*row['boot'])} "
                    f"| {pct(s['false_reach'])} | {row['brier']:.5f} | {row['noskill']:.5f} | {row['bss']:+.3f} |")
                csv_rows.append({
                    "tile": tile.tile_id, "model": name, "roughness": rtxt, "confidence": conf,
                    "det_km2": s["area_km2"]["deterministic"], "cal_km2": s["area_km2"]["calibrated"],
                    "truth_km2": s["area_km2"]["truth"], "coverage": s["coverage"],
                    "wilson_low": row["wilson"][0], "wilson_high": row["wilson"][1],
                    "boot_low": row["boot"][0], "boot_high": row["boot"][1],
                    "false_reach": s["false_reach"], "brier": round(row["brier"], 6),
                    "brier_noskill": round(row["noskill"], 6), "bss": round(row["bss"], 4),
                })
                if (is_h or rough == CURVE_ROUGHNESS) and conf == CONFIDENCE[-1]:
                    keep[name] = row["fields"]
        body.append("")
        for n in notes:
            body.append(f"- not computed, {n}")
        if notes:
            body.append("")
    if noskill is not None:
        lines += [f"No-skill Brier (always \"never steep\") for this tile: {noskill:.5f}. "
                  f"A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.", ""]
    lines += body

    lines += ["### Reliability of the reach probability", "",
              "Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those "
              f"cells reachable in the truth. Roughness {CURVE_ROUGHNESS} for the multiplicative models.", ""]
    for name, _ in MODELS:
        if name not in keep:
            continue
        f = keep[name]
        lines += [f"{name}", "", "| bin | cells | predicted | observed |", "|---|---|---|---|"]
        for b in reach_reliability(f["p_reach"], f["truth"]):
            lines.append(f"| {b['bin']} | {b['n']} | {b['pred']:.3f} | {b['obs']:.3f} |")
        lines.append("")

    lines += ["### Coverage and false reach against the confidence threshold", "",
              f"Roughness {CURVE_ROUGHNESS} for the multiplicative models. Each cell: coverage / false reach (calibrated cells).", "",
              "| threshold | " + " | ".join(n for n, _ in MODELS if n in keep) + " |",
              "|---|" + "---|" * sum(1 for n, _ in MODELS if n in keep)]
    curves = {n: coverage_by_confidence(keep[n]["p_reach"], keep[n]["truth"]) for n, _ in MODELS if n in keep}
    if curves:
        n_rows = len(next(iter(curves.values())))
        for i in range(n_rows):
            thr = next(iter(curves.values()))[i]["threshold"]
            cells = [f"{pct(c[i]['coverage'])} / {pct(c[i]['false_reach'])} ({c[i]['cells']})" for c in curves.values()]
            lines.append(f"| {thr} | " + " | ".join(cells) + " |")
    lines.append("")
    return lines


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-ids", nargs="*", help="default: every .npz in the tile directory")
    ap.add_argument("--scale-effect", type=Path, default=Path("reports/scale_effect.md"))
    ap.add_argument("--hurst", type=float, help="override H (default: read from the scale-effect report)")
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    args = ap.parse_args()

    hurst = args.hurst if args.hurst is not None else read_hurst(args.scale_effect)
    ids = args.tile_ids or sorted(p.stem for p in args.tile_dir.glob("*.npz"))
    tiles = [(i, load_tile(i, args.tile_dir)) for i in ids]
    missing = [i for i, t in tiles if t is None]
    if missing:
        raise SystemExit(f"tile(s) not found: {missing}")
    if not tiles:
        raise SystemExit("no tiles to validate")

    lines = [
        "# Extended validation (exploratory, registered before it was run)",
        "",
        "This is not the validation result. The pre-registered headline in validation_report.md is unchanged.",
        "Registered in PREREGISTRATION.md, section \"Extended validation and sub-grid roughness\".",
        "",
        f"Fixed: habitat ({BASE['habitat_row']}, {BASE['habitat_col']}), budget {BASE['budget_s']} s, speed "
        f"{BASE['speed_mps']} m/s (assumed), cutoff {BASE['cutoff_deg']} deg (assumed), 16 realizations, seed 1234.",
        "",
        f"The hurst model uses H = {hurst:g}, read from {args.scale_effect}. That value was measured on the same 2 km "
        "window that is validated here, so every hurst row is IN-SAMPLE. No out-of-sample claim is made.",
        "",
        "All rows of all three models are reported. No row is chosen as the result. When one interval is needed, quote the "
        "wider of the Wilson and the block-bootstrap interval. If no row reaches 95 % coverage, that is a shortfall.",
        "",
    ]
    csv_rows: list[dict] = []
    for _, tile in tiles:
        lines += tile_section(tile, hurst, csv_rows)
    lines += [
        "How to read it:",
        "",
        "- Coverage = share of truth-reachable cells that the calibrated region contains. False reach = share of calibrated "
        "cells that the truth says are not reachable. Coverage is never read without false reach.",
        "- Wilson treats cells as independent. The block bootstrap resamples 200 m blocks and keeps cells inside a block together.",
        "- The Gaussian sub-grid noise of the hurst model is thin-tailed, the truth is not. Read the Brier skill score and the steep-cell results with that in mind.",
        "- Speeds, cutoff and roughness are assumptions. Each tile is one 2 km window of one terrain class.",
        "",
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    md = args.out_dir / "validation_extended.md"
    md.write_text("\n".join(lines), encoding="utf-8")
    with open(args.out_dir / "validation_extended.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(csv_rows)
    print(f"wrote {md} and {md.with_suffix('.csv')} ({len(csv_rows)} rows, {len(tiles)} tile(s), H = {hurst:g})")


if __name__ == "__main__":
    main()
