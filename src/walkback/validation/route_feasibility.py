"""Route feasibility, registered in PREREGISTRATION.md ("Route feasibility").

The model gives an area. This module checks the ROUTE the planner would choose: walk that exact route on the
truth speed field and ask whether it gets home within the budget. Exploratory: changes no registered number.
Pure Python plus numpy, linear (symmetric) speed model, 8-connected, as in compute.travel_time.
"""
from __future__ import annotations

import heapq
import math

import numpy as np

from ..compute import NEIGHBOURS


def planner_tree(speed: np.ndarray, hab: tuple[int, int], cell_m: float):
    """Dijkstra from the habitat on `speed`. Returns (time, parent, order).

    time[r, c] is seconds (inf if unreachable), parent[r, c] is the flat index of the previous cell on the shortest
    route (-1 for the habitat and for unreachable cells), order lists the flat indices in settled order, so a parent
    always comes before its children. Same edge rule as compute.travel_time (never enter a cell of speed <= 0)."""
    n_r, n_c = speed.shape
    v = speed.tolist()
    T = np.full((n_r, n_c), math.inf)
    parent = np.full((n_r, n_c), -1, dtype=np.int64)
    order: list[int] = []
    r0, c0 = hab
    if v[r0][c0] <= 0:
        return T, parent, order
    T[r0, c0] = 0.0
    heap = [(0.0, r0, c0)]
    done = np.zeros((n_r, n_c), dtype=bool)
    while heap:
        d, r, c = heapq.heappop(heap)
        if done[r, c] or d > T[r, c]:
            continue
        done[r, c] = True
        order.append(r * n_c + c)
        for dr, dc in NEIGHBOURS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n_r and 0 <= nc < n_c) or v[nr][nc] <= 0:
                continue
            nd = d + cell_m * math.hypot(dr, dc) / ((v[r][c] + v[nr][nc]) / 2)
            if nd < T[nr, nc]:
                T[nr, nc] = nd
                parent[nr, nc] = r * n_c + c
                heapq.heappush(heap, (nd, nr, nc))
    return T, parent, order


def truth_time_along_tree(speed_truth: np.ndarray, parent: np.ndarray, order: list[int], hab: tuple[int, int],
                          cell_m: float) -> np.ndarray:
    """Seconds to walk, on the truth speed field, the planner's route from the habitat to every cell.

    inf where the planner has no route, or where its route enters a cell that is impassable in the truth."""
    n_r, n_c = speed_truth.shape
    vt = speed_truth.ravel()
    out = np.full(n_r * n_c, math.inf)
    h = hab[0] * n_c + hab[1]
    if vt[h] <= 0:
        return out.reshape(n_r, n_c)
    out[h] = 0.0
    for idx in order:
        p = parent.ravel()[idx]
        if p < 0:
            continue
        if vt[idx] <= 0 or not math.isfinite(out[p]):
            continue
        dr, dc = divmod(idx, n_c)[0] - divmod(p, n_c)[0], divmod(idx, n_c)[1] - divmod(p, n_c)[1]
        out[idx] = out[p] + cell_m * math.hypot(dr, dc) / ((vt[p] + vt[idx]) / 2)
    return out.reshape(n_r, n_c)


def route_feasibility(region: np.ndarray, plan_time: np.ndarray, truth_route_time: np.ndarray, budget_s: float) -> dict:
    """Feasibility of the planner routes to the cells of `region` (boolean mask, the habitat cell is ignored)."""
    mask = region & np.isfinite(plan_time) & (plan_time > 0)
    n = int(mask.sum())
    if n == 0:
        return {"n": 0, "feasible": 0, "share": None, "blocked": 0, "too_slow": 0, "ratio_median": None, "ratio_p95": None}
    t_truth = truth_route_time[mask]
    blocked = int((~np.isfinite(t_truth)).sum())
    feasible = int((t_truth <= budget_s).sum())
    finite = np.isfinite(t_truth)
    ratio = t_truth[finite] / plan_time[mask][finite]
    return {
        "n": n, "feasible": feasible, "share": feasible / n, "blocked": blocked,
        "too_slow": n - feasible - blocked,
        "ratio_median": float(np.median(ratio)) if ratio.size else None,
        "ratio_p95": float(np.percentile(ratio, 95)) if ratio.size else None,
    }
