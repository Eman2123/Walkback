"""Reliability diagram and coverage checks against the held-out high-resolution truth."""
import numpy as np

def brier(p: np.ndarray, y: np.ndarray) -> float:
    return float(np.mean((p - y) ** 2))

def reliability_bins(p: np.ndarray, y: np.ndarray, n_bins: int = 10):
    edges = np.linspace(0, 1, n_bins + 1)
    idx = np.clip(np.digitize(p, edges) - 1, 0, n_bins - 1)
    out = []
    for b in range(n_bins):
        m = idx == b
        if m.any():
            out.append({"bin": b, "n": int(m.sum()), "pred": float(p[m].mean()), "obs": float(y[m].mean())})
    return out

def coverage(region_pred: np.ndarray, region_truth: np.ndarray) -> float:
    """Share of truth-feasible cells that the predicted region contains."""
    denom = region_truth.sum()
    return float((region_pred & region_truth).sum() / denom) if denom else float("nan")
