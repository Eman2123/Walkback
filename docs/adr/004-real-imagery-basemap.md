# ADR 004: Real HiRISE imagery as the map basemap

Status: proposed (2026-11-15). Amends ADR 002 (points 3 and 4) and ADR 003.

## Context
- The map showed a shaded relief made from the planner's own coarse DEM. It looks like terrain but it is not a photograph, and it is derived from the same data the model uses.
- USGS publishes a 25 cm HiRISE orthomosaic of the same Mars 2020 TRN product as the DTM (DOI 10.5066/P9QJDP48), in the same projection family (equirectangular, Mars sphere 3,396,190 m).
- ADR 002 said not to use Mars Trek tiles live. The Trek documentation does not list HiRISE or Jezero layers or its CORS behaviour, so a live tile dependency could not be checked.

## Decision
1. Crop the real orthophoto to exactly the DTM window with scripts/build_basemap.py and ship it as a static file (web/public/basemap-jezero-20m.jpg, about 2 m per pixel) with a JSON file holding the corner and centre latitude and longitude.
2. The window location is read from the DTM's georeferencing and the orthomosaic bounds are taken from the same coordinates. The script stops if the two projections differ.
3. The frontend uses the real image when it exists, then the shaded relief, then a plain background. The caption names the image that is actually on screen.
4. No colour is added to the photograph. Real coordinates are shown for the habitat only when the JSON file exists.
5. Mars Trek stays as an external link for exploration. No live tile layer.

## Alternatives
- Live Mars Trek WMTS tiles: unverified layers, CORS and licence, and a runtime dependency on a third party.
- Leaflet with CRS.Simple and imageOverlay: only needed for pan and zoom.

## Consequences
- Someone with the DTM and a connection to the USGS file must run the script once and commit the two output files. Until then the app falls back to the relief.
- The photograph is an extra context layer. It is not ground truth, and the HiRISE DTM remains the only ground truth.
- Light and shadow in the photograph come from the HiRISE acquisition, not from the hillshade sun angle.
- Alignment between DTM and orthophoto is as good as the USGS co-registration. Check the result by eye against the relief before publishing.
