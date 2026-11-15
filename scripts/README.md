Command-line entry points go here. Each script must be runnable from the repo root.

Planned:
- scripts/build_terrain.py: crop, degrade, slope, scale effect, write terrain_tiles rows.
- scripts/run_validation.py: reads PREREGISTRATION.md, runs the validation, writes reports/.
- scripts/seed_db.py: loads datasets and terrain_tiles into Neon (after migrations).
- scripts/find_steep_windows.py: scans a 1 m DTM and prints the steepest non-overlapping 2 km windows, with ready-to-run build_terrain.py commands. Selection rule is registered in PREREGISTRATION.md.
- scripts/run_validation.py: extended validation (staircase, grid200, grid200 + hurst) over every tile in data/processed; writes reports/validation_extended.md and .csv. Registered in PREREGISTRATION.md.
- scripts/run_solver_directional.py: compares the 16-neighbour solver and the Minetti direction factor (out and back) against the registered model over every tile in data/processed; writes reports/solver_directional.md and .csv. Registered in PREREGISTRATION.md.
