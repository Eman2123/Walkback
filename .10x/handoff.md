# Handoff

## Current
- To Shela (backend): implement POST /api/runs using src/walkback modules; add Alembic and Neon schema; add slowapi rate limit.
- To Urooj (frontend): replace App.jsx scaffold with map, sliders and results; install 21st.dev components after setting API_KEY_21ST; set VITE_API_URL.
- To Eman: sign off the JSON response contract before compute is wired; provision Vultr VM and Neon project.

## History
- 2026-11-13: design approved, scaffold committed locally.
- 2026-11-14: CI switched to requirements-api.txt (pipeline geo deps were not verified in CI). Deploy target changed from Vultr to FastAPI Cloud; Vultr deploy workflow removed.
- 2026-11-14: POST /api/runs now computes. Dev tile (dev-synthetic-20m) runs only when WALKBACK_ENV=dev and is labelled synthetic. Real tiles load from WALKBACK_TILE_DIR (data/processed/<tile>.npz) and return 503 until built. In-memory store in store.py; swap to Neon via db/repository.py. Bug found by test and fixed: travel time could enter impassable cells (same bug is in the browser demo, not yet fixed there).
