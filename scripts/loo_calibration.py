"""Leave-one-window-out calibration, as registered in PREREGISTRATION.md ("Leave-one-window-out calibration").

EXPLORATORY. It looks for a setting (planner slope, roughness, confidence) that lowers false reach WITHOUT being tuned
on the window it is judged on: for each tile, the setting is chosen on all the other tiles and then run on that tile.
It uses the v2 profile. It needs at least 3 tiles in the tile directory (the owner's computer has 7); it changes no
default and no registered number.

Usage (repo root):
    PYTHONPATH=src python scripts/loo_calibration.py
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from walkback.compute import compute_run_v2
from walkback.tiles import load_tile
from walkback.validation.loo import (
    CONFIDENCE, DEFAULT_SETTING, PLANNERS, ROUGHNESS, TARGET, all_settings, select_setting,
)
from walkback.validation.metrics import block_bootstrap_ci, brier_skill_score

BASE = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5, "cutoff_deg": 20.0}
CSV_FIELDS = ["held_out", "which", "planner", "roughness", "confidence", "target_met_on_training", "cal_km2",
              "truth_km2", "coverage", "wilson_low", "wilson_high", "boot_low", "boot_high", "false_reach", "bss", "note"]


def pct(x):
    return "n/a" if x is None else f"{x * 100:.1f} %"


def ci(lo, hi):
    return "n/a" if lo is None or hi is None else f"{pct(lo)} to {pct(hi)}"


def run_cell(tile, setting):
    planner, rough, conf = setting
    try:
        res = compute_run_v2(tile, dict(BASE, confidence=conf, roughness=rough),
                             planner_slope_mode=planner, return_fields=True)
    except ValueError as exc:
        return {"error": str(exc)}
    s, f = res["stats"], res["_fields"]
    obs = f["obs_steep"].astype(float)
    brier_full = float(np.mean((f["p_steep"] - obs) ** 2))
    noskill = float(obs.mean() * (1.0 - obs.mean()))
    boot = block_bootstrap_ci(f["cal"], f["truth"])[:2]
    return {
        "coverage": s["coverage"], "false_reach": s["false_reach"], "wilson": tuple(s["coverage_ci"]), "boot": boot,
        "bss": brier_skill_score(brier_full, noskill), "cal_km2": s["area_km2"]["calibrated"],
        "truth_km2": s["area_km2"]["truth"],
    }


def row_text(r):
    if r is None or "error" in (r or {}):
        return ["not computed"] + [""] * 4
    return [f"{pct(r['coverage'])} ({ci(*r['wilson'])}; boot {ci(*r['boot'])})", pct(r["false_reach"]),
            "n/a" if np.isnan(r["bss"]) else f"{r['bss']:+.3f}", f"{r['cal_km2']:.3f} / {r['truth_km2']:.3f}"]


def run(tile_dir: Path, ids: list[str], settings, out_dir: Path) -> tuple[Path, Path]:
    tiles = {i: load_tile(i, tile_dir) for i in ids}
    missing = [i for i, t in tiles.items() if t is None]
    if missing:
        raise SystemExit(f"tile(s) not found: {missing}")
    if len(ids) < 3:
        raise SystemExit("leave-one-window-out needs at least 3 tiles")

    # the v2 default setting is always computed, also when a reduced grid leaves it out of the candidates
    cells = {(i, s): run_cell(tiles[i], s) for i in ids for s in sorted(set(settings) | {DEFAULT_SETTING})}
    table = {k: (None if "error" in v else v) for k, v in cells.items() if k[1] in set(settings)}

    lines = [
        "# Leave-one-window-out calibration (exploratory, registered before it was run)",
        "",
        "Registered in PREREGISTRATION.md, section \"Model profile v2 ... and leave-one-window-out calibration\". "
        "Profile v2, habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20 deg (assumed), 16 realizations, seed 1234.",
        "",
        f"Tiles ({len(ids)}): {', '.join(ids)}. Settings ({len(settings)}): planner {sorted({s[0] for s in settings})}, "
        f"roughness {sorted({s[1] for s in settings})}, confidence {sorted({s[2] for s in settings})}.",
        "",
        "For each held-out tile the setting is chosen on the other tiles only (eligible: computes on every training tile; "
        f"lowest mean training false reach among settings with mean training coverage at or above {TARGET:.0%}; otherwise the highest mean "
        "training coverage, flagged). It is then run on the held-out tile and shown next to the v2 default setting "
        f"{DEFAULT_SETTING}. Every fold is reported. The held-out mean is an estimate from {len(ids)} windows of one DTM, some chosen by steepness; "
        "it is not a claim about other terrain, and no selected setting becomes a default without its own registration.",
        "",
        "| held-out tile | which | setting (planner, roughness, confidence) | training target met | coverage (Wilson; block bootstrap) | false reach | Brier skill | calibrated / truth km2 |",
        "|---|---|---|---|---|---|---|---|",
    ]
    csv_rows, chosen_fr, default_fr, chosen_cov, default_cov = [], [], [], [], []
    for held in ids:
        train = [i for i in ids if i != held]
        sel, met, n_elig = select_setting(table, train, settings)
        pair = [("selected", sel, "yes" if met else ("NO" if sel else "no eligible setting")),
                ("v2 default", DEFAULT_SETTING, "")]
        for which, st, flag in pair:
            r = None if st is None else cells.get((held, st))
            if st is None:
                lines.append(f"| {held} | {which} | none ({n_elig} eligible) | {flag} | not computed | | | |")
                csv_rows.append(dict(held_out=held, which=which, note="no eligible setting"))
                continue
            vals = row_text(r)
            lines.append(f"| {held} | {which} | {st} | {flag} | " + " | ".join(vals) + " |")
            ok = r is not None and "error" not in r
            csv_rows.append(dict(
                held_out=held, which=which, planner=st[0], roughness=st[1], confidence=st[2], target_met_on_training=flag,
                cal_km2=r["cal_km2"] if ok else "", truth_km2=r["truth_km2"] if ok else "",
                coverage=r["coverage"] if ok else "", wilson_low=r["wilson"][0] if ok else "",
                wilson_high=r["wilson"][1] if ok else "", boot_low=r["boot"][0] if ok else "",
                boot_high=r["boot"][1] if ok else "", false_reach=r["false_reach"] if ok else "",
                bss=("" if (not ok or np.isnan(r["bss"])) else round(r["bss"], 4)), note="" if ok else r["error"]))
            if ok and r["coverage"] is not None:
                (chosen_cov if which == "selected" else default_cov).append(r["coverage"])
                (chosen_fr if which == "selected" else default_fr).append(r["false_reach"] or 0.0)
    lines += ["", "Mean over the folds that computed (false reach of an empty region counted as 0):", "",
              "| which | folds computed | mean coverage | mean false reach |", "|---|---|---|---|"]
    for name, cov, fr in (("selected", chosen_cov, chosen_fr), ("v2 default", default_cov, default_fr)):
        lines.append(f"| {name} | {len(cov)} of {len(ids)} | {pct(np.mean(cov)) if cov else 'n/a'} | {pct(np.mean(fr)) if fr else 'n/a'} |")
    lines += ["",
              "Reading it: a lower held-out false reach with coverage still below the target is a trade, not a fix. The registered planner "
              "(staircase) does not run on tiles whose habitat cell is impassable at 200 m, so it is ineligible whenever such a tile is in the training set.",
              "Speed, cutoff and roughness are assumptions; the truth shares the speed model, so none of this tests the speed model itself (docs/mobility-assumptions.md).",
              ""]
    out_dir.mkdir(parents=True, exist_ok=True)
    md, cs = out_dir / "loo_calibration.md", out_dir / "loo_calibration.csv"
    md.write_text("\n".join(lines), encoding="utf-8")
    with open(cs, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
        w.writeheader()
        w.writerows(csv_rows)
    return md, cs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-ids", nargs="*", help="default: every .npz in the tile directory")
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    ap.add_argument("--planners", nargs="*", default=list(PLANNERS))
    ap.add_argument("--roughness", nargs="*", type=float, default=list(ROUGHNESS))
    ap.add_argument("--confidence", nargs="*", type=float, default=list(CONFIDENCE))
    a = ap.parse_args()
    ids = a.tile_ids or sorted(p.stem for p in a.tile_dir.glob("*.npz"))
    md, cs = run(a.tile_dir, ids, all_settings(a.planners, a.roughness, a.confidence), a.out_dir)
    print(f"wrote {md} and {cs}")


if __name__ == "__main__":
    main()
