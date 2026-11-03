# Prompt v1 (prompt_id = p2v1, DRAFT)

## Inputs
1. **Input video:** a 5 s screen recording of an eye-level camera path through the Astra 3D model of the living room. Slow push from the near end of the room toward the hallway and the front door, no cuts, no UI on screen. Saved as `evidence/p2_input_astra_path.mp4` (gitignored). Recorded once, before the freeze, and used for every clip.
2. **Reference image (if every arm accepts one, see README):** `evidence/input_living_stripped.jpg`, the real living room photo with EXIF and GPS stripped. The nook photo is not used: it shows the skyline and adds a second variable.

The real photo has different furniture from the Astra plan (the drying rack, no Wassily, no rug). The prompt says to take materials and light from it, not furniture.

## Prompt text
> The input video is a camera walkthrough recorded in a 3D model of my living room. The reference image is a real photo of the same room. Turn the input video into realistic footage, as if filmed on a phone in my real apartment in daylight. Keep the camera path, the timing, the room's walls, ceiling, doorways and every piece of furniture exactly as in the input video: the same pieces, the same number of them, in the same positions, with the same shapes and colors. Do not add, remove or move any furniture, door or window. Take only the materials and light from the reference photo, not its furniture: a dark brown wood plank floor with visible grain, matte white walls with white baseboards, the ceiling step along the right wall, and soft daylight. Add natural contact shadows under every piece. No people.

If no reference image is used, drop the second sentence and the words "from the reference photo, not its furniture"; the material description stays. That variant is `p2v1-noref`, decided in pre-flight, and the same one is used for every arm.

## Settings (fill per arm in pre-flight, then frozen)
| Arm | Model | Takes input video | Takes reference image | Duration set to | Aspect ratio | Other defaults touched |
|---|---|---|---|---|---|---|
| A | Aleph 2.0 | FILL | FILL | FILL | FILL | audio off, enhancer off |
| B | FILL | FILL | FILL | FILL | FILL | audio off, enhancer off |
| C | FILL | FILL | FILL | FILL | FILL | audio off, enhancer off |

## Run order
A1, B1, C1, A2, B2, C2. Case id `astra_walk`, arm `A`/`B`/`C`, attempt 1 or 2.

## Per clip, at generation time
- Write case id, arm, attempt and the cost the app shows, before clicking generate.
- Screenshot the settings and the cost.
- `minutes`: from the generate click to the finished clip.
- `credits`: the cost shown; if none, the balance difference. Note the balance before and after in `notes`.
- Download the clip as `evidence/p2_<arm>_a<attempt>.mp4`.
- Gut call (acceptable yes or no, `RUBRIC.md`) right away, before scoring.
