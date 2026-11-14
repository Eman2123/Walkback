# Handoff

## Current
- To Shela (backend): implement POST /api/runs using src/walkback modules; add Alembic and Neon schema; add slowapi rate limit.
- To Urooj (frontend): replace App.jsx scaffold with map, sliders and results; install 21st.dev components after setting API_KEY_21ST; set VITE_API_URL.
- To Eman: sign off the JSON response contract before compute is wired; provision Vultr VM and Neon project.

## History
- 2026-11-13: design approved, scaffold committed locally.
- 2026-11-14: CI switched to requirements-api.txt (pipeline geo deps were not verified in CI). Deploy target changed from Vultr to FastAPI Cloud; Vultr deploy workflow removed.
- 2026-11-14: POST /api/runs now computes. Dev tile (dev-synthetic-20m) runs only when WALKBACK_ENV=dev and is labelled synthetic. Real tiles load from WALKBACK_TILE_DIR (data/processed/<tile>.npz) and return 503 until built. In-memory store in store.py; swap to Neon via db/repository.py. Bug found by test and fixed: travel time could enter impassable cells (same bug is in the browser demo, not yet fixed there).
- 2026-11-14: frontend wired to API (map, controls, results, reliability, assumptions, explain). Explain endpoint uses AIML API via OpenAI SDK; needs AIMLAPI_API_KEY and AIML_MODEL. Rate limit per IP (WALKBACK_RATE_PER_MIN, default 30). 30 tests pass; vite build passes.
- Still open: Neon store (db/repository.py), terrain build script (scripts/build_terrain.py) for the real Jezero tile, deploy to FastAPI Cloud.
- 2026-11-14: Neon store written (db/store_sql.py), chosen automatically when DATABASE_URL is set. Initial Alembic migration generated and verified on sqlite (migrations/versions). Terrain build script written (scripts/build_terrain.py, pipeline/build.py); smoke-tested on a tiny GeoTIFF, not yet on the real DTM. 35 tests pass.
- Still open: run the migration on Neon (alembic upgrade head with DATABASE_URL), download the Jezero DTM and run build_terrain on it, deploy to FastAPI Cloud.
- 2026-11-15: Shela's backend tasks merged into main (habitat check). Dockerfile now uses requirements-api.txt and copies the Jezero tile. Scale effect: measure_scale_effect (1 m window, H = 0.853). Validation report and sensitivity generated locally from the real tile. Remaining for deploy: Render (render.yaml) and server env vars.
