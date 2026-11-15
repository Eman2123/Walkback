## Registration: steep windows with a passable habitat cell (steep-P)

Status: registered BEFORE any steep-P window is run. Append to PREREGISTRATION.md.

### Why

In steep-1 and steep-2 the registered model did not run because the habitat cell is impassable at 200 m. That is a window-selection problem, not a result about steep terrain. We keep the registered model unchanged and change only which windows it is tested on. We do not change the habitat-cell rule, because that would be tuning the model after seeing its failure.

### Window selection rule (fixed now)

1. Candidate windows: 2 km windows on the same Jezero DTM, same size and degradation as before.
2. Habitat cell = the same cell definition as registered (window centre). Include a window only if its habitat cell is below the registered slope cutoff at 200 m (passable).
3. Include a window only if at least 10 % of its 20 m cells are at or above the 20 deg cutoff (steep enough to be informative). If fewer than 3 windows meet this, report how many did and use only those.
4. Selection uses terrain only (slope and the habitat-cell test). Model outputs, coverage and Brier are never used to choose windows.
5. Windows are taken in a fixed order (raster scan from the top-left, non-overlapping), the first 3 that pass. No skipping and no replacing.

### What is run (nothing new)

Same registered model, same grid200 variant, same hurst, same Minetti variants, same 16-neighbour check, same rows as steep-1..3.

### Same decision rules

- Coverage target: lower end of the wider interval reaches 95 %. Otherwise it is a shortfall.
- Skill: Brier score skill score against "never steep".
- False reach reported per window for every model.

### Reporting rule

Every row of every window is written to the change log, including windows where something fails. Windows that did not meet rule 2 or 3 are listed with the reason, not dropped silently.

### Claims allowed after the run

- Allowed: statements about these windows on this DTM, labelled "estimated".
- Not allowed: "the model is fine for steep terrain", or anything about other parts of Mars. Windows are steepness-selected, so this stays a limitation whatever the outcome.

### Not registered here (exploratory only, labelled if run)

Changing the habitat-cell rule. If run later, it is reported as a separate exploratory variant, never as the registered result.