"""Extra validation metrics, registered in PREREGISTRATION.md ("Extended validation and sub-grid roughness").

All additive: none of them changes a registered number. Pure numpy.
"""
from __future__ import annotations

import numpy as np

from ..calibrate import coverage, reliability_bins

CONF_CURVE = (0.1, 0.25, 0.5, 0.7, 0.9, 0.95)


def brier_skill_score(brier_value: float, baseline: float) -> float:
    """1 - Brier / no-skill Brier. At or below 0 means no skill. NaN when the no-skill Brier is 0."""
    return float("nan") if baseline <= 0 else 1.0 - brier_value / baseline


def reach_reliability(p_reach: np.ndarray, truth: np.ndarray, n_bins: int = 10) -> list[dict]:
    """Reliability of the probability of reaching a cell against the truth reachable set."""
    return reliability_bins(p_reach.ravel(), truth.ravel().astype(float), n_bins)


def coverage_by_confidence(p_reach: np.ndarray, truth: np.ndarray, thresholds=CONF_CURVE) -> list[dict]:
    """Coverage, false reach and size of the calibrated region at each confidence threshold."""
    rows = []
    for thr in thresholds:
        cal = p_reach >= thr
        n_cal = int(cal.sum())
        cov = coverage(cal, truth)
        rows.append({
            "threshold": thr,
            "cells": n_cal,
            "coverage": None if np.isnan(cov) else cov,
            "false_reach": None if n_cal == 0 else float((cal & ~truth).sum()) / n_cal,
        })
    return rows


def block_bootstrap_ci(
    cal: np.ndarray, truth: np.ndarray, block: int = 10, n_boot: int = 2000, seed: int = 0, level: float = 0.95
) -> tuple[float | None, float | None, int]:
    """Block-bootstrap interval for coverage.

    The tile is cut into block x block cell blocks (10 cells = 200 m, the planner's own block size), blocks are
    resampled with replacement, and coverage is recomputed. Cells inside a block stay together, so spatial
    correlation within a block is kept. Resamples with no truth cell are dropped (count returned).
    Returns (low, high, resamples_used), or (None, None, 0) when the truth is empty.
    """
    if cal.shape != truth.shape:
        raise ValueError("cal and truth must have the same shape")
    h, w = (cal.shape[0] // block) * block, (cal.shape[1] // block) * block
    hit = (cal & truth)[:h, :w]
    tru = truth[:h, :w]
    nb_r, nb_c = h // block, w // block
    num = hit.reshape(nb_r, block, nb_c, block).sum(axis=(1, 3)).ravel().astype(np.int64)
    den = tru.reshape(nb_r, block, nb_c, block).sum(axis=(1, 3)).ravel().astype(np.int64)
    if den.sum() == 0:
        return None, None, 0
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, num.size, size=(n_boot, num.size))
    d = den[idx].sum(axis=1)
    ok = d > 0
    cov = num[idx].sum(axis=1)[ok] / d[ok]
    alpha = (1.0 - level) / 2.0
    lo, hi = np.percentile(cov, [100 * alpha, 100 * (1 - alpha)])
    return float(lo), float(hi), int(ok.sum())


def wider_interval(a: tuple[float | None, float | None], b: tuple[float | None, float | None]):
    """The wider of two intervals (registered rule when a single interval is quoted)."""
    if a[0] is None or a[1] is None:
        return b
    if b[0] is None or b[1] is None:
        return a
    return (min(a[0], b[0]), max(a[1], b[1]))
