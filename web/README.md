# Frontend (Urooj)

Vite + React + Tailwind. UI components come from 21st.dev once API_KEY_21ST is set.

Run locally:
    cd web && npm install && npm run dev

Environment: copy .env.example to .env and set VITE_API_URL.

Rules:
- All backend calls go through src/lib/api.js.
- All numbers go through src/lib/format.js, so labels and units stay consistent.
- Never put secrets in the frontend.

Layout:
- src/components/: one component per file, each with an owner comment at the top.
- src/lib/: api client and formatting helpers.
- public/: static assets (the Jezero hillshade PNG goes here once built).
