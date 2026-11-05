# Prompts (FROZEN 2026-11-04)

## Inputs
| File (in `evidence/`, gitignored) | What | Given to the models? |
|---|---|---|
| `p2_astra_start.png` | Eye-level Astra render from the taped spot: 16:9, daylight, ceiling on, no cutaway | Yes, as the start frame for every arm |
| `p2_astra_end.png` | Optional Astra render about 1.5 m further along the path | Only if every scored arm takes a last frame |
| `p2_photo_a.jpg` | Real photo from the taped spot, 16:9, 1x lens, EXIF stripped | Only as a materials reference, and only if every scored arm takes one |
| `p2_photo_b.jpg`, `p2_walk.mp4` | Real end photo and a 5 s phone walk from A to B | Not used. No hallway-direction walk was recorded (`p2_walk.mp4` does not exist); ground truth for scoring is `p2_photo_a.jpg` and the start frame, never given to the models |

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

## Eval prompt (prompt_id = p2v1, frozen)
`p2v1` is `b03`, byte for byte (`p2/prompts/p2v1.txt`):
> Photorealistic phone video of this living room in daylight. The camera moves slowly forward in a straight line toward the hallway and the front door at the far end, at walking pace and eye level, without turning. Keep the room exactly as shown: the same walls, ceiling, doorways and floor, and every piece of furniture in the same place, shape and color. Nothing appears or disappears. Soft natural shadows under the furniture, real materials. No people, no text. Real materials of this apartment: a dark brown wood plank floor with visible grain, matte white walls with white baseboards, and a step in the ceiling along the right wall. Shot on a phone, not a 3D render. Shot on an iPhone, slight natural grain and lens softness.

**Why `b03`:** it was picked across all three arms, not for one. Candidate `b03`, backup `b02` (T25, 2026-11-04). `b03` adds one sentence ("Shot on an iPhone, slight natural grain and lens softness.") to `b02`, applied to every arm. In the b03 runs all three arms kept the camera moving forward with no `path` failure and still read as realistic; Gemini kept the TV reflections, Gen-4.5 showed them less, Seedance not at all and read slightly too soft. It did not cure the identity differences (Gen-4.5's stools, Gemini's invented side table), which are what the eval is meant to measure. Backup `b02` is not used. If `p2v1` is ever changed it becomes a new version (`p2v2`), committed before use, and never mixed with `p2v1` rows.

No reference image and no last frame for any arm: Gen-4.5 takes neither, so by the fairness rule no scored arm gets one (checked 2026-11-04).

## Settings (per arm, frozen)

Observed 2026-11-04: all three models run on the current plan and are named in the picker, but the app shows no credit cost before generating. Cost per clip is therefore the balance before minus the balance after.

| Arm | Model | Credits per clip (from the balance) | Start image | Last frame | Reference image | 16:9 | Duration set | Other defaults touched |
|---|---|---|---|---|---|---|---|---|
| A | Gen-4.5 | 60 | yes | no end image; "use frame" only turns a frame of a generated clip into a new input (checked 2026-11-04) | no (checked 2026-11-04) | yes | 5 s | audio off, enhancer off |
| B | Seedance 2.5 | 150 | yes | yes (checked 2026-11-04, not used) | yes (checked 2026-11-04, not used) | yes | 5 s | audio off, enhancer off |
| C | Gemini Omni 1.1 Flash | 51 | yes | yes (checked 2026-11-04, not used) | yes (checked 2026-11-04, not used) | yes | 5 s | audio off, enhancer off |

Audio: set off on every arm. Seedance and Gemini defaulted to audio on in the build (footsteps added); audio is not scored. If an arm cannot turn it off, leave the default, write "audio forced on" in `notes`, and do not retry for it. Prompt enhancer off.

## Run order (eval)
A1, B1, C1, A2, B2, C2. Case id `astra_walk`.

## GWM (deferred, outside the frozen protocol)
The GWM Worlds probe was deprioritized by Helen on 2026-11-04 (HEL-90 / T26) and is not a gate for the freeze. It is not an arm and is not scored, and nothing in the eval depends on it. If it is run later it is a separate side note, reported beside Gen-4.5, never ranked against B and C.

## Per clip, at generation time
- Write case id, arm, attempt and the cost the app shows before clicking generate. Screenshot the settings and cost.
- `minutes`: generate click to finished clip. `credits`: the cost shown; if none, the balance difference (both balances in `notes`).
- Download as `evidence/p2_<arm>_a<attempt>.mp4` (build: `p2_<arm>_b<NN>.mp4`).
- Gut call (acceptable yes or no, `RUBRIC.md`) right away, before scoring.
