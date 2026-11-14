# Data model: walkback
Tables: datasets, terrain_tiles, runs (unique param_hash), calibration, assumptions, validation_base.
Runs are cached by a SHA-256 of tile id plus rounded parameters.
Migrations: Alembic, run in the deploy step (not at app startup). Connection via DATABASE_URL with sslmode=require.
