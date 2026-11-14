# ADR 002: Map rendering

Status: accepted for the build (2026-11-14). Pending Eman's confirmation of the Leaflet alternative.

Context: the map shows one 2 km x 2 km Jezero crop (100 x 100 cells at 20 m), not global Mars. Coordinates are local metres. The planner grid is fixed by the API.

Decision: render with inline SVG in web/src/components/MapView.jsx. Regions arrive as GeoJSON in metres, so no projection is needed. The hillshade PNG will be drawn with an SVG image element when it exists.

Alternatives:
- Leaflet with L.CRS.Simple and imageOverlay: works, but adds a dependency and projection setup for a fixed small crop. Only worth it if the team needs pan and zoom over a much larger area.
- Earth tile maps (OpenStreetMap, MapLibre): not applicable. They assume Earth Web Mercator.

Consequences: no zoom or pan beyond the crop unless added later. Click-to-cell mapping is exact because the viewBox equals the grid size in metres.
