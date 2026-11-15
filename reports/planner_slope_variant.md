# Planner-slope variant (exploratory, registered before it was run)

This is not the validation result. The pre-registered headline in validation_report.md is unchanged.

Tile: Mars 2020 TRN HiRISE DTM (USGS, DOI 10.5066/P9REJ9JN), 2 km window, degraded to 200 m planner. Habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20.0 deg (assumed). 16 realizations, seed 1234.

## What the planner sees

| planner slope | mean (deg) | 95th percentile (deg) | share of cells at or above the cutoff | share of cells that are exactly 0 |
|---|---|---|---|---|
| staircase | 2.76 | 13.64 | 2.0 % | 67.2 % |
| grid200 | 2.31 | 4.39 | 0.0 % | 0.0 % |
| truth (20 m) | 4.01 | 10.25 | 0.2 % | 0.0 % |

staircase = the registered model. grid200 = slope on the 200 m block means (200 m spacing).

Only 0.2 % of the 20 m truth cells reach the 20.0 deg cutoff. A forecast that always says
"never steep" therefore scores a Brier of 0.0020. A Brier at or above this value shows no skill.

## staircase

| roughness | confidence | calibrated area (km2) | coverage (95 % CI) | false reach | Brier |
|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.450 | 97.7 % (96.6 % to 98.5 %) | 8.4 % | 0.0168 |
| 0.1 | 0.7 | 0.444 | 97.2 % (96.0 % to 98.0 %) | 7.8 % | 0.0168 |
| 0.1 | 0.9 | 0.433 | 95.8 % (94.4 % to 96.9 %) | 6.7 % | 0.0168 |
| 0.3 | 0.5 | 0.462 | 98.6 % (97.7 % to 99.1 %) | 10.0 % | 0.0139 |
| 0.3 | 0.7 | 0.441 | 96.6 % (95.3 % to 97.5 %) | 7.7 % | 0.0139 |
| 0.3 | 0.9 | 0.396 | 88.5 % (86.5 % to 90.3 %) | 5.9 % | 0.0139 |
| 0.5 | 0.5 | 0.469 | 98.6 % (97.7 % to 99.1 %) | 11.3 % | 0.0157 |
| 0.5 | 0.7 | 0.415 | 90.9 % (89.0 % to 92.5 %) | 7.6 % | 0.0157 |
| 0.5 | 0.9 | 0.000 | 0.0 % (0.0 % to 0.4 %) | n/a | 0.0157 |

## grid200

| roughness | confidence | calibrated area (km2) | coverage (95 % CI) | false reach | Brier |
|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.467 | 99.9 % (99.5 % to 100.0 %) | 9.8 % | 0.0020 |
| 0.1 | 0.7 | 0.466 | 99.9 % (99.5 % to 100.0 %) | 9.6 % | 0.0020 |
| 0.1 | 0.9 | 0.465 | 99.9 % (99.5 % to 100.0 %) | 9.4 % | 0.0020 |
| 0.3 | 0.5 | 0.472 | 100.0 % (99.6 % to 100.0 %) | 10.7 % | 0.0020 |
| 0.3 | 0.7 | 0.469 | 99.9 % (99.5 % to 100.0 %) | 10.2 % | 0.0020 |
| 0.3 | 0.9 | 0.466 | 99.8 % (99.3 % to 99.9 %) | 9.7 % | 0.0020 |
| 0.5 | 0.5 | 0.474 | 100.0 % (99.6 % to 100.0 %) | 11.1 % | 0.0020 |
| 0.5 | 0.7 | 0.470 | 100.0 % (99.6 % to 100.0 %) | 10.3 % | 0.0020 |
| 0.5 | 0.9 | 0.461 | 99.7 % (99.2 % to 99.9 %) | 8.8 % | 0.0020 |

How to read it:

- Coverage = share of truth-reachable cells that the calibrated region contains. False reach = share of calibrated cells that the truth says are not reachable. High coverage with high false reach means an optimistic planner.
- All rows are reported for both models. No row is chosen as the result.
- Speeds, cutoff and roughness are assumptions. One 2 km window of one terrain class.
- grid200 is exploratory and is not promoted to the default without its own registration.
