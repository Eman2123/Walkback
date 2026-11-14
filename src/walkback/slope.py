"""Slope in degrees from a DEM with known cell size in metres."""
import numpy as np

def slope_deg(z: np.ndarray, cell_m: float) -> np.ndarray:
    dzdy, dzdx = np.gradient(z, cell_m)
    return np.degrees(np.arctan(np.hypot(dzdx, dzdy)))
