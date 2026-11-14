"""Validation report written from a compute_run result. The status line is decided by the numbers, not by hand."""
from __future__ import annotations

from pathlib import Path

TARGET = 0.95


def _pct(x):
    return "n/a" if x is None else f"{x * 100:.1f} %"


def status_line(coverage: float | None) -> str:
    if coverage is None:
        return "Coverage could not be computed (the truth region is empty)."
    if coverage < TARGET:
        return f"SHORTFALL: coverage {_pct(coverage)} is below the 95 % target for this setting."
    return (f"Coverage {_pct(coverage)} meets the 95 % target for this setting. "
            "Check the sensitivity table before claiming it, because other settings may not.")


def write_report(result: dict, out_path: Path) -> Path:
    s = result["stats"]
    cal = result["calibration"]
    p = result["params"]
    lines = [
        "# Validation report",
        "",
        f"Tile: {result['tile']['label']}",
        f"Cell size: {result['tile']['cell_m']} m. Truth is the 20 m block mean of the 1 m DTM.",
        "",
        "## Headline (default setting, pre-registered)",
        "",
        status_line(s["coverage"]),
        "",
        f"- Settings: habitat ({p['habitat_row']}, {p['habitat_col']}), budget {p['budget_s']} s, "
        f"speed {p['speed_mps']} m/s (assumed), cutoff {p['cutoff_deg']} deg (assumed), "
        f"roughness {p['roughness']} (assumed), confidence {p['confidence']} (derived).",
        f"- Areas (km2): deterministic {s['area_km2']['deterministic']:.3f}, "
        f"calibrated {s['area_km2']['calibrated']:.3f}, truth {s['area_km2']['truth']:.3f}.",
        f"- Coverage of truth: {_pct(s['coverage'])} "
        f"(95 % CI {_pct(s['coverage_ci'][0])} to {_pct(s['coverage_ci'][1])}).",
        f"- Brier score: {s['brier']:.4f} (lower is better).",
        "",
        "## Reliability (predicted vs observed steep probability)",
        "",
        "| bin | cells | predicted | observed |",
        "|---|---|---|---|",
    ]
    for b in cal["bins"]:
        lines.append(f"| {b['bin']} | {b['n']} | {b['pred']:.3f} | {b['obs']:.3f} |")
    lines += ["", "## Assumptions used", "", "| name | value | label |", "|---|---|---|"]
    for a in result["assumptions"]:
        lines.append(f"| {a['name']} | {a['value']} | {a['label']} |")
    lines += [
        "",
        "## Limits",
        "",
        "- Result is for one 2 km window of one terrain class.",
        "- Walking speed, slope cutoff and roughness are assumptions, not measured values.",
        "- This is a planning aid, not flight software. No route is declared safe.",
        "",
    ]
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    return out_path
