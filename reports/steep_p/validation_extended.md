# Extended validation (exploratory, registered before it was run)

This is not the validation result. The pre-registered headline in validation_report.md is unchanged.
Registered in PREREGISTRATION.md, section "Extended validation and sub-grid roughness".

Fixed: habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20.0 deg (assumed), 16 realizations, seed 1234.

The hurst model uses H = 0.853, read from reports\scale_effect.md. That value was measured on the 2 km window of tile jezero-20m: the hurst rows of that tile are IN-SAMPLE, the hurst rows of every other tile are out-of-sample (a different window of the same DTM, same site). One value of H from one window is a thin basis; no claim about other terrain is made.

All rows of all three models are reported. No row is chosen as the result. When one interval is needed, quote the wider of the Wilson and the block-bootstrap interval. If no row reaches 95 % coverage, that is a shortfall.

## Tile: HiRISE Jezero DTM, 2 km window 1 (selected for steepness, passable habitat), degraded to 200 m planner

Tile id steep-p-1, cell 20 m.

No-skill Brier (always "never steep") for this tile: 0.07594. A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.

### staircase (registered)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.237 | 0.228 | 77.9 % | 74.3 % to 81.1 % | 52.6 % to 91.6 % | 25.0 % | 0.24723 | 0.07594 | -2.255 |
| 0.1 | 0.7 | 0.229 | 0.228 | 76.5 % | 72.8 % to 79.8 % | 50.8 % to 90.7 % | 23.8 % | 0.24723 | 0.07594 | -2.255 |
| 0.1 | 0.9 | 0.220 | 0.228 | 75.3 % | 71.6 % to 78.6 % | 49.9 % to 89.3 % | 22.1 % | 0.24723 | 0.07594 | -2.255 |
| 0.3 | 0.5 | 0.256 | 0.228 | 80.9 % | 77.4 % to 83.9 % | 59.5 % to 93.3 % | 28.0 % | 0.23271 | 0.07594 | -2.064 |
| 0.3 | 0.7 | 0.230 | 0.228 | 74.9 % | 71.2 % to 78.3 % | 53.0 % to 87.3 % | 25.7 % | 0.23271 | 0.07594 | -2.064 |
| 0.3 | 0.9 | 0.202 | 0.228 | 66.5 % | 62.5 % to 70.2 % | 42.3 % to 78.4 % | 25.1 % | 0.23271 | 0.07594 | -2.064 |
| 0.5 | 0.5 | 0.261 | 0.228 | 80.3 % | 76.9 % to 83.4 % | 60.2 % to 92.5 % | 29.8 % | 0.21053 | 0.07594 | -1.772 |
| 0.5 | 0.7 | 0.217 | 0.228 | 68.4 % | 64.5 % to 72.1 % | 48.3 % to 79.0 % | 28.0 % | 0.21053 | 0.07594 | -1.772 |
| 0.5 | 0.9 | 0.000 | 0.228 | 0.0 % | 0.0 % to 0.7 % | 0.0 % to 0.0 % | n/a | 0.21053 | 0.07594 | -1.772 |

### grid200

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.405 | 0.228 | 100.0 % | 99.3 % to 100.0 % | 100.0 % to 100.0 % | 43.7 % | 0.07580 | 0.07594 | +0.002 |
| 0.1 | 0.7 | 0.401 | 0.228 | 100.0 % | 99.3 % to 100.0 % | 100.0 % to 100.0 % | 43.2 % | 0.07580 | 0.07594 | +0.002 |
| 0.1 | 0.9 | 0.399 | 0.228 | 100.0 % | 99.3 % to 100.0 % | 100.0 % to 100.0 % | 42.9 % | 0.07580 | 0.07594 | +0.002 |
| 0.3 | 0.5 | 0.412 | 0.228 | 100.0 % | 99.3 % to 100.0 % | 100.0 % to 100.0 % | 44.6 % | 0.06709 | 0.07594 | +0.117 |
| 0.3 | 0.7 | 0.401 | 0.228 | 99.8 % | 99.0 % to 100.0 % | 99.3 % to 100.0 % | 43.3 % | 0.06709 | 0.07594 | +0.117 |
| 0.3 | 0.9 | 0.393 | 0.228 | 99.1 % | 98.0 % to 99.6 % | 97.6 % to 100.0 % | 42.5 % | 0.06709 | 0.07594 | +0.117 |
| 0.5 | 0.5 | 0.414 | 0.228 | 100.0 % | 99.3 % to 100.0 % | 100.0 % to 100.0 % | 44.9 % | 0.07481 | 0.07594 | +0.015 |
| 0.5 | 0.7 | 0.400 | 0.228 | 99.1 % | 98.0 % to 99.6 % | 97.6 % to 100.0 % | 43.6 % | 0.07481 | 0.07594 | +0.015 |
| 0.5 | 0.9 | 0.366 | 0.228 | 93.3 % | 91.0 % to 95.1 % | 80.8 % to 99.5 % | 41.9 % | 0.07481 | 0.07594 | +0.015 |

### grid200 + hurst (out-of-sample H, measured on jezero-20m)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| n/a | 0.5 | 0.212 | 0.228 | 74.2 % | 70.5 % to 77.6 % | 45.1 % to 91.2 % | 20.3 % | 0.07981 | 0.07594 | -0.051 |
| n/a | 0.7 | 0.188 | 0.228 | 68.2 % | 64.3 % to 71.9 % | 34.9 % to 87.6 % | 17.2 % | 0.07981 | 0.07594 | -0.051 |
| n/a | 0.9 | 0.102 | 0.228 | 36.8 % | 33.0 % to 40.9 % | 12.2 % to 51.3 % | 18.0 % | 0.07981 | 0.07594 | -0.051 |

### Reliability of the reach probability

Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those cells reachable in the truth. Roughness 0.5 for the multiplicative models.

staircase (registered)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9074 | 0.001 | 0.003 |
| 1 | 162 | 0.151 | 0.241 |
| 2 | 42 | 0.250 | 0.333 |
| 3 | 49 | 0.343 | 0.388 |
| 4 | 21 | 0.438 | 0.524 |
| 5 | 39 | 0.529 | 0.667 |
| 6 | 71 | 0.664 | 0.592 |
| 7 | 43 | 0.750 | 0.581 |
| 8 | 499 | 0.812 | 0.731 |

grid200

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 8916 | 0.000 | 0.000 |
| 1 | 16 | 0.156 | 0.000 |
| 2 | 9 | 0.250 | 0.000 |
| 3 | 18 | 0.340 | 0.000 |
| 4 | 6 | 0.438 | 0.000 |
| 5 | 14 | 0.522 | 0.000 |
| 6 | 20 | 0.659 | 0.250 |
| 7 | 10 | 0.750 | 0.100 |
| 8 | 76 | 0.854 | 0.421 |
| 9 | 915 | 0.995 | 0.581 |

grid200 + hurst (out-of-sample H, measured on jezero-20m)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9381 | 0.000 | 0.010 |
| 1 | 41 | 0.155 | 0.463 |
| 2 | 12 | 0.250 | 0.667 |
| 3 | 17 | 0.346 | 0.706 |
| 4 | 18 | 0.438 | 0.556 |
| 5 | 27 | 0.525 | 0.519 |
| 6 | 34 | 0.660 | 0.588 |
| 7 | 30 | 0.750 | 0.767 |
| 8 | 184 | 0.858 | 0.848 |
| 9 | 256 | 0.938 | 0.820 |

### Coverage and false reach against the confidence threshold

Roughness 0.5 for the multiplicative models. Each cell: coverage / false reach (calibrated cells).

| threshold | staircase (registered) | grid200 | grid200 + hurst (out-of-sample H, measured on jezero-20m) |
|---|---|---|---|
| 0.1 | 94.9 % / 41.6 % (926) | 100.0 % / 47.4 % (1084) | 82.8 % / 23.7 % (619) |
| 0.25 | 88.1 % / 34.3 % (764) | 100.0 % / 46.6 % (1068) | 79.5 % / 21.6 % (578) |
| 0.5 | 80.4 % / 29.8 % (652) | 100.0 % / 44.9 % (1035) | 74.2 % / 20.3 % (531) |
| 0.7 | 68.4 % / 28.0 % (542) | 99.1 % / 43.6 % (1001) | 68.2 % / 17.2 % (470) |
| 0.9 | 0.0 % / n/a (0) | 93.3 % / 41.9 % (915) | 36.8 % / 18.0 % (256) |
| 0.95 | 0.0 % / n/a (0) | 87.4 % / 40.4 % (836) | 0.0 % / n/a (0) |

## Tile: HiRISE Jezero DTM, 2 km window 2 (selected for steepness, passable habitat), degraded to 200 m planner

Tile id steep-p-2, cell 20 m.

No-skill Brier (always "never steep") for this tile: 0.05384. A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.

### staircase (registered)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.224 | 0.329 | 66.1 % | 62.8 % to 69.2 % | 39.7 % to 82.8 % | 3.0 % | 0.18690 | 0.05384 | -2.471 |
| 0.1 | 0.7 | 0.208 | 0.329 | 61.6 % | 58.2 % to 64.8 % | 35.5 % to 78.0 % | 2.9 % | 0.18690 | 0.05384 | -2.471 |
| 0.1 | 0.9 | 0.194 | 0.329 | 58.0 % | 54.6 % to 61.4 % | 32.1 % to 74.4 % | 1.8 % | 0.18690 | 0.05384 | -2.471 |
| 0.3 | 0.5 | 0.234 | 0.329 | 66.3 % | 63.0 % to 69.5 % | 42.4 % to 81.8 % | 6.7 % | 0.17598 | 0.05384 | -2.269 |
| 0.3 | 0.7 | 0.188 | 0.329 | 55.8 % | 52.4 % to 59.2 % | 33.8 % to 69.7 % | 2.5 % | 0.17598 | 0.05384 | -2.269 |
| 0.3 | 0.9 | 0.000 | 0.329 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | 0.17598 | 0.05384 | -2.269 |
| 0.5 | 0.5 | 0.250 | 0.329 | 69.2 % | 66.0 % to 72.3 % | 48.7 % to 82.3 % | 8.8 % | 0.16148 | 0.05384 | -1.999 |
| 0.5 | 0.7 | 0.187 | 0.329 | 54.4 % | 51.0 % to 57.8 % | 34.1 % to 68.0 % | 4.5 % | 0.16148 | 0.05384 | -1.999 |
| 0.5 | 0.9 | 0.000 | 0.329 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | 0.16148 | 0.05384 | -1.999 |

### grid200

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.317 | 0.329 | 92.0 % | 89.9 % to 93.6 % | 83.0 % to 97.7 % | 4.5 % | 0.04885 | 0.05384 | +0.093 |
| 0.1 | 0.7 | 0.314 | 0.329 | 91.1 % | 89.0 % to 92.9 % | 81.2 % to 97.3 % | 4.6 % | 0.04885 | 0.05384 | +0.093 |
| 0.1 | 0.9 | 0.310 | 0.329 | 90.3 % | 88.1 % to 92.1 % | 79.5 % to 97.0 % | 4.3 % | 0.04885 | 0.05384 | +0.093 |
| 0.3 | 0.5 | 0.325 | 0.329 | 93.4 % | 91.5 % to 94.9 % | 85.9 % to 98.2 % | 5.4 % | 0.06068 | 0.05384 | -0.127 |
| 0.3 | 0.7 | 0.315 | 0.329 | 91.4 % | 89.2 % to 93.1 % | 81.6 % to 97.4 % | 4.7 % | 0.06068 | 0.05384 | -0.127 |
| 0.3 | 0.9 | 0.300 | 0.329 | 87.5 % | 85.0 % to 89.6 % | 73.3 % to 96.0 % | 4.3 % | 0.06068 | 0.05384 | -0.127 |
| 0.5 | 0.5 | 0.331 | 0.329 | 94.7 % | 92.9 % to 96.0 % | 88.3 % to 98.5 % | 5.9 % | 0.07340 | 0.05384 | -0.363 |
| 0.5 | 0.7 | 0.311 | 0.329 | 90.1 % | 87.9 % to 92.0 % | 79.2 % to 96.7 % | 4.8 % | 0.07340 | 0.05384 | -0.363 |
| 0.5 | 0.9 | 0.279 | 0.329 | 82.1 % | 79.3 % to 84.6 % | 62.4 % to 94.1 % | 3.3 % | 0.07340 | 0.05384 | -0.363 |

### grid200 + hurst (out-of-sample H, measured on jezero-20m)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| n/a | 0.5 | 0.172 | 0.329 | 52.3 % | 48.9 % to 55.7 % | 21.8 % to 74.1 % | 0.0 % | 0.09256 | 0.05384 | -0.719 |
| n/a | 0.7 | 0.143 | 0.329 | 43.4 % | 40.1 % to 46.8 % | 13.9 % to 64.8 % | 0.0 % | 0.09256 | 0.05384 | -0.719 |
| n/a | 0.9 | 0.042 | 0.329 | 12.9 % | 10.8 % to 15.4 % | 3.0 % to 20.6 % | 0.0 % | 0.09256 | 0.05384 | -0.719 |

### Reliability of the reach probability

Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those cells reachable in the truth. Roughness 0.5 for the multiplicative models.

staircase (registered)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9082 | 0.001 | 0.006 |
| 1 | 140 | 0.149 | 0.479 |
| 2 | 36 | 0.250 | 0.806 |
| 3 | 75 | 0.340 | 0.813 |
| 4 | 43 | 0.438 | 0.884 |
| 5 | 64 | 0.523 | 0.797 |
| 6 | 92 | 0.660 | 0.772 |
| 7 | 468 | 0.750 | 0.955 |

grid200

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9113 | 0.000 | 0.002 |
| 1 | 28 | 0.154 | 0.571 |
| 2 | 6 | 0.250 | 0.500 |
| 3 | 16 | 0.332 | 0.500 |
| 4 | 10 | 0.438 | 0.300 |
| 5 | 19 | 0.543 | 0.737 |
| 6 | 30 | 0.662 | 0.767 |
| 7 | 18 | 0.750 | 0.778 |
| 8 | 62 | 0.846 | 0.839 |
| 9 | 698 | 0.995 | 0.967 |

grid200 + hurst (out-of-sample H, measured on jezero-20m)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9456 | 0.000 | 0.029 |
| 1 | 47 | 0.154 | 1.000 |
| 2 | 17 | 0.250 | 1.000 |
| 3 | 35 | 0.345 | 1.000 |
| 4 | 15 | 0.438 | 1.000 |
| 5 | 28 | 0.545 | 1.000 |
| 6 | 45 | 0.660 | 1.000 |
| 7 | 42 | 0.750 | 1.000 |
| 8 | 209 | 0.851 | 1.000 |
| 9 | 106 | 0.938 | 1.000 |

### Coverage and false reach against the confidence threshold

Roughness 0.5 for the multiplicative models. Each cell: coverage / false reach (calibrated cells).

| threshold | staircase (registered) | grid200 | grid200 + hurst (out-of-sample H, measured on jezero-20m) |
|---|---|---|---|
| 0.1 | 92.9 % / 16.8 % (918) | 98.3 % / 8.9 % (887) | 66.2 % / 0.0 % (544) |
| 0.25 | 84.8 % / 10.4 % (778) | 96.4 % / 7.8 % (859) | 60.5 % / 0.0 % (497) |
| 0.5 | 69.2 % / 8.8 % (624) | 94.6 % / 5.9 % (827) | 52.3 % / 0.0 % (430) |
| 0.7 | 54.4 % / 4.5 % (468) | 90.1 % / 4.8 % (778) | 43.4 % / 0.0 % (357) |
| 0.9 | 0.0 % / n/a (0) | 82.1 % / 3.3 % (698) | 12.9 % / 0.0 % (106) |
| 0.95 | 0.0 % / n/a (0) | 75.5 % / 2.7 % (638) | 0.0 % / n/a (0) |

## Tile: HiRISE Jezero DTM, 2 km window 3 (selected for steepness, passable habitat), degraded to 200 m planner

Tile id steep-p-3, cell 20 m.

No-skill Brier (always "never steep") for this tile: 0.05242. A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.

### staircase (registered)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.309 | 0.308 | 91.0 % | 88.8 % to 92.8 % | 79.7 % to 97.4 % | 9.4 % | 0.10670 | 0.05242 | -1.036 |
| 0.1 | 0.7 | 0.302 | 0.308 | 89.3 % | 87.0 % to 91.3 % | 74.7 % to 97.1 % | 8.9 % | 0.10670 | 0.05242 | -1.036 |
| 0.1 | 0.9 | 0.296 | 0.308 | 88.3 % | 85.8 % to 90.4 % | 73.7 % to 96.4 % | 8.1 % | 0.10670 | 0.05242 | -1.036 |
| 0.3 | 0.5 | 0.322 | 0.308 | 92.8 % | 90.8 % to 94.5 % | 84.3 % to 98.2 % | 11.3 % | 0.09679 | 0.05242 | -0.846 |
| 0.3 | 0.7 | 0.298 | 0.308 | 88.6 % | 86.1 % to 90.6 % | 76.1 % to 96.0 % | 8.6 % | 0.09679 | 0.05242 | -0.846 |
| 0.3 | 0.9 | 0.268 | 0.308 | 81.0 % | 78.1 % to 83.6 % | 66.7 % to 90.0 % | 7.0 % | 0.09679 | 0.05242 | -0.846 |
| 0.5 | 0.5 | 0.322 | 0.308 | 91.9 % | 89.8 % to 93.7 % | 83.2 % to 97.3 % | 12.3 % | 0.09052 | 0.05242 | -0.727 |
| 0.5 | 0.7 | 0.262 | 0.308 | 77.1 % | 74.0 % to 79.9 % | 67.1 % to 84.1 % | 9.6 % | 0.09052 | 0.05242 | -0.727 |
| 0.5 | 0.9 | 0.000 | 0.308 | 0.0 % | 0.0 % to 0.5 % | 0.0 % to 0.0 % | n/a | 0.09052 | 0.05242 | -0.727 |

### grid200

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.410 | 0.308 | 98.8 % | 97.8 % to 99.4 % | 97.1 % to 100.0 % | 25.8 % | 0.05550 | 0.05242 | -0.059 |
| 0.1 | 0.7 | 0.406 | 0.308 | 98.4 % | 97.3 % to 99.1 % | 96.4 % to 99.8 % | 25.5 % | 0.05550 | 0.05242 | -0.059 |
| 0.1 | 0.9 | 0.404 | 0.308 | 98.2 % | 97.0 % to 98.9 % | 96.0 % to 99.6 % | 25.3 % | 0.05550 | 0.05242 | -0.059 |
| 0.3 | 0.5 | 0.414 | 0.308 | 99.1 % | 98.1 % to 99.6 % | 97.4 % to 100.0 % | 26.5 % | 0.05474 | 0.05242 | -0.044 |
| 0.3 | 0.7 | 0.409 | 0.308 | 98.3 % | 97.1 % to 99.0 % | 96.4 % to 99.6 % | 26.0 % | 0.05474 | 0.05242 | -0.044 |
| 0.3 | 0.9 | 0.399 | 0.308 | 97.5 % | 96.2 % to 98.4 % | 94.8 % to 99.4 % | 24.8 % | 0.05474 | 0.05242 | -0.044 |
| 0.5 | 0.5 | 0.419 | 0.308 | 99.0 % | 98.0 % to 99.5 % | 97.2 % to 100.0 % | 27.4 % | 0.05224 | 0.05242 | +0.003 |
| 0.5 | 0.7 | 0.406 | 0.308 | 97.9 % | 96.6 % to 98.7 % | 95.4 % to 99.6 % | 25.9 % | 0.05224 | 0.05242 | +0.003 |
| 0.5 | 0.9 | 0.392 | 0.308 | 96.8 % | 95.2 % to 97.8 % | 93.3 % to 99.2 % | 24.2 % | 0.05224 | 0.05242 | +0.003 |

### grid200 + hurst (out-of-sample H, measured on jezero-20m)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| n/a | 0.5 | 0.348 | 0.308 | 89.1 % | 86.7 % to 91.1 % | 80.0 % to 96.0 % | 21.2 % | 0.05546 | 0.05242 | -0.058 |
| n/a | 0.7 | 0.336 | 0.308 | 87.3 % | 84.7 % to 89.4 % | 77.0 % to 94.7 % | 20.2 % | 0.05546 | 0.05242 | -0.058 |
| n/a | 0.9 | 0.321 | 0.308 | 84.9 % | 82.2 % to 87.3 % | 73.6 % to 93.5 % | 18.7 % | 0.05546 | 0.05242 | -0.058 |

### Reliability of the reach probability

Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those cells reachable in the truth. Roughness 0.5 for the multiplicative models.

staircase (registered)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9022 | 0.000 | 0.002 |
| 1 | 120 | 0.142 | 0.117 |
| 2 | 9 | 0.250 | 0.556 |
| 3 | 26 | 0.349 | 0.538 |
| 4 | 17 | 0.438 | 0.471 |
| 5 | 50 | 0.532 | 0.760 |
| 6 | 100 | 0.662 | 0.760 |
| 7 | 656 | 0.750 | 0.904 |

grid200

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 8909 | 0.000 | 0.000 |
| 1 | 22 | 0.151 | 0.045 |
| 2 | 6 | 0.250 | 0.000 |
| 3 | 10 | 0.338 | 0.200 |
| 4 | 5 | 0.438 | 0.200 |
| 5 | 16 | 0.543 | 0.125 |
| 6 | 16 | 0.660 | 0.375 |
| 7 | 8 | 0.750 | 0.125 |
| 8 | 27 | 0.850 | 0.296 |
| 9 | 981 | 0.996 | 0.758 |

grid200 + hurst (out-of-sample H, measured on jezero-20m)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9071 | 0.000 | 0.006 |
| 1 | 24 | 0.156 | 0.500 |
| 2 | 7 | 0.250 | 0.429 |
| 3 | 23 | 0.342 | 0.522 |
| 4 | 6 | 0.438 | 0.500 |
| 5 | 12 | 0.531 | 0.583 |
| 6 | 16 | 0.664 | 0.438 |
| 7 | 10 | 0.750 | 0.600 |
| 8 | 28 | 0.850 | 0.429 |
| 9 | 803 | 0.998 | 0.813 |

### Coverage and false reach against the confidence threshold

Roughness 0.5 for the multiplicative models. Each cell: coverage / false reach (calibrated cells).

| threshold | staircase (registered) | grid200 | grid200 + hurst (out-of-sample H, measured on jezero-20m) |
|---|---|---|---|
| 0.1 | 97.3 % / 23.5 % (978) | 99.5 % / 29.9 % (1091) | 93.0 % / 23.0 % (929) |
| 0.25 | 95.4 % / 14.5 % (858) | 99.3 % / 28.5 % (1069) | 91.4 % / 22.3 % (905) |
| 0.5 | 91.9 % / 12.3 % (806) | 99.0 % / 27.4 % (1048) | 89.1 % / 21.2 % (869) |
| 0.7 | 77.1 % / 9.6 % (656) | 97.9 % / 25.9 % (1016) | 87.3 % / 20.2 % (841) |
| 0.9 | 0.0 % / n/a (0) | 96.7 % / 24.2 % (981) | 84.9 % / 18.7 % (803) |
| 0.95 | 0.0 % / n/a (0) | 91.5 % / 23.5 % (920) | 83.1 % / 17.7 % (776) |

How to read it:

- Coverage = share of truth-reachable cells that the calibrated region contains. False reach = share of calibrated cells that the truth says are not reachable. Coverage is never read without false reach.
- Wilson treats cells as independent. The block bootstrap resamples 200 m blocks and keeps cells inside a block together.
- The Gaussian sub-grid noise of the hurst model is thin-tailed, the truth is not. Read the Brier skill score and the steep-cell results with that in mind.
- Speeds, cutoff and roughness are assumptions. Each tile is one 2 km window of one terrain class.
