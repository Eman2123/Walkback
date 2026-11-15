# Mobility assumptions and what the model leaves out

Walkback answers "from which cells can a crew on foot get back to the habitat within a time budget?" with a deliberately simple walking model. This page lists what is in it, what is not, and what that means for the results. Nothing here is a measurement of Mars walking.

| Effect | In the model? | How | Label |
|---|---|---|---|
| Slope slows walking | Yes | Speed falls linearly from the flat-ground speed to 0 at the slope cutoff. A cell at or above the cutoff is impassable | assumed |
| Flat-ground speed (0.3 to 1.0 m/s, default 0.5) | Yes | One number for the whole crew and route | assumed |
| Slope cutoff (10 to 30 degrees, default 20) | Yes | Hard threshold on the slope of the 20 m cell | assumed |
| Uphill slower than downhill | Not by default | The default speed is the same in both directions. The opt-in `speed_model="minetti"` and `"minetti_cap"` use the Minetti et al. 2002 walking-cost polynomial (Earth, treadmill). `minetti_cap` never speeds the crew up | assumed |
| Return direction | Yes (v2) | The result is the time TO the habitat. With the default symmetric speed this equals the time from the habitat (tested); with a Minetti model it does not | assumed |
| Crew starts inside the habitat | Yes (v2) | The habitat cell stays passable in every ensemble realization | assumed |
| Mars gravity (about 3.7 m/s2, 0.38 of Earth) | **No** | Gait, cost of walking and slip all change; no source for coefficients is used here, so none is invented | not modelled |
| Suit, life-support backpack, carried load | **No** | | not modelled |
| Rocks, sand and regolith softness, boot slip | **No** | Only elevation is used; two cells of equal slope are equally easy | not modelled |
| Obstacles smaller than the cell (20 m) | **No** | Terrain is the block mean of a 1 m model, so a narrow cliff or boulder field inside a cell is averaged away, in the planner and in the truth | not modelled |
| Rest, fatigue, thermal and consumable limits | **No** | The only limit is the time budget | not modelled |
| Path shape | Approximately | 8-connected Dijkstra on the 20 m grid; on flat ground the area is 9.6 % smaller than the true circle. `solver="dijkstra16"` (opt-in) reduces this to about 2.7 % path error | derived |

## What the validation can and cannot tell you

The "truth" is the same speed model run on slopes of the 1 m terrain model (averaged to 20 m). Validation therefore tests one thing: how much the coarse terrain map misleads the planner. It does **not** test whether the speed model is right, because the truth shares it. A wrong speed model moves planner and truth together and the coverage and false-reach numbers will not show it.

How much the speed model matters, measured on the committed windows: the truth area changes by a factor of 0.3 to 3 depending on the direction and speed assumption alone (see the steep-window sections of `PREREGISTRATION.md` and `reports/steep_p/solver_directional.md`).

## What would be needed to model these effects

- Mars gravity and a suit: a published walking-cost relation for reduced gravity with a suited, loaded subject, and a stated source for each coefficient. Until then the effect is listed as not modelled, not approximated.
- Surface: a terrain-class layer (rocky, sandy, bedrock) with a speed factor per class, each factor labelled as assumed or sourced.
- Sub-cell obstacles: a roughness measure from the 1 m terrain model (for example the spread of 1 m slopes inside a 20 m cell) used as a cost, validated against held-out windows.

Each of these changes the model, so each needs its own entry in `PREREGISTRATION.md` before it is run.
