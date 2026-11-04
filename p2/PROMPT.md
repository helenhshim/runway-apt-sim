# Prompts (DRAFT)

## Inputs
| File (in `evidence/`, gitignored) | What | Given to the models? |
|---|---|---|
| `p2_astra_start.png` | Eye-level Astra render from the taped spot: 16:9, daylight, ceiling on, no cutaway | Yes, as the start frame for every arm |
| `p2_astra_end.png` | Optional Astra render about 1.5 m further along the path | Only if every scored arm takes a last frame |
| `p2_photo_a.jpg` | Real photo from the taped spot, 16:9, 1x lens, EXIF stripped | Only as a materials reference, and only if every scored arm takes one |
| `p2_photo_b.jpg`, `p2_walk.mp4` | Real end photo and a 5 s phone walk from A to B | Never. Ground truth for scoring |

The real photos show my current furniture, not the plan. Prompts say to take only materials and light from them.

## Build prompts (iterations, every arm, in this order)
`b01`, base:
> Photorealistic phone video of this living room in daylight. The camera moves slowly forward in a straight line toward the hallway and the front door at the far end, at walking pace and eye level, without turning. Keep the room exactly as shown: the same walls, ceiling, doorways and floor, and every piece of furniture in the same place, shape and color. Nothing appears or disappears. Soft natural shadows under the furniture, real materials. No people, no text.

`b02`, materials in words (decided 2026-11-04: Gen-4.5 takes no reference image, so per the fairness rule no arm gets one; b02 describes the real materials instead):
> b01 text, then: Real materials of this apartment: a dark brown wood plank floor with visible grain, matte white walls with white baseboards, and a step in the ceiling along the right wall. Shot on a phone, not a 3D render.

`b03`, one fix chosen after watching `b01` and `b02` on all three arms, applied to all:
| If I see | Add |
|---|---|
| Camera turns or drifts | "The camera does not pan, tilt or rotate." |
| Still looks like a render | "Shot on an iPhone, slight natural grain and lens softness." |
| Furniture wobbles or morphs | "All furniture is rigid and stays still." |
| Something new appears | "Show only what is in the image." |

Each prompt is saved as `p2/prompts/bNN.txt` before use. Extra demo tries beyond `b03` are logged as demo only.

## Eval prompt (prompt_id = p2v1, filled at the freeze)
The best of `b01` to `b03` across all three arms, not the best for one arm. Text and the reason it was picked go here: FILL.

## Settings (fill per arm before the freeze, then frozen)

Observed 2026-11-04: all three models run on the current plan and are named in the picker, but the app shows no credit cost before generating. Cost per clip is therefore the balance before minus the balance after.

| Arm | Model | Start image | Last frame | Reference image | 16:9 | Duration set | Other defaults touched |
|---|---|---|---|---|---|---|---|
| A | Gen-4.5 | yes | no end image; "use frame" only turns a frame of a generated clip into a new input (checked 2026-11-04) | no (checked 2026-11-04) | yes | 5 s | audio off, enhancer off |
| B | Seedance 2.5 | yes | yes (checked 2026-11-04, not used) | yes (checked 2026-11-04, not used) | yes | 5 s | audio off, enhancer off |
| C | Gemini Omni 1.1 Flash | yes | yes (checked 2026-11-04, not used) | yes (checked 2026-11-04, not used) | yes | 5 s | audio off, enhancer off |

## Run order (eval)
A1, B1, C1, A2, B2, C2. Case id `astra_walk`.

## GWM probe
Genesis prompt: "A photorealistic living room in daylight, exactly as in the first frame." First frame: `p2_astra_start.png`. Steer straight forward slowly for about 5 s, no turning, and screen-record the steering so a second run can repeat it. Scored on the same rubric, reported beside Gen-4.5, never ranked against B and C.

## Per clip, at generation time
- Write case id, arm, attempt and the cost the app shows before clicking generate. Screenshot the settings and cost.
- `minutes`: generate click to finished clip. `credits`: the cost shown; if none, the balance difference (both balances in `notes`).
- Download as `evidence/p2_<arm>_a<attempt>.mp4` (build: `p2_<arm>_b<NN>.mp4`).
- Gut call (acceptable yes or no, `RUBRIC.md`) right away, before scoring.
