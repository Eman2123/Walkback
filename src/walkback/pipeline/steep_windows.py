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


PLANNER_BLOCK = 10   # 200 m planner block = 10 x 10 cells of 20 m


def planner_center_deg(block20: np.ndarray, cell_m: float = 20.0) -> tuple[float, float]:
    """Slope at the habitat cell (grid // 2, grid // 2) as the PLANNER sees it, for one window of 20 m cells.

    Returns (staircase, grid200). The window is block-averaged to 200 m, the same degradation as
    pipeline.build.build_arrays. staircase = slope on the 200 m blocks drawn on the 20 m grid (registered model;
    the habitat cell sits on a block edge, so a step between two blocks lands on it). grid200 = slope on the 10 x 10
    grid of block means, read at the block that contains the habitat cell.
    """
    k = PLANNER_BLOCK
    n = block20.shape[0]
    if block20.shape != (n, n) or n % k:
        raise ValueError("need a square window of whole 200 m blocks")
    small = block20.reshape(n // k, k, n // k, k).mean(axis=(1, 3))
    coarse = np.repeat(np.repeat(small, k, axis=0), k, axis=1)
    half = n // 2
    stair = float(slope_deg(coarse, cell_m)[half, half])
    g200 = float(slope_deg(small, cell_m * k)[half // k, half // k])
    return stair, g200


@dataclass(frozen=True)
class Window:
    row: int            # top-left row on the 20 m grid
    col: int            # top-left column on the 20 m grid
    steep_share: float  # share of cells at or above the cutoff
    mean_deg: float
    p95_deg: float
    center_deg: float   # slope at the habitat cell (grid // 2, grid // 2), 20 m truth scale
    planner_stair_deg: float = float("nan")   # same cell, registered (staircase) planner slope
    planner_g200_deg: float = float("nan")    # same cell, grid200 planner slope


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
    require_planner_center: bool = False,
    exclude: list[tuple[int, int]] | None = None,
) -> list[Window]:
    """Return up to top_n non-overlapping grid x grid windows, steepest first.

    Windows with any nodata (NaN) are dropped. Windows that are mostly steep are dropped too
    (max_steep_share): if nothing is reachable the test is as uninformative as when everything is.
    With require_walkable_center the habitat cell (center) must itself be below the cutoff at the 20 m truth scale.
    With require_planner_center it must also be below the cutoff in the planner's own slope (staircase AND grid200),
    which is what compute_run checks and what made steep-1 and steep-2 fail ("habitat is impassable").
    exclude lists (row, col) top-left corners on the 20 m grid of windows already analysed: a candidate that
    overlaps one is not returned (same separation rule as between chosen windows).
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
    blocked: list[tuple[int, int]] = list(exclude or [])
    for i in order:
        r, c = int(rows[i]), int(cols[i])
        if not all(max(abs(r - r0), abs(c - c0)) >= sep for r0, c0 in chosen + blocked):
            continue
        if require_planner_center:
            st, g2 = planner_center_deg(z20[r:r + grid, c:c + grid], cell_m)
            if not (st < cutoff_deg and g2 < cutoff_deg):
                continue
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
            planner_stair_deg=planner_center_deg(z20[r:r + grid, c:c + grid], cell_m)[0],
            planner_g200_deg=planner_center_deg(z20[r:r + grid, c:c + grid], cell_m)[1],
        ))
    return out
