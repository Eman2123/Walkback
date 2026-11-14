"""Terrain tiles: the planner sees `coarse`, validation alone sees `fine` (the truth).

Real tiles are built from the 1 m HiRISE DTM by scripts/build_terrain.py (not done yet) and
stored as <tile_dir>/<tile_id>.npz with keys: coarse, fine, cell_m, label.

DEV_TILE_ID is synthetic terrain for development only. It is served only when WALKBACK_ENV=dev,
and its label says so in every response.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

import numpy as np

DEV_TILE_ID = "dev-synthetic-20m"
DEFAULT_TILE_DIR = Path(os.environ.get("WALKBACK_TILE_DIR", "data/processed"))


@dataclass(frozen=True)
class Tile:
    tile_id: str
    cell_m: float
    coarse: np.ndarray   # elevation in metres at the planning resolution
    fine: np.ndarray     # elevation in metres at truth resolution, validation only
    label: str


def synthetic_tile(seed: int = 7, n: int = 100, cell_m: float = 20.0) -> Tile:
    """Smooth sinusoidal terrain with small-scale roughness. Not Mars data."""
    rng = np.random.default_rng(seed)
    x = np.arange(n) * cell_m
    X, Y = np.meshgrid(x, x)
    fine = np.zeros((n, n))
    for _ in range(6):
        A = rng.uniform(4, 13)
        lx, ly = rng.uniform(300, 1200, 2)
        px, py = rng.uniform(0, 2 * np.pi, 2)
        fine += A * np.sin(2 * np.pi * X / lx + px) * np.cos(2 * np.pi * Y / ly + py)
    for _ in range(10):
        A = rng.uniform(1, 3.5)
        l = rng.uniform(50, 140)
        p, q = rng.uniform(0, 2 * np.pi, 2)
        fine += A * np.sin(2 * np.pi * X / l + p) * np.sin(2 * np.pi * Y / l + q)
    coarse = _box_blur(fine, radius=2)
    return Tile(
        tile_id=DEV_TILE_ID,
        cell_m=cell_m,
        coarse=coarse,
        fine=fine,
        label="SYNTHETIC development terrain (not Mars data)",
    )


def _box_blur(z: np.ndarray, radius: int) -> np.ndarray:
    n = z.shape[0]
    out = np.zeros_like(z)
    for i in range(n):
        for j in range(n):
            y0, y1 = max(0, i - radius), min(n, i + radius + 1)
            x0, x1 = max(0, j - radius), min(n, j + radius + 1)
            out[i, j] = z[y0:y1, x0:x1].mean()
    return out


def load_tile(tile_id: str, tile_dir: Path = DEFAULT_TILE_DIR) -> Tile | None:
    path = tile_dir / f"{tile_id}.npz"
    if not path.exists():
        return None
    with np.load(path, allow_pickle=False) as d:
        return Tile(
            tile_id=tile_id,
            cell_m=float(d["cell_m"]),
            coarse=d["coarse"],
            fine=d["fine"],
            label=str(d["label"]),
        )
