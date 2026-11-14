"""Deterministic walkback region: travel time from the habitat over a coarse grid.

Speed model and cutoff are assumptions and must be read from the scenario contract.
"""
import numpy as np
import skfmm

def speed_from_slope(slope_deg_arr: np.ndarray, v_flat: float, cutoff_deg: float) -> np.ndarray:
    """Assumed linear speed reduction with slope; zero above cutoff (impassable)."""
    v = v_flat * np.clip(1.0 - slope_deg_arr / cutoff_deg, 0.0, 1.0)
    return v

def travel_time(speed: np.ndarray, habitat_rc: tuple, cell_m: float) -> np.ndarray:
    phi = np.ones_like(speed)
    phi[habitat_rc] = -1.0
    masked = np.ma.MaskedArray(phi, mask=(speed <= 0))
    return skfmm.travel_time(masked, speed, dx=cell_m)

def walkback_mask(time_s: np.ndarray, budget_s: float) -> np.ndarray:
    return np.isfinite(time_s) & (time_s <= budget_s)
