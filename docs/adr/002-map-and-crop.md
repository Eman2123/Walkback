# ADR 002: Map library and crop size

Status: accepted (2026-11-14, Eman).

## Context
- The earlier plans said "5 x 5 km crop". The code uses a 100 x 100 grid at 20 m, which is 2 km x 2 km. The 2 km size is the one the code and the API use.
- The only map needed is a local crop of Jezero. The whole of Mars is not needed.
- The PDF plans named Leaflet with CRS.Simple, but the frontend already uses an SVG map (src/components/MapView.jsx) with no extra library.

## Decision
1. Crop size: 2 km x 2 km (2000 x 2000 px at 1 m, 100 x 100 cells at 20 m). It is enough for the largest walking budget: 1800 s at 0.5 m/s is about 900 m, so a habitat near the centre stays inside the window.
2. Map: keep the SVG map for the MVP. It needs no extra dependency, no tile server and no CDN, and it is already tested in the Vite build.
3. Hillshade background: add it later as an SVG <image> from public/, not as a map tile layer.
4. Leaflet with L.CRS.Simple is the upgrade path only if pan and zoom are required. Do not use MapLibre (Earth Web Mercator, wrong for Mars coordinates). Do not use Mars Trek tiles live: the crop is local and the API does not need them.

## Consequences
- The 5 x 5 km references in old PDFs are out of date. The repo is the source of truth.
- If the crop size changes, GRID in api.py, build.py and MapView.jsx must change together.
