"""Walkback computation: speed model, travel time (Dijkstra, 8-connected), ensemble calibration.

Pure Python plus numpy, so the API does not need scikit-fmm. The speed model and the
calibration logic match the browser demo, and they are assumptions until sources are confirmed.
"""
from __future__ import annotations

import heapq
import math
import time

import numpy as np

from .calibrate import brier, coverage, reliability_bins
from .slope import slope_deg
from .tiles import Tile

ENSEMBLE_K = 16          # realizations for the calibrated region
ENSEMBLE_SEED = 1234     # fixed, so the same parameters give the same result
NEIGHBOURS = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]


def speed_field(slope: np.ndarray, v_flat: float, cutoff_deg: float) -> np.ndarray:
    """Assumed linear speed reduction with slope. Zero at or above the cutoff (impassable)."""
    v = v_flat * np.clip(1.0 - slope / cutoff_deg, 0.0, 1.0)
    v[slope >= cutoff_deg] = 0.0
    return v


def travel_time(speed: np.ndarray, hab: tuple[int, int], cell_m: float) -> np.ndarray:
    """Seconds from the habitat to every cell. Infinity where unreachable."""
    n_r, n_c = speed.shape
    v = speed.tolist()
    T = [[math.inf] * n_c for _ in range(n_r)]
    r0, c0 = hab
    if v[r0][c0] <= 0:
        return np.array(T)
    T[r0][c0] = 0.0
    heap = [(0.0, r0, c0)]
    diag = cell_m * math.sqrt(2)
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > T[r][c]:
            continue
        for dr, dc in NEIGHBOURS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n_r and 0 <= nc < n_c):
                continue
            if v[nr][nc] <= 0:          # impassable neighbour: never enter it
                continue
            vavg = (v[r][c] + v[nr][nc]) / 2
            step = diag if (dr and dc) else cell_m
            nd = d + step / vavg
            if nd < T[nr][nc]:
                T[nr][nc] = nd
                heapq.heappush(heap, (nd, nr, nc))
    return np.array(T)


def runs_to_geojson(mask: np.ndarray, cell_m: float) -> dict:
    """MultiPolygon of horizontal runs of True cells, in local metres (CRS.Simple)."""
    polys = []
    for r in range(mask.shape[0]):
        row = mask[r]
        c = 0
        while c < mask.shape[1]:
            if row[c]:
                start = c
                while c + 1 < mask.shape[1] and row[c + 1]:
                    c += 1
                x0, x1 = start * cell_m, (c + 1) * cell_m
                y0, y1 = r * cell_m, (r + 1) * cell_m
                polys.append([[[x0, y0], [x1, y0], [x1, y1], [x0, y1], [x0, y0]]])
            c += 1
    return {"type": "MultiPolygon", "coordinates": polys}


def wilson_ci(successes: int, n: int, z: float = 1.96) -> tuple[float | None, float | None]:
    if n == 0:
        return None, None
    p = successes / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def compute_run(tile: Tile, params: dict, pin_start: bool = False) -> dict:
    """Run the walkback model.

    pin_start=False is the pre-registered behaviour and the default everywhere (API, report).
    pin_start=True keeps the habitat cell passable in every ensemble realization. It exists only for
    the post-hoc diagnostic in scripts/start_cell_diagnostic.py and must not replace the registered result.
    """
    t0 = time.perf_counter()
    cell = tile.cell_m
    hab = (params["habitat_row"], params["habitat_col"])
    budget, v_flat, cutoff = params["budget_s"], params["speed_mps"], params["cutoff_deg"]
    conf, rough = params["confidence"], params["roughness"]

    slope_coarse = slope_deg(tile.coarse, cell)
    slope_fine = slope_deg(tile.fine, cell)
    if slope_coarse[hab] >= cutoff or slope_fine[hab] >= cutoff:
        raise ValueError("habitat is impassable at coarse or fine resolution")

    speed_det = speed_field(slope_coarse, v_flat, cutoff)
    det = travel_time(speed_det, hab, cell) <= budget
    truth = travel_time(speed_field(slope_fine, v_flat, cutoff), hab, cell) <= budget

    rng = np.random.default_rng(ENSEMBLE_SEED)
    reach = np.zeros(tile.coarse.shape)
    steep = np.zeros(tile.coarse.shape)
    for _ in range(ENSEMBLE_K):
        factor = np.exp(rough * rng.standard_normal(tile.coarse.shape))
        sk = slope_coarse * factor
        steep += sk >= cutoff
        speed_k = speed_field(sk, v_flat, cutoff)
        if pin_start:
            speed_k[hab] = speed_det[hab]   # the crew starts here, so the start cell is not re-rolled
        reach += travel_time(speed_k, hab, cell) <= budget
    p_reach = reach / ENSEMBLE_K
    p_steep = steep / ENSEMBLE_K
    cal = p_reach >= conf

    obs_steep = slope_fine >= cutoff
    bins = reliability_bins(p_steep.ravel(), obs_steep.ravel().astype(float))
    b = brier(p_steep.ravel(), obs_steep.ravel().astype(float))
    cov = coverage(cal, truth)
    n_truth = int(truth.sum())
    lo, hi = wilson_ci(int((cal & truth).sum()), n_truth)

    cell_km2 = cell * cell / 1e6
    counts = {"deterministic": int(det.sum()), "calibrated": int(cal.sum()), "truth": n_truth}
    runtime_ms = int((time.perf_counter() - t0) * 1000)

    return {
        "tile": {"id": tile.tile_id, "cell_m": cell, "label": tile.label},
        "params": params,
        "regions": {
            "deterministic": runs_to_geojson(det, cell),
            "calibrated": runs_to_geojson(cal, cell),
            "truth": runs_to_geojson(truth, cell),
        },
        "stats": {
            "area_km2": {k: round(v * cell_km2, 3) for k, v in counts.items()},
            "counts": counts,
            "coverage": None if math.isnan(cov) else round(cov, 4),
            "coverage_ci": [lo, hi] if lo is not None else [None, None],
            "brier": round(b, 4),
            "runtime_ms": runtime_ms,
        },
        "calibration": {
            "bins": bins,
            "brier": round(b, 4),
            "coverage": None if math.isnan(cov) else round(cov, 4),
            "coverage_ci": [lo, hi] if lo is not None else [None, None],
        },
        "assumptions": [
            {"name": "time_budget_s", "value": str(budget), "label": "assumed"},
            {"name": "walking_speed_mps", "value": str(v_flat), "label": "assumed"},
            {"name": "slope_cutoff_deg", "value": str(cutoff), "label": "assumed"},
            {"name": "confidence_threshold", "value": str(conf), "label": "derived"},
            {"name": "unresolved_roughness", "value": str(rough), "label": "assumed"},
            {"name": "resolution_m", "value": str(cell), "label": "derived"},
            {"name": "ensemble_realizations", "value": str(ENSEMBLE_K), "label": "derived"},
        ],
    }
