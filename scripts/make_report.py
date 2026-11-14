"""Write reports/validation_report.md for the default setting on the real tile.

Usage (repo root, venv active):
    $env:PYTHONPATH="src"
    python scripts/make_report.py --tile-dir data/processed --tile-id jezero-20m
"""
import argparse
from pathlib import Path

from walkback.compute import compute_run
from walkback.tiles import load_tile
from walkback.validation.report import write_report

DEFAULT = {"habitat_row": 50, "habitat_col": 50, "budget_s": 900, "speed_mps": 0.5,
           "cutoff_deg": 20.0, "confidence": 0.9, "roughness": 0.5}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-id", default="jezero-20m")
    ap.add_argument("--out", type=Path, default=Path("reports/validation_report.md"))
    args = ap.parse_args()
    tile = load_tile(args.tile_id, args.tile_dir)
    if tile is None:
        raise SystemExit(f"tile not found: {args.tile_dir / (args.tile_id + '.npz')}")
    result = compute_run(tile, dict(DEFAULT))
    print("wrote", write_report(result, args.out))


if __name__ == "__main__":
    main()
