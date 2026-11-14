"""Sensitivity analysis over unresolved roughness and confidence threshold.

Exploratory. It never changes the default run. See PREREGISTRATION.md (sensitivity section).
"""
from __future__ import annotations

import csv
from pathlib import Path

from .compute import compute_run
from .tiles import Tile

ROUGHNESS_GRID = [0.1, 0.3, 0.5]
CONFIDENCE_GRID = [0.5, 0.7, 0.9]
DEFAULT = {"roughness": 0.5, "confidence": 0.9}
BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0}
FIELDS = [
    "roughness", "confidence", "is_default",
    "det_km2", "cal_km2", "truth_km2",
    "coverage", "coverage_ci_low", "coverage_ci_high", "brier",
]


def run_sensitivity(tile: Tile, habitat_row: int = 50, habitat_col: int = 50) -> list[dict]:
    rows = []
    for rough in ROUGHNESS_GRID:
        for conf in CONFIDENCE_GRID:
            params = {**BASE, "habitat_row": habitat_row, "habitat_col": habitat_col,
                      "roughness": rough, "confidence": conf}
            res = compute_run(tile, params)
            ci = res["stats"]["coverage_ci"]
            rows.append({
                "roughness": rough,
                "confidence": conf,
                "is_default": rough == DEFAULT["roughness"] and conf == DEFAULT["confidence"],
                "det_km2": res["stats"]["area_km2"]["deterministic"],
                "cal_km2": res["stats"]["area_km2"]["calibrated"],
                "truth_km2": res["stats"]["area_km2"]["truth"],
                "coverage": res["stats"]["coverage"],
                "coverage_ci_low": ci[0],
                "coverage_ci_high": ci[1],
                "brier": res["stats"]["brier"],
            })
    return rows


def write_outputs(rows: list[dict], tile_label: str, out_dir: Path) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "sensitivity.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    def pct(x):
        return "n/a" if x is None else f"{x * 100:.1f} %"

    lines = [
        "# Sensitivity analysis (exploratory)",
        "",
        f"Tile: {tile_label}",
        "Fixed: habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20 deg (assumed), 16 realizations.",
        "Default setting: roughness 0.5, confidence 0.9 (marked). Not changed by these results.",
        "",
        "| roughness | confidence | default | deterministic km2 | calibrated km2 | truth km2 | coverage (CI) | Brier |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        ci = "" if r["coverage_ci_low"] is None else f" ({pct(r['coverage_ci_low'])}-{pct(r['coverage_ci_high'])})"
        lines.append(
            f"| {r['roughness']} | {r['confidence']} | {'yes' if r['is_default'] else ''} | "
            f"{r['det_km2']:.3f} | {r['cal_km2']:.3f} | {r['truth_km2']:.3f} | {pct(r['coverage'])}{ci} | {r['brier']:.4f} |"
        )
    best = max((r["coverage"] or 0) for r in rows)
    lines += [
        "",
        f"Highest coverage across all 9 settings: {pct(best)}.",
        "If this is below 95 %, the result is a shortfall and must be reported as one.",
    ]
    md_path = out_dir / "sensitivity.md"
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return csv_path, md_path
