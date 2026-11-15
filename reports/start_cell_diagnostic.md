# Start-cell diagnostic (post-hoc, exploratory)

This is not the validation result. The pre-registered headline in validation_report.md is unchanged.

Tile: Mars 2020 TRN HiRISE DTM (USGS, DOI 10.5066/P9REJ9JN), 2 km window, degraded to 200 m planner. Habitat (50, 50), coarse slope at the habitat 10.3 deg, cutoff 20.0 deg.
Ensemble: 16 realizations, seed 1234.

Registered = the model exactly as run for the report. Pinned = same model, but the habitat cell
keeps its deterministic speed in every realization (the crew is already standing there).

| roughness | confidence | start cell blocked | registered area (km2) | registered coverage (95 % CI) | pinned area (km2) | pinned coverage (95 % CI) |
|---|---|---|---|---|---|---|
| 0.1 | 0.5 | 0.0 % | 0.450 | 97.7 % (96.6 % to 98.5 %) | 0.448 | 97.6 % (96.5 % to 98.4 %) |
| 0.1 | 0.7 | 0.0 % | 0.444 | 97.2 % (96.0 % to 98.0 %) | 0.443 | 97.2 % (96.0 % to 98.0 %) |
| 0.1 | 0.9 | 0.0 % | 0.433 | 95.8 % (94.4 % to 96.9 %) | 0.438 | 96.5 % (95.2 % to 97.4 %) |
| 0.3 | 0.5 | 0.0 % | 0.462 | 98.6 % (97.7 % to 99.1 %) | 0.461 | 98.5 % (97.5 % to 99.1 %) |
| 0.3 | 0.7 | 0.0 % | 0.441 | 96.6 % (95.3 % to 97.5 %) | 0.446 | 96.8 % (95.5 % to 97.7 %) |
| 0.3 | 0.9 | 0.0 % | 0.396 | 88.5 % (86.5 % to 90.3 %) | 0.413 | 91.3 % (89.4 % to 92.8 %) |
| 0.5 | 0.5 | 12.5 % | 0.469 | 98.6 % (97.7 % to 99.1 %) | 0.469 | 99.0 % (98.1 % to 99.4 %) |
| 0.5 | 0.7 | 12.5 % | 0.415 | 90.9 % (89.0 % to 92.5 %) | 0.440 | 94.6 % (93.1 % to 95.8 %) |
| 0.5 | 0.9 | 12.5 % | 0.000 | 0.0 % (0.0 % to 0.4 %) | 0.395 | 86.9 % (84.7 % to 88.8 %) |

How to read it:

- A row is empty in the registered model when the start-cell blocked share is above 1 minus the confidence.
  Then even the habitat cell cannot reach the confidence threshold.
- Rows where pinned coverage is still below 95 % are still shortfalls. Report them as shortfalls.
- All speeds, cutoffs and roughness values are assumptions. This is one 2 km window of one terrain class.
- This table was produced after the headline result was known. It explains the headline; it does not replace it.
