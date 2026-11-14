from pathlib import Path

import numpy as np

from walkback.slope import slope_deg
from walkback.pipeline.scale_effect import measure_hurst


# Load synthetic terrain
data = np.load("data/processed/synthetic_jezero.npz")
z = data["elevation_1m"].astype(np.float64)


def downsample_mean(array, factor):
    h, w = array.shape
    return array.reshape(
        h // factor, factor,
        w // factor, factor
    ).mean(axis=(1, 3))


# Generate elevation grids at different resolutions
terrain_1m = z
terrain_20m = downsample_mean(z, 20)
terrain_200m = downsample_mean(z, 200)

# Calculate slope at each resolution
slope_1m = slope_deg(terrain_1m, 1)
slope_20m = slope_deg(terrain_20m, 20)
slope_200m = slope_deg(terrain_200m, 200)

# Calculate RMS slope
rms = {
    1: float(np.sqrt(np.mean(slope_1m ** 2))),
    20: float(np.sqrt(np.mean(slope_20m ** 2))),
    200: float(np.sqrt(np.mean(slope_200m ** 2))),
}

# Calculate Hurst-style scale exponent
exponent = measure_hurst(rms)

print("\nSYNTHETIC TERRAIN SCALE ANALYSIS")
print("--------------------------------")

for scale, value in rms.items():
    print(f"{scale}m RMS slope: {value:.6f} degrees")

print(f"\nHurst-style exponent: {exponent:.4f}")
print("\nNOTE: These are synthetic results, not real Mars measurements.")