# Solver and directional speed (exploratory, registered before it was run)

This is not the validation result. The pre-registered headline in validation_report.md is unchanged.
Registered in PREREGISTRATION.md, section "Solver and directional speed" and its amendment.

Fixed: habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20.0 deg (assumed), 16 realizations, seed 1234.

Speed models: linear = registered, symmetric. minetti = edge speed times Cs(g)/C(g) from the Minetti et al. 2002 walking cost (assumed: Earth treadmill, speed inverse to cost, no Mars gravity or suit); it speeds the crew up on downhill grades (up to about 4 times), which is not a defensible planning speed. minetti_cap = the same with the factor limited to 1, so uphill penalties only; read this one for a return-time question. direction out = time from the habitat (registered); back = time from each cell to the habitat, which is the walkback.

Grades use the planner elevation (200 m blocks drawn on the 20 m grid) for the planner, so the staircase artifact of the registered model also affects the direction factor, for grid200 as well. The fine elevation is used for the truth.

Solver check on flat ground at uniform speed (101 x 101 cells, 20 m, 0.5 m/s, 900 s):

| solver | worst path error | reach area km2 | against the true circle |
|---|---|---|---|
| dijkstra8 | +8.2 % | 0.575 | -9.6 % (circle 0.636) |
| dijkstra16 | +2.7 % | 0.623 | -2.1 % (circle 0.636) |

All rows are reported. No row is chosen as the result. A difference between out and back is reported even when it is zero.

## Tile: Mars 2020 TRN HiRISE DTM (USGS, DOI 10.5066/P9REJ9JN), 2 km window, degraded to 200 m planner

Tile id jezero-20m, cell 20 m.

### Planner model: staircase (registered)

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | 0.450 | 0.422 | 97.7 % | 96.6 % to 98.5 % | 95.2 % to 99.4 % | 8.4 % | -7.429 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.7 | 0.444 | 0.422 | 97.2 % | 96.0 % to 98.0 % | 93.9 % to 99.2 % | 7.8 % | -7.429 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.9 | 0.433 | 0.422 | 95.8 % | 94.4 % to 96.9 % | 91.4 % to 98.7 % | 6.7 % | -7.429 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.5 | 0.462 | 0.422 | 98.6 % | 97.7 % to 99.1 % | 96.7 % to 99.7 % | 10.0 % | -5.945 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.7 | 0.441 | 0.422 | 96.6 % | 95.3 % to 97.5 % | 93.1 % to 98.9 % | 7.7 % | -5.945 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.9 | 0.396 | 0.422 | 88.5 % | 86.5 % to 90.3 % | 81.7 % to 93.3 % | 5.9 % | -5.945 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.5 | 0.469 | 0.422 | 98.6 % | 97.7 % to 99.1 % | 97.0 % to 99.6 % | 11.3 % | -6.853 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.7 | 0.415 | 0.422 | 90.9 % | 89.0 % to 92.5 % | 86.5 % to 94.1 % | 7.6 % | -6.853 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.9 | 0.000 | 0.422 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | minetti | out | 0.1 | 0.5 | 0.462 | 0.533 | 84.2 % | 82.2 % to 86.1 % | 73.0 % to 92.9 % | 2.8 % | -7.429 | +0.012 | +0.111 | -13.5 |
| dijkstra8 | minetti | out | 0.1 | 0.7 | 0.454 | 0.533 | 83.0 % | 80.9 % to 84.9 % | 71.0 % to 92.1 % | 2.6 % | -7.429 | +0.010 | +0.111 | -14.2 |
| dijkstra8 | minetti | out | 0.1 | 0.9 | 0.443 | 0.533 | 81.0 % | 78.7 % to 83.0 % | 68.7 % to 90.4 % | 2.5 % | -7.429 | +0.010 | +0.111 | -14.9 |
| dijkstra8 | minetti | out | 0.3 | 0.5 | 0.469 | 0.533 | 85.3 % | 83.3 % to 87.1 % | 74.1 % to 93.6 % | 3.1 % | -5.945 | +0.007 | +0.111 | -13.3 |
| dijkstra8 | minetti | out | 0.3 | 0.7 | 0.446 | 0.533 | 81.5 % | 79.4 % to 83.5 % | 69.7 % to 90.5 % | 2.6 % | -5.945 | +0.005 | +0.111 | -15.0 |
| dijkstra8 | minetti | out | 0.3 | 0.9 | 0.399 | 0.533 | 73.1 % | 70.6 % to 75.4 % | 59.6 % to 83.1 % | 2.3 % | -5.945 | +0.003 | +0.111 | -15.4 |
| dijkstra8 | minetti | out | 0.5 | 0.5 | 0.475 | 0.533 | 86.0 % | 84.0 % to 87.7 % | 75.5 % to 94.0 % | 3.5 % | -6.853 | +0.006 | +0.111 | -12.6 |
| dijkstra8 | minetti | out | 0.5 | 0.7 | 0.419 | 0.533 | 76.7 % | 74.4 % to 78.9 % | 65.1 % to 85.3 % | 2.4 % | -6.853 | +0.004 | +0.111 | -14.2 |
| dijkstra8 | minetti | out | 0.5 | 0.9 | 0.000 | 0.533 | 0.0 % | 0.0 % to 0.3 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | +0.111 | +0.0 |
| dijkstra8 | minetti | back | 0.1 | 0.5 | 0.461 | 0.376 | 99.2 % | 98.5 % to 99.6 % | 98.1 % to 99.9 % | 19.1 % | -7.429 | +0.011 | -0.046 | +1.5 |
| dijkstra8 | minetti | back | 0.1 | 0.7 | 0.455 | 0.376 | 98.9 % | 98.1 % to 99.4 % | 97.5 % to 99.8 % | 18.3 % | -7.429 | +0.011 | -0.046 | +1.8 |
| dijkstra8 | minetti | back | 0.1 | 0.9 | 0.445 | 0.376 | 98.6 % | 97.6 % to 99.2 % | 96.8 % to 99.7 % | 16.8 % | -7.429 | +0.012 | -0.046 | +2.8 |
| dijkstra8 | minetti | back | 0.3 | 0.5 | 0.474 | 0.376 | 99.4 % | 98.6 % to 99.7 % | 98.4 % to 99.9 % | 21.3 % | -5.945 | +0.012 | -0.046 | +0.8 |
| dijkstra8 | minetti | back | 0.3 | 0.7 | 0.456 | 0.376 | 98.3 % | 97.3 % to 98.9 % | 96.6 % to 99.4 % | 19.1 % | -5.945 | +0.015 | -0.046 | +1.7 |
| dijkstra8 | minetti | back | 0.3 | 0.9 | 0.422 | 0.376 | 93.8 % | 92.1 % to 95.2 % | 90.0 % to 96.6 % | 16.5 % | -5.945 | +0.026 | -0.046 | +5.3 |
| dijkstra8 | minetti | back | 0.5 | 0.5 | 0.482 | 0.376 | 99.2 % | 98.5 % to 99.6 % | 98.4 % to 99.8 % | 22.7 % | -6.853 | +0.013 | -0.046 | +0.7 |
| dijkstra8 | minetti | back | 0.5 | 0.7 | 0.434 | 0.376 | 93.5 % | 91.7 % to 94.9 % | 89.9 % to 96.4 % | 19.0 % | -6.853 | +0.019 | -0.046 | +2.6 |
| dijkstra8 | minetti | back | 0.5 | 0.9 | 0.000 | 0.376 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | -0.046 | +0.0 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | 0.407 | 0.369 | 97.5 % | 96.3 % to 98.3 % | 94.3 % to 99.5 % | 11.6 % | -7.429 | -0.043 | -0.053 | -0.2 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | 0.398 | 0.369 | 96.6 % | 95.3 % to 97.6 % | 92.5 % to 99.2 % | 10.5 % | -7.429 | -0.046 | -0.053 | -0.5 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | 0.387 | 0.369 | 94.9 % | 93.3 % to 96.1 % | 89.4 % to 98.4 % | 9.6 % | -7.429 | -0.046 | -0.053 | -0.9 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | 0.418 | 0.369 | 98.3 % | 97.2 % to 98.9 % | 95.5 % to 99.9 % | 13.2 % | -5.945 | -0.044 | -0.053 | -0.3 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | 0.392 | 0.369 | 95.2 % | 93.7 % to 96.4 % | 89.2 % to 98.7 % | 10.4 % | -5.945 | -0.049 | -0.053 | -1.3 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | 0.342 | 0.369 | 84.5 % | 82.0 % to 86.7 % | 72.6 % to 92.2 % | 8.9 % | -5.945 | -0.054 | -0.053 | -4.0 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | 0.423 | 0.369 | 98.2 % | 97.1 % to 98.8 % | 95.4 % to 99.7 % | 14.5 % | -6.853 | -0.046 | -0.053 | -0.4 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | 0.369 | 0.369 | 89.6 % | 87.4 % to 91.4 % | 84.4 % to 93.5 % | 10.5 % | -6.853 | -0.046 | -0.053 | -1.3 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | 0.000 | 0.369 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | -0.053 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | 0.408 | 0.317 | 98.4 % | 97.2 % to 99.0 % | 95.5 % to 100.0 % | 23.5 % | -7.429 | -0.042 | -0.105 | +0.6 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | 0.403 | 0.317 | 98.1 % | 96.9 % to 98.9 % | 95.1 % to 100.0 % | 22.7 % | -7.429 | -0.041 | -0.105 | +1.0 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | 0.390 | 0.317 | 97.0 % | 95.5 % to 98.0 % | 92.1 % to 100.0 % | 21.1 % | -7.429 | -0.043 | -0.105 | +1.1 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | 0.421 | 0.317 | 98.5 % | 97.4 % to 99.1 % | 95.9 % to 100.0 % | 25.8 % | -5.945 | -0.041 | -0.105 | -0.1 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | 0.400 | 0.317 | 96.7 % | 95.2 % to 97.8 % | 92.3 % to 99.6 % | 23.3 % | -5.945 | -0.041 | -0.105 | +0.1 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | 0.355 | 0.317 | 89.4 % | 87.1 % to 91.4 % | 80.4 % to 95.0 % | 20.1 % | -5.945 | -0.041 | -0.105 | +0.9 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | 0.430 | 0.317 | 98.5 % | 97.4 % to 99.1 % | 96.2 % to 99.7 % | 27.4 % | -6.853 | -0.039 | -0.105 | -0.1 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | 0.376 | 0.317 | 90.9 % | 88.7 % to 92.7 % | 84.5 % to 95.0 % | 23.4 % | -6.853 | -0.039 | -0.105 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | 0.000 | 0.317 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | -0.105 | +0.0 |
| dijkstra16 | linear | out | 0.1 | 0.5 | 0.515 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 12.0 % | -7.429 | +0.065 | +0.031 | +2.3 |
| dijkstra16 | linear | out | 0.1 | 0.7 | 0.512 | 0.453 | 99.9 % | 99.5 % to 100.0 % | 99.7 % to 100.0 % | 11.5 % | -7.429 | +0.068 | +0.031 | +2.8 |
| dijkstra16 | linear | out | 0.1 | 0.9 | 0.504 | 0.453 | 99.7 % | 99.1 % to 99.9 % | 99.0 % to 100.0 % | 10.5 % | -7.429 | +0.071 | +0.031 | +3.8 |
| dijkstra16 | linear | out | 0.3 | 0.5 | 0.524 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 13.5 % | -5.945 | +0.062 | +0.031 | +1.4 |
| dijkstra16 | linear | out | 0.3 | 0.7 | 0.504 | 0.453 | 99.2 % | 98.5 % to 99.6 % | 98.3 % to 99.9 % | 10.9 % | -5.945 | +0.063 | +0.031 | +2.6 |
| dijkstra16 | linear | out | 0.3 | 0.9 | 0.469 | 0.453 | 94.9 % | 93.4 % to 96.0 % | 93.0 % to 96.7 % | 8.3 % | -5.945 | +0.073 | +0.031 | +6.4 |
| dijkstra16 | linear | out | 0.5 | 0.5 | 0.526 | 0.453 | 99.8 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 13.9 % | -6.853 | +0.057 | +0.031 | +1.2 |
| dijkstra16 | linear | out | 0.5 | 0.7 | 0.459 | 0.453 | 91.7 % | 90.0 % to 93.2 % | 88.3 % to 94.5 % | 9.4 % | -6.853 | +0.044 | +0.031 | +0.8 |
| dijkstra16 | linear | out | 0.5 | 0.9 | 0.000 | 0.453 | 0.0 % | 0.0 % to 0.3 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | +0.031 | +0.0 |
| dijkstra16 | minetti | out | 0.1 | 0.5 | 0.545 | 0.577 | 90.4 % | 88.7 % to 91.8 % | 83.6 % to 95.5 % | 4.3 % | -7.429 | +0.095 | +0.155 | -7.4 |
| dijkstra16 | minetti | out | 0.1 | 0.7 | 0.539 | 0.577 | 89.5 % | 87.8 % to 91.0 % | 82.3 % to 95.1 % | 4.2 % | -7.429 | +0.095 | +0.155 | -7.6 |
| dijkstra16 | minetti | out | 0.1 | 0.9 | 0.528 | 0.577 | 88.2 % | 86.5 % to 89.8 % | 80.6 % to 94.1 % | 3.6 % | -7.429 | +0.095 | +0.155 | -7.6 |
| dijkstra16 | minetti | out | 0.3 | 0.5 | 0.555 | 0.577 | 91.5 % | 89.9 % to 92.8 % | 85.2 % to 96.1 % | 4.9 % | -5.945 | +0.093 | +0.155 | -7.1 |
| dijkstra16 | minetti | out | 0.3 | 0.7 | 0.537 | 0.577 | 89.0 % | 87.3 % to 90.6 % | 81.7 % to 94.6 % | 4.2 % | -5.945 | +0.096 | +0.155 | -7.5 |
| dijkstra16 | minetti | out | 0.3 | 0.9 | 0.488 | 0.577 | 82.1 % | 80.1 % to 84.0 % | 74.1 % to 88.5 % | 2.9 % | -5.945 | +0.092 | +0.155 | -6.4 |
| dijkstra16 | minetti | out | 0.5 | 0.5 | 0.559 | 0.577 | 91.8 % | 90.3 % to 93.1 % | 85.9 % to 96.3 % | 5.2 % | -6.853 | +0.090 | +0.155 | -6.8 |
| dijkstra16 | minetti | out | 0.5 | 0.7 | 0.495 | 0.577 | 82.3 % | 80.3 % to 84.2 % | 74.9 % to 87.9 % | 4.0 % | -6.853 | +0.080 | +0.155 | -8.6 |
| dijkstra16 | minetti | out | 0.5 | 0.9 | 0.000 | 0.577 | 0.0 % | 0.0 % to 0.3 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | +0.155 | +0.0 |
| dijkstra16 | minetti | back | 0.1 | 0.5 | 0.525 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 23.4 % | -7.429 | +0.075 | -0.019 | +2.2 |
| dijkstra16 | minetti | back | 0.1 | 0.7 | 0.519 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 22.5 % | -7.429 | +0.075 | -0.019 | +2.7 |
| dijkstra16 | minetti | back | 0.1 | 0.9 | 0.515 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 21.8 % | -7.429 | +0.082 | -0.019 | +4.1 |
| dijkstra16 | minetti | back | 0.3 | 0.5 | 0.535 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 24.8 % | -5.945 | +0.073 | -0.019 | +1.3 |
| dijkstra16 | minetti | back | 0.3 | 0.7 | 0.523 | 0.403 | 99.6 % | 99.0 % to 99.8 % | 99.1 % to 100.0 % | 23.3 % | -5.945 | +0.082 | -0.019 | +3.0 |
| dijkstra16 | minetti | back | 0.3 | 0.9 | 0.489 | 0.403 | 96.4 % | 95.1 % to 97.4 % | 93.7 % to 98.7 % | 20.6 % | -5.945 | +0.093 | -0.019 | +7.9 |
| dijkstra16 | minetti | back | 0.5 | 0.5 | 0.540 | 0.403 | 99.7 % | 99.1 % to 99.9 % | 99.3 % to 100.0 % | 25.6 % | -6.853 | +0.071 | -0.019 | +1.1 |
| dijkstra16 | minetti | back | 0.5 | 0.7 | 0.477 | 0.403 | 94.4 % | 92.8 % to 95.7 % | 90.9 % to 97.2 % | 20.3 % | -6.853 | +0.062 | -0.019 | +3.5 |
| dijkstra16 | minetti | back | 0.5 | 0.9 | 0.000 | 0.403 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | -0.019 | +0.0 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | 0.455 | 0.395 | 98.7 % | 97.8 % to 99.2 % | 96.7 % to 99.9 % | 14.4 % | -7.429 | +0.005 | -0.027 | +1.0 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | 0.450 | 0.395 | 98.1 % | 97.0 % to 98.8 % | 95.1 % to 99.9 % | 14.0 % | -7.429 | +0.006 | -0.027 | +0.9 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | 0.441 | 0.395 | 97.3 % | 96.0 % to 98.1 % | 93.6 % to 99.5 % | 12.9 % | -7.429 | +0.008 | -0.027 | +1.4 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | 0.464 | 0.395 | 99.1 % | 98.3 % to 99.5 % | 97.5 % to 100.0 % | 15.8 % | -5.945 | +0.002 | -0.027 | +0.5 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | 0.447 | 0.395 | 97.7 % | 96.5 % to 98.4 % | 94.6 % to 99.5 % | 13.8 % | -5.945 | +0.006 | -0.027 | +1.1 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | 0.402 | 0.395 | 90.8 % | 88.8 % to 92.4 % | 85.1 % to 94.9 % | 10.8 % | -5.945 | +0.006 | -0.027 | +2.3 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | 0.466 | 0.395 | 98.9 % | 98.0 % to 99.4 % | 97.2 % to 99.9 % | 16.2 % | -6.853 | -0.003 | -0.027 | +0.3 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | 0.406 | 0.395 | 90.1 % | 88.0 % to 91.8 % | 84.9 % to 94.0 % | 12.4 % | -6.853 | -0.009 | -0.027 | -0.8 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | 0.000 | 0.395 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | -0.027 | +0.0 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | 0.457 | 0.338 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 26.1 % | -7.429 | +0.007 | -0.084 | +2.2 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | 0.451 | 0.338 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 25.0 % | -7.429 | +0.007 | -0.084 | +2.7 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | 0.446 | 0.338 | 99.7 % | 99.0 % to 99.9 % | 99.1 % to 100.0 % | 24.5 % | -7.429 | +0.013 | -0.084 | +3.8 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | 0.470 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.0 % | -5.945 | +0.008 | -0.084 | +1.4 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | 0.448 | 0.338 | 99.1 % | 98.1 % to 99.5 % | 98.1 % to 99.9 % | 25.2 % | -5.945 | +0.007 | -0.084 | +2.5 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | 0.413 | 0.338 | 94.3 % | 92.6 % to 95.7 % | 90.8 % to 97.0 % | 22.8 % | -5.945 | +0.017 | -0.084 | +5.8 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | 0.476 | 0.338 | 99.8 % | 99.1 % to 99.9 % | 99.4 % to 100.0 % | 29.0 % | -6.853 | +0.007 | -0.084 | +1.2 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | 0.410 | 0.338 | 91.6 % | 89.5 % to 93.3 % | 86.7 % to 95.3 % | 24.3 % | -6.853 | -0.005 | -0.084 | +0.7 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | 0.000 | 0.338 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -6.853 | +0.000 | -0.084 | +0.0 |

### Planner model: grid200

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | 0.467 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 9.8 % | -0.002 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.7 | 0.466 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 9.6 % | -0.002 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.9 | 0.465 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 9.4 % | -0.002 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.5 | 0.472 | 0.422 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 10.7 % | -0.002 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.7 | 0.469 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 10.2 % | -0.002 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.9 | 0.466 | 0.422 | 99.8 % | 99.3 % to 99.9 % | 99.4 % to 100.0 % | 9.7 % | -0.002 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.5 | 0.474 | 0.422 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 11.1 % | -0.007 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.7 | 0.470 | 0.422 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 10.3 % | -0.007 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.9 | 0.461 | 0.422 | 99.7 % | 99.2 % to 99.9 % | 99.1 % to 100.0 % | 8.8 % | -0.007 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | minetti | out | 0.1 | 0.5 | 0.486 | 0.533 | 86.7 % | 84.7 % to 88.4 % | 75.9 % to 94.8 % | 5.0 % | -0.002 | +0.019 | +0.111 | -13.3 |
| dijkstra8 | minetti | out | 0.1 | 0.7 | 0.484 | 0.533 | 86.2 % | 84.2 % to 87.9 % | 75.3 % to 94.5 % | 5.0 % | -0.002 | +0.018 | +0.111 | -13.7 |
| dijkstra8 | minetti | out | 0.1 | 0.9 | 0.480 | 0.533 | 85.8 % | 83.8 % to 87.6 % | 74.7 % to 94.3 % | 4.8 % | -0.002 | +0.015 | +0.111 | -14.1 |
| dijkstra8 | minetti | out | 0.3 | 0.5 | 0.488 | 0.533 | 86.8 % | 84.9 % to 88.5 % | 76.0 % to 95.0 % | 5.2 % | -0.002 | +0.016 | +0.111 | -13.2 |
| dijkstra8 | minetti | out | 0.3 | 0.7 | 0.484 | 0.533 | 86.3 % | 84.3 % to 88.0 % | 75.2 % to 94.6 % | 4.9 % | -0.002 | +0.015 | +0.111 | -13.6 |
| dijkstra8 | minetti | out | 0.3 | 0.9 | 0.480 | 0.533 | 85.9 % | 83.9 % to 87.7 % | 74.6 % to 94.5 % | 4.5 % | -0.002 | +0.014 | +0.111 | -13.9 |
| dijkstra8 | minetti | out | 0.5 | 0.5 | 0.491 | 0.533 | 87.0 % | 85.1 % to 88.7 % | 76.1 % to 95.2 % | 5.5 % | -0.007 | +0.017 | +0.111 | -13.0 |
| dijkstra8 | minetti | out | 0.5 | 0.7 | 0.483 | 0.533 | 86.3 % | 84.3 % to 88.0 % | 75.1 % to 94.7 % | 4.7 % | -0.007 | +0.013 | +0.111 | -13.7 |
| dijkstra8 | minetti | out | 0.5 | 0.9 | 0.476 | 0.533 | 85.3 % | 83.3 % to 87.1 % | 73.6 % to 94.2 % | 4.4 % | -0.007 | +0.015 | +0.111 | -14.4 |
| dijkstra8 | minetti | back | 0.1 | 0.5 | 0.481 | 0.376 | 99.5 % | 98.8 % to 99.8 % | 98.6 % to 100.0 % | 22.4 % | -0.002 | +0.014 | -0.046 | -0.4 |
| dijkstra8 | minetti | back | 0.1 | 0.7 | 0.479 | 0.376 | 99.5 % | 98.8 % to 99.8 % | 98.6 % to 100.0 % | 22.0 % | -0.002 | +0.013 | -0.046 | -0.4 |
| dijkstra8 | minetti | back | 0.1 | 0.9 | 0.476 | 0.376 | 99.5 % | 98.8 % to 99.8 % | 98.6 % to 100.0 % | 21.6 % | -0.002 | +0.011 | -0.046 | -0.4 |
| dijkstra8 | minetti | back | 0.3 | 0.5 | 0.483 | 0.376 | 99.6 % | 98.9 % to 99.8 % | 99.0 % to 100.0 % | 22.5 % | -0.002 | +0.011 | -0.046 | -0.4 |
| dijkstra8 | minetti | back | 0.3 | 0.7 | 0.479 | 0.376 | 99.5 % | 98.8 % to 99.8 % | 98.6 % to 100.0 % | 22.0 % | -0.002 | +0.010 | -0.046 | -0.4 |
| dijkstra8 | minetti | back | 0.3 | 0.9 | 0.476 | 0.376 | 99.2 % | 98.3 % to 99.6 % | 97.9 % to 99.8 % | 21.7 % | -0.002 | +0.010 | -0.046 | -0.7 |
| dijkstra8 | minetti | back | 0.5 | 0.5 | 0.483 | 0.376 | 99.5 % | 98.8 % to 99.8 % | 98.6 % to 100.0 % | 22.6 % | -0.007 | +0.009 | -0.046 | -0.5 |
| dijkstra8 | minetti | back | 0.5 | 0.7 | 0.477 | 0.376 | 99.4 % | 98.6 % to 99.7 % | 98.4 % to 99.9 % | 21.8 % | -0.007 | +0.007 | -0.046 | -0.6 |
| dijkstra8 | minetti | back | 0.5 | 0.9 | 0.472 | 0.376 | 99.0 % | 98.2 % to 99.5 % | 97.7 % to 99.8 % | 21.2 % | -0.007 | +0.011 | -0.046 | -0.7 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | 0.436 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.4 % | -0.002 | -0.031 | -0.053 | +0.1 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | 0.435 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.3 % | -0.002 | -0.031 | -0.053 | +0.1 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | 0.435 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.2 % | -0.002 | -0.030 | -0.053 | +0.1 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | 0.441 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 16.3 % | -0.002 | -0.031 | -0.053 | +0.0 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | 0.438 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.8 % | -0.002 | -0.031 | -0.053 | +0.1 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | 0.434 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 14.9 % | -0.002 | -0.032 | -0.053 | +0.2 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | 0.443 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 16.8 % | -0.007 | -0.031 | -0.053 | +0.0 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | 0.435 | 0.369 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.2 % | -0.007 | -0.035 | -0.053 | +0.0 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | 0.428 | 0.369 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 13.9 % | -0.007 | -0.033 | -0.053 | +0.2 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | 0.442 | 0.317 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 28.4 % | -0.002 | -0.025 | -0.105 | -0.0 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | 0.439 | 0.317 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 27.9 % | -0.002 | -0.027 | -0.105 | -0.0 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | 0.438 | 0.317 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 27.7 % | -0.002 | -0.027 | -0.105 | -0.0 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | 0.445 | 0.317 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.7 % | -0.002 | -0.027 | -0.105 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | 0.440 | 0.317 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 27.9 % | -0.002 | -0.029 | -0.105 | -0.0 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | 0.438 | 0.317 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 27.6 % | -0.002 | -0.028 | -0.105 | +0.1 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | 0.446 | 0.317 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.9 % | -0.007 | -0.028 | -0.105 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | 0.440 | 0.317 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 27.9 % | -0.007 | -0.030 | -0.105 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | 0.433 | 0.317 | 99.9 % | 99.3 % to 100.0 % | 99.5 % to 100.0 % | 26.9 % | -0.007 | -0.028 | -0.105 | +0.2 |
| dijkstra16 | linear | out | 0.1 | 0.5 | 0.502 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 9.8 % | -0.002 | +0.035 | +0.031 | +0.1 |
| dijkstra16 | linear | out | 0.1 | 0.7 | 0.502 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 9.7 % | -0.002 | +0.036 | +0.031 | +0.1 |
| dijkstra16 | linear | out | 0.1 | 0.9 | 0.501 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 9.6 % | -0.002 | +0.036 | +0.031 | +0.1 |
| dijkstra16 | linear | out | 0.3 | 0.5 | 0.510 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 11.1 % | -0.002 | +0.038 | +0.031 | +0.0 |
| dijkstra16 | linear | out | 0.3 | 0.7 | 0.506 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 10.4 % | -0.002 | +0.037 | +0.031 | +0.1 |
| dijkstra16 | linear | out | 0.3 | 0.9 | 0.501 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 9.6 % | -0.002 | +0.035 | +0.031 | +0.2 |
| dijkstra16 | linear | out | 0.5 | 0.5 | 0.514 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 11.8 % | -0.007 | +0.040 | +0.031 | +0.0 |
| dijkstra16 | linear | out | 0.5 | 0.7 | 0.508 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 10.8 % | -0.007 | +0.038 | +0.031 | +0.0 |
| dijkstra16 | linear | out | 0.5 | 0.9 | 0.501 | 0.453 | 100.0 % | 99.7 % to 100.0 % | 100.0 % to 100.0 % | 9.5 % | -0.007 | +0.040 | +0.031 | +0.3 |
| dijkstra16 | minetti | out | 0.1 | 0.5 | 0.558 | 0.577 | 90.2 % | 88.6 % to 91.7 % | 82.1 % to 96.4 % | 6.7 % | -0.002 | +0.091 | +0.155 | -9.7 |
| dijkstra16 | minetti | out | 0.1 | 0.7 | 0.554 | 0.577 | 89.7 % | 88.0 % to 91.1 % | 80.9 % to 96.3 % | 6.6 % | -0.002 | +0.088 | +0.155 | -10.2 |
| dijkstra16 | minetti | out | 0.1 | 0.9 | 0.551 | 0.577 | 89.5 % | 87.8 % to 91.0 % | 80.7 % to 96.2 % | 6.2 % | -0.002 | +0.086 | +0.155 | -10.4 |
| dijkstra16 | minetti | out | 0.3 | 0.5 | 0.560 | 0.577 | 90.3 % | 88.7 % to 91.7 % | 82.2 % to 96.4 % | 7.0 % | -0.002 | +0.088 | +0.155 | -9.7 |
| dijkstra16 | minetti | out | 0.3 | 0.7 | 0.558 | 0.577 | 90.3 % | 88.7 % to 91.7 % | 82.2 % to 96.4 % | 6.7 % | -0.002 | +0.089 | +0.155 | -9.6 |
| dijkstra16 | minetti | out | 0.3 | 0.9 | 0.551 | 0.577 | 89.8 % | 88.1 % to 91.3 % | 81.4 % to 96.3 % | 5.9 % | -0.002 | +0.085 | +0.155 | -10.0 |
| dijkstra16 | minetti | out | 0.5 | 0.5 | 0.566 | 0.577 | 90.8 % | 89.2 % to 92.2 % | 83.1 % to 96.7 % | 7.4 % | -0.007 | +0.092 | +0.155 | -9.2 |
| dijkstra16 | minetti | out | 0.5 | 0.7 | 0.558 | 0.577 | 90.3 % | 88.7 % to 91.7 % | 82.2 % to 96.4 % | 6.6 % | -0.007 | +0.088 | +0.155 | -9.7 |
| dijkstra16 | minetti | out | 0.5 | 0.9 | 0.550 | 0.577 | 89.7 % | 88.1 % to 91.2 % | 81.4 % to 96.1 % | 5.8 % | -0.007 | +0.089 | +0.155 | -10.0 |
| dijkstra16 | minetti | back | 0.1 | 0.5 | 0.539 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 25.4 % | -0.002 | +0.072 | -0.019 | -0.0 |
| dijkstra16 | minetti | back | 0.1 | 0.7 | 0.537 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 25.1 % | -0.002 | +0.071 | -0.019 | -0.0 |
| dijkstra16 | minetti | back | 0.1 | 0.9 | 0.536 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 24.9 % | -0.002 | +0.071 | -0.019 | -0.0 |
| dijkstra16 | minetti | back | 0.3 | 0.5 | 0.543 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 25.9 % | -0.002 | +0.071 | -0.019 | -0.1 |
| dijkstra16 | minetti | back | 0.3 | 0.7 | 0.539 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 25.3 % | -0.002 | +0.070 | -0.019 | -0.0 |
| dijkstra16 | minetti | back | 0.3 | 0.9 | 0.536 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 24.9 % | -0.002 | +0.070 | -0.019 | +0.1 |
| dijkstra16 | minetti | back | 0.5 | 0.5 | 0.550 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 26.8 % | -0.007 | +0.076 | -0.019 | -0.1 |
| dijkstra16 | minetti | back | 0.5 | 0.7 | 0.542 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 25.8 % | -0.007 | +0.072 | -0.019 | -0.1 |
| dijkstra16 | minetti | back | 0.5 | 0.9 | 0.534 | 0.403 | 99.9 % | 99.4 % to 100.0 % | 99.6 % to 100.0 % | 24.6 % | -0.007 | +0.073 | -0.019 | +0.2 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | 0.468 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.6 % | -0.002 | +0.001 | -0.027 | +0.1 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | 0.467 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.4 % | -0.002 | +0.001 | -0.027 | +0.1 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | 0.466 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.2 % | -0.002 | +0.001 | -0.027 | +0.1 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | 0.472 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 16.4 % | -0.002 | +0.000 | -0.027 | +0.0 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | 0.470 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.9 % | -0.002 | +0.001 | -0.027 | +0.1 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | 0.465 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 15.1 % | -0.002 | -0.001 | -0.027 | +0.2 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | 0.476 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 17.1 % | -0.007 | +0.002 | -0.027 | +0.0 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | 0.471 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 16.2 % | -0.007 | +0.001 | -0.027 | +0.0 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | 0.462 | 0.395 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 14.5 % | -0.007 | +0.001 | -0.027 | +0.3 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | 0.471 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.2 % | -0.002 | +0.004 | -0.084 | +0.1 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | 0.470 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.0 % | -0.002 | +0.004 | -0.084 | +0.1 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | 0.468 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 27.7 % | -0.002 | +0.003 | -0.084 | +0.1 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | 0.475 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.7 % | -0.002 | +0.003 | -0.084 | +0.0 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | 0.473 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.4 % | -0.002 | +0.004 | -0.084 | +0.1 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | 0.469 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 27.9 % | -0.002 | +0.003 | -0.084 | +0.2 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | 0.480 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 29.5 % | -0.007 | +0.006 | -0.084 | +0.0 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | 0.474 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 28.6 % | -0.007 | +0.004 | -0.084 | +0.0 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | 0.467 | 0.338 | 100.0 % | 99.5 % to 100.0 % | 100.0 % to 100.0 % | 27.6 % | -0.007 | +0.006 | -0.084 | +0.3 |

## Tile: HiRISE Jezero DTM, 2 km window 1 (selected for steepness), degraded to 200 m planner

Tile id steep-1, cell 20 m.

### Planner model: staircase (registered)

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | not computed |||||||||| 

- not computed, dijkstra8 linear out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution

### Planner model: grid200

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | 0.070 | 0.054 | 86.0 % | 79.2 % to 90.9 % | 64.3 % to 98.6 % | 33.1 % | +0.459 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.7 | 0.063 | 0.054 | 84.6 % | 77.5 % to 89.7 % | 59.5 % to 98.6 % | 27.2 % | +0.459 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.9 | 0.057 | 0.054 | 80.9 % | 73.5 % to 86.6 % | 57.1 % to 94.3 % | 23.1 % | +0.459 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.5 | 0.079 | 0.054 | 91.2 % | 85.2 % to 94.9 % | 76.2 % to 100.0 % | 37.4 % | +0.406 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.7 | 0.061 | 0.054 | 80.2 % | 72.7 % to 86.0 % | 45.2 % to 98.6 % | 28.8 % | +0.406 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.9 | 0.018 | 0.054 | 27.2 % | 20.4 % to 35.2 % | 2.4 % to 38.6 % | 15.9 % | +0.406 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.5 | 0.077 | 0.054 | 88.2 % | 81.7 % to 92.6 % | 66.7 % to 98.6 % | 37.8 % | +0.336 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.7 | 0.008 | 0.054 | 11.8 % | 7.4 % to 18.3 % | 0.0 % to 17.1 % | 15.8 % | +0.336 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.9 | 0.000 | 0.054 | 0.0 % | 0.0 % to 2.7 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | minetti | out | 0.1 | 0.5 | 0.074 | 0.175 | 34.7 % | 30.4 % to 39.3 % | 1.7 % to 64.0 % | 18.3 % | +0.459 | +0.004 | +0.121 | -51.3 |
| dijkstra8 | minetti | out | 0.1 | 0.7 | 0.065 | 0.175 | 32.0 % | 27.8 % to 36.5 % | 0.3 % to 59.7 % | 14.1 % | +0.459 | +0.002 | +0.121 | -52.6 |
| dijkstra8 | minetti | out | 0.1 | 0.9 | 0.059 | 0.175 | 30.1 % | 26.0 % to 34.6 % | 0.0 % to 56.5 % | 10.8 % | +0.459 | +0.002 | +0.121 | -50.7 |
| dijkstra8 | minetti | out | 0.3 | 0.5 | 0.090 | 0.175 | 40.4 % | 35.9 % to 45.1 % | 5.1 % to 70.8 % | 21.0 % | +0.406 | +0.011 | +0.121 | -50.8 |
| dijkstra8 | minetti | out | 0.3 | 0.7 | 0.068 | 0.175 | 34.7 % | 30.4 % to 39.3 % | 2.3 % to 63.3 % | 11.1 % | +0.406 | +0.007 | +0.121 | -45.5 |
| dijkstra8 | minetti | out | 0.3 | 0.9 | 0.019 | 0.175 | 9.8 % | 7.4 % to 13.0 % | 0.4 % to 18.9 % | 8.5 % | +0.406 | +0.001 | +0.121 | -17.4 |
| dijkstra8 | minetti | out | 0.5 | 0.5 | 0.088 | 0.175 | 40.0 % | 35.5 % to 44.6 % | 6.5 % to 69.2 % | 20.4 % | +0.336 | +0.011 | +0.121 | -48.3 |
| dijkstra8 | minetti | out | 0.5 | 0.7 | 0.008 | 0.175 | 3.9 % | 2.4 % to 6.1 % | 0.0 % to 8.0 % | 15.0 % | +0.336 | +0.000 | +0.121 | -7.9 |
| dijkstra8 | minetti | out | 0.5 | 0.9 | 0.000 | 0.175 | 0.0 % | 0.0 % to 0.9 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | +0.121 | +0.0 |
| dijkstra8 | minetti | back | 0.1 | 0.5 | 0.068 | 0.111 | 34.3 % | 29.0 % to 40.1 % | 0.0 % to 75.4 % | 44.1 % | +0.459 | -0.002 | +0.057 | -51.7 |
| dijkstra8 | minetti | back | 0.1 | 0.7 | 0.062 | 0.111 | 33.2 % | 27.9 % to 39.0 % | 0.0 % to 73.9 % | 40.3 % | +0.459 | -0.001 | +0.057 | -51.4 |
| dijkstra8 | minetti | back | 0.1 | 0.9 | 0.056 | 0.111 | 32.5 % | 27.2 % to 38.2 % | 0.0 % to 73.9 % | 35.2 % | +0.459 | -0.001 | +0.057 | -48.4 |
| dijkstra8 | minetti | back | 0.3 | 0.5 | 0.076 | 0.111 | 36.1 % | 30.7 % to 41.9 % | 0.0 % to 76.1 % | 47.6 % | +0.406 | -0.003 | +0.057 | -55.1 |
| dijkstra8 | minetti | back | 0.3 | 0.7 | 0.059 | 0.111 | 31.1 % | 25.9 % to 36.7 % | 0.0 % to 73.5 % | 41.9 % | +0.406 | -0.002 | +0.057 | -49.1 |
| dijkstra8 | minetti | back | 0.3 | 0.9 | 0.016 | 0.111 | 8.7 % | 5.9 % to 12.6 % | 0.0 % to 26.8 % | 41.5 % | +0.406 | -0.002 | +0.057 | -18.6 |
| dijkstra8 | minetti | back | 0.5 | 0.5 | 0.076 | 0.111 | 34.7 % | 29.3 % to 40.4 % | 0.6 % to 73.9 % | 49.7 % | +0.336 | -0.001 | +0.057 | -53.6 |
| dijkstra8 | minetti | back | 0.5 | 0.7 | 0.006 | 0.111 | 2.9 % | 1.5 % to 5.6 % | 0.0 % to 10.1 % | 50.0 % | +0.336 | -0.002 | +0.057 | -8.9 |
| dijkstra8 | minetti | back | 0.5 | 0.9 | 0.000 | 0.111 | 0.0 % | 0.0 % to 1.4 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | +0.057 | +0.0 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | 0.066 | 0.038 | 99.0 % | 94.3 % to 99.8 % | 95.0 % to 100.0 % | 43.4 % | +0.459 | -0.004 | -0.016 | +12.9 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | 0.061 | 0.038 | 99.0 % | 94.3 % to 99.8 % | 95.0 % to 100.0 % | 38.2 % | +0.459 | -0.002 | -0.016 | +14.4 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | 0.054 | 0.038 | 95.8 % | 89.7 % to 98.4 % | 88.9 % to 100.0 % | 32.6 % | +0.459 | -0.003 | -0.016 | +14.9 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | 0.076 | 0.038 | 100.0 % | 96.1 % to 100.0 % | 100.0 % to 100.0 % | 50.0 % | +0.406 | -0.003 | -0.016 | +8.8 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | 0.060 | 0.038 | 94.7 % | 88.3 % to 97.7 % | 77.8 % to 100.0 % | 39.6 % | +0.406 | -0.001 | -0.016 | +14.6 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | 0.017 | 0.038 | 33.7 % | 25.0 % to 43.7 % | 5.6 % to 42.1 % | 25.6 % | +0.406 | -0.001 | -0.016 | +6.5 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | 0.076 | 0.038 | 96.8 % | 91.1 % to 98.9 % | 88.9 % to 100.0 % | 51.3 % | +0.336 | -0.001 | -0.016 | +8.6 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | 0.008 | 0.038 | 12.6 % | 7.4 % to 20.8 % | 0.0 % to 15.8 % | 36.8 % | +0.336 | +0.000 | -0.016 | +0.9 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | 0.000 | 0.038 | 0.0 % | 0.0 % to 3.9 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | -0.016 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | 0.064 | 0.034 | 83.5 % | 74.2 % to 89.9 % | 65.0 % to 100.0 % | 55.9 % | +0.459 | -0.006 | -0.020 | -2.5 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | 0.059 | 0.034 | 81.2 % | 71.6 % to 88.1 % | 60.0 % to 100.0 % | 53.1 % | +0.459 | -0.004 | -0.020 | -3.4 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | 0.053 | 0.034 | 80.0 % | 70.3 % to 87.1 % | 57.5 % to 100.0 % | 48.9 % | +0.459 | -0.004 | -0.020 | -0.9 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | 0.072 | 0.034 | 88.2 % | 79.7 % to 93.5 % | 75.0 % to 100.0 % | 58.3 % | +0.406 | -0.007 | -0.020 | -2.9 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | 0.057 | 0.034 | 74.1 % | 63.9 % to 82.2 % | 45.0 % to 100.0 % | 55.9 % | +0.406 | -0.004 | -0.020 | -6.0 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | 0.016 | 0.034 | 21.2 % | 13.8 % to 31.0 % | 2.5 % to 40.0 % | 53.8 % | +0.406 | -0.002 | -0.020 | -6.0 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | 0.072 | 0.034 | 83.5 % | 74.2 % to 89.9 % | 67.5 % to 100.0 % | 60.3 % | +0.336 | -0.005 | -0.020 | -4.7 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | 0.006 | 0.034 | 7.1 % | 3.3 % to 14.6 % | 0.0 % to 15.0 % | 62.5 % | +0.336 | -0.002 | -0.020 | -4.7 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | 0.000 | 0.034 | 0.0 % | 0.0 % to 4.3 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | -0.020 | +0.0 |
| dijkstra16 | linear | out | 0.1 | 0.5 | 0.078 | 0.059 | 89.8 % | 83.8 % to 93.7 % | 71.1 % to 100.0 % | 32.6 % | +0.459 | +0.008 | +0.005 | +3.8 |
| dijkstra16 | linear | out | 0.1 | 0.7 | 0.072 | 0.059 | 87.8 % | 81.5 % to 92.1 % | 68.9 % to 100.0 % | 28.3 % | +0.459 | +0.009 | +0.005 | +3.2 |
| dijkstra16 | linear | out | 0.1 | 0.9 | 0.063 | 0.059 | 83.0 % | 76.1 % to 88.2 % | 60.0 % to 97.3 % | 22.8 % | +0.459 | +0.006 | +0.005 | +2.1 |
| dijkstra16 | linear | out | 0.3 | 0.5 | 0.096 | 0.059 | 95.2 % | 90.5 % to 97.7 % | 84.4 % to 100.0 % | 41.9 % | +0.406 | +0.017 | +0.005 | +4.1 |
| dijkstra16 | linear | out | 0.3 | 0.7 | 0.072 | 0.059 | 83.0 % | 76.1 % to 88.2 % | 48.9 % to 100.0 % | 32.6 % | +0.406 | +0.011 | +0.005 | +2.8 |
| dijkstra16 | linear | out | 0.3 | 0.9 | 0.020 | 0.059 | 27.9 % | 21.3 % to 35.6 % | 2.2 % to 42.5 % | 19.6 % | +0.406 | +0.002 | +0.005 | +0.7 |
| dijkstra16 | linear | out | 0.5 | 0.5 | 0.093 | 0.059 | 87.8 % | 81.5 % to 92.1 % | 66.7 % to 98.6 % | 44.4 % | +0.336 | +0.016 | +0.005 | -0.5 |
| dijkstra16 | linear | out | 0.5 | 0.7 | 0.009 | 0.059 | 10.9 % | 6.8 % to 16.9 % | 0.0 % to 16.4 % | 30.4 % | +0.336 | +0.001 | +0.005 | -0.9 |
| dijkstra16 | linear | out | 0.5 | 0.9 | 0.000 | 0.059 | 0.0 % | 0.0 % to 2.5 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | +0.005 | +0.0 |
| dijkstra16 | minetti | out | 0.1 | 0.5 | 0.098 | 0.220 | 37.5 % | 33.6 % to 41.6 % | 8.3 % to 63.9 % | 16.3 % | +0.459 | +0.028 | +0.166 | -48.5 |
| dijkstra16 | minetti | out | 0.1 | 0.7 | 0.088 | 0.220 | 35.1 % | 31.3 % to 39.2 % | 7.1 % to 60.3 % | 12.7 % | +0.459 | +0.025 | +0.166 | -49.4 |
| dijkstra16 | minetti | out | 0.1 | 0.9 | 0.079 | 0.220 | 32.4 % | 28.6 % to 36.4 % | 5.5 % to 56.5 % | 10.1 % | +0.459 | +0.022 | +0.166 | -48.5 |
| dijkstra16 | minetti | out | 0.3 | 0.5 | 0.120 | 0.220 | 44.3 % | 40.2 % to 48.4 % | 12.4 % to 72.7 % | 19.0 % | +0.406 | +0.041 | +0.166 | -46.9 |
| dijkstra16 | minetti | out | 0.3 | 0.7 | 0.094 | 0.220 | 37.5 % | 33.6 % to 41.6 % | 7.0 % to 64.5 % | 12.0 % | +0.406 | +0.033 | +0.166 | -42.6 |
| dijkstra16 | minetti | out | 0.3 | 0.9 | 0.029 | 0.220 | 13.1 % | 10.5 % to 16.2 % | 1.7 % to 22.3 % | 1.4 % | +0.406 | +0.011 | +0.166 | -14.1 |
| dijkstra16 | minetti | out | 0.5 | 0.5 | 0.113 | 0.220 | 42.6 % | 38.6 % to 46.8 % | 11.0 % to 69.7 % | 17.3 % | +0.336 | +0.036 | +0.166 | -45.6 |
| dijkstra16 | minetti | out | 0.5 | 0.7 | 0.014 | 0.220 | 6.2 % | 4.5 % to 8.5 % | 0.7 % to 10.2 % | 2.9 % | +0.336 | +0.006 | +0.166 | -5.6 |
| dijkstra16 | minetti | out | 0.5 | 0.9 | 0.000 | 0.220 | 0.0 % | 0.0 % to 0.7 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | +0.166 | +0.0 |
| dijkstra16 | minetti | back | 0.1 | 0.5 | 0.080 | 0.131 | 35.1 % | 30.1 % to 40.4 % | 2.1 % to 73.0 % | 42.5 % | +0.459 | +0.010 | +0.077 | -51.0 |
| dijkstra16 | minetti | back | 0.1 | 0.7 | 0.072 | 0.131 | 33.8 % | 28.9 % to 39.1 % | 1.6 % to 72.5 % | 38.7 % | +0.459 | +0.009 | +0.077 | -50.7 |
| dijkstra16 | minetti | back | 0.1 | 0.9 | 0.068 | 0.131 | 33.2 % | 28.4 % to 38.5 % | 1.1 % to 72.2 % | 36.3 % | +0.459 | +0.011 | +0.077 | -47.6 |
| dijkstra16 | minetti | back | 0.3 | 0.5 | 0.093 | 0.131 | 36.6 % | 31.6 % to 41.9 % | 2.9 % to 74.1 % | 48.3 % | +0.406 | +0.014 | +0.077 | -54.6 |
| dijkstra16 | minetti | back | 0.3 | 0.7 | 0.069 | 0.131 | 29.3 % | 24.6 % to 34.4 % | 0.5 % to 69.6 % | 44.2 % | +0.406 | +0.008 | +0.077 | -50.9 |
| dijkstra16 | minetti | back | 0.3 | 0.9 | 0.019 | 0.131 | 8.2 % | 5.7 % to 11.7 % | 0.0 % to 24.8 % | 43.8 % | +0.406 | +0.001 | +0.077 | -19.0 |
| dijkstra16 | minetti | back | 0.5 | 0.5 | 0.086 | 0.131 | 32.9 % | 28.1 % to 38.2 % | 2.7 % to 70.3 % | 49.5 % | +0.336 | +0.009 | +0.077 | -55.3 |
| dijkstra16 | minetti | back | 0.5 | 0.7 | 0.008 | 0.131 | 2.4 % | 1.2 % to 4.7 % | 0.0 % to 8.5 % | 61.9 % | +0.336 | +0.000 | +0.077 | -9.3 |
| dijkstra16 | minetti | back | 0.5 | 0.9 | 0.000 | 0.131 | 0.0 % | 0.0 % to 1.2 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | +0.077 | +0.0 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | 0.075 | 0.040 | 100.0 % | 96.3 % to 100.0 % | 100.0 % to 100.0 % | 46.5 % | +0.459 | +0.005 | -0.014 | +14.0 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | 0.068 | 0.040 | 100.0 % | 96.3 % to 100.0 % | 100.0 % to 100.0 % | 41.2 % | +0.459 | +0.005 | -0.014 | +15.4 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | 0.060 | 0.040 | 98.0 % | 93.0 % to 99.4 % | 95.0 % to 100.0 % | 34.7 % | +0.459 | +0.003 | -0.014 | +17.1 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | 0.090 | 0.040 | 100.0 % | 96.3 % to 100.0 % | 100.0 % to 100.0 % | 55.8 % | +0.406 | +0.011 | -0.014 | +8.8 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | 0.071 | 0.040 | 96.0 % | 90.2 % to 98.4 % | 80.0 % to 100.0 % | 46.1 % | +0.406 | +0.010 | -0.014 | +15.8 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | 0.020 | 0.040 | 36.0 % | 27.3 % to 45.8 % | 5.0 % to 45.8 % | 26.5 % | +0.406 | +0.002 | -0.014 | +8.8 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | 0.089 | 0.040 | 95.0 % | 88.8 % to 97.8 % | 85.0 % to 98.3 % | 57.4 % | +0.336 | +0.012 | -0.014 | +6.8 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | 0.009 | 0.040 | 12.0 % | 7.0 % to 19.8 % | 0.0 % to 15.3 % | 47.8 % | +0.336 | +0.001 | -0.014 | +0.2 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | 0.000 | 0.040 | 0.0 % | 0.0 % to 3.7 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | -0.014 | +0.0 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | 0.071 | 0.035 | 86.2 % | 77.4 % to 91.9 % | 70.7 % to 100.0 % | 57.9 % | +0.459 | +0.001 | -0.019 | +0.2 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | 0.066 | 0.035 | 85.1 % | 76.1 % to 91.1 % | 68.3 % to 100.0 % | 54.9 % | +0.459 | +0.003 | -0.019 | +0.5 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | 0.060 | 0.035 | 80.5 % | 70.9 % to 87.4 % | 58.5 % to 100.0 % | 53.0 % | +0.459 | +0.003 | -0.019 | -0.4 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | 0.083 | 0.035 | 92.0 % | 84.3 % to 96.0 % | 82.9 % to 100.0 % | 61.5 % | +0.406 | +0.004 | -0.019 | +0.8 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | 0.065 | 0.035 | 75.9 % | 65.9 % to 83.6 % | 48.8 % to 100.0 % | 59.5 % | +0.406 | +0.004 | -0.019 | -4.3 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | 0.018 | 0.035 | 20.7 % | 13.5 % to 30.4 % | 2.4 % to 37.5 % | 60.9 % | +0.406 | +0.000 | -0.019 | -6.5 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | 0.079 | 0.035 | 83.9 % | 74.8 % to 90.2 % | 68.3 % to 100.0 % | 63.1 % | +0.336 | +0.002 | -0.019 | -4.3 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | 0.008 | 0.035 | 6.9 % | 3.2 % to 14.2 % | 0.0 % to 15.0 % | 70.0 % | +0.336 | +0.000 | -0.019 | -4.9 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | 0.000 | 0.035 | 0.0 % | 0.0 % to 4.2 % | 0.0 % to 0.0 % | n/a | +0.336 | +0.000 | -0.019 | +0.0 |

## Tile: HiRISE Jezero DTM, 2 km window 2 (selected for steepness), degraded to 200 m planner

Tile id steep-2, cell 20 m.

### Planner model: staircase (registered)

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | linear | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti | back | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | linear | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti | back | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | not computed |||||||||| 
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | not computed |||||||||| 

- not computed, dijkstra8 linear out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 linear out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra8 minetti_cap back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 linear out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap out, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, dijkstra16 minetti_cap back, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution

### Planner model: grid200

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | 0.202 | 0.095 | 99.2 % | 97.0 % to 99.8 % | 93.8 % to 100.0 % | 53.2 % | +0.406 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.7 | 0.194 | 0.095 | 98.3 % | 95.8 % to 99.3 % | 87.5 % to 100.0 % | 51.7 % | +0.406 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.9 | 0.188 | 0.095 | 97.5 % | 94.6 % to 98.8 % | 81.2 % to 100.0 % | 50.5 % | +0.406 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.5 | 0.213 | 0.095 | 98.7 % | 96.4 % to 99.6 % | 90.6 % to 100.0 % | 55.8 % | +0.400 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.7 | 0.190 | 0.095 | 95.8 % | 92.4 % to 97.7 % | 71.5 % to 100.0 % | 51.9 % | +0.400 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.9 | 0.159 | 0.095 | 84.9 % | 79.8 % to 88.9 % | 35.7 % to 100.0 % | 49.1 % | +0.400 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.5 | 0.221 | 0.095 | 98.3 % | 95.8 % to 99.3 % | 87.5 % to 100.0 % | 57.7 % | +0.361 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.7 | 0.176 | 0.095 | 89.9 % | 85.4 % to 93.1 % | 52.6 % to 100.0 % | 51.5 % | +0.361 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.9 | 0.132 | 0.095 | 73.1 % | 67.1 % to 78.3 % | 17.4 % to 99.0 % | 47.3 % | +0.361 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | minetti | out | 0.1 | 0.5 | 0.210 | 0.252 | 36.3 % | 32.6 % to 40.1 % | 6.8 % to 63.5 % | 56.4 % | +0.406 | +0.008 | +0.157 | -62.9 |
| dijkstra8 | minetti | out | 0.1 | 0.7 | 0.202 | 0.252 | 35.2 % | 31.6 % to 39.0 % | 6.0 % to 62.3 % | 56.0 % | +0.406 | +0.008 | +0.157 | -63.1 |
| dijkstra8 | minetti | out | 0.1 | 0.9 | 0.194 | 0.252 | 34.1 % | 30.5 % to 37.9 % | 6.0 % to 60.9 % | 55.6 % | +0.406 | +0.006 | +0.157 | -63.4 |
| dijkstra8 | minetti | out | 0.3 | 0.5 | 0.223 | 0.252 | 39.8 % | 36.0 % to 43.6 % | 7.2 % to 68.2 % | 54.9 % | +0.400 | +0.010 | +0.157 | -59.0 |
| dijkstra8 | minetti | out | 0.3 | 0.7 | 0.198 | 0.252 | 36.4 % | 32.8 % to 40.3 % | 5.7 % to 64.8 % | 53.4 % | +0.400 | +0.008 | +0.157 | -59.3 |
| dijkstra8 | minetti | out | 0.3 | 0.9 | 0.159 | 0.252 | 26.6 % | 23.3 % to 30.2 % | 3.0 % to 52.4 % | 57.8 % | +0.400 | +0.000 | +0.157 | -58.2 |
| dijkstra8 | minetti | out | 0.5 | 0.5 | 0.232 | 0.252 | 42.3 % | 38.5 % to 46.2 % | 8.2 % to 71.7 % | 54.0 % | +0.361 | +0.011 | +0.157 | -56.0 |
| dijkstra8 | minetti | out | 0.5 | 0.7 | 0.182 | 0.252 | 32.2 % | 28.6 % to 35.9 % | 5.6 % to 58.7 % | 55.4 % | +0.361 | +0.006 | +0.157 | -57.8 |
| dijkstra8 | minetti | out | 0.5 | 0.9 | 0.130 | 0.252 | 19.3 % | 16.4 % to 22.6 % | 1.1 % to 44.8 % | 62.6 % | +0.361 | -0.002 | +0.157 | -53.8 |
| dijkstra8 | minetti | back | 0.1 | 0.5 | 0.203 | 0.124 | 92.9 % | 89.5 % to 95.3 % | 77.2 % to 99.3 % | 43.4 % | +0.406 | +0.001 | +0.029 | -6.3 |
| dijkstra8 | minetti | back | 0.1 | 0.7 | 0.194 | 0.124 | 92.2 % | 88.7 % to 94.7 % | 74.7 % to 99.3 % | 41.2 % | +0.406 | +0.000 | +0.029 | -6.1 |
| dijkstra8 | minetti | back | 0.1 | 0.9 | 0.187 | 0.124 | 91.3 % | 87.6 % to 93.9 % | 70.3 % to 99.3 % | 39.7 % | +0.406 | -0.001 | +0.029 | -6.2 |
| dijkstra8 | minetti | back | 0.3 | 0.5 | 0.211 | 0.124 | 93.2 % | 89.8 % to 95.5 % | 78.3 % to 99.3 % | 45.4 % | +0.400 | -0.002 | +0.029 | -5.5 |
| dijkstra8 | minetti | back | 0.3 | 0.7 | 0.190 | 0.124 | 90.3 % | 86.5 % to 93.1 % | 64.2 % to 98.8 % | 41.1 % | +0.400 | +0.000 | +0.029 | -5.5 |
| dijkstra8 | minetti | back | 0.3 | 0.9 | 0.158 | 0.124 | 86.7 % | 82.5 % to 90.1 % | 54.7 % to 97.0 % | 32.3 % | +0.400 | -0.001 | +0.029 | +1.9 |
| dijkstra8 | minetti | back | 0.5 | 0.5 | 0.218 | 0.124 | 93.5 % | 90.2 % to 95.8 % | 78.8 % to 99.3 % | 47.1 % | +0.361 | -0.003 | +0.029 | -4.8 |
| dijkstra8 | minetti | back | 0.5 | 0.7 | 0.178 | 0.124 | 88.3 % | 84.3 % to 91.5 % | 59.6 % to 97.6 % | 38.5 % | +0.361 | +0.002 | +0.029 | -1.6 |
| dijkstra8 | minetti | back | 0.5 | 0.9 | 0.136 | 0.124 | 81.2 % | 76.5 % to 85.2 % | 35.3 % to 94.2 % | 26.2 % | +0.361 | +0.004 | +0.029 | +8.1 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | 0.193 | 0.059 | 100.0 % | 97.5 % to 100.0 % | 100.0 % to 100.0 % | 69.6 % | +0.406 | -0.009 | -0.036 | +0.8 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | 0.187 | 0.059 | 100.0 % | 97.5 % to 100.0 % | 100.0 % to 100.0 % | 68.5 % | +0.406 | -0.007 | -0.036 | +1.7 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | 0.180 | 0.059 | 100.0 % | 97.5 % to 100.0 % | 100.0 % to 100.0 % | 67.4 % | +0.406 | -0.008 | -0.036 | +2.5 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | 0.203 | 0.059 | 100.0 % | 97.5 % to 100.0 % | 100.0 % to 100.0 % | 71.1 % | +0.400 | -0.010 | -0.036 | +1.3 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | 0.181 | 0.059 | 99.3 % | 96.2 % to 99.9 % | 96.6 % to 100.0 % | 67.8 % | +0.400 | -0.009 | -0.036 | +3.5 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | 0.152 | 0.059 | 81.6 % | 74.6 % to 87.1 % | 37.9 % to 100.0 % | 68.4 % | +0.400 | -0.007 | -0.036 | -3.2 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | 0.210 | 0.059 | 100.0 % | 97.5 % to 100.0 % | 100.0 % to 100.0 % | 72.0 % | +0.361 | -0.011 | -0.036 | +1.7 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | 0.168 | 0.059 | 89.8 % | 83.8 % to 93.7 % | 62.1 % to 100.0 % | 68.6 % | +0.361 | -0.008 | -0.036 | -0.1 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | 0.126 | 0.059 | 63.3 % | 55.2 % to 70.6 % | 17.2 % to 100.0 % | 70.4 % | +0.361 | -0.006 | -0.036 | -9.8 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | 0.191 | 0.069 | 100.0 % | 97.8 % to 100.0 % | 100.0 % to 100.0 % | 63.7 % | +0.406 | -0.011 | -0.026 | +0.8 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | 0.183 | 0.069 | 100.0 % | 97.8 % to 100.0 % | 100.0 % to 100.0 % | 62.1 % | +0.406 | -0.011 | -0.026 | +1.7 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | 0.176 | 0.069 | 100.0 % | 97.8 % to 100.0 % | 100.0 % to 100.0 % | 60.8 % | +0.406 | -0.012 | -0.026 | +2.5 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | 0.198 | 0.069 | 100.0 % | 97.8 % to 100.0 % | 100.0 % to 100.0 % | 65.0 % | +0.400 | -0.015 | -0.026 | +1.3 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | 0.180 | 0.069 | 99.4 % | 96.8 % to 99.9 % | 92.3 % to 100.0 % | 61.7 % | +0.400 | -0.010 | -0.026 | +3.6 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | 0.150 | 0.069 | 93.1 % | 88.3 % to 96.0 % | 23.1 % to 100.0 % | 57.2 % | +0.400 | -0.009 | -0.026 | +8.2 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | 0.206 | 0.069 | 100.0 % | 97.8 % to 100.0 % | 100.0 % to 100.0 % | 66.5 % | +0.361 | -0.015 | -0.026 | +1.7 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | 0.167 | 0.069 | 96.0 % | 91.9 % to 98.0 % | 53.8 % to 100.0 % | 60.2 % | +0.361 | -0.009 | -0.026 | +6.0 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | 0.128 | 0.069 | 85.5 % | 79.5 % to 90.0 % | 7.7 % to 100.0 % | 53.8 % | +0.361 | -0.004 | -0.026 | +12.4 |
| dijkstra16 | linear | out | 0.1 | 0.5 | 0.226 | 0.104 | 100.0 % | 98.5 % to 100.0 % | 100.0 % to 100.0 % | 54.1 % | +0.406 | +0.024 | +0.009 | +0.8 |
| dijkstra16 | linear | out | 0.1 | 0.7 | 0.215 | 0.104 | 98.5 % | 96.1 % to 99.4 % | 90.0 % to 100.0 % | 52.6 % | +0.406 | +0.021 | +0.009 | +0.1 |
| dijkstra16 | linear | out | 0.1 | 0.9 | 0.204 | 0.104 | 96.9 % | 94.0 % to 98.4 % | 79.9 % to 100.0 % | 50.7 % | +0.406 | +0.016 | +0.009 | -0.6 |
| dijkstra16 | linear | out | 0.3 | 0.5 | 0.235 | 0.104 | 98.8 % | 96.7 % to 99.6 % | 92.5 % to 100.0 % | 56.5 % | +0.400 | +0.022 | +0.009 | +0.1 |
| dijkstra16 | linear | out | 0.3 | 0.7 | 0.211 | 0.104 | 95.4 % | 92.1 % to 97.3 % | 70.0 % to 100.0 % | 53.2 % | +0.400 | +0.021 | +0.009 | -0.4 |
| dijkstra16 | linear | out | 0.3 | 0.9 | 0.171 | 0.104 | 84.6 % | 79.7 % to 88.4 % | 37.9 % to 99.3 % | 48.7 % | +0.400 | +0.012 | +0.009 | -0.3 |
| dijkstra16 | linear | out | 0.5 | 0.5 | 0.242 | 0.104 | 98.5 % | 96.1 % to 99.4 % | 90.0 % to 100.0 % | 57.8 % | +0.361 | +0.021 | +0.009 | +0.1 |
| dijkstra16 | linear | out | 0.5 | 0.7 | 0.194 | 0.104 | 89.2 % | 84.8 % to 92.4 % | 53.7 % to 99.3 % | 52.4 % | +0.361 | +0.018 | +0.009 | -0.7 |
| dijkstra16 | linear | out | 0.5 | 0.9 | 0.140 | 0.104 | 72.2 % | 66.5 % to 77.3 % | 20.2 % to 98.4 % | 46.7 % | +0.361 | +0.008 | +0.009 | -0.9 |
| dijkstra16 | minetti | out | 0.1 | 0.5 | 0.250 | 0.298 | 39.1 % | 35.7 % to 42.7 % | 11.7 % to 65.0 % | 53.3 % | +0.406 | +0.048 | +0.203 | -60.0 |
| dijkstra16 | minetti | out | 0.1 | 0.7 | 0.238 | 0.298 | 37.8 % | 34.4 % to 41.3 % | 10.6 % to 63.7 % | 52.6 % | +0.406 | +0.044 | +0.203 | -60.5 |
| dijkstra16 | minetti | out | 0.1 | 0.9 | 0.221 | 0.298 | 35.1 % | 31.8 % to 38.6 % | 7.7 % to 61.1 % | 52.5 % | +0.406 | +0.033 | +0.203 | -62.4 |
| dijkstra16 | minetti | out | 0.3 | 0.5 | 0.265 | 0.298 | 43.7 % | 40.2 % to 47.3 % | 14.7 % to 69.9 % | 50.8 % | +0.400 | +0.052 | +0.203 | -55.0 |
| dijkstra16 | minetti | out | 0.3 | 0.7 | 0.232 | 0.298 | 38.5 % | 35.0 % to 42.0 % | 9.8 % to 64.8 % | 50.4 % | +0.400 | +0.042 | +0.203 | -57.3 |
| dijkstra16 | minetti | out | 0.3 | 0.9 | 0.183 | 0.298 | 28.0 % | 24.9 % to 31.3 % | 5.6 % to 52.3 % | 54.4 % | +0.400 | +0.024 | +0.203 | -56.9 |
| dijkstra16 | minetti | out | 0.5 | 0.5 | 0.270 | 0.298 | 44.6 % | 41.1 % to 48.2 % | 15.1 % to 71.5 % | 50.7 % | +0.361 | +0.049 | +0.203 | -53.7 |
| dijkstra16 | minetti | out | 0.5 | 0.7 | 0.208 | 0.298 | 32.3 % | 29.0 % to 35.7 % | 7.8 % to 57.0 % | 53.6 % | +0.361 | +0.032 | +0.203 | -57.6 |
| dijkstra16 | minetti | out | 0.5 | 0.9 | 0.143 | 0.298 | 18.6 % | 16.0 % to 21.6 % | 2.2 % to 41.3 % | 61.1 % | +0.361 | +0.011 | +0.203 | -54.5 |
| dijkstra16 | minetti | back | 0.1 | 0.5 | 0.227 | 0.135 | 97.9 % | 95.8 % to 99.0 % | 92.3 % to 100.0 % | 41.8 % | +0.406 | +0.025 | +0.040 | -1.2 |
| dijkstra16 | minetti | back | 0.1 | 0.7 | 0.216 | 0.135 | 96.4 % | 93.9 % to 98.0 % | 86.4 % to 99.7 % | 39.7 % | +0.406 | +0.022 | +0.040 | -1.9 |
| dijkstra16 | minetti | back | 0.1 | 0.9 | 0.204 | 0.135 | 95.0 % | 92.1 % to 96.8 % | 77.9 % to 99.7 % | 37.2 % | +0.406 | +0.016 | +0.040 | -2.5 |
| dijkstra16 | minetti | back | 0.3 | 0.5 | 0.238 | 0.135 | 97.3 % | 95.0 % to 98.6 % | 89.6 % to 99.8 % | 44.9 % | +0.400 | +0.025 | +0.040 | -1.4 |
| dijkstra16 | minetti | back | 0.3 | 0.7 | 0.209 | 0.135 | 93.8 % | 90.7 % to 95.9 % | 72.1 % to 99.4 % | 39.5 % | +0.400 | +0.019 | +0.040 | -2.0 |
| dijkstra16 | minetti | back | 0.3 | 0.9 | 0.172 | 0.135 | 89.3 % | 85.6 % to 92.2 % | 59.1 % to 97.6 % | 30.2 % | +0.400 | +0.013 | +0.040 | +4.4 |
| dijkstra16 | minetti | back | 0.5 | 0.5 | 0.242 | 0.135 | 97.0 % | 94.6 % to 98.4 % | 87.1 % to 100.0 % | 46.0 % | +0.361 | +0.021 | +0.040 | -1.3 |
| dijkstra16 | minetti | back | 0.5 | 0.7 | 0.192 | 0.135 | 91.4 % | 87.9 % to 93.9 % | 64.4 % to 98.2 % | 35.8 % | +0.361 | +0.016 | +0.040 | +1.5 |
| dijkstra16 | minetti | back | 0.5 | 0.9 | 0.148 | 0.135 | 82.2 % | 77.8 % to 85.9 % | 34.4 % to 95.0 % | 25.1 % | +0.361 | +0.016 | +0.040 | +9.1 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | 0.214 | 0.064 | 100.0 % | 97.7 % to 100.0 % | 100.0 % to 100.0 % | 69.9 % | +0.406 | +0.012 | -0.031 | +0.8 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | 0.204 | 0.064 | 100.0 % | 97.7 % to 100.0 % | 100.0 % to 100.0 % | 68.4 % | +0.406 | +0.010 | -0.031 | +1.7 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | 0.194 | 0.064 | 100.0 % | 97.7 % to 100.0 % | 100.0 % to 100.0 % | 66.8 % | +0.406 | +0.006 | -0.031 | +2.5 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | 0.224 | 0.064 | 100.0 % | 97.7 % to 100.0 % | 100.0 % to 100.0 % | 71.2 % | +0.400 | +0.011 | -0.031 | +1.3 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | 0.202 | 0.064 | 99.4 % | 96.6 % to 99.9 % | 96.6 % to 100.0 % | 68.3 % | +0.400 | +0.012 | -0.031 | +3.6 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | 0.162 | 0.064 | 82.6 % | 76.0 % to 87.7 % | 37.9 % to 100.0 % | 67.2 % | +0.400 | +0.003 | -0.031 | -2.3 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | 0.231 | 0.064 | 100.0 % | 97.7 % to 100.0 % | 100.0 % to 100.0 % | 72.1 % | +0.361 | +0.010 | -0.031 | +1.7 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | 0.182 | 0.064 | 90.1 % | 84.5 % to 93.8 % | 62.1 % to 100.0 % | 68.1 % | +0.361 | +0.006 | -0.031 | +0.1 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | 0.133 | 0.064 | 63.3 % | 55.7 % to 70.4 % | 17.2 % to 100.0 % | 69.3 % | +0.361 | +0.001 | -0.031 | -9.8 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | 0.204 | 0.074 | 100.0 % | 98.0 % to 100.0 % | 100.0 % to 100.0 % | 63.6 % | +0.406 | +0.002 | -0.021 | +0.8 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | 0.196 | 0.074 | 99.5 % | 97.0 % to 99.9 % | 91.3 % to 100.0 % | 62.5 % | +0.406 | +0.002 | -0.021 | +1.1 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | 0.189 | 0.074 | 99.5 % | 97.0 % to 99.9 % | 91.3 % to 100.0 % | 61.1 % | +0.406 | +0.001 | -0.021 | +2.0 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | 0.216 | 0.074 | 100.0 % | 98.0 % to 100.0 % | 100.0 % to 100.0 % | 65.7 % | +0.400 | +0.003 | -0.021 | +1.3 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | 0.194 | 0.074 | 98.9 % | 96.1 % to 99.7 % | 85.7 % to 100.0 % | 62.3 % | +0.400 | +0.004 | -0.021 | +3.1 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | 0.159 | 0.074 | 92.4 % | 87.7 % to 95.4 % | 21.4 % to 100.0 % | 56.9 % | +0.400 | +0.000 | -0.021 | +7.6 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | 0.220 | 0.074 | 99.5 % | 97.0 % to 99.9 % | 91.3 % to 100.0 % | 66.6 % | +0.361 | -0.001 | -0.021 | +1.1 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | 0.179 | 0.074 | 95.1 % | 91.0 % to 97.4 % | 50.0 % to 100.0 % | 60.6 % | +0.361 | +0.003 | -0.021 | +5.2 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | 0.136 | 0.074 | 83.8 % | 77.8 % to 88.4 % | 7.1 % to 100.0 % | 54.4 % | +0.361 | +0.004 | -0.021 | +10.7 |

## Tile: HiRISE Jezero DTM, 2 km window 3 (selected for steepness), degraded to 200 m planner

Tile id steep-3, cell 20 m.

### Planner model: staircase (registered)

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | 0.227 | 0.353 | 62.2 % | 58.9 % to 65.3 % | 38.6 % to 78.3 % | 3.2 % | -0.945 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.7 | 0.208 | 0.353 | 57.2 % | 53.9 % to 60.4 % | 32.2 % to 75.4 % | 3.1 % | -0.945 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.9 | 0.178 | 0.353 | 48.8 % | 45.5 % to 52.1 % | 22.1 % to 69.5 % | 3.4 % | -0.945 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.5 | 0.241 | 0.353 | 66.1 % | 63.0 % to 69.2 % | 43.4 % to 80.6 % | 3.1 % | -0.842 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.7 | 0.188 | 0.353 | 51.8 % | 48.5 % to 55.0 % | 29.4 % to 68.3 % | 3.0 % | -0.842 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.9 | 0.000 | 0.353 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.5 | 0.257 | 0.353 | 70.5 % | 67.5 % to 73.5 % | 51.8 % to 82.4 % | 3.1 % | -0.736 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.7 | 0.180 | 0.353 | 49.6 % | 46.3 % to 52.9 % | 28.7 % to 64.5 % | 2.7 % | -0.736 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.9 | 0.000 | 0.353 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | minetti | out | 0.1 | 0.5 | 0.267 | 0.302 | 81.7 % | 78.8 % to 84.3 % | 65.0 % to 89.8 % | 7.6 % | -0.945 | +0.040 | -0.051 | +19.6 |
| dijkstra8 | minetti | out | 0.1 | 0.7 | 0.258 | 0.302 | 79.5 % | 76.4 % to 82.2 % | 62.2 % to 88.0 % | 7.1 % | -0.945 | +0.050 | -0.051 | +22.3 |
| dijkstra8 | minetti | out | 0.1 | 0.9 | 0.234 | 0.302 | 71.8 % | 68.5 % to 74.9 % | 52.4 % to 81.9 % | 7.2 % | -0.945 | +0.056 | -0.051 | +23.0 |
| dijkstra8 | minetti | out | 0.3 | 0.5 | 0.274 | 0.302 | 82.9 % | 80.1 % to 85.4 % | 67.4 % to 90.4 % | 8.8 % | -0.842 | +0.033 | -0.051 | +16.8 |
| dijkstra8 | minetti | out | 0.3 | 0.7 | 0.232 | 0.302 | 71.0 % | 67.7 % to 74.1 % | 54.3 % to 79.4 % | 7.6 % | -0.842 | +0.044 | -0.051 | +19.2 |
| dijkstra8 | minetti | out | 0.3 | 0.9 | 0.000 | 0.302 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | -0.051 | +0.0 |
| dijkstra8 | minetti | out | 0.5 | 0.5 | 0.277 | 0.302 | 83.0 % | 80.2 % to 85.6 % | 68.7 % to 90.3 % | 9.5 % | -0.736 | +0.020 | -0.051 | +12.5 |
| dijkstra8 | minetti | out | 0.5 | 0.7 | 0.211 | 0.302 | 64.1 % | 60.6 % to 67.4 % | 48.6 % to 72.2 % | 8.3 % | -0.736 | +0.031 | -0.051 | +14.5 |
| dijkstra8 | minetti | out | 0.5 | 0.9 | 0.000 | 0.302 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | -0.051 | +0.0 |
| dijkstra8 | minetti | back | 0.1 | 0.5 | 0.198 | 0.712 | 27.7 % | 25.7 % to 29.9 % | 10.1 % to 46.1 % | 0.0 % | -0.945 | -0.029 | +0.359 | -34.4 |
| dijkstra8 | minetti | back | 0.1 | 0.7 | 0.182 | 0.712 | 25.5 % | 23.5 % to 27.6 % | 7.9 % to 43.7 % | 0.0 % | -0.945 | -0.026 | +0.359 | -31.7 |
| dijkstra8 | minetti | back | 0.1 | 0.9 | 0.164 | 0.712 | 23.0 % | 21.1 % to 25.0 % | 6.9 % to 39.5 % | 0.0 % | -0.945 | -0.014 | +0.359 | -25.8 |
| dijkstra8 | minetti | back | 0.3 | 0.5 | 0.219 | 0.712 | 30.7 % | 28.6 % to 32.9 % | 13.3 % to 49.1 % | 0.0 % | -0.842 | -0.022 | +0.359 | -35.4 |
| dijkstra8 | minetti | back | 0.3 | 0.7 | 0.168 | 0.712 | 23.6 % | 21.7 % to 25.6 % | 7.8 % to 39.7 % | 0.0 % | -0.842 | -0.020 | +0.359 | -28.2 |
| dijkstra8 | minetti | back | 0.3 | 0.9 | 0.000 | 0.712 | 0.0 % | 0.0 % to 0.2 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | +0.359 | +0.0 |
| dijkstra8 | minetti | back | 0.5 | 0.5 | 0.277 | 0.712 | 38.8 % | 36.6 % to 41.1 % | 21.2 % to 55.6 % | 0.3 % | -0.736 | +0.020 | +0.359 | -31.8 |
| dijkstra8 | minetti | back | 0.5 | 0.7 | 0.182 | 0.712 | 25.6 % | 23.6 % to 27.7 % | 11.4 % to 40.0 % | 0.0 % | -0.736 | +0.002 | +0.359 | -24.0 |
| dijkstra8 | minetti | back | 0.5 | 0.9 | 0.000 | 0.712 | 0.0 % | 0.0 % to 0.2 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | +0.359 | +0.0 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | 0.215 | 0.252 | 77.9 % | 74.5 % to 81.0 % | 58.1 % to 88.7 % | 8.9 % | -0.945 | -0.012 | -0.101 | +15.7 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | 0.197 | 0.252 | 70.9 % | 67.2 % to 74.3 % | 44.0 % to 86.6 % | 9.3 % | -0.945 | -0.011 | -0.101 | +13.7 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | 0.166 | 0.252 | 59.1 % | 55.3 % to 62.9 % | 26.6 % to 80.0 % | 10.6 % | -0.945 | -0.012 | -0.101 | +10.3 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | 0.228 | 0.252 | 82.8 % | 79.7 % to 85.6 % | 67.7 % to 90.5 % | 8.8 % | -0.842 | -0.013 | -0.101 | +16.7 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | 0.177 | 0.252 | 64.1 % | 60.2 % to 67.7 % | 39.1 % to 78.2 % | 9.0 % | -0.842 | -0.011 | -0.101 | +12.3 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | 0.000 | 0.252 | 0.0 % | 0.0 % to 0.6 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | -0.101 | +0.0 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | 0.235 | 0.252 | 83.6 % | 80.5 % to 86.3 % | 71.2 % to 90.1 % | 10.5 % | -0.736 | -0.022 | -0.101 | +13.1 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | 0.171 | 0.252 | 62.2 % | 58.3 % to 65.9 % | 41.1 % to 73.2 % | 8.6 % | -0.736 | -0.009 | -0.101 | +12.6 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | 0.000 | 0.252 | 0.0 % | 0.0 % to 0.6 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | -0.101 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | 0.187 | 0.307 | 58.2 % | 54.7 % to 61.6 % | 27.6 % to 78.0 % | 4.5 % | -0.945 | -0.040 | -0.046 | -4.0 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | 0.172 | 0.307 | 53.5 % | 50.0 % to 57.0 % | 21.2 % to 74.6 % | 4.4 % | -0.945 | -0.036 | -0.046 | -3.7 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | 0.150 | 0.307 | 46.4 % | 42.9 % to 49.9 % | 17.7 % to 65.3 % | 4.8 % | -0.945 | -0.028 | -0.046 | -2.5 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | 0.202 | 0.307 | 63.0 % | 59.5 % to 66.4 % | 36.6 % to 80.5 % | 4.3 % | -0.842 | -0.039 | -0.046 | -3.1 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | 0.156 | 0.307 | 48.6 % | 45.0 % to 52.1 % | 20.9 % to 66.2 % | 4.4 % | -0.842 | -0.032 | -0.046 | -3.2 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | 0.000 | 0.307 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | -0.046 | +0.0 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | 0.220 | 0.307 | 68.0 % | 64.6 % to 71.2 % | 46.3 % to 82.4 % | 4.9 % | -0.736 | -0.037 | -0.046 | -2.6 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | 0.152 | 0.307 | 47.4 % | 43.9 % to 50.9 % | 22.6 % to 63.4 % | 4.0 % | -0.736 | -0.028 | -0.046 | -2.2 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | 0.000 | 0.307 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | -0.046 | +0.0 |
| dijkstra16 | linear | out | 0.1 | 0.5 | 0.283 | 0.375 | 72.8 % | 69.8 % to 75.5 % | 50.0 % to 88.4 % | 3.7 % | -0.945 | +0.056 | +0.022 | +10.6 |
| dijkstra16 | linear | out | 0.1 | 0.7 | 0.278 | 0.375 | 71.9 % | 69.0 % to 74.7 % | 49.0 % to 87.5 % | 3.2 % | -0.945 | +0.070 | +0.022 | +14.7 |
| dijkstra16 | linear | out | 0.1 | 0.9 | 0.265 | 0.375 | 68.7 % | 65.7 % to 71.6 % | 46.3 % to 84.2 % | 2.9 % | -0.945 | +0.087 | +0.022 | +19.9 |
| dijkstra16 | linear | out | 0.3 | 0.5 | 0.283 | 0.375 | 72.2 % | 69.3 % to 75.0 % | 49.5 % to 87.5 % | 4.2 % | -0.842 | +0.042 | +0.022 | +6.1 |
| dijkstra16 | linear | out | 0.3 | 0.7 | 0.228 | 0.375 | 59.0 % | 55.8 % to 62.1 % | 39.2 % to 72.4 % | 3.0 % | -0.842 | +0.040 | +0.022 | +7.3 |
| dijkstra16 | linear | out | 0.3 | 0.9 | 0.000 | 0.375 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | +0.022 | +0.0 |
| dijkstra16 | linear | out | 0.5 | 0.5 | 0.298 | 0.375 | 77.0 % | 74.1 % to 79.5 % | 61.9 % to 86.7 % | 3.2 % | -0.736 | +0.041 | +0.022 | +6.4 |
| dijkstra16 | linear | out | 0.5 | 0.7 | 0.194 | 0.375 | 50.0 % | 46.8 % to 53.1 % | 30.4 % to 64.6 % | 3.5 % | -0.736 | +0.014 | +0.022 | +0.4 |
| dijkstra16 | linear | out | 0.5 | 0.9 | 0.000 | 0.375 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | +0.022 | +0.0 |
| dijkstra16 | minetti | out | 0.1 | 0.5 | 0.323 | 0.321 | 89.0 % | 86.7 % to 91.0 % | 79.3 % to 94.4 % | 11.4 % | -0.945 | +0.096 | -0.032 | +26.9 |
| dijkstra16 | minetti | out | 0.1 | 0.7 | 0.320 | 0.321 | 88.9 % | 86.6 % to 90.9 % | 79.2 % to 94.3 % | 10.9 % | -0.945 | +0.112 | -0.032 | +31.7 |
| dijkstra16 | minetti | out | 0.1 | 0.9 | 0.313 | 0.321 | 86.8 % | 84.3 % to 89.0 % | 76.4 % to 92.8 % | 10.9 % | -0.945 | +0.135 | -0.032 | +38.0 |
| dijkstra16 | minetti | out | 0.3 | 0.5 | 0.323 | 0.321 | 88.0 % | 85.6 % to 90.1 % | 78.4 % to 93.5 % | 12.4 % | -0.842 | +0.082 | -0.032 | +21.9 |
| dijkstra16 | minetti | out | 0.3 | 0.7 | 0.269 | 0.321 | 77.2 % | 74.2 % to 80.0 % | 63.6 % to 84.6 % | 7.9 % | -0.842 | +0.081 | -0.032 | +25.5 |
| dijkstra16 | minetti | out | 0.3 | 0.9 | 0.000 | 0.321 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | -0.032 | +0.0 |
| dijkstra16 | minetti | out | 0.5 | 0.5 | 0.322 | 0.321 | 86.9 % | 84.4 % to 89.1 % | 77.2 % to 92.5 % | 13.3 % | -0.736 | +0.065 | -0.032 | +16.4 |
| dijkstra16 | minetti | out | 0.5 | 0.7 | 0.236 | 0.321 | 67.2 % | 63.9 % to 70.4 % | 51.8 % to 74.9 % | 8.3 % | -0.736 | +0.056 | -0.032 | +17.6 |
| dijkstra16 | minetti | out | 0.5 | 0.9 | 0.000 | 0.321 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | -0.032 | +0.0 |
| dijkstra16 | minetti | back | 0.1 | 0.5 | 0.243 | 0.779 | 31.0 % | 29.0 % to 33.1 % | 14.1 % to 49.6 % | 0.7 % | -0.945 | +0.016 | +0.426 | -31.2 |
| dijkstra16 | minetti | back | 0.1 | 0.7 | 0.238 | 0.779 | 30.5 % | 28.5 % to 32.6 % | 13.7 % to 48.9 % | 0.3 % | -0.945 | +0.030 | +0.426 | -26.7 |
| dijkstra16 | minetti | back | 0.1 | 0.9 | 0.223 | 0.779 | 28.6 % | 26.7 % to 30.7 % | 12.4 % to 46.1 % | 0.0 % | -0.945 | +0.045 | +0.426 | -20.2 |
| dijkstra16 | minetti | back | 0.3 | 0.5 | 0.251 | 0.779 | 32.0 % | 30.0 % to 34.1 % | 15.1 % to 50.8 % | 0.6 % | -0.842 | +0.010 | +0.426 | -34.1 |
| dijkstra16 | minetti | back | 0.3 | 0.7 | 0.204 | 0.779 | 26.2 % | 24.3 % to 28.2 % | 11.4 % to 42.3 % | 0.0 % | -0.842 | +0.016 | +0.426 | -25.5 |
| dijkstra16 | minetti | back | 0.3 | 0.9 | 0.000 | 0.779 | 0.0 % | 0.0 % to 0.2 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | +0.426 | +0.0 |
| dijkstra16 | minetti | back | 0.5 | 0.5 | 0.316 | 0.779 | 40.2 % | 38.0 % to 42.4 % | 22.5 % to 57.3 % | 0.9 % | -0.736 | +0.059 | +0.426 | -30.3 |
| dijkstra16 | minetti | back | 0.5 | 0.7 | 0.200 | 0.779 | 25.7 % | 23.8 % to 27.7 % | 11.9 % to 39.9 % | 0.0 % | -0.736 | +0.020 | +0.426 | -23.9 |
| dijkstra16 | minetti | back | 0.5 | 0.9 | 0.000 | 0.779 | 0.0 % | 0.0 % to 0.2 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | +0.426 | +0.0 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | 0.266 | 0.269 | 89.0 % | 86.4 % to 91.2 % | 78.9 % to 94.3 % | 9.9 % | -0.945 | +0.039 | -0.084 | +26.8 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | 0.259 | 0.269 | 87.8 % | 85.1 % to 90.1 % | 77.4 % to 93.4 % | 8.8 % | -0.945 | +0.051 | -0.084 | +30.6 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | 0.248 | 0.269 | 84.2 % | 81.3 % to 86.8 % | 72.9 % to 90.8 % | 8.6 % | -0.945 | +0.070 | -0.084 | +35.4 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | 0.269 | 0.269 | 88.7 % | 86.1 % to 90.9 % | 78.6 % to 94.2 % | 11.2 % | -0.842 | +0.028 | -0.084 | +22.6 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | 0.206 | 0.269 | 70.6 % | 67.0 % to 73.9 % | 55.7 % to 78.7 % | 8.0 % | -0.842 | +0.018 | -0.084 | +18.8 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | 0.000 | 0.269 | 0.0 % | 0.0 % to 0.6 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | -0.084 | +0.0 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | 0.262 | 0.269 | 87.1 % | 84.3 % to 89.4 % | 77.1 % to 92.5 % | 10.7 % | -0.736 | +0.005 | -0.084 | +16.5 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | 0.180 | 0.269 | 61.1 % | 57.3 % to 64.7 % | 41.9 % to 72.1 % | 8.9 % | -0.736 | +0.000 | -0.084 | +11.5 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | 0.000 | 0.269 | 0.0 % | 0.0 % to 0.6 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | -0.084 | +0.0 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | 0.228 | 0.329 | 66.7 % | 63.4 % to 69.8 % | 41.1 % to 83.9 % | 4.0 % | -0.945 | +0.001 | -0.024 | +4.5 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | 0.223 | 0.329 | 65.2 % | 61.9 % to 68.4 % | 39.3 % to 82.6 % | 3.8 % | -0.945 | +0.015 | -0.024 | +8.0 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | 0.209 | 0.329 | 61.2 % | 57.8 % to 64.5 % | 36.0 % to 79.0 % | 3.6 % | -0.945 | +0.031 | -0.024 | +12.4 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | 0.232 | 0.329 | 67.6 % | 64.4 % to 70.7 % | 42.6 % to 84.5 % | 4.3 % | -0.842 | -0.009 | -0.024 | +1.5 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | 0.188 | 0.329 | 55.0 % | 51.6 % to 58.4 % | 31.5 % to 71.4 % | 3.8 % | -0.842 | +0.000 | -0.024 | +3.2 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | 0.000 | 0.329 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.842 | +0.000 | -0.024 | +0.0 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | 0.255 | 0.329 | 74.2 % | 71.1 % to 77.1 % | 58.2 % to 85.4 % | 4.2 % | -0.736 | -0.002 | -0.024 | +3.7 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | 0.160 | 0.329 | 46.5 % | 43.1 % to 49.9 % | 22.6 % to 63.2 % | 4.5 % | -0.736 | -0.020 | -0.024 | -3.1 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | 0.000 | 0.329 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | -0.736 | +0.000 | -0.024 | +0.0 |

### Planner model: grid200

Differences are against the registered row of the same planner model, roughness and confidence (dijkstra8, linear, out). Area in km2, coverage difference in percentage points.

| solver | speed | direction | roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier skill | d calibrated | d truth | d coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dijkstra8 | linear | out | 0.1 | 0.5 | 0.340 | 0.353 | 94.3 % | 92.6 % to 95.7 % | 88.2 % to 98.0 % | 2.0 % | +0.190 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.7 | 0.337 | 0.353 | 93.9 % | 92.1 % to 95.3 % | 87.3 % to 97.9 % | 1.7 % | +0.190 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.1 | 0.9 | 0.334 | 0.353 | 93.3 % | 91.5 % to 94.8 % | 86.3 % to 97.7 % | 1.4 % | +0.190 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.5 | 0.345 | 0.353 | 95.8 % | 94.3 % to 96.9 % | 91.4 % to 98.6 % | 2.0 % | +0.254 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.7 | 0.337 | 0.353 | 93.8 % | 92.0 % to 95.2 % | 86.9 % to 97.9 % | 1.8 % | +0.254 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.3 | 0.9 | 0.323 | 0.353 | 90.4 % | 88.2 % to 92.1 % | 79.9 % to 96.9 % | 1.1 % | +0.254 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.5 | 0.348 | 0.353 | 96.5 % | 95.1 % to 97.5 % | 92.7 % to 98.9 % | 2.2 % | +0.215 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.7 | 0.330 | 0.353 | 92.4 % | 90.5 % to 94.0 % | 84.1 % to 97.5 % | 1.2 % | +0.215 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | linear | out | 0.5 | 0.9 | 0.300 | 0.353 | 84.4 % | 81.8 % to 86.6 % | 68.4 % to 94.2 % | 0.8 % | +0.215 | +0.000 | +0.000 | +0.0 |
| dijkstra8 | minetti | out | 0.1 | 0.5 | 0.349 | 0.302 | 96.0 % | 94.4 % to 97.2 % | 88.7 % to 100.0 % | 16.9 % | +0.190 | +0.009 | -0.051 | +1.7 |
| dijkstra8 | minetti | out | 0.1 | 0.7 | 0.346 | 0.302 | 95.9 % | 94.2 % to 97.1 % | 88.4 % to 100.0 % | 16.4 % | +0.190 | +0.009 | -0.051 | +2.0 |
| dijkstra8 | minetti | out | 0.1 | 0.9 | 0.343 | 0.302 | 95.5 % | 93.8 % to 96.8 % | 87.6 % to 99.8 % | 15.9 % | +0.190 | +0.009 | -0.051 | +2.2 |
| dijkstra8 | minetti | out | 0.3 | 0.5 | 0.355 | 0.302 | 95.9 % | 94.2 % to 97.1 % | 88.4 % to 100.0 % | 18.4 % | +0.254 | +0.010 | -0.051 | +0.1 |
| dijkstra8 | minetti | out | 0.3 | 0.7 | 0.347 | 0.302 | 95.8 % | 94.1 % to 97.0 % | 88.0 % to 100.0 % | 16.6 % | +0.254 | +0.010 | -0.051 | +2.0 |
| dijkstra8 | minetti | out | 0.3 | 0.9 | 0.333 | 0.302 | 95.0 % | 93.2 % to 96.3 % | 86.5 % to 99.3 % | 13.9 % | +0.254 | +0.010 | -0.051 | +4.6 |
| dijkstra8 | minetti | out | 0.5 | 0.5 | 0.358 | 0.302 | 95.8 % | 94.1 % to 97.0 % | 87.9 % to 100.0 % | 19.2 % | +0.215 | +0.010 | -0.051 | -0.7 |
| dijkstra8 | minetti | out | 0.5 | 0.7 | 0.346 | 0.302 | 95.4 % | 93.6 % to 96.6 % | 86.9 % to 100.0 % | 16.7 % | +0.215 | +0.016 | -0.051 | +2.9 |
| dijkstra8 | minetti | out | 0.5 | 0.9 | 0.317 | 0.302 | 92.7 % | 90.6 % to 94.4 % | 82.0 % to 98.0 % | 11.7 % | +0.215 | +0.017 | -0.051 | +8.4 |
| dijkstra8 | minetti | back | 0.1 | 0.5 | 0.358 | 0.712 | 47.3 % | 45.0 % to 49.6 % | 30.1 % to 64.6 % | 5.8 % | +0.190 | +0.018 | +0.359 | -47.1 |
| dijkstra8 | minetti | back | 0.1 | 0.7 | 0.354 | 0.712 | 46.9 % | 44.6 % to 49.2 % | 29.7 % to 64.3 % | 5.8 % | +0.190 | +0.017 | +0.359 | -47.0 |
| dijkstra8 | minetti | back | 0.1 | 0.9 | 0.351 | 0.712 | 46.5 % | 44.2 % to 48.8 % | 29.2 % to 64.1 % | 5.6 % | +0.190 | +0.017 | +0.359 | -46.8 |
| dijkstra8 | minetti | back | 0.3 | 0.5 | 0.362 | 0.712 | 47.9 % | 45.6 % to 50.3 % | 30.7 % to 65.3 % | 5.7 % | +0.254 | +0.017 | +0.359 | -47.9 |
| dijkstra8 | minetti | back | 0.3 | 0.7 | 0.353 | 0.712 | 46.8 % | 44.5 % to 49.1 % | 29.6 % to 64.2 % | 5.5 % | +0.254 | +0.016 | +0.359 | -46.9 |
| dijkstra8 | minetti | back | 0.3 | 0.9 | 0.338 | 0.712 | 45.0 % | 42.7 % to 47.3 % | 27.1 % to 62.7 % | 5.1 % | +0.254 | +0.015 | +0.359 | -45.4 |
| dijkstra8 | minetti | back | 0.5 | 0.5 | 0.366 | 0.712 | 48.6 % | 46.3 % to 50.9 % | 31.4 % to 65.7 % | 5.6 % | +0.215 | +0.018 | +0.359 | -47.9 |
| dijkstra8 | minetti | back | 0.5 | 0.7 | 0.347 | 0.712 | 46.2 % | 43.9 % to 48.5 % | 28.7 % to 63.7 % | 5.1 % | +0.215 | +0.017 | +0.359 | -46.2 |
| dijkstra8 | minetti | back | 0.5 | 0.9 | 0.307 | 0.712 | 41.0 % | 38.8 % to 43.3 % | 22.5 % to 59.8 % | 4.8 % | +0.215 | +0.007 | +0.359 | -43.3 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.5 | 0.312 | 0.252 | 99.7 % | 98.8 % to 99.9 % | 98.8 % to 100.0 % | 19.6 % | +0.190 | -0.028 | -0.101 | +5.3 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.7 | 0.311 | 0.252 | 99.7 % | 98.8 % to 99.9 % | 98.8 % to 100.0 % | 19.3 % | +0.190 | -0.026 | -0.101 | +5.8 |
| dijkstra8 | minetti_cap | out | 0.1 | 0.9 | 0.308 | 0.252 | 99.7 % | 98.8 % to 99.9 % | 98.8 % to 100.0 % | 18.7 % | +0.190 | -0.026 | -0.101 | +6.4 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.5 | 0.318 | 0.252 | 99.8 % | 99.1 % to 100.0 % | 99.4 % to 100.0 % | 21.0 % | +0.254 | -0.027 | -0.101 | +4.0 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.7 | 0.312 | 0.252 | 99.7 % | 98.8 % to 99.9 % | 98.8 % to 100.0 % | 19.5 % | +0.254 | -0.025 | -0.101 | +5.9 |
| dijkstra8 | minetti_cap | out | 0.3 | 0.9 | 0.298 | 0.252 | 99.1 % | 97.9 % to 99.6 % | 97.2 % to 100.0 % | 16.5 % | +0.254 | -0.025 | -0.101 | +8.7 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.5 | 0.320 | 0.252 | 99.8 % | 99.1 % to 100.0 % | 99.4 % to 100.0 % | 21.6 % | +0.215 | -0.028 | -0.101 | +3.3 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.7 | 0.307 | 0.252 | 99.1 % | 97.9 % to 99.6 % | 96.9 % to 100.0 % | 18.8 % | +0.215 | -0.023 | -0.101 | +6.6 |
| dijkstra8 | minetti_cap | out | 0.5 | 0.9 | 0.284 | 0.252 | 97.0 % | 95.3 % to 98.1 % | 92.8 % to 99.1 % | 14.2 % | +0.215 | -0.016 | -0.101 | +12.6 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.5 | 0.315 | 0.307 | 94.0 % | 92.1 % to 95.5 % | 86.6 % to 98.5 % | 8.3 % | +0.190 | -0.025 | -0.046 | -0.3 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.7 | 0.312 | 0.307 | 93.4 % | 91.4 % to 94.9 % | 85.2 % to 98.4 % | 8.0 % | +0.190 | -0.025 | -0.046 | -0.5 |
| dijkstra8 | minetti_cap | back | 0.1 | 0.9 | 0.308 | 0.307 | 93.0 % | 90.9 % to 94.6 % | 84.3 % to 98.3 % | 7.4 % | +0.190 | -0.026 | -0.046 | -0.4 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.5 | 0.320 | 0.307 | 95.6 % | 93.9 % to 96.8 % | 90.1 % to 98.9 % | 8.2 % | +0.254 | -0.025 | -0.046 | -0.2 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.7 | 0.312 | 0.307 | 93.2 % | 91.2 % to 94.8 % | 84.4 % to 98.5 % | 8.1 % | +0.254 | -0.025 | -0.046 | -0.5 |
| dijkstra8 | minetti_cap | back | 0.3 | 0.9 | 0.298 | 0.307 | 90.2 % | 87.9 % to 92.1 % | 78.4 % to 97.7 % | 7.1 % | +0.254 | -0.025 | -0.046 | -0.1 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.5 | 0.322 | 0.307 | 96.2 % | 94.6 % to 97.4 % | 91.4 % to 99.2 % | 8.1 % | +0.215 | -0.026 | -0.046 | -0.3 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.7 | 0.305 | 0.307 | 91.7 % | 89.5 % to 93.4 % | 81.4 % to 98.0 % | 7.7 % | +0.215 | -0.025 | -0.046 | -0.7 |
| dijkstra8 | minetti_cap | back | 0.5 | 0.9 | 0.276 | 0.307 | 84.4 % | 81.6 % to 86.8 % | 66.3 % to 95.6 % | 6.1 % | +0.215 | -0.024 | -0.046 | +0.0 |
| dijkstra16 | linear | out | 0.1 | 0.5 | 0.363 | 0.375 | 95.0 % | 93.4 % to 96.2 % | 89.8 % to 98.3 % | 2.0 % | +0.190 | +0.023 | +0.022 | +0.6 |
| dijkstra16 | linear | out | 0.1 | 0.7 | 0.360 | 0.375 | 94.2 % | 92.6 % to 95.6 % | 88.4 % to 98.0 % | 1.8 % | +0.190 | +0.023 | +0.022 | +0.4 |
| dijkstra16 | linear | out | 0.1 | 0.9 | 0.356 | 0.375 | 93.5 % | 91.7 % to 94.9 % | 86.9 % to 97.8 % | 1.7 % | +0.190 | +0.022 | +0.022 | +0.2 |
| dijkstra16 | linear | out | 0.3 | 0.5 | 0.376 | 0.375 | 97.1 % | 95.8 % to 98.0 % | 94.2 % to 99.2 % | 3.2 % | +0.254 | +0.031 | +0.022 | +1.3 |
| dijkstra16 | linear | out | 0.3 | 0.7 | 0.366 | 0.375 | 95.5 % | 94.0 % to 96.7 % | 90.7 % to 98.6 % | 2.1 % | +0.254 | +0.029 | +0.022 | +1.8 |
| dijkstra16 | linear | out | 0.3 | 0.9 | 0.351 | 0.375 | 92.2 % | 90.3 % to 93.8 % | 83.7 % to 97.5 % | 1.5 % | +0.254 | +0.028 | +0.022 | +1.8 |
| dijkstra16 | linear | out | 0.5 | 0.5 | 0.386 | 0.375 | 98.5 % | 97.5 % to 99.1 % | 96.8 % to 99.7 % | 4.2 % | +0.215 | +0.038 | +0.022 | +2.0 |
| dijkstra16 | linear | out | 0.5 | 0.7 | 0.366 | 0.375 | 94.8 % | 93.2 % to 96.0 % | 88.8 % to 98.6 % | 2.8 % | +0.215 | +0.036 | +0.022 | +2.4 |
| dijkstra16 | linear | out | 0.5 | 0.9 | 0.328 | 0.375 | 86.2 % | 83.9 % to 88.3 % | 72.2 % to 95.3 % | 1.3 % | +0.215 | +0.028 | +0.022 | +1.9 |
| dijkstra16 | minetti | out | 0.1 | 0.5 | 0.399 | 0.321 | 98.8 % | 97.7 % to 99.3 % | 95.8 % to 100.0 % | 20.5 % | +0.190 | +0.059 | -0.032 | +4.4 |
| dijkstra16 | minetti | out | 0.1 | 0.7 | 0.395 | 0.321 | 98.8 % | 97.7 % to 99.3 % | 95.8 % to 100.0 % | 19.7 % | +0.190 | +0.058 | -0.032 | +4.9 |
| dijkstra16 | minetti | out | 0.1 | 0.9 | 0.392 | 0.321 | 98.8 % | 97.7 % to 99.3 % | 95.8 % to 100.0 % | 19.2 % | +0.190 | +0.058 | -0.032 | +5.4 |
| dijkstra16 | minetti | out | 0.3 | 0.5 | 0.412 | 0.321 | 98.8 % | 97.7 % to 99.3 % | 95.8 % to 100.0 % | 22.9 % | +0.254 | +0.067 | -0.032 | +2.9 |
| dijkstra16 | minetti | out | 0.3 | 0.7 | 0.400 | 0.321 | 98.8 % | 97.7 % to 99.3 % | 95.8 % to 100.0 % | 20.7 % | +0.254 | +0.063 | -0.032 | +5.0 |
| dijkstra16 | minetti | out | 0.3 | 0.9 | 0.386 | 0.321 | 97.9 % | 96.6 % to 98.7 % | 94.2 % to 99.7 % | 18.5 % | +0.254 | +0.063 | -0.032 | +7.5 |
| dijkstra16 | minetti | out | 0.5 | 0.5 | 0.420 | 0.321 | 99.0 % | 98.0 % to 99.5 % | 96.4 % to 100.0 % | 24.4 % | +0.215 | +0.072 | -0.032 | +2.5 |
| dijkstra16 | minetti | out | 0.5 | 0.7 | 0.402 | 0.321 | 98.6 % | 97.6 % to 99.2 % | 95.5 % to 99.9 % | 21.3 % | +0.215 | +0.072 | -0.032 | +6.2 |
| dijkstra16 | minetti | out | 0.5 | 0.9 | 0.365 | 0.321 | 95.6 % | 94.0 % to 96.8 % | 88.9 % to 98.9 % | 15.9 % | +0.215 | +0.065 | -0.032 | +11.3 |
| dijkstra16 | minetti | back | 0.1 | 0.5 | 0.418 | 0.779 | 50.7 % | 48.5 % to 52.9 % | 33.5 % to 67.5 % | 5.4 % | +0.190 | +0.078 | +0.426 | -43.6 |
| dijkstra16 | minetti | back | 0.1 | 0.7 | 0.414 | 0.779 | 50.4 % | 48.1 % to 52.6 % | 33.0 % to 67.2 % | 5.3 % | +0.190 | +0.077 | +0.426 | -43.5 |
| dijkstra16 | minetti | back | 0.1 | 0.9 | 0.407 | 0.779 | 49.6 % | 47.4 % to 51.8 % | 32.5 % to 66.4 % | 5.1 % | +0.190 | +0.073 | +0.426 | -43.7 |
| dijkstra16 | minetti | back | 0.3 | 0.5 | 0.434 | 0.779 | 52.7 % | 50.5 % to 54.9 % | 35.3 % to 69.1 % | 5.4 % | +0.254 | +0.089 | +0.426 | -43.1 |
| dijkstra16 | minetti | back | 0.3 | 0.7 | 0.418 | 0.779 | 50.7 % | 48.5 % to 52.9 % | 33.2 % to 67.1 % | 5.5 % | +0.254 | +0.081 | +0.426 | -43.0 |
| dijkstra16 | minetti | back | 0.3 | 0.9 | 0.393 | 0.779 | 47.9 % | 45.7 % to 50.2 % | 30.5 % to 65.0 % | 5.0 % | +0.254 | +0.070 | +0.426 | -42.4 |
| dijkstra16 | minetti | back | 0.5 | 0.5 | 0.443 | 0.779 | 53.7 % | 51.5 % to 55.9 % | 36.1 % to 70.0 % | 5.5 % | +0.215 | +0.095 | +0.426 | -42.8 |
| dijkstra16 | minetti | back | 0.5 | 0.7 | 0.416 | 0.779 | 50.6 % | 48.3 % to 52.8 % | 33.1 % to 67.4 % | 5.2 % | +0.215 | +0.086 | +0.426 | -41.9 |
| dijkstra16 | minetti | back | 0.5 | 0.9 | 0.358 | 0.779 | 43.7 % | 41.5 % to 46.0 % | 26.1 % to 61.8 % | 4.8 % | +0.215 | +0.058 | +0.426 | -40.6 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.5 | 0.330 | 0.269 | 99.1 % | 98.1 % to 99.6 % | 96.9 % to 100.0 % | 19.2 % | +0.190 | -0.010 | -0.084 | +4.8 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.7 | 0.329 | 0.269 | 99.1 % | 98.1 % to 99.6 % | 96.9 % to 100.0 % | 19.0 % | +0.190 | -0.008 | -0.084 | +5.2 |
| dijkstra16 | minetti_cap | out | 0.1 | 0.9 | 0.325 | 0.269 | 99.0 % | 97.9 % to 99.5 % | 96.4 % to 100.0 % | 18.0 % | +0.190 | -0.009 | -0.084 | +5.6 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.5 | 0.341 | 0.269 | 99.3 % | 98.3 % to 99.7 % | 97.4 % to 100.0 % | 21.7 % | +0.254 | -0.004 | -0.084 | +3.5 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.7 | 0.329 | 0.269 | 99.1 % | 98.1 % to 99.6 % | 96.9 % to 100.0 % | 19.0 % | +0.254 | -0.008 | -0.084 | +5.3 |
| dijkstra16 | minetti_cap | out | 0.3 | 0.9 | 0.320 | 0.269 | 98.4 % | 97.1 % to 99.1 % | 95.2 % to 100.0 % | 17.2 % | +0.254 | -0.003 | -0.084 | +8.0 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.5 | 0.349 | 0.269 | 99.4 % | 98.5 % to 99.8 % | 97.9 % to 100.0 % | 23.3 % | +0.215 | +0.001 | -0.084 | +2.9 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.7 | 0.332 | 0.269 | 99.1 % | 98.1 % to 99.6 % | 97.1 % to 100.0 % | 19.5 % | +0.215 | +0.002 | -0.084 | +6.7 |
| dijkstra16 | minetti_cap | out | 0.5 | 0.9 | 0.305 | 0.269 | 96.0 % | 94.2 % to 97.2 % | 90.5 % to 98.8 % | 15.3 % | +0.215 | +0.005 | -0.084 | +11.6 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.5 | 0.335 | 0.329 | 94.9 % | 93.2 % to 96.2 % | 89.1 % to 98.6 % | 6.9 % | +0.190 | -0.005 | -0.024 | +0.5 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.7 | 0.333 | 0.329 | 94.3 % | 92.5 % to 95.7 % | 87.8 % to 98.3 % | 6.9 % | +0.190 | -0.004 | -0.024 | +0.4 |
| dijkstra16 | minetti_cap | back | 0.1 | 0.9 | 0.328 | 0.329 | 93.3 % | 91.4 % to 94.8 % | 85.7 % to 98.0 % | 6.5 % | +0.190 | -0.006 | -0.024 | -0.0 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.5 | 0.347 | 0.329 | 97.2 % | 95.8 % to 98.1 % | 93.9 % to 99.3 % | 8.0 % | +0.254 | +0.002 | -0.024 | +1.4 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.7 | 0.337 | 0.329 | 95.5 % | 93.9 % to 96.7 % | 90.1 % to 98.9 % | 6.9 % | +0.254 | +0.000 | -0.024 | +1.7 |
| dijkstra16 | minetti_cap | back | 0.3 | 0.9 | 0.321 | 0.329 | 91.6 % | 89.5 % to 93.3 % | 81.5 % to 97.6 % | 6.1 % | +0.254 | -0.002 | -0.024 | +1.2 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.5 | 0.354 | 0.329 | 98.3 % | 97.2 % to 99.0 % | 96.3 % to 99.6 % | 8.8 % | +0.215 | +0.006 | -0.024 | +1.8 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.7 | 0.338 | 0.329 | 94.9 % | 93.2 % to 96.2 % | 88.2 % to 99.1 % | 7.6 % | +0.215 | +0.008 | -0.024 | +2.5 |
| dijkstra16 | minetti_cap | back | 0.5 | 0.9 | 0.299 | 0.329 | 85.6 % | 83.1 % to 87.9 % | 69.9 % to 95.7 % | 5.9 % | +0.215 | -0.001 | -0.024 | +1.3 |

