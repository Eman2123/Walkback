from pathlib import Path

import numpy as np

from walkback.pipeline.build import build_arrays, FINE_CELL_M

# Reproducible synthetic terrain: 2000m x 2000m at 1m resolution
rng = np.random.default_rng(42)

side = 2000
y, x = np.mgrid[0:side, 0:side]

# Artificial hills, ridges and gentle elevation changes
z = (
    0.012 * x
    + 0.008 * y
    + 18 * np.exp(-((x - 600)**2 + (y - 700)**2) / 180000)
    + 12 * np.exp(-((x - 1450)**2 + (y - 1300)**2) / 240000)
    + 5 * np.sin(x / 120)
    + 4 * np.cos(y / 160)
)

z += rng.normal(0, 0.15, (side, side))

# Build 20m and 200m terrain representations
coarse, fine = build_arrays(z)

out_dir = Path("data/processed")
out_dir.mkdir(parents=True, exist_ok=True)

output = out_dir / "synthetic_jezero.npz"

np.savez_compressed(
    output,
    elevation_1m=z.astype(np.float32),
    coarse=coarse,
    fine=fine,
    cell_m=np.float64(FINE_CELL_M),
    label=np.str_("Synthetic terrain - NOT real Mars measurements"),
)

print("Synthetic terrain created:", output)
print("1m elevation:", z.shape)
print("20m grid:", fine.shape)
print("200m grid:", coarse.shape)