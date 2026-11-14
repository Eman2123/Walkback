# Sensitivity analysis (exploratory)

Tile: Mars 2020 TRN HiRISE DTM (USGS, DOI 10.5066/P9REJ9JN), 2 km window, degraded to 200 m planner
Fixed: habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20 deg (assumed), 16 realizations.
Default setting: roughness 0.5, confidence 0.9 (marked). Not changed by these results.

| roughness | confidence | default | deterministic km2 | calibrated km2 | truth km2 | coverage (CI) | Brier |
|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 |  | 0.444 | 0.450 | 0.422 | 97.7 % (96.6 %-98.5 %) | 0.0168 |
| 0.1 | 0.7 |  | 0.444 | 0.444 | 0.422 | 97.2 % (96.0 %-98.0 %) | 0.0168 |
| 0.1 | 0.9 |  | 0.444 | 0.433 | 0.422 | 95.8 % (94.4 %-96.9 %) | 0.0168 |
| 0.3 | 0.5 |  | 0.444 | 0.462 | 0.422 | 98.6 % (97.7 %-99.1 %) | 0.0139 |
| 0.3 | 0.7 |  | 0.444 | 0.441 | 0.422 | 96.6 % (95.3 %-97.5 %) | 0.0139 |
| 0.3 | 0.9 |  | 0.444 | 0.396 | 0.422 | 88.5 % (86.5 %-90.3 %) | 0.0139 |
| 0.5 | 0.5 |  | 0.444 | 0.469 | 0.422 | 98.6 % (97.7 %-99.1 %) | 0.0157 |
| 0.5 | 0.7 |  | 0.444 | 0.415 | 0.422 | 90.9 % (89.0 %-92.5 %) | 0.0157 |
| 0.5 | 0.9 | yes | 0.444 | 0.000 | 0.422 | 0.0 % (0.0 %-0.4 %) | 0.0157 |

Highest coverage across all 9 settings: 98.6 %.
If this is below 95 %, the result is a shortfall and must be reported as one.
