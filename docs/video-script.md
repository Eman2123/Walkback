# 30-second video script (numbers from the repo, nothing rounded in our favour)

Every number below comes from a file in this repository; the source is in the right-hand column. Read the shortfall out loud: the honest result is the strongest part of the pitch.

| Time | Screen | Voice-over | Source |
|---|---|---|---|
| 0-5 s | Map of the Jezero window, habitat dot, one orange region growing | "A crew is out on Mars. How far can they go and still walk home before time runs out?" | README |
| 5-12 s | Orange (planner) region next to the grey 1 m truth region | "We plan on a coarse 200 metre map and check against a 1 metre map the planner never sees." | README, docs/methods.md |
| 12-20 s | Coverage bar at 86.9 %, 95 % target line above it, label SHORTFALL | "Result: the region covers 86.9 percent of what is truly reachable. Our target was 95. That is a shortfall, and we show it." | PREREGISTRATION.md (v2 change log) |
| 20-26 s | One route drawn on the map, then the feasibility number 88.8 % | "Walk the planner's own route on the real terrain: 88.8 percent of routes make it home in time. The rest are too slow." | reports/route_feasibility.md |
| 26-30 s | Steep window, false-reach warning, text: "Not flight software" | "On steep ground the only setting that hits 95 percent calls 25 to 45 percent too much reachable. Walkback shows where the model is blind." | README (steep-P, grid200 rows) |

## Word count
About 90 spoken words, which is tight for 30 s. If it runs long, cut the 5-12 s line first.

## Lines not to say
- "Validated" or "safe": the headline is a shortfall and no route is declared safe.
- Any claim about other places on Mars: one Jezero window, plus steep windows chosen by steepness.
- "Mars gravity" or "suit" as features: they are not modelled (docs/mobility-assumptions.md).

## Check before recording
- The 25 % to 45 % false reach is a steep-P grid200 result (README, Steep-P section) from the owner's tiles, which are not in this repo. Confirm it against your own reports before recording.
- Route feasibility (88.8 %) is Jezero only, linear speed model, and its interval is optimistic because cells are correlated.

## Recording checklist
1. Open https://walkback-rlvz.vercel.app, hard refresh (Ctrl+Shift+R), wait until the badge says the API is reachable. If it falls back to the demo, say so or retry.
2. Keep the default inputs (roughness 0.5, confidence 0.9). Do not move sliders while recording: the Route check card is a fixed report.
3. Shots in order: map with the three regions, the Result card with the SHORTFALL banner, the Route check card (88.8 %), the Reliability chart.
4. Read the numbers from the screen, not from memory. They must match: coverage 86.9 %, Brier 0.0157 against 0.002, route feasibility 88.8 %.
5. Record at 1080p, 30 s. If it runs over, cut the 5-12 s line first.
6. After uploading, put the link in README.md under "Demo links and latest changes".
