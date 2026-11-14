# Validation report

Tile: Mars 2020 TRN HiRISE DTM (USGS, DOI 10.5066/P9REJ9JN), 2 km window, degraded to 200 m planner
Cell size: 20.0 m. Truth is the 20 m block mean of the 1 m DTM.

## Headline (default setting, pre-registered)

SHORTFALL: coverage 0.0 % is below the 95 % target for this setting.

- Settings: habitat (50, 50), budget 900 s, speed 0.5 m/s (assumed), cutoff 20.0 deg (assumed), roughness 0.5 (assumed), confidence 0.9 (derived).
- Areas (km2): deterministic 0.444, calibrated 0.000, truth 0.422.
- Coverage of truth: 0.0 % (95 % CI 0.0 % to 0.4 %).
- Brier score: 0.0157 (lower is better).

## Reliability (predicted vs observed steep probability)

| bin | cells | predicted | observed |
|---|---|---|---|
| 0 | 8956 | 0.003 | 0.002 |
| 1 | 452 | 0.152 | 0.000 |
| 2 | 151 | 0.250 | 0.000 |
| 3 | 184 | 0.344 | 0.005 |
| 4 | 50 | 0.438 | 0.000 |
| 5 | 89 | 0.527 | 0.000 |
| 6 | 73 | 0.653 | 0.000 |
| 7 | 23 | 0.750 | 0.000 |
| 8 | 21 | 0.824 | 0.000 |
| 9 | 1 | 0.938 | 0.000 |

## Assumptions used

| name | value | label |
|---|---|---|
| time_budget_s | 900 | assumed |
| walking_speed_mps | 0.5 | assumed |
| slope_cutoff_deg | 20.0 | assumed |
| confidence_threshold | 0.9 | derived |
| unresolved_roughness | 0.5 | assumed |
| resolution_m | 20.0 | derived |
| ensemble_realizations | 16 | derived |

## Limits

- Result is for one 2 km window of one terrain class.
- Walking speed, slope cutoff and roughness are assumptions, not measured values.
- This is a planning aid, not flight software. No route is declared safe.
