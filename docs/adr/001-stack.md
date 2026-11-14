# ADR 001: Stack

Status: accepted (2026-11-13).
Context: 48-hour build, team of three, live what-if tool, judges need a working demo.
Decision: FastAPI backend, Vite + React + Tailwind frontend, Neon Postgres, AIML API for the explainer, Vercel for the frontend, FastAPI Cloud for the backend (Docker image kept as a fallback).
Alternatives: Next.js full stack (too much complexity); static GitHub Pages (not a live tool); Vultr VM (reconsidered, the team chose FastAPI Cloud).
Consequences: backend access depends on FastAPI Cloud beta; Vultr config remains in the repo as a fallback.
