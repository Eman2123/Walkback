"""Degrade a 1 m DTM to coarse resolutions by block averaging (200 m and 20 m)."""
import numpy as np

def block_mean(z: np.ndarray, factor: int) -> np.ndarray:
    """Average non-overlapping factor x factor blocks. Trims edges that do not fill a block."""
    h, w = z.shape
    h2, w2 = h // factor * factor, w // factor * factor
    z = z[:h2, :w2]
    return z.reshape(h2 // factor, factor, w2 // factor, factor).mean(axis=(1, 3))
