# Architecture

Frontend (Vercel): Vite, React, Tailwind, 21st.dev components. Calls the API over HTTPS.
Backend (FastAPI Cloud, pending access; Docker image for any other host): uvicorn, validated inputs, cached runs.
Database (Neon Postgres): datasets, terrain_tiles, runs, calibration, assumptions, validation_base. Alembic migrations.
Explainer (AIML API, OpenAI-compatible): receives only the run JSON; numbers must match the JSON or the fallback is shown.

Trust boundary: every browser request body is untrusted and is validated in src/walkback/api.py.
See .10x/decisions/architect/walkback.md for the reasoning.
