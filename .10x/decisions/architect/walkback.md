# Architecture: walkback
Components: web (Vercel), api (Vultr Docker), db (Neon Postgres), storage (rasters in image).
Trust boundary: all request bodies from the browser are untrusted and validated in api.py.
Decision: one API container, Caddy as TLS front. Rejected: Kubernetes (overkill), Vercel-hosted Python (cold starts and limits for compute).
