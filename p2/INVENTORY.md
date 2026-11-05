# Inventory (FROZEN 2026-11-04, filled from the Astra start frame)

Read off `evidence/p2_astra_start.png`. Positions are percent across, percent down. Nothing here changes after the freeze.

## Input baseline check (once, not per clip)
The start frame is the same for every arm, so how well Astra matches my real room is measured once, here, not in the clip scores. Overlay `p2_astra_start.png` on `p2_photo_a.jpg` at 50%. For each landmark below, write whether it sits within 2% of the frame width of its place in the photo.

Result: **4 of 8** landmarks match (2026-11-04). This is reported on the page as the input's fidelity, separate from the models.

Method: positions read by eye off a 5% grid on both images (about 1% error), `p2_photo_a.jpg` resized to the start frame's 1672x941. Photo A was shot from a slightly different spot than the Astra camera, so the render's hallway sits a few percent left of the photo's. Misses 4, 5 and 6 share that same rightward shift; #7 is the largest miss. Labeled images (not committed): `evidence/p2_landmarks_start_v2.png`, `evidence/p2_landmarks_photoA_v2.jpg`, overlay `evidence/p2_overlay_start_photoA.png`.

| # | Start frame (x) | Photo A (x) | Difference | Match |
|---|---|---|---|---|
| 1 | 37.5 | 35.9 | 1.6 | yes |
| 2 | 37.5 | 35.9 | 1.6 | yes |
| 3 | 49.0 | 50.8 | 1.8 | yes |
| 4 | 45.4 | 48.6 | 3.2 | no |
| 5 | 57.5 | 61.0 | 3.5 | no |
| 6 | 58.5 | 61.5 | 3.0 | no |
| 7 | 41.0 | 48.8 | 7.8 | no |
| 8 | 40.7 | 42.2 | 1.5 | yes |

Render-vs-room mismatch (Astra's output, not a video model's invention): the render has a wall across from the hallway bench that is not in the real room. Photo A shows an open hallway there (with moving boxes). Any clip that keeps that wall is keeping the plan's render, not inventing it.

## Sample frames
At 0%, 25%, 50%, 75% and 100% of each output clip's own duration. There are no ground-truth walk frames (`p2_walk.mp4` was never recorded); the reference is `p2_photo_a.jpg`.

Getting frames: with ffmpeg (`brew install ffmpeg`), `ffmpeg -ss <seconds> -i clip.mp4 -frames:v 1 out.png`. Without it, pause in QuickTime and screenshot the video area only.

## Landmarks (architecture only, 8)
Chosen on the start frame, only things that also exist in my real room: corners, doorway edges, the ceiling step, baseboard corners, the hallway and the front door. No furniture.

| # | Landmark | Position in start frame |
|---|---|---|
| 1 | Left doorway, outer edge | 37.5, 40 |
| 2 | Left doorway, head corner | 37.5, 13.5 |
| 3 | Front door, centre | 49, 39 |
| 4 | Hallway entry ceiling soffit, left corner (where the lowered ceiling meets the left wall) | 45.4, 12.5 |
| 5 | Ceiling step (beam) end on the right wall | 57.5, 15 |
| 6 | Hallway entry ceiling soffit, bottom-right corner (meets the right wall) | 58.5, 20.2 |
| 7 | Left wall base corner at the doorway (baseboard meets floor) | 41, 58 |
| 8 | Left doorway recess, right edge (vertical edge on the hallway side) | 40.7, 35 |

## Reveal checks (what the start frame does not fully show)
Things that come into view as the camera moves forward, checked against `p2_photo_a.jpg` and the start frame:
1. The front door at the end of the hallway: present, dark, in the right place.
2. The open doorway on the left of the far wall stays open, with nothing invented behind it.
3. The ceiling step continues along the right wall into the hallway.
Note (2026-11-04): there is no usable hallway-direction phone walk (`p2_walk.mp4` was never recorded; the one phone clip walks the other way). These three checks are written from the start frame and the real photo A, which shows the same hallway end: dark front door, left doorway recess, ceiling step along the right wall. Reveal checks are judged against photo A and the start frame, and ground-truth sample frames from a walk do not exist. Settled at the freeze (T28, 2026-11-04): `RUBRIC.md`, `PROMPT.md`, `FAILURE_TYPES.md` and this file now name photo A and the start frame instead of the walk.

## Furniture pieces (from the Astra plan, as visible in the start frame)
Hero pieces are marked H. Keep only what the start frame shows.

| Piece | Hero | In the start frame |
|---|---|---|
| Cream sofa with two pillows | H | Yes, centre right. Cushions on the left seat and back. Right arm is cut by the frame edge. |
| Black leather and chrome Wassily chair | H | Yes, bottom left, partly cut by the bottom edge. |
| Glass and steel coffee table, books and black bowl on it | H | Yes, centre. Books and black bowl on top. |
| Walnut TV console with TV above it | H | Yes, left. TV on top, console runs back toward the doorway. |
| Orange vase and small box on the console | | Yes, on the console, left. |
| White mushroom table lamp | | Yes, left, behind the console, tall with white dome shade. |
| Plant in a white pot | | Yes, left edge, partly cut by the frame. |
| Beige rug | | Yes, under the coffee table and extends across the foreground. |
| Chrome arc floor lamp | | Yes, right edge, cut by the frame; shade at the top right. |
| Large abstract painting above the sofa | | Yes, right wall above the sofa. |
| Wooden stool by the sofa | | Yes, behind the sofa, reads as two stacked stools. |
| Hallway bench with bowl, and the blue art on the hallway wall | | Bench and blue art yes, on the right in the hallway. The bowl on the bench is not visible at this size. |
