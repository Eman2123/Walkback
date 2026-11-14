"""Build the planner (coarse) and truth (fine) arrays for one tile from a 1 m elevation window.

Degradation is block averaging: the planner sees a 200 m model, shown on the 20 m grid,
and the truth is the 20 m block mean of the 1 m DTM. The planner never sees the truth.
"""
from __future__ import annotations

import numpy as np

from ..degrade import block_mean

GRID = 100          # cells per side in the API (fixed)
FINE_CELL_M = 20.0
COARSE_CELL_M = 200.0


def build_arrays(z_1m: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """z_1m must be square with side GRID * FINE_CELL_M (2000 px for the 2 km tile)."""
    side = GRID * int(FINE_CELL_M)
    if z_1m.shape != (side, side):
        raise ValueError(f"expected a {side} x {side} window at 1 m, got {z_1m.shape}")
    fine = block_mean(z_1m, int(FINE_CELL_M))                       # 100 x 100 at 20 m
    coarse_small = block_mean(z_1m, int(COARSE_CELL_M))             # 10 x 10 at 200 m
    coarse = np.repeat(np.repeat(coarse_small, 10, axis=0), 10, axis=1)  # shown on the 20 m grid
    return coarse, fine
