"""Measured scale effect of slope on a terrain window.

RMS gradient G(L) is computed at baselines L = factor x cell (block-averaged terrain).
A log-log fit gives G ~ L^b, and a Hurst-style exponent H = b + 1.
Values are measured from the window they are computed on. They are not assumed.
"""
from __future__ import annotations

import numpy as np

from ..degrade import block_mean

FACTORS = (1, 2, 4, 5, 8, 10, 16, 20, 25, 40, 50, 80, 100)


def rms_gradient(z: np.ndarray, cell_m: float, factor: int) -> float:
    zz = block_mean(z, factor) if factor > 1 else z
    baseline = cell_m * factor
    dzdy, dzdx = np.gradient(zz, baseline)
    return float(np.sqrt(np.mean(dzdx ** 2 + dzdy ** 2)))


def measure_scale_effect(z: np.ndarray, cell_m: float, factors=FACTORS) -> dict:
    baselines, grads = [], []
    for f in factors:
        if z.shape[0] // f < 3 or z.shape[1] // f < 3:
            continue
        baselines.append(cell_m * f)
        grads.append(rms_gradient(z, cell_m, f))
    if len(baselines) < 3:
        raise ValueError("need at least 3 baselines to fit the scale effect")
    L = np.log(np.array(baselines))
    G = np.log(np.array(grads))
    b, a = np.polyfit(L, G, 1)
    fit = a + b * L
    ss_res = float(np.sum((G - fit) ** 2))
    ss_tot = float(np.sum((G - G.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    return {
        "baselines_m": baselines,
        "rms_gradient": grads,
        "slope_b": float(b),
        "H": float(b + 1.0),
        "r2": r2,
    }
