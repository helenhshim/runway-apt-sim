# Rubric p2 (DRAFT, frozen with the P2 protocol commit)

Each scored clip gets 1 to 5 on four criteria. Anchors are fixed before the first scored clip and meant to be decidable without a gut feel. If a score is still a coin flip, pick the lower one and write both numbers in `notes`. Score clips by their `blind_id` (see `blind.py`), in the shuffled order, in a Claude session that writes each row to `p2/log.csv`, validates it, and keeps my words in `p2/scoring_notes.md`.

What each criterion is judged against:
- **The start frame** (`p2_astra_start.png`) for the plan: furniture and the room as rendered. The Astra render is AI-generated, so "kept" means kept from the plan.
- **The real photo and the phone walk** for what my room actually looks like: materials, light, and anything the start frame does not show.

Log column names stay as in `schema.sql`: `geometry` = criterion 1, `plan` = 2, `realism` = 3, `temporal` = 4.

## 1. Real-room fidelity (log column `geometry`)
Does the architecture hold as the camera moves, and is what comes into view my real room?

Part one, landmarks. At each sample frame after frame 1 (25%, 50%, 75%, 100%), for each landmark from `INVENTORY.md` that is in view, it is **kept** if all three hold: it is still there (or hidden behind something in front of it), its edges stay straight, and its order against its neighbours (left to right, top to bottom) is unchanged. `geometry_checks` = landmark-frame pairs in view; `geometry_kept` = kept pairs.

| geometry_kept / geometry_checks | Base score |
|---|---|
| 0.95 or more | 5 |
| 0.85 to under 0.95 | 4 |
| 0.70 to under 0.85 | 3 |
| 0.50 to under 0.70 | 2 |
| under 0.50 | 1 |

Part two, reveal checks (`INVENTORY.md`), judged against the phone walk. Each failed reveal check lowers the base score by 1, to a minimum of 1. A reveal check that never comes into view is not counted; note it.

Caps: an opening added, removed or closed caps at 1. Walls or ceiling visibly bending caps at 2.

## 2. Plan fidelity (log column `plan`)
Each piece listed in `INVENTORY.md`, over the whole clip:

| Call | Meaning |
|---|---|
| Pass | Same type, shape, color and place throughout, moving only as the camera move explains |
| Marginal | One detail differs (shade, material, a leg or pillow), or it deforms for under half a second and recovers |
| Fail | Missing, replaced by another type, duplicated, moved against the room, or changed and stays changed |

| Score | Anchor |
|---|---|
| 5 | All pass |
| 4 | One or two marginal, no fail |
| 3 | Three or more marginal, or one fail on a non-hero piece |
| 2 | Two fails, or one fail on a hero piece |
| 1 | Three or more fails, or two hero pieces fail |

## 3. Realism against the real photo (log column `realism`)
Five checks:
- (a) Floor: dark brown plank with visible grain, tone close to the photo.
- (b) Walls and ceiling: matte white walls, white baseboards, the ceiling step where the room has it.
- (c) Light: reads as daylight, contact shadows under every piece.
- (d) Photographic look, none of these render tells: one uniform plastic sheen, repeating texture tiles, perfectly clean edges with no lens softness or noise, waxy fabric.
- (e) Reflective items (chrome lamp, glass table, TV screen) reflect the room plausibly.

A flaw is minor if visible only when paused or zoomed, clear if visible at normal playback.

| Score | Anchor |
|---|---|
| 5 | All five pass |
| 4 | One minor flaw |
| 3 | One clear flaw, or two minor flaws |
| 2 | Two clear flaws, or three or more flaws of any kind |
| 1 | Still reads as a 3D render overall, or a material is replaced (for example a light floor) |

## 4. Temporal and scene consistency (log column `temporal`)
Watch twice at full speed, then frame by frame through any span that looked wrong. Count events:
- **flicker:** texture or light pulsing.
- **morph:** a piece or surface changes shape or identity, including growing or shrinking against the room (scale constancy).
- **pop:** something appears or disappears without being hidden by something else (object permanence).
- **drift:** architecture slides or warps, near and far things move at the wrong relative speeds (parallax), or light and shadows move with the screen instead of staying fixed to the room.
- **path:** the camera does not move forward as asked (turns, stops, reverses) or the clip freezes.

An event is minor if only visible frame by frame, clear if visible at full speed. `temporal_events` = total count.

| Score | Anchor |
|---|---|
| 5 | No events |
| 4 | One minor event |
| 3 | One clear event, or two minor |
| 2 | Two clear events, or three or more of any kind |
| 1 | The room or a hero piece turns into something else, or the camera path is ignored |

## Acceptable (gut call, right after generating, before scoring)
Would I show this clip as "my apartment with this furniture" and trust it to judge how the plan would look? Yes or no. After scoring, the page reports how often the gut call agrees with all four scores at 4 or higher.

## Failure row
Pick the single most important failure type (`FAILURE_TYPES.md`); mention others in `notes`. A clip with no failure has blank type and severity.

## Severity
- 1: only visible paused, zoomed or on the overlay.
- 2: visible at normal playback; would mislead how the room would look.
- 3: the room or a hero piece is not recognizable, an opening is wrong, or it still looks like a render; unusable.

## Checking the eval itself
- Rubric-critic agent review before the freeze; accepted changes logged in the PRD decision log.
- One automated metric beside criterion 4 (frame-to-frame consistency; method fixed at the freeze; see `EVAL_RESEARCH.md`).
- If time allows, re-score 3 of the 6 clips at least 24 hours later, reshuffled, without looking at the first scores.
