# Methods (draft, owner: Eman)

Terrain statistics: slope at 1, 5, 20 and 200 m; scale effect measured on the 1 m crop.
Deterministic walkback: linear speed reduction with slope, zero above cutoff; fast marching from the habitat on a fixed 100 x 100 grid.
Calibrated region: unresolved roughness as a random factor on coarse slope; cells kept when reach probability >= confidence threshold.
Validation: reliability of predicted steep probability vs observed steepness on the 1 m truth; Brier score; coverage with confidence interval; shortfall reported if below 95 percent.
All speeds, cutoffs and roughness levels are assumptions and are labelled. Minetti coefficients and suit factor are unverified until a source is confirmed.

Tile: 2 km x 2 km window, 100 x 100 cells at 20 m (see docs/adr/002-map-and-crop.md).
