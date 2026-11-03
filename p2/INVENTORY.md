# Inventory (DRAFT, filled from the Astra start frame before the freeze)

Read off `evidence/p2_astra_start.png`. Positions are percent across and percent down. Nothing here changes after the freeze.

## Input baseline check (once, not per clip)
The start frame is the same for every arm, so how well Astra matches my real room is measured once, here, not in the clip scores. Overlay `p2_astra_start.png` on `p2_photo_a.jpg` at 50%. For each landmark below, write whether it sits within 2% of the frame width of its place in the photo.

Result: FILL of 8 landmarks match. This is reported on the page as the input's fidelity, separate from the models.

## Sample frames
At 0%, 25%, 50%, 75% and 100% of each output clip's own duration. Ground-truth frames at the same percentages come from `p2_walk.mp4`.

Getting frames: with ffmpeg (`brew install ffmpeg`), `ffmpeg -ss <seconds> -i clip.mp4 -frames:v 1 out.png`. Without it, pause in QuickTime and screenshot the video area only.

## Landmarks (architecture only, 8)
Chosen on the start frame, only things that also exist in my real room: corners, doorway edges, the ceiling step, baseboard corners, the hallway and the front door. No furniture.

| # | Landmark | Position in start frame |
|---|---|---|
| 1 | FILL | FILL |
| 2 | FILL | FILL |
| 3 | FILL | FILL |
| 4 | FILL | FILL |
| 5 | FILL | FILL |
| 6 | FILL | FILL |
| 7 | FILL | FILL |
| 8 | FILL | FILL |

## Reveal checks (what the start frame does not fully show)
Things that come into view as the camera moves forward, checked against `p2_walk.mp4`:
1. The front door at the end of the hallway: present, dark, in the right place.
2. The open doorway on the left of the far wall stays open, with nothing invented behind it.
3. The ceiling step continues along the right wall into the hallway.
FILL or adjust from the ground-truth walk.

## Furniture pieces (from the Astra plan, as visible in the start frame)
Hero pieces are marked H. Keep only what the start frame shows.

| Piece | Hero | In the start frame |
|---|---|---|
| Cream sofa with two pillows | H | FILL |
| Black leather and chrome Wassily chair | H | FILL |
| Glass and steel coffee table, books and black bowl on it | H | FILL |
| Walnut TV console with TV above it | H | FILL |
| Orange vase and small box on the console | | FILL |
| White mushroom table lamp | | FILL |
| Plant in a white pot | | FILL |
| Beige rug | | FILL |
| Chrome arc floor lamp | | FILL |
| Large abstract painting above the sofa | | FILL |
| Wooden stool by the sofa | | FILL |
| Hallway bench with bowl, and the blue art on the hallway wall | | FILL |
