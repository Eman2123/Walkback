# Methods (draft, owner: Eman)

Terrain statistics: slope at 1, 5, 20 and 200 m; scale effect measured on the 1 m crop.
Deterministic walkback: linear speed reduction with slope, zero above cutoff; travel time from the habitat by Dijkstra on an 8-connected 100 x 100 grid (not fast marching).
Calibrated region: unresolved roughness as a random factor on coarse slope; cells kept when reach probability >= confidence threshold.
Validation: reliability of predicted steep probability vs observed steepness on the 1 m truth; Brier score; coverage with confidence interval; shortfall reported if below 95 percent.
All speeds, cutoffs and roughness levels are assumptions and are labelled. Minetti coefficients and suit factor are unverified until a source is confirmed.

Tile: 2 km x 2 km window, 100 x 100 cells at 20 m (see docs/adr/002-map-and-crop.md).

Known limit (2026-11-15): the registered planner slope is computed from 200 m blocks drawn on the 20 m grid, so it is zero inside blocks and large on block edges. The variant that computes slope on the 200 m block grid is in reports/planner_slope_variant.md. Only 0.2 % of the 20 m truth cells reach the 20 deg cutoff in this window, so a Brier score is compared with the no-skill value 0.0020 before it is called good.

Known numerical bias (measured 2026-11-15): on flat ground at uniform speed the 8-connected path is up to 8.2 % longer than the straight line, and the 900 s reach area is 0.575 km2 against 0.636 km2 for the true circle (-9.6 %). Reach areas are therefore slightly pessimistic. Not changed, because changing the solver would change the registered numbers; a 16-neighbour or fast-marching solver needs its own registration.

Extended validation (exploratory, PREREGISTRATION.md section "Extended validation and sub-grid roughness"): Brier skill score, reliability of the reach probability, coverage against the confidence threshold, a block-bootstrap interval next to the Wilson one, and a scale-law sub-grid roughness variant ("hurst", in-sample H). Run with scripts/run_validation.py, output in reports/validation_extended.md.
