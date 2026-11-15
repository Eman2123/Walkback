# Extended validation (exploratory, registered before it was run)

This is not the validation result. The pre-registered headline in validation_report.md is unchanged.
Registered in PREREGISTRATION.md, section "Extended validation and sub-grid roughness".

Fixed: habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20.0 deg (assumed), 16 realizations, seed 1234.

The hurst model uses H = 0.853, read from reports\scale_effect.md. That value was measured on the 2 km window of tile jezero-20m: the hurst rows of that tile are IN-SAMPLE, the hurst rows of every other tile are out-of-sample (a different window of the same DTM, same site). One value of H from one window is a thin basis; no claim about other terrain is made.

All rows of all three models are reported. No row is chosen as the result. When one interval is needed, quote the wider of the Wilson and the block-bootstrap interval. If no row reaches 95 % coverage, that is a shortfall.

## Tile: Mars 2020 TRN HiRISE DTM (USGS, DOI 10.5066/P9REJ9JN), 2 km window, degraded to 200 m planner

Tile id jezero-20m, cell 20 m.

No-skill Brier (always "never steep") for this tile: 0.00200. A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.

### staircase (registered)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.450 | 0.422 | 97.7 % | 96.6 % to 98.5 % | 95.2 % to 99.4 % | 8.4 % | 0.01682 | 0.00200 | -7.429 |
| 0.1 | 0.7 | 0.444 | 0.422 | 97.2 % | 96.0 % to 98.0 % | 93.9 % to 99.2 % | 7.8 % | 0.01682 | 0.00200 | -7.429 |
| 0.1 | 0.9 | 0.433 | 0.422 | 95.8 % | 94.4 % to 96.9 % | 91.4 % to 98.7 % | 6.7 % | 0.01682 | 0.00200 | -7.429 |
| 0.3 | 0.5 | 0.462 | 0.422 | 98.6 % | 97.7 % to 99.1 % | 96.7 % to 99.7 % | 10.0 % | 0.01386 | 0.00200 | -5.945 |
| 0.3 | 0.7 | 0.441 | 0.422 | 96.6 % | 95.3 % to 97.5 % | 93.1 % to 98.9 % | 7.7 % | 0.01386 | 0.00200 | -5.945 |
| 0.3 | 0.9 | 0.396 | 0.422 | 88.5 % | 86.5 % to 90.3 % | 81.7 % to 93.3 % | 5.9 % | 0.01386 | 0.00200 | -5.945 |
| 0.5 | 0.5 | 0.469 | 0.422 | 98.6 % | 97.7 % to 99.1 % | 97.0 % to 99.6 % | 11.3 % | 0.01567 | 0.00200 | -6.853 |
| 0.5 | 0.7 | 0.415 | 0.422 | 90.9 % | 89.0 % to 92.5 % | 86.5 % to 94.1 % | 7.6 % | 0.01567 | 0.00200 | -6.853 |
| 0.5 | 0.9 | 0.000 | 0.422 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | 0.01567 | 0.00200 | -6.853 |

### grid200

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.467 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 9.8 % | 0.00200 | 0.00200 | -0.002 |
| 0.1 | 0.7 | 0.466 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 9.6 % | 0.00200 | 0.00200 | -0.002 |
| 0.1 | 0.9 | 0.465 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 9.4 % | 0.00200 | 0.00200 | -0.002 |
| 0.3 | 0.5 | 0.472 | 0.422 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 10.7 % | 0.00200 | 0.00200 | -0.002 |
| 0.3 | 0.7 | 0.469 | 0.422 | 99.9 % | 99.5 % to 100.0 % | 99.6 % to 100.0 % | 10.2 % | 0.00200 | 0.00200 | -0.002 |
| 0.3 | 0.9 | 0.466 | 0.422 | 99.8 % | 99.3 % to 99.9 % | 99.4 % to 100.0 % | 9.7 % | 0.00200 | 0.00200 | -0.002 |
| 0.5 | 0.5 | 0.474 | 0.422 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 11.1 % | 0.00201 | 0.00200 | -0.007 |
| 0.5 | 0.7 | 0.470 | 0.422 | 100.0 % | 99.6 % to 100.0 % | 100.0 % to 100.0 % | 10.3 % | 0.00201 | 0.00200 | -0.007 |
| 0.5 | 0.9 | 0.461 | 0.422 | 99.7 % | 99.2 % to 99.9 % | 99.1 % to 100.0 % | 8.8 % | 0.00201 | 0.00200 | -0.007 |

### grid200 + hurst (in-sample H)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| n/a | 0.5 | 0.446 | 0.422 | 98.2 % | 97.2 % to 98.8 % | 96.4 % to 99.6 % | 7.2 % | 0.00200 | 0.00200 | -0.002 |
| n/a | 0.7 | 0.441 | 0.422 | 97.9 % | 96.9 % to 98.6 % | 95.9 % to 99.5 % | 6.4 % | 0.00200 | 0.00200 | -0.002 |
| n/a | 0.9 | 0.433 | 0.422 | 96.7 % | 95.4 % to 97.6 % | 93.8 % to 98.7 % | 5.8 % | 0.00200 | 0.00200 | -0.002 |

### Reliability of the reach probability

Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those cells reachable in the truth. Roughness 0.5 for the multiplicative models.

staircase (registered)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 8757 | 0.000 | 0.000 |
| 1 | 31 | 0.159 | 0.161 |
| 2 | 13 | 0.250 | 0.077 |
| 3 | 15 | 0.333 | 0.200 |
| 4 | 12 | 0.438 | 0.500 |
| 5 | 48 | 0.535 | 0.583 |
| 6 | 87 | 0.657 | 0.609 |
| 7 | 56 | 0.750 | 0.625 |
| 8 | 981 | 0.868 | 0.941 |

grid200

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 8783 | 0.000 | 0.000 |
| 1 | 15 | 0.142 | 0.000 |
| 2 | 6 | 0.250 | 0.000 |
| 3 | 8 | 0.344 | 0.000 |
| 4 | 2 | 0.438 | 0.000 |
| 5 | 8 | 0.523 | 0.000 |
| 6 | 3 | 0.667 | 0.000 |
| 7 | 5 | 0.750 | 0.400 |
| 8 | 17 | 0.831 | 0.059 |
| 9 | 1153 | 1.000 | 0.912 |

grid200 + hurst (in-sample H)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 8847 | 0.000 | 0.001 |
| 1 | 14 | 0.156 | 0.071 |
| 2 | 5 | 0.250 | 0.200 |
| 3 | 15 | 0.350 | 0.333 |
| 4 | 4 | 0.438 | 0.500 |
| 5 | 7 | 0.536 | 0.286 |
| 6 | 5 | 0.637 | 0.200 |
| 7 | 6 | 0.750 | 0.500 |
| 8 | 15 | 0.858 | 0.667 |
| 9 | 1082 | 0.999 | 0.942 |

### Coverage and false reach against the confidence threshold

Roughness 0.5 for the multiplicative models. Each cell: coverage / false reach (calibrated cells).

| threshold | staircase (registered) | grid200 | grid200 + hurst (in-sample H) |
|---|---|---|---|
| 0.1 | 100.0 % / 15.2 % (1243) | 100.0 % / 13.4 % (1217) | 99.1 % / 9.5 % (1153) |
| 0.25 | 99.5 % / 13.4 % (1212) | 100.0 % / 12.3 % (1202) | 99.0 % / 8.4 % (1139) |
| 0.5 | 98.6 % / 11.3 % (1172) | 100.0 % / 11.1 % (1186) | 98.2 % / 7.2 % (1115) |
| 0.7 | 90.9 % / 7.6 % (1037) | 100.0 % / 10.3 % (1175) | 97.9 % / 6.4 % (1103) |
| 0.9 | 0.0 % / n/a (0) | 99.7 % / 8.8 % (1153) | 96.7 % / 5.8 % (1082) |
| 0.95 | 0.0 % / n/a (0) | 99.5 % / 8.4 % (1145) | 96.2 % / 5.1 % (1068) |

## Tile: HiRISE Jezero DTM, 2 km window 1 (selected for steepness), degraded to 200 m planner

Tile id steep-1, cell 20 m.

No-skill Brier (always "never steep") for this tile: 0.22327. A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.

### staircase (registered)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | not computed | | | | | | | | |
| 0.1 | 0.7 | not computed | | | | | | | | |
| 0.1 | 0.9 | not computed | | | | | | | | |
| 0.3 | 0.5 | not computed | | | | | | | | |
| 0.3 | 0.7 | not computed | | | | | | | | |
| 0.3 | 0.9 | not computed | | | | | | | | |
| 0.5 | 0.5 | not computed | | | | | | | | |
| 0.5 | 0.7 | not computed | | | | | | | | |
| 0.5 | 0.9 | not computed | | | | | | | | |

- not computed, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution

### grid200

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.070 | 0.054 | 86.0 % | 79.2 % to 90.9 % | 64.3 % to 98.6 % | 33.1 % | 0.12085 | 0.22327 | +0.459 |
| 0.1 | 0.7 | 0.063 | 0.054 | 84.6 % | 77.5 % to 89.7 % | 59.5 % to 98.6 % | 27.2 % | 0.12085 | 0.22327 | +0.459 |
| 0.1 | 0.9 | 0.057 | 0.054 | 80.9 % | 73.5 % to 86.6 % | 57.1 % to 94.3 % | 23.1 % | 0.12085 | 0.22327 | +0.459 |
| 0.3 | 0.5 | 0.079 | 0.054 | 91.2 % | 85.2 % to 94.9 % | 76.2 % to 100.0 % | 37.4 % | 0.13260 | 0.22327 | +0.406 |
| 0.3 | 0.7 | 0.061 | 0.054 | 80.2 % | 72.7 % to 86.0 % | 45.2 % to 98.6 % | 28.8 % | 0.13260 | 0.22327 | +0.406 |
| 0.3 | 0.9 | 0.018 | 0.054 | 27.2 % | 20.4 % to 35.2 % | 2.4 % to 38.6 % | 15.9 % | 0.13260 | 0.22327 | +0.406 |
| 0.5 | 0.5 | 0.077 | 0.054 | 88.2 % | 81.7 % to 92.6 % | 66.7 % to 98.6 % | 37.8 % | 0.14815 | 0.22327 | +0.336 |
| 0.5 | 0.7 | 0.008 | 0.054 | 11.8 % | 7.4 % to 18.3 % | 0.0 % to 17.1 % | 15.8 % | 0.14815 | 0.22327 | +0.336 |
| 0.5 | 0.9 | 0.000 | 0.054 | 0.0 % | 0.0 % to 2.7 % | 0.0 % to 0.0 % | n/a | 0.14815 | 0.22327 | +0.336 |

### grid200 + hurst (out-of-sample H, measured on jezero-20m)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| n/a | 0.5 | 0.000 | 0.054 | 0.0 % | 0.0 % to 2.7 % | 0.0 % to 0.0 % | n/a | 0.19127 | 0.22327 | +0.143 |
| n/a | 0.7 | 0.000 | 0.054 | 0.0 % | 0.0 % to 2.7 % | 0.0 % to 0.0 % | n/a | 0.19127 | 0.22327 | +0.143 |
| n/a | 0.9 | 0.000 | 0.054 | 0.0 % | 0.0 % to 2.7 % | 0.0 % to 0.0 % | n/a | 0.19127 | 0.22327 | +0.143 |

### Reliability of the reach probability

Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those cells reachable in the truth. Roughness 0.5 for the multiplicative models.

grid200

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9660 | 0.000 | 0.000 |
| 1 | 55 | 0.153 | 0.036 |
| 2 | 22 | 0.250 | 0.091 |
| 3 | 44 | 0.347 | 0.136 |
| 4 | 26 | 0.438 | 0.231 |
| 5 | 77 | 0.537 | 0.584 |
| 6 | 97 | 0.656 | 0.608 |
| 7 | 19 | 0.750 | 0.842 |

grid200 + hurst (out-of-sample H, measured on jezero-20m)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9848 | 0.000 | 0.004 |
| 1 | 98 | 0.152 | 0.582 |
| 2 | 34 | 0.250 | 0.735 |
| 3 | 20 | 0.334 | 0.900 |

### Coverage and false reach against the confidence threshold

Roughness 0.5 for the multiplicative models. Each cell: coverage / false reach (calibrated cells).

| threshold | grid200 | grid200 + hurst (out-of-sample H, measured on jezero-20m) |
|---|---|---|
| 0.1 | 100.0 % / 60.0 % (340) | 73.5 % / 34.2 % (152) |
| 0.25 | 98.5 % / 53.0 % (285) | 31.6 % / 20.4 % (54) |
| 0.5 | 88.2 % / 37.8 % (193) | 0.0 % / n/a (0) |
| 0.7 | 11.8 % / 15.8 % (19) | 0.0 % / n/a (0) |
| 0.9 | 0.0 % / n/a (0) | 0.0 % / n/a (0) |
| 0.95 | 0.0 % / n/a (0) | 0.0 % / n/a (0) |

## Tile: HiRISE Jezero DTM, 2 km window 2 (selected for steepness), degraded to 200 m planner

Tile id steep-2, cell 20 m.

No-skill Brier (always "never steep") for this tile: 0.22004. A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.

### staircase (registered)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | not computed | | | | | | | | |
| 0.1 | 0.7 | not computed | | | | | | | | |
| 0.1 | 0.9 | not computed | | | | | | | | |
| 0.3 | 0.5 | not computed | | | | | | | | |
| 0.3 | 0.7 | not computed | | | | | | | | |
| 0.3 | 0.9 | not computed | | | | | | | | |
| 0.5 | 0.5 | not computed | | | | | | | | |
| 0.5 | 0.7 | not computed | | | | | | | | |
| 0.5 | 0.9 | not computed | | | | | | | | |

- not computed, roughness 0.1, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.1, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.1, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.3, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.3, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.3, confidence 0.9: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.5, confidence 0.5: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.5, confidence 0.7: habitat is impassable at coarse or fine resolution
- not computed, roughness 0.5, confidence 0.9: habitat is impassable at coarse or fine resolution

### grid200

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.202 | 0.095 | 99.2 % | 97.0 % to 99.8 % | 93.8 % to 100.0 % | 53.2 % | 0.13078 | 0.22004 | +0.406 |
| 0.1 | 0.7 | 0.194 | 0.095 | 98.3 % | 95.8 % to 99.3 % | 87.5 % to 100.0 % | 51.7 % | 0.13078 | 0.22004 | +0.406 |
| 0.1 | 0.9 | 0.188 | 0.095 | 97.5 % | 94.6 % to 98.8 % | 81.2 % to 100.0 % | 50.5 % | 0.13078 | 0.22004 | +0.406 |
| 0.3 | 0.5 | 0.213 | 0.095 | 98.7 % | 96.4 % to 99.6 % | 90.6 % to 100.0 % | 55.8 % | 0.13200 | 0.22004 | +0.400 |
| 0.3 | 0.7 | 0.190 | 0.095 | 95.8 % | 92.4 % to 97.7 % | 71.5 % to 100.0 % | 51.9 % | 0.13200 | 0.22004 | +0.400 |
| 0.3 | 0.9 | 0.159 | 0.095 | 84.9 % | 79.8 % to 88.9 % | 35.7 % to 100.0 % | 49.1 % | 0.13200 | 0.22004 | +0.400 |
| 0.5 | 0.5 | 0.221 | 0.095 | 98.3 % | 95.8 % to 99.3 % | 87.5 % to 100.0 % | 57.7 % | 0.14065 | 0.22004 | +0.361 |
| 0.5 | 0.7 | 0.176 | 0.095 | 89.9 % | 85.4 % to 93.1 % | 52.6 % to 100.0 % | 51.5 % | 0.14065 | 0.22004 | +0.361 |
| 0.5 | 0.9 | 0.132 | 0.095 | 73.1 % | 67.1 % to 78.3 % | 17.4 % to 99.0 % | 47.3 % | 0.14065 | 0.22004 | +0.361 |

### grid200 + hurst (out-of-sample H, measured on jezero-20m)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| n/a | 0.5 | 0.063 | 0.095 | 62.6 % | 56.3 % to 68.5 % | 9.6 % to 77.6 % | 5.7 % | 0.16909 | 0.22004 | +0.232 |
| n/a | 0.7 | 0.008 | 0.095 | 8.8 % | 5.8 % to 13.1 % | 0.0 % to 13.2 % | 0.0 % | 0.16909 | 0.22004 | +0.232 |
| n/a | 0.9 | 0.000 | 0.095 | 0.0 % | 0.0 % to 1.6 % | 0.0 % to 0.0 % | n/a | 0.16909 | 0.22004 | +0.232 |

### Reliability of the reach probability

Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those cells reachable in the truth. Roughness 0.5 for the multiplicative models.

grid200

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9337 | 0.000 | 0.000 |
| 1 | 36 | 0.156 | 0.000 |
| 2 | 17 | 0.250 | 0.059 |
| 3 | 39 | 0.348 | 0.051 |
| 4 | 18 | 0.438 | 0.056 |
| 5 | 41 | 0.535 | 0.171 |
| 6 | 71 | 0.658 | 0.183 |
| 7 | 39 | 0.750 | 0.359 |
| 8 | 72 | 0.846 | 0.361 |
| 9 | 330 | 0.991 | 0.527 |

grid200 + hurst (out-of-sample H, measured on jezero-20m)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9677 | 0.000 | 0.001 |
| 1 | 61 | 0.150 | 0.164 |
| 2 | 22 | 0.250 | 0.409 |
| 3 | 55 | 0.345 | 0.655 |
| 4 | 27 | 0.438 | 0.741 |
| 5 | 63 | 0.525 | 0.889 |
| 6 | 74 | 0.655 | 0.973 |
| 7 | 15 | 0.750 | 1.000 |
| 8 | 6 | 0.812 | 1.000 |

### Coverage and false reach against the confidence threshold

Roughness 0.5 for the multiplicative models. Each cell: coverage / false reach (calibrated cells).

| threshold | grid200 | grid200 + hurst (out-of-sample H, measured on jezero-20m) |
|---|---|---|
| 0.1 | 100.0 % / 64.1 % (663) | 94.1 % / 30.7 % (323) |
| 0.25 | 100.0 % / 62.0 % (627) | 89.9 % / 18.3 % (262) |
| 0.5 | 98.3 % / 57.7 % (553) | 62.6 % / 5.7 % (158) |
| 0.7 | 89.9 % / 51.5 % (441) | 8.8 % / 0.0 % (21) |
| 0.9 | 73.1 % / 47.3 % (330) | 0.0 % / n/a (0) |
| 0.95 | 65.5 % / 44.7 % (282) | 0.0 % / n/a (0) |

## Tile: HiRISE Jezero DTM, 2 km window 3 (selected for steepness), degraded to 200 m planner

Tile id steep-3, cell 20 m.

No-skill Brier (always "never steep") for this tile: 0.14097. A Brier skill score at or below 0 means no skill. Brier values here are computed from the unrounded probabilities.

### staircase (registered)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.227 | 0.353 | 62.2 % | 58.9 % to 65.3 % | 38.6 % to 78.3 % | 3.2 % | 0.27423 | 0.14097 | -0.945 |
| 0.1 | 0.7 | 0.208 | 0.353 | 57.2 % | 53.9 % to 60.4 % | 32.2 % to 75.4 % | 3.1 % | 0.27423 | 0.14097 | -0.945 |
| 0.1 | 0.9 | 0.178 | 0.353 | 48.8 % | 45.5 % to 52.1 % | 22.1 % to 69.5 % | 3.4 % | 0.27423 | 0.14097 | -0.945 |
| 0.3 | 0.5 | 0.241 | 0.353 | 66.1 % | 63.0 % to 69.2 % | 43.4 % to 80.6 % | 3.1 % | 0.25973 | 0.14097 | -0.842 |
| 0.3 | 0.7 | 0.188 | 0.353 | 51.8 % | 48.5 % to 55.0 % | 29.4 % to 68.3 % | 3.0 % | 0.25973 | 0.14097 | -0.842 |
| 0.3 | 0.9 | 0.000 | 0.353 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | 0.25973 | 0.14097 | -0.842 |
| 0.5 | 0.5 | 0.257 | 0.353 | 70.5 % | 67.5 % to 73.5 % | 51.8 % to 82.4 % | 3.1 % | 0.24479 | 0.14097 | -0.736 |
| 0.5 | 0.7 | 0.180 | 0.353 | 49.6 % | 46.3 % to 52.9 % | 28.7 % to 64.5 % | 2.7 % | 0.24479 | 0.14097 | -0.736 |
| 0.5 | 0.9 | 0.000 | 0.353 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | 0.24479 | 0.14097 | -0.736 |

### grid200

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.340 | 0.353 | 94.3 % | 92.6 % to 95.7 % | 88.2 % to 98.0 % | 2.0 % | 0.11419 | 0.14097 | +0.190 |
| 0.1 | 0.7 | 0.337 | 0.353 | 93.9 % | 92.1 % to 95.3 % | 87.3 % to 97.9 % | 1.7 % | 0.11419 | 0.14097 | +0.190 |
| 0.1 | 0.9 | 0.334 | 0.353 | 93.3 % | 91.5 % to 94.8 % | 86.3 % to 97.7 % | 1.4 % | 0.11419 | 0.14097 | +0.190 |
| 0.3 | 0.5 | 0.345 | 0.353 | 95.8 % | 94.3 % to 96.9 % | 91.4 % to 98.6 % | 2.0 % | 0.10510 | 0.14097 | +0.254 |
| 0.3 | 0.7 | 0.337 | 0.353 | 93.8 % | 92.0 % to 95.2 % | 86.9 % to 97.9 % | 1.8 % | 0.10510 | 0.14097 | +0.254 |
| 0.3 | 0.9 | 0.323 | 0.353 | 90.4 % | 88.2 % to 92.1 % | 79.9 % to 96.9 % | 1.1 % | 0.10510 | 0.14097 | +0.254 |
| 0.5 | 0.5 | 0.348 | 0.353 | 96.5 % | 95.1 % to 97.5 % | 92.7 % to 98.9 % | 2.2 % | 0.11067 | 0.14097 | +0.215 |
| 0.5 | 0.7 | 0.330 | 0.353 | 92.4 % | 90.5 % to 94.0 % | 84.1 % to 97.5 % | 1.2 % | 0.11067 | 0.14097 | +0.215 |
| 0.5 | 0.9 | 0.300 | 0.353 | 84.4 % | 81.8 % to 86.6 % | 68.4 % to 94.2 % | 0.8 % | 0.11067 | 0.14097 | +0.215 |

### grid200 + hurst (out-of-sample H, measured on jezero-20m)

| roughness | confidence | calibrated km2 | truth km2 | coverage | Wilson 95 % | block bootstrap 95 % | false reach | Brier | no-skill Brier | Brier skill score |
|---|---|---|---|---|---|---|---|---|---|---|
| n/a | 0.5 | 0.157 | 0.353 | 44.5 % | 41.3 % to 47.8 % | 16.2 % to 67.0 % | 0.0 % | 0.12566 | 0.14097 | +0.109 |
| n/a | 0.7 | 0.105 | 0.353 | 29.8 % | 26.9 % to 32.9 % | 7.7 % to 47.7 % | 0.0 % | 0.12566 | 0.14097 | +0.109 |
| n/a | 0.9 | 0.000 | 0.353 | 0.0 % | 0.0 % to 0.4 % | 0.0 % to 0.0 % | n/a | 0.12566 | 0.14097 | +0.109 |

### Reliability of the reach probability

Predicted = mean share of the 16 realizations in which a cell is reachable. Observed = share of those cells reachable in the truth. Roughness 0.5 for the multiplicative models.

staircase (registered)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9106 | 0.001 | 0.008 |
| 1 | 135 | 0.156 | 0.615 |
| 2 | 29 | 0.250 | 0.759 |
| 3 | 56 | 0.342 | 0.911 |
| 4 | 31 | 0.438 | 0.968 |
| 5 | 87 | 0.534 | 0.989 |
| 6 | 106 | 0.658 | 0.934 |
| 7 | 450 | 0.750 | 0.973 |

grid200

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9071 | 0.000 | 0.001 |
| 1 | 27 | 0.153 | 0.370 |
| 2 | 9 | 0.250 | 0.000 |
| 3 | 11 | 0.347 | 0.636 |
| 4 | 11 | 0.438 | 0.727 |
| 5 | 17 | 0.548 | 0.882 |
| 6 | 28 | 0.661 | 0.750 |
| 7 | 13 | 0.750 | 1.000 |
| 8 | 62 | 0.856 | 0.935 |
| 9 | 751 | 0.994 | 0.992 |

grid200 + hurst (out-of-sample H, measured on jezero-20m)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 9490 | 0.000 | 0.039 |
| 1 | 50 | 0.152 | 1.000 |
| 2 | 20 | 0.250 | 1.000 |
| 3 | 29 | 0.345 | 1.000 |
| 4 | 18 | 0.438 | 1.000 |
| 5 | 37 | 0.529 | 1.000 |
| 6 | 93 | 0.658 | 1.000 |
| 7 | 93 | 0.750 | 1.000 |
| 8 | 170 | 0.838 | 1.000 |

### Coverage and false reach against the confidence threshold

Roughness 0.5 for the multiplicative models. Each cell: coverage / false reach (calibrated cells).

| threshold | staircase (registered) | grid200 | grid200 + hurst (out-of-sample H, measured on jezero-20m) |
|---|---|---|---|
| 0.1 | 91.6 % / 9.5 % (894) | 99.3 % / 5.6 % (929) | 57.8 % / 0.0 % (510) |
| 0.25 | 82.2 % / 4.3 % (759) | 98.2 % / 3.9 % (902) | 52.1 % / 0.0 % (460) |
| 0.5 | 70.6 % / 3.1 % (643) | 96.5 % / 2.2 % (871) | 44.5 % / 0.0 % (393) |
| 0.7 | 49.6 % / 2.7 % (450) | 92.4 % / 1.2 % (826) | 29.8 % / 0.0 % (263) |
| 0.9 | 0.0 % / n/a (0) | 84.4 % / 0.8 % (751) | 0.0 % / n/a (0) |
| 0.95 | 0.0 % / n/a (0) | 75.9 % / 0.7 % (675) | 0.0 % / n/a (0) |

How to read it:

- Coverage = share of truth-reachable cells that the calibrated region contains. False reach = share of calibrated cells that the truth says are not reachable. Coverage is never read without false reach.
- Wilson treats cells as independent. The block bootstrap resamples 200 m blocks and keeps cells inside a block together.
- The Gaussian sub-grid noise of the hurst model is thin-tailed, the truth is not. Read the Brier skill score and the steep-cell results with that in mind.
- Speeds, cutoff and roughness are assumptions. Each tile is one 2 km window of one terrain class.
