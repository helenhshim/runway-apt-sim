# Seedance 15 s probe: GWM gate and a 15 s Seedance walk (T26, HEL-90)

Post-freeze exploration, 2026-11-05. Never mixed into the 6 scored rows in `p2/log.csv`. Scores below use the frozen rubric but are one person's single pass on one clip, not blind.

**Question:** Gen-4.5 came last on keeping my room intact (0 of 2 acceptable, both failed at the left doorway). GWM-1 is built on Gen-4.5. Does world-model training fix that over a long walk? And can a text prompt steer a room the start frame never shows (the dining nook)?

**Short answer:** I couldn't test GWM. I don't have access to GWM Worlds on my plan. So I ran the fallback: a single 15 s walk on Seedance 2.5, the eval winner, with no world model. It kept the living room through a pan away and back, including the left doorway where Gen-4.5 broke. It failed where nothing anchored it: the nook it had never seen came out as the prompt's words, not the plan's furniture. It also skipped the "turn around". A rerun with a reference image of the nook furniture got the chairs and pendant exactly right, but invented the nook's walls and windows, which the reference didn't show.

## Gate (GWM Worlds)
- Balance before: 1,095.
- **Failed at step one (17:24): no access to GWM Worlds.** No upload, export or cost could be checked; 0 credits spent. Logged as a `demo` row in `build_log.csv` (tag `ux`).
- This matches `I2V_RESEARCH.md`: Worlds is a research preview behind an access request, not self-serve.
- Finding: a paying Runway user can't reach Runway's own world model. The model built to fix long-horizon consistency can't be tried on the task where Gen-4.5 failed.

## Fallback: one 15 s Seedance 2.5 walk
- Why Seedance: it won the eval (2 of 2 acceptable, 5/5/4/5). Without a world model, a long clip from the best image-to-video model is what a user would reach for.
- Settings: 720p, 16:9, 15 s, audio off. Start frame `evidence/p2_astra_start.png` (Helen confirmed the upload). No last frame and no reference image, same as the eval.
- Prompt `p2/prompts/walk15.txt`: the eval prompt's room and material lines (via `gwm1.txt`), one nook sentence, and the whole path in one camera sentence (forward to the front door, turn around, back past the sofa into the nook, pause at the table, back to the start facing the hallway).
- Nook description: furniture from the Astra plan (round white table, four light wood chairs, white pendant), architecture from the real photo `evidence/input_nook_stripped.jpg` (floor-to-ceiling windows on the right wall, white sill, roller shade).
- Path changes during planning: a 20 to 30 s GWM round trip, then 4 chained 5 s Seedance clips, then one 15 s clip once Helen found Seedance goes to 15 to 20 s (no seams; 15 s for budget).
- Cost: **450 credits** (1,095 to 645), as expected at ~30 credits/s. No price shown before generating.
- Gut call: **yes**, it shows as my apartment.
- File: 1280x720, 24 fps, 361 frames, 15.04 s, `evidence/p2_walk15_seedance.mp4` (saved as a QuickTime .mov). Stills every 1.25 s in `evidence/stills/walk15/`.

## What the camera did
| Time | Camera | Facing |
|---|---|---|
| 0 to 2.5 s | Pushes forward toward the hallway | Start direction |
| 2.5 to 5 s | Pans right across the sofa and painting | Sofa wall |
| 5 to 11.5 s | Into the nook past the arc lamp, holds on the table | Nook |
| 11.5 to 15 s | Pans back left past the sofa | Start direction by 13.75 s |

It never turned around. It replaced the 180 with a pan right and back.

## Scores (draft, frozen rubric, living room and hallway)
| Criterion | Score | Why |
|---|---|---|
| Geometry | 5 | Every landmark in view kept at 0, 2.5 and 15 s. Reveal checks: front door yes, left doorway open with nothing behind it yes, ceiling step along the right wall yes. The 25%, 50% and 75% sample frames face the sofa and nook, so no landmarks are in view there. |
| Plan | 5 | Sofa, pillows, glass table with books and bowl, TV console, orange vase, rug, arc lamp, painting, stools, bench and blue art all pass, and they still match on the return. The Wassily chair only shows at the frame edge at 15 s. The mushroom lamp and plant never come into view (see frame 0 below), so they're not counted. |
| Realism | 4 | Daylight, dark plank floor, matte white walls and baseboards, contact shadows. One minor flaw: the TV shows no room reflection, same as both eval Seedance clips. |
| Temporal | 3 | One clear `path` event: the turn around is ignored. No flicker; brightness changes follow what's in frame, not frame-to-frame pulses. |

## Nook (new; not in the start frame)
Furniture is judged against the Astra plan, architecture against `input_nook_stripped.jpg`.

| Check | Result |
|---|---|
| Placement | Pass. Right of the sofa past the arc lamp, where the plan has it. |
| Table | Marginal. Round, white, pedestal, but a fluted column, not the plan's tulip base. |
| Chairs | **Fail.** Four light wood chairs, but wishbone style. The plan has molded plywood chairs on chrome legs. |
| Pendant | Marginal. A white paper globe, not the plan's white dome. |
| Windows | Fail. Black frames with a radiator, on two walls. The real nook has white-framed floor-to-ceiling windows on one wall, with a sill. |
| Walls and floor | Pass. White walls, the same dark wood floor. |
| Nothing extra | Pass. No extra room, door or side table. |

Plan score for the nook alone would be 3 (one fail on a non-hero piece plus marginals).

## Drift (landmarks kept, out of 8)
The brief asked for 5, 10, 15 and 20 s. The clip is 15 s, and the camera faces away from the landmarks from about 3 to 13.5 s.

| Time | Kept / in view | Notes |
|---|---|---|
| 0 s | 8 / 8 | Pushed in compared with the start frame |
| 5 s | n/a | Facing the sofa and painting |
| 10 s | n/a | Facing the nook |
| 15 s | 8 / 8 | Same order, straight edges, doorway open |

No drift after 12 s out of view. This is the closest thing to "turn around, and what was behind you is still there" this probe could test.

## Loop closure
Final frame against frame 0 and the start frame: sofa, pillows, stools, left doorway, front door, arc lamp, painting, glass table with books and bowl, and TV console all match. **Pass.** The end spot is a little left of and higher than frame 0. The end frame is darker only because it's framed on the sofa wall.

## Frame 0 is not the start frame
Frame 0 is pushed in compared with `p2_astra_start.png` (mean pixel difference 52, against 2.9 for eval clip B1). Helen confirmed she uploaded the start frame. So at 15 s, Seedance didn't hold the first frame exactly: the Wassily chair, plant and mushroom lamp start out of shot. The 5 s eval clips didn't do this. With one clip, I can't say if it's the 15 s length or chance.

## Failures (`FAILURE_TYPES.md`)
| Time | Type | Severity | What |
|---|---|---|---|
| ~3 to 13 s | path_ignored | 2 | Turn around replaced by a pan right and back |
| ~7.5 to 11.5 s | identity | 2 | Nook chairs wishbone instead of the plan's molded plywood; table and pendant off in one detail each |
| ~5 to 11.5 s | invented_area | 2 | Nook windows black-framed on two walls, not the real white floor-to-ceiling windows on one |
| 0 s | (not a type) | | Frame 0 pushed in from the uploaded start frame |

Worst failure: **nook identity**. The model drew the words ("round white table, four light wood chairs, white pendant"), not the pieces. Text gets the category, not the piece.

## Side by side with Gen-4.5 (A1, A2 from `FINDINGS.md`)
| | Gen-4.5 A1 | Gen-4.5 A2 | Seedance 15 s walk |
|---|---|---|---|
| Length | 5 s | 5 s | 15 s |
| Left doorway | Closed at 4.75 s | Replaced by an invented corner by 2.5 s | Open and unchanged at 0, 2.5 and 15 s |
| Stools | Wrong in every build | Morphed | Held, and the same on the return |
| Geometry / plan / realism / temporal | 1 / 3 / 4 / 5 | 1 / 3 / 3 / 2 | 5 / 5 / 4 / 3 |
| Worst failure | opening | invented_area | identity (nook, unseen) |

## Rerun (the one allowed rerun)
Helen approved the walk 1 scores (2026-11-05) and wanted a version with the plan's chairs and pendant.
- **Reference image:** `evidence/p2_nook_ref.png`, the nook cropped from the Astra overhead (`astra_living_staged_reference.webp`): Series 7 style molded plywood chairs on chrome legs, tulip table, white ribbed saucer pendant. Seedance takes reference images (`build_log.csv`, T23); walk 1 used none.
- **Prompt `p2/prompts/walk15_v2.txt`:** names the pieces by design (Saarinen tulip table, Arne Jacobsen Series 7 chairs, ribbed saucer pendant) and says what they are not (no armrests, no spindles). Window wording tightened (thin white frames, right wall only, no radiator, no black frames). The path changes from "turn around" to the pan right and back that Seedance did anyway.
- Same start frame, settings and length. Cost about 450, leaving about 195.
- Confound: three things change at once (reference, wording, path). If the nook comes out right, this can't say which one fixed it. The reference is the most likely, since walk 1 matched every noun it was given and still drew the wrong pieces.

### Rerun result
- File `evidence/p2_walk15_v2_seedance.mp4` (QuickTime .mov from Runway, 1280x720, 24 fps, 361 frames). Stills in `evidence/stills/walk15_v2/`. Cost about 450 (balance about 195, inferred, not read).
- **Nook furniture fixed.** Helen: the chairs and lamp came out exactly right. Series 7 shell chairs on chrome legs, a tulip table on a flared base, and the ribbed saucer pendant all match the plan.
- **Nook architecture broke instead.** There's no wall pier or opening between the living room and the nook, so the nook runs straight on from the arc lamp. A slanted, attic-like wall plane sits above the table. The window frames are black again, despite "thin white frames" in the prompt. Helen's read: no reference showed the nook's architecture. The overhead crop shows the furniture, not the walls and windows from eye level.
- **Living room held again, and better.** Frame 0 is much closer to the start frame (mean pixel difference 19.7 vs 52). Wassily, plant and mushroom lamp are all in view at 0 s and again at 15 s.
- **Path followed.** Forward, pan right into the nook, hold, pan back. No `path` event this time.
- **Loop closure: pass.** The 15 s frame matches frame 0 piece for piece.
- Read across both walks: the reference fixed what it showed (the furniture) and nothing else. The windows got the same black frames with or without the words. **Pictures steer what they show; words don't steer much at all.**

## Verdict
- **Does GWM fix what Gen-4.5 broke?** Untested. I couldn't get access, and that's a finding in itself.
- **What the probe does show:** the bar GWM has to clear is higher than Gen-4.5's results suggest. A third-party image-to-video model in Runway's own picker already keeps the room over 15 s, including the doorway Gen-4.5 broke and a return after 10 s looking away.
- What no model did was build an unseen room from words. A reference image fixed exactly what it showed: the rerun got the chairs and pendant right, but invented the nook's walls and windows, which the reference didn't show. That's the case a world model is pitched for: a space you have to get right without having seen it.
- Total T26 spend: about 900 credits (0 for the gate, 450 per walk), above the 400 planned. Helen raised the cap on purpose.

## For the case study: "A 15 s walk on Seedance 2.5 (GWM wasn't available)"
The video here is Seedance 2.5, not a world model. It's the hero demo for T22b (HEL-103): `evidence/p2_walk15_v2_seedance.mp4`, the rerun with the nook reference.

I wanted to test it, and couldn't: GWM Worlds isn't open on my plan. So I ran the closest thing I could, a 15 s walk on Seedance 2.5, the model that won my eval, from the same start frame where Gen-4.5 broke the doorway twice. Seedance held the living room the whole way, including a pan away and back after about 10 s looking at the dining nook. Where it broke was the nook itself. The start frame never shows it, so the model only had my words: it drew a round white table and four wood chairs, but the wrong chairs and the wrong windows. When I added a reference image of the planned nook furniture, it got the chairs and the pendant exactly right, and then invented the nook's walls and windows, which the reference didn't show. Pictures steer what they show. Words barely steer at all. That's the gap I'd want a world model to close, and the eval I'd want before saying it does: hold what you saw, and get what you didn't see right from the plan, not just the prompt.
