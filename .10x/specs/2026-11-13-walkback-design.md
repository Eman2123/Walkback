# Walkback Under Uncertainty: approved design (2026-11-13)

Architecture: Vercel (Vite, React, Tailwind, 21st.dev components) -> HTTPS -> Vultr VM (Docker: FastAPI + uvicorn, Caddy for TLS) -> Neon Postgres.
Terrain rasters: small crop (under 100 MB) shipped in the image; DB stores paths and checksums.
Compute: fast marching (scikit-fmm) on a fixed 100 x 100 grid. Results cached by parameter hash.
Scope: live what-if tool. Calibration claims are labelled; slider changes change assumptions, not terrain.
Budget: Vultr credit USD 150 available.
