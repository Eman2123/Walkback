FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PYTHONPATH=/app/src
WORKDIR /app

# API dependencies only (the geo pipeline is not needed at runtime)
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

COPY src/ ./src/
# Terrain tile built from the real DTM (161 KB). The API serves it from here.
COPY data/processed/ ./data/processed/
ENV WALKBACK_TILE_DIR=/app/data/processed

RUN useradd --create-home --uid 10001 appuser
USER appuser

EXPOSE 8000
CMD ["sh", "-c", "uvicorn walkback.api:app --host 0.0.0.0 --port ${PORT:-8000} --workers 2 --proxy-headers"]
