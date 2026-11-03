# Inventory (DRAFT, filled from the input recording before the freeze)

Read off `evidence/p2_input_astra_path.mp4` once it is recorded. Positions are percent across and percent down on the sampled input frame. Nothing here is changed after the freeze.

## Sample frames
At 0%, 25%, 50%, 75% and 100% of the clip's duration (the last frame for 100%). The same percentages are used on every output clip, measured on the output's own duration.

Getting the frames: with ffmpeg (`brew install ffmpeg`, not installed yet), `ffmpeg -ss <seconds> -i clip.mp4 -frames:v 1 out.png`. Without it, pause in QuickTime at each time and take a screenshot of the video area only.

## Landmarks (architecture only, up to 8)
Chosen on the input frames. Only things no restyle may legitimately move: corners, door and opening edges, the ceiling step, baseboard corners. Mark in which sample frames each is visible.

| # | Landmark | Visible at (0/25/50/75/100) | Position at first visible frame |
|---|---|---|---|
| 1 | FILL | FILL | FILL |
| 2 | FILL | FILL | FILL |
| 3 | FILL | FILL | FILL |
| 4 | FILL | FILL | FILL |
| 5 | FILL | FILL | FILL |
| 6 | FILL | FILL | FILL |
| 7 | FILL | FILL | FILL |
| 8 | FILL | FILL | FILL |

`geometry_checks` for every clip = the number of (landmark, frame) pairs where the landmark is visible in the input. It is the same for all six clips; write it here: FILL.

## Furniture pieces (from the Astra plan, as visible in the input recording)
Candidates from the Astra living room render; keep only the pieces the recorded path shows. Hero pieces are marked H.

| Piece | Hero | In the recording |
|---|---|---|
| Cream sofa with two pillows | H | FILL |
| Black leather and chrome Wassily chair | H | FILL |
| Glass and steel coffee table, books and black bowl on it | H | FILL |
| Walnut TV console with TV on the wall above it | H | FILL |
| Orange vase and small box on the console | | FILL |
| White mushroom table lamp | | FILL |
| Plant in a white pot | | FILL |
| Beige rug | | FILL |
| Chrome arc floor lamp | | FILL |
| Large abstract painting above the sofa | | FILL |
| Wooden stool by the sofa | | FILL |
| Hallway bench with bowl, and the blue art on the hallway wall | | FILL |
| Wood front door at the end of the hallway | | FILL |
