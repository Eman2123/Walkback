"""Rank candidate 2 km windows of a DTM by how much of them is steep at the truth scale.

Why: the Jezero window used so far has only 0.2 % of 20 m cells at or above the 20 deg cutoff, so it
cannot tell a good planner from a bad one. This picks windows where the cutoff actually bites.

Works on the 20 m block-mean grid (the same degradation that makes the truth), so the slope seen here is the
slope the validation will see. Pure numpy; file reading lives in scripts/find_steep_windows.py.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..slope import slope_deg


@dataclass(frozen=True)
class Window:
    row: int            # top-left row on the 20 m grid
    col: int            # top-left column on the 20 m grid
    steep_share: float  # share of cells at or above the cutoff
    mean_deg: float
    p95_deg: float
    center_deg: float   # slope at the habitat cell (grid // 2, grid // 2)


def _box_sum(a: np.ndarray, k: int) -> np.ndarray:
    """Sum over every k x k window (top-left indexed), via an integral image."""
    c = np.pad(a.cumsum(axis=0).cumsum(axis=1), ((1, 0), (1, 0)))
    return c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]


def rank_windows(
    z20: np.ndarray,
    cell_m: float = 20.0,
    grid: int = 100,
    cutoff_deg: float = 20.0,
    stride: int = 25,
    top_n: int = 3,
    min_steep_share: float = 0.02,
    max_steep_share: float = 0.6,
    min_separation: int | None = None,
    require_walkable_center: bool = True,
) -> list[Window]:
    """Return up to top_n non-overlapping grid x grid windows, steepest first.

    Windows with any nodata (NaN) are dropped. Windows that are mostly steep are dropped too
    (max_steep_share): if nothing is reachable the test is as uninformative as when everything is.
    With require_walkable_center the habitat cell (center) must itself be below the cutoff.
    """
    z20 = np.asarray(z20, dtype=np.float64)
    if z20.ndim != 2 or min(z20.shape) < grid:
        raise ValueError(f"need a 2-D grid at least {grid} x {grid}, got {z20.shape}")
    if not 0.0 <= min_steep_share <= max_steep_share <= 1.0:
        raise ValueError("need 0 <= min_steep_share <= max_steep_share <= 1")
    sep = grid if min_separation is None else min_separation

    slope = slope_deg(z20, cell_m)          # NaN propagates to the neighbours of a NaN cell
    bad = ~np.isfinite(slope)
    s0 = np.where(bad, 0.0, slope)
    steep = (~bad) & (slope >= cutoff_deg)

    n_bad = _box_sum(bad.astype(np.int64), grid)
    n_steep = _box_sum(steep.astype(np.int64), grid)
    mean = _box_sum(s0, grid) / (grid * grid)
    share = n_steep / (grid * grid)

    ok = n_bad == 0
    ok &= (share >= min_steep_share) & (share <= max_steep_share)
    if require_walkable_center:
        half = grid // 2
        center = s0[half:half + ok.shape[0], half:half + ok.shape[1]]
        ok &= center < cutoff_deg
    # stride grid: only windows whose top-left lies on the stride lattice
    lattice = np.zeros_like(ok)
    lattice[::stride, ::stride] = True
    ok &= lattice

    rows, cols = np.nonzero(ok)
    order = np.lexsort((-mean[rows, cols], -share[rows, cols]))   # share first, mean breaks ties
    chosen: list[tuple[int, int]] = []
    for i in order:
        r, c = int(rows[i]), int(cols[i])
        if all(max(abs(r - r0), abs(c - c0)) >= sep for r0, c0 in chosen):
            chosen.append((r, c))
            if len(chosen) == top_n:
                break

    half = grid // 2
    out = []
    for r, c in chosen:
        block = slope[r:r + grid, c:c + grid]
        out.append(Window(
            row=r, col=c,
            steep_share=float(share[r, c]),
            mean_deg=float(mean[r, c]),
            p95_deg=float(np.percentile(block, 95)),
            center_deg=float(slope[r + half, c + half]),
        ))
    return out
