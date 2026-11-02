# Coverage (test-set review, ticket T14 / HEL-77)

Frozen with the protocol. Scope: living room only, 4 generations: `living_v1` attempts 1 and 2, `living_v2` attempts 1 and 2. One scorer, one pass.

## Which cases can disprove each hypothesis

| Hypothesis | Disproved by | Cases |
|---|---|---|
| H1: at least 6 of 8 landmarks survive | Fewer than 6 of 8 in most generations | All 4 |
| H2: scale is weaker than layout (scale error over 10% more often than layout breaks) | Scale scores equal or beat layout scores | All 4. Scale has no score of its own; `furniture` (which also covers identity, placement and path) is the proxy, and `scale_error_pct` is filled only when measurable. A screening check, not a measurement |
| H3: lighting and material realism scores highest | Lighting below layout | All 4 |
| H4: retries drive cost (best-of-2 clearly beats the mean) | Best-of-2 within about 0.3 points of the mean | One pair per condition: `living_v1` and `living_v2` |
| H5: the model route matters | Same results across models, or the model is never shown | Cannot be tested. One surface (Agent, Quality), and the image model is probably not shown. Stated as a limit, and the page says so |
| H6: extra context improves furniture and scale | Mean furniture and the scale call no better under v2 | `living_v1` against `living_v2`. 2 against 2 can only show a large effect. Runs are interleaved and scored without looking at the prompt to limit drift. Likely failure under v2: the nook bleeding into the living room (`hallucination` or `side_effect`) |

With n = 2 per condition these are directional readings, not statistics. The page says so. A longer analysis (budget, hypothesis weaknesses, page wording) was written for the earlier 3-room, 8-run scope and sits unmerged on branch `claude/t14-coverage-8f9af5`; this file is the single frozen coverage table.

## Hard cases the test set leaves out

| Hard case | Status | Where |
|---|---|---|
| Furnished, lived-in room (couch, console, stool, clutter) | In scope | The living room photo is furnished; the keep-list tests preservation |
| Ceiling with a step or bulkhead | In scope | Landmark 6 |
| Reflective objects (chrome lamp shade, TV screen) | In scope, lightly | Lighting check (c). No mirror or large glass surface in frame |
| Mirrors and large glass | Stated limit | Not in the living room photo |
| Low light or hard direct sun | Deferred | Bedroom photo has a low sun patch; T13 (more rooms) and T9 (lamp relighting) |
| Sloped or angled ceilings | Deferred | The dining nook has one; T13 |
| View outside the window | Stated limit | No window in the living room frame |
| Removing existing objects (the drying rack) | Stated limit | Tried once in the pilot, not scored; T15 repair pass |
| More than one piece, or four of the same piece | Deferred | The nook chairs; T13 |
| Other rooms, other camera angles, other apartments | Stated limit | One room in one apartment |
| Second scorer, blind re-score | Deferred | T11 |
| Other image models and Cost or Speed routing | Stated limit | One surface and setting; Cost run is an optional extra, logged as its own case |
