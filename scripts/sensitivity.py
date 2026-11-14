"""Run the pre-registered sensitivity grid on the real tile and write reports/sensitivity.{csv,md}.

Usage (repo root, venv active):
    $env:PYTHONPATH="src"
    python scripts/sensitivity.py --tile-dir data/processed --tile-id jezero-20m
"""
import argparse
from pathlib import Path

from walkback.sensitivity import run_sensitivity, write_outputs
from walkback.tiles import load_tile


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tile-dir", type=Path, default=Path("data/processed"))
    ap.add_argument("--tile-id", default="jezero-20m")
    ap.add_argument("--out-dir", type=Path, default=Path("reports"))
    args = ap.parse_args()

    tile = load_tile(args.tile_id, args.tile_dir)
    if tile is None:
        raise SystemExit(f"tile not found: {args.tile_dir / (args.tile_id + '.npz')}")
    rows = run_sensitivity(tile)
    csv_path, md_path = write_outputs(rows, tile.label, args.out_dir)
    print(f"wrote {csv_path}")
    print(f"wrote {md_path}")


if __name__ == "__main__":
    main()
