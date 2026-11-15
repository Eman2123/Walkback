"""Entrypoint for hosts that look for app.py at the repository root (Vercel, FastAPI Cloud).

The package lives in src/, so put it on the path and re-export the FastAPI app.
Locally you can still run: PYTHONPATH=src uvicorn walkback.api:app
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from walkback.api import app  # noqa: E402,F401
