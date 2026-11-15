# Extended validation (exploratory, registered before it was run)

This is not the validation result. The pre-registered headline in validation_report.md is unchanged.
Registered in PREREGISTRATION.md, section "Extended validation and sub-grid roughness".

Fixed: habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20.0 deg (assumed), 16 realizations, seed 1234.

The hurst model uses H = 0.853, read from reports/scale_effect.md. That value was measured on the same 2 km window that is validated here, so every hurst row is IN-SAMPLE. No out-of-sample claim is made.

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

How to read it:

- Coverage = share of truth-reachable cells that the calibrated region contains. False reach = share of calibrated cells that the truth says are not reachable. Coverage is never read without false reach.
- Wilson treats cells as independent. The block bootstrap resamples 200 m blocks and keeps cells inside a block together.
- The Gaussian sub-grid noise of the hurst model is thin-tailed, the truth is not. Read the Brier skill score and the steep-cell results with that in mind.
- Speeds, cutoff and roughness are assumptions. Each tile is one 2 km window of one terrain class.
