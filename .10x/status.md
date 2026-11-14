# Status: walkback

Phase: Implementation (scaffold)
Approved: frontend Vite + React + Tailwind (21st.dev); backend Vultr VM Docker; DB Neon; frontend Vercel.

Done:
- Pipeline stubs, contract, tests (earlier foundation commit)
- API skeleton with validation and tests (api.py, test_api.py)
- Dockerfile, docker-compose, Caddyfile
- CI workflow, deploy workflow
- Vite + React + Tailwind skeleton (web/)
- .10x state files

Done (added):
- POST /api/runs computes walkback and calibration on the dev tile; cache by parameter hash; GET /api/runs/{id}
- Impassable-neighbour bug in travel time fixed (test added)

Not done:
- Neon schema and Alembic migrations
- Rate limit
- 21st.dev components (needs API_KEY_21ST)
- Vultr VM provisioning, DNS, Caddy live
- Push to GitHub (no credentials in this environment)
