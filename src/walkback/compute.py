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
from .pipeline.build import COARSE_CELL_M, FINE_CELL_M
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


KNIGHT_MOVES = [(1, 2), (2, 1), (1, -2), (2, -1), (-1, 2), (-2, 1), (-1, -2), (-2, -1)]
NEIGHBOURS16 = NEIGHBOURS + KNIGHT_MOVES
SOLVERS = {"dijkstra8": NEIGHBOURS, "dijkstra16": NEIGHBOURS16}
SPEED_MODELS = ("linear", "minetti", "minetti_cap")
DIRECTIONS = ("out", "back")
MINETTI_MAX_GRADE = 0.45   # range of the treadmill data the polynomial was fitted to


def minetti_cost(g):
    """Metabolic cost of walking, J per kg per m, at grade g (rise over run). Minetti et al. 2002, J Appl Physiol
    93:1039-1046, fitted between g = -0.45 and +0.45. g is clipped to that range."""
    g = np.clip(g, -MINETTI_MAX_GRADE, MINETTI_MAX_GRADE)
    return 280.5 * g**5 - 58.7 * g**4 - 76.8 * g**3 + 51.9 * g**2 + 19.6 * g + 2.5


def minetti_factor(g):
    """Direction factor f(g) = Cs(g) / C(g): the symmetric part of the cost over the cost in this direction.
    f(0) = 1, f < 1 where this direction is costlier than the average of up and down, f > 1 where it is cheaper."""
    return 0.5 * (minetti_cost(g) + minetti_cost(-g)) / minetti_cost(g)


def edge_factors(elev: np.ndarray, cell_m: float, neighbours, direction: str = "out", cap: bool = False) -> dict:
    """Per move, an array F with F[r, c] = direction factor for the edge between (r, c) and (r + dr, c + dc).

    direction "out": the crew walks from (r, c) to the neighbour (travel time from the habitat).
    direction "back": the crew walks from the neighbour to (r, c) (travel time to the habitat), so the grade is reversed.
    cap=True is the "minetti_cap" model: f is limited to 1, so there are uphill penalties and no downhill speed-up.
    Cells whose neighbour is outside the grid keep 1.0 (never used)."""
    if direction not in DIRECTIONS:
        raise ValueError(f"unknown direction: {direction}")
    sign = 1.0 if direction == "out" else -1.0
    n_r, n_c = elev.shape
    out = {}
    for dr, dc in neighbours:
        h = cell_m * math.hypot(dr, dc)
        F = np.ones(elev.shape)
        r0, r1 = max(0, -dr), min(n_r, n_r - dr)
        c0, c1 = max(0, -dc), min(n_c, n_c - dc)
        g = sign * (elev[r0 + dr:r1 + dr, c0 + dc:c1 + dc] - elev[r0:r1, c0:c1]) / h
        f = minetti_factor(g)
        F[r0:r1, c0:c1] = np.minimum(f, 1.0) if cap else f
        out[(dr, dc)] = F.tolist()
    return out


def travel_time(speed: np.ndarray, hab: tuple[int, int], cell_m: float, neighbours=NEIGHBOURS,
                factors: dict | None = None) -> np.ndarray:
    """Seconds from the habitat to every cell. Infinity where unreachable.

    neighbours: NEIGHBOURS (8, registered) or NEIGHBOURS16 (adds knight moves; both cells a knight move passes beside
    must be passable). factors: optional per-move direction factors from edge_factors(); None is the registered
    symmetric speed."""
    n_r, n_c = speed.shape
    v = speed.tolist()
    T = [[math.inf] * n_c for _ in range(n_r)]
    r0, c0 = hab
    if v[r0][c0] <= 0:
        return np.array(T)
    T[r0][c0] = 0.0
    heap = [(0.0, r0, c0)]
    moves = []
    for dr, dc in neighbours:
        step = cell_m * math.hypot(dr, dc)
        if abs(dr) == 2:
            mids = ((dr // 2, 0), (dr // 2, dc))
        elif abs(dc) == 2:
            mids = ((0, dc // 2), (dr, dc // 2))
        else:
            mids = ()
        moves.append((dr, dc, step, mids, None if factors is None else factors[(dr, dc)]))
    while heap:
        d, r, c = heapq.heappop(heap)
        if d > T[r][c]:
            continue
        for dr, dc, step, mids, fac in moves:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < n_r and 0 <= nc < n_c):
                continue
            if v[nr][nc] <= 0:          # impassable neighbour: never enter it
                continue
            if mids and (v[r + mids[0][0]][c + mids[0][1]] <= 0 or v[r + mids[1][0]][c + mids[1][1]] <= 0):
                continue                # a knight move may not pass beside an impassable cell
            vavg = (v[r][c] + v[nr][nc]) / 2
            if fac is not None:
                vavg *= fac[r][c]
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


PLANNER_SLOPES = ("staircase", "grid200")


def planner_slope(coarse: np.ndarray, cell_m: float, mode: str = "staircase") -> np.ndarray:
    """Slope the planner uses, in degrees, on the 20 m grid.

    "staircase" (registered, default): np.gradient on the 200 m blocks drawn on the 20 m grid. Inside a block the
        slope is exactly 0 and the whole step lands on the block edge, so it is not the slope a 200 m model has.
    "grid200" (exploratory variant): slope on the 10 x 10 grid of block means with 200 m spacing, each value
        repeated over its 20 m cells.
    """
    if mode == "staircase":
        return slope_deg(coarse, cell_m)
    if mode != "grid200":
        raise ValueError(f"unknown planner slope mode: {mode}")
    k = int(round(COARSE_CELL_M / FINE_CELL_M))
    n = coarse.shape[0]
    if coarse.shape[0] != coarse.shape[1] or n % k:
        raise ValueError("grid200 needs a square tile whose side is a whole number of 200 m blocks")
    small = coarse[k // 2::k, k // 2::k]
    if not np.allclose(np.repeat(np.repeat(small, k, axis=0), k, axis=1), coarse):
        raise ValueError("grid200 needs a planner DEM made of constant 200 m blocks")
    return np.repeat(np.repeat(slope_deg(small, cell_m * k), k, axis=0), k, axis=1)


ROUGHNESS_MODES = ("multiplicative", "hurst")


def hurst_subgrid(coarse: np.ndarray, cell_m: float, hurst: float) -> dict:
    """Sub-grid gradient noise predicted from the 200 m model alone plus a scale exponent H.

    The planner sees only the 200 m block means. G200 is the RMS gradient of that 10 x 10 grid. The scale law
    G ~ L^(H - 1) predicts the RMS gradient at the 20 m cell size, G20 = G200 x 10^(1 - H). The part the 200 m model
    cannot resolve is split evenly over the two gradient components:
        sigma = sqrt(max(G20^2 - G200^2, 0) / 2).
    Returns the 200 m gradient vector repeated over the 20 m cells (gx, gy, tangent units) and the numbers used.
    The truth is never used. H is an input (measured elsewhere), see PREREGISTRATION.md.
    """
    if not math.isfinite(hurst):
        raise ValueError("hurst exponent must be a finite number")
    k = int(round(COARSE_CELL_M / FINE_CELL_M))
    n = coarse.shape[0]
    if coarse.shape[0] != coarse.shape[1] or n % k:
        raise ValueError("hurst roughness needs a square tile whose side is a whole number of 200 m blocks")
    small = coarse[k // 2::k, k // 2::k]
    if not np.allclose(np.repeat(np.repeat(small, k, axis=0), k, axis=1), coarse):
        raise ValueError("hurst roughness needs a planner DEM made of constant 200 m blocks")
    dzdy, dzdx = np.gradient(small, cell_m * k)
    g200 = float(np.sqrt(np.mean(dzdx ** 2 + dzdy ** 2)))
    g20 = g200 * 10.0 ** (1.0 - hurst)
    sigma = math.sqrt(max(g20 ** 2 - g200 ** 2, 0.0) / 2.0)
    up = lambda a: np.repeat(np.repeat(a, k, axis=0), k, axis=1)  # noqa: E731
    return {"gx": up(dzdx), "gy": up(dzdy), "sigma": sigma, "g200": g200, "g20_pred": g20}


def compute_run(
    tile: Tile,
    params: dict,
    pin_start: bool = False,
    planner_slope_mode: str = "staircase",
    roughness_mode: str = "multiplicative",
    hurst: float | None = None,
    solver: str = "dijkstra8",
    speed_model: str = "linear",
    direction: str = "out",
    return_fields: bool = False,
) -> dict:
    """Run the walkback model.

    pin_start=False is the pre-registered behaviour and the default everywhere (API, report).
    pin_start=True keeps the habitat cell passable in every ensemble realization. It exists only for
    the post-hoc diagnostic in scripts/start_cell_diagnostic.py and must not replace the registered result.
    planner_slope_mode="staircase" is the registered behaviour. "grid200" is the exploratory variant used only by
    scripts/planner_slope_variant.py (see PREREGISTRATION.md).
    roughness_mode="multiplicative" is the registered behaviour. "hurst" is the exploratory, opt-in variant of the
    "Extended validation" section of PREREGISTRATION.md: it needs planner_slope_mode="grid200" and an exponent H, it
    ignores params["roughness"], and H is an input measured elsewhere (in-sample if measured on this tile).
    solver="dijkstra8" is the registered behaviour; "dijkstra16" adds knight moves. speed_model="linear" is the registered
    behaviour; "minetti" multiplies the edge speed by a direction factor from the Minetti 2002 walking cost, and
    "minetti_cap" limits that factor to 1 (no downhill speed-up).
    direction="out" is the registered behaviour (time from the habitat); "back" is the time from each cell to the habitat.
    All three are the opt-in variants of the "Solver and directional speed" section of PREREGISTRATION.md.
    return_fields=True adds the underlying arrays under "_fields" (not JSON serializable; for scripts only).
    """
    if roughness_mode not in ROUGHNESS_MODES:
        raise ValueError(f"unknown roughness mode: {roughness_mode}")
    if solver not in SOLVERS:
        raise ValueError(f"unknown solver: {solver}")
    if speed_model not in SPEED_MODELS:
        raise ValueError(f"unknown speed model: {speed_model}")
    if direction not in DIRECTIONS:
        raise ValueError(f"unknown direction: {direction}")
    nb = SOLVERS[solver]
    sub = None
    if roughness_mode == "hurst":
        if planner_slope_mode != "grid200":
            raise ValueError("hurst roughness needs planner_slope_mode='grid200'")
        if hurst is None:
            raise ValueError("hurst roughness needs the exponent H")
        sub = hurst_subgrid(tile.coarse, tile.cell_m, hurst)
    t0 = time.perf_counter()
    cell = tile.cell_m
    hab = (params["habitat_row"], params["habitat_col"])
    budget, v_flat, cutoff = params["budget_s"], params["speed_mps"], params["cutoff_deg"]
    conf, rough = params["confidence"], params["roughness"]

    slope_coarse = planner_slope(tile.coarse, cell, planner_slope_mode)
    slope_fine = slope_deg(tile.fine, cell)
    if slope_coarse[hab] >= cutoff or slope_fine[hab] >= cutoff:
        raise ValueError("habitat is impassable at coarse or fine resolution")

    fac_plan = fac_truth = None
    if speed_model in ("minetti", "minetti_cap"):
        cap = speed_model == "minetti_cap"
        fac_plan = edge_factors(tile.coarse, cell, nb, direction, cap)
        fac_truth = edge_factors(tile.fine, cell, nb, direction, cap)

    speed_det = speed_field(slope_coarse, v_flat, cutoff)
    det = travel_time(speed_det, hab, cell, nb, fac_plan) <= budget
    truth = travel_time(speed_field(slope_fine, v_flat, cutoff), hab, cell, nb, fac_truth) <= budget

    rng = np.random.default_rng(ENSEMBLE_SEED)
    reach = np.zeros(tile.coarse.shape)
    steep = np.zeros(tile.coarse.shape)
    for _ in range(ENSEMBLE_K):
        if sub is None:
            factor = np.exp(rough * rng.standard_normal(tile.coarse.shape))
            sk = slope_coarse * factor
        else:
            ex = sub["sigma"] * rng.standard_normal(tile.coarse.shape)
            ey = sub["sigma"] * rng.standard_normal(tile.coarse.shape)
            sk = np.degrees(np.arctan(np.hypot(sub["gx"] + ex, sub["gy"] + ey)))
        steep += sk >= cutoff
        speed_k = speed_field(sk, v_flat, cutoff)
        if pin_start:
            speed_k[hab] = speed_det[hab]   # the crew starts here, so the start cell is not re-rolled
        reach += travel_time(speed_k, hab, cell, nb, fac_plan) <= budget
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

    result = {
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
            "brier_baseline": round(float(obs_steep.mean()) * (1 - float(obs_steep.mean())), 4),
            "false_reach": None if counts["calibrated"] == 0 else round(int((cal & ~truth).sum()) / counts["calibrated"], 4),
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
    if sub is not None:   # only the opt-in variant adds keys, so the registered output is unchanged
        result["assumptions"] = [a for a in result["assumptions"] if a["name"] != "unresolved_roughness"] + [
            {"name": "hurst_exponent", "value": str(hurst), "label": "measured elsewhere (in-sample if on this tile)"},
            {"name": "subgrid_gradient_sigma", "value": f"{sub['sigma']:.4f}", "label": "derived"},
        ]
        result["variant"] = {
            "roughness_mode": "hurst", "hurst": hurst,
            "g200": round(sub["g200"], 5), "g20_pred": round(sub["g20_pred"], 5), "sigma": round(sub["sigma"], 5),
        }
    if (solver, speed_model, direction) != ("dijkstra8", "linear", "out"):   # opt-in only, registered output unchanged
        result.setdefault("variant", {}).update({"solver": solver, "speed_model": speed_model, "direction": direction})
        if speed_model in ("minetti", "minetti_cap"):
            how = "edge factor min(Cs/C, 1), no downhill speed-up" if speed_model == "minetti_cap" else "edge factor Cs(g)/C(g)"
            result["assumptions"] += [
                {"name": "directional_speed", "value": f"Minetti et al. 2002 walking cost, {how}", "label": "assumed (Earth treadmill, speed inverse to cost, no Mars gravity or suit)"},
            ]
    if return_fields:
        result["_fields"] = {
            "p_reach": p_reach, "p_steep": p_steep, "cal": cal, "truth": truth, "det": det,
            "obs_steep": obs_steep, "slope_fine": slope_fine, "slope_coarse": slope_coarse,
        }
    return result


PROFILE_V2 = "v2"


def compute_run_v2(tile: Tile, params: dict, **kwargs) -> dict:
    """Model profile v2 (PREREGISTRATION.md, "Model profile v2"): the registered model with two changes.

    pin_start=True: the habitat cell is not re-rolled in the ensemble (the crew starts inside the habitat; in the
    registered model that cell was blocked in 12.5 % of the realizations at roughness 0.5, which emptied the calibrated
    region at confidence 0.9). direction="back": the time TO the habitat, the "walkback" question (equal to the time
    from it under the symmetric linear speed model). Everything else is as registered. compute_run keeps the registered
    defaults, so v1 stays reproducible. Other keyword arguments (planner_slope_mode, solver, ...) pass through.
    """
    for forbidden in ("pin_start", "direction"):
        if forbidden in kwargs:
            raise TypeError(f"{forbidden} is fixed by the v2 profile")
    result = compute_run(tile, params, pin_start=True, direction="back", **kwargs)
    result.setdefault("variant", {}).update({"profile": PROFILE_V2, "pin_start": True, "direction": "back"})
    result["assumptions"] += [
        {"name": "start_cell", "value": "the habitat cell stays passable in every realization (the crew starts inside it)", "label": "assumed"},
        {"name": "return_direction", "value": "time to the habitat; equal to the time from it under the symmetric linear speed model", "label": "assumed"},
        {"name": "mobility_not_modelled", "value": "Mars gravity, suit and load, rocks, sand, boot slip, rest and fatigue are not modelled; speed falls linearly with slope to zero at the cutoff", "label": "assumed"},
    ]
    return result
