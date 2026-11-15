# Route feasibility (exploratory)

Registered in PREREGISTRATION.md before it was run. This does not replace the headline in validation_report.md.

Tile: Mars 2020 TRN HiRISE DTM (USGS, DOI 10.5066/P9REJ9JN), 2 km window, degraded to 200 m planner. Model v2, habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20.0 deg (assumed). For each cell the model calls reachable, the planner's shortest route (on the 200 m model) is walked on the 1 m truth. Feasible = the route never enters a truth-impassable cell and takes no longer than the budget.

## Headline (roughness 0.5, confidence 0.9, calibrated region)

- Planner routes that work on the truth: 876 of 987 (88.8 %, 95 % Wilson 86.6 % to 90.6 %; cells are spatially correlated, so the interval is optimistic).
- Failures: 0 cross a truth-impassable cell, 111 are too slow.
- Truth time over planner time: median 1.04, 95th percentile 1.24.
- Area view of the same setting: false reach 7.3 %.

## All settings

| roughness | confidence | region | cells | feasible | blocked | too slow | truth/planner time (median, p95) | area false reach |
|---|---|---|---|---|---|---|---|---|
| 0.1 | 0.5 | calibrated | 1120 | 87.7 % | 0 | 138 | 1.04, 1.24 | 8.2 % |
| 0.1 | 0.5 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.1 | 0.7 | calibrated | 1106 | 88.4 % | 0 | 128 | 1.04, 1.24 | 7.5 % |
| 0.1 | 0.7 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.1 | 0.9 | calibrated | 1093 | 89.0 % | 0 | 120 | 1.04, 1.24 | 7.0 % |
| 0.1 | 0.9 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.3 | 0.5 | calibrated | 1151 | 85.5 % | 0 | 167 | 1.04, 1.24 | 9.9 % |
| 0.3 | 0.5 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.3 | 0.7 | calibrated | 1113 | 87.5 % | 0 | 139 | 1.04, 1.24 | 8.4 % |
| 0.3 | 0.7 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.3 | 0.9 | calibrated | 1031 | 89.2 % | 0 | 111 | 1.04, 1.24 | 6.8 % |
| 0.3 | 0.9 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.5 | 0.5 | calibrated | 1172 | 84.3 % | 0 | 184 | 1.04, 1.24 | 11.1 % |
| 0.5 | 0.5 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.5 | 0.7 | calibrated | 1098 | 86.4 % | 0 | 149 | 1.04, 1.24 | 9.3 % |
| 0.5 | 0.7 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |
| 0.5 | 0.9 | calibrated | 987 | 88.8 % | 0 | 111 | 1.04, 1.24 | 7.3 % |
| 0.5 | 0.9 | deterministic | 1109 | 88.6 % | 0 | 126 | 1.04, 1.24 | n/a |

## Limits

- One 2 km Jezero window, which has almost no steep cells. This says nothing about steep terrain; the steep tiles are not in this repository, so they were not run.
- Linear speed model, an assumption. Truth uses the same speed model on the 1 m data, so this tests the planner's terrain information, not the speed model.
- A planning aid, not flight software. No route is declared safe.
