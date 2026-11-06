# TDD: Astra render to real-world video (P2)

Helen Shim · written 2026-11-03, before the build

> **About this copy.** This is the public version of the technical design I wrote before building anything. Internal references (ticket numbers, private links, local paths) are removed and cited commits use their current hashes. The design is left as written, because the gap between plan and build is part of the record. What changed is listed right below. The requirements are in [`PRD.md`](PRD.md) and the results in [`p2/FINDINGS.md`](../p2/FINDINGS.md).

## What changed between this design and the build

| Planned here | What happened | Why |
|---|---|---|
| End frame (Astra, 1.5 m further along) and an end photo plus a 5 s phone walk as ground truth | Neither was used. Photo A and the start frame are the ground truth | Gen-4.5 takes no last frame, so no arm gets one (fairness rule). The walk was never recorded |
| Iteration 2 adds the real photo as a reference image | Iteration 2 describes the real materials in words instead | Gen-4.5 takes no reference image, so no arm gets one |
| GWM Worlds probe before the eval | Deferred, not run before the freeze | Deprioritized to protect the eval |
| 24 h re-score as part of the eval of the eval | Canceled | Second in the cut order; the findings report single-pass scoring and say so in the limits |
| 11 tests (validator and blind script) | 40 P2 tests: also the build-log validator, the summary script and the warping metric, each written test-first | The rest of the pipeline got built |
| Eval protocol draft at `21a1939` | Frozen at [`f589500`](https://github.com/helenhshim/runway-apt-sim/commit/f589500) on 2026-11-05, before any scored clip | Build observations changed the protocol only before the freeze, as planned |

## Goal

Build first: a Gen-4.5 video that goes from my eye-level Astra render to a photoreal walkthrough of my real living room, as the MVP. Then the same build on Seedance 2.5 and Gemini Omni 1.1 Flash, plus a GWM Worlds probe. The eval and the case study come after, fed by observations logged during the build.

- **What gets built:** a 5 s eye-level walkthrough of the Astra living room, turned into footage that looks like my real apartment (floor, walls, light from my photos), with the Astra furniture intact.
- **Who it's for:** me as the renter deciding on furniture, and a model research team, who should see real output first and evidence second.
- **What it isn't:** image staging. That was P1 (one formal run, now a pilot). This replaces it as the headline.
- **Success for the build:** at least one clip I'd show as "my apartment with this furniture", plus a logged observation for every generation made along the way.

## Build-first sequence

Four phases, three gates. Each gate has to pass before the next phase starts.

```
inputs ──gate: start frame and photo A ready──▶ build (3 iterations x 3 models)
       ──gate: protocol frozen in a commit────▶ eval (3 models x 2 clips, blind)
       ──gate: every row scored and valid─────▶ findings and case study
```

The freeze commit lands before the first scored clip, same rule as P1.

## Pipeline and components

The build and the eval share one start frame, the eye-level Astra render. The only thing passed from build to eval is the chosen prompt, frozen in a commit.

```
build row:  start frame + prompt b01..b03 ──▶ Runway picker ──▶ clip ──▶ p2/build_log.csv (observations, never scored)
eval row:   start frame + frozen p2v1 ─────▶ Runway picker ──▶ clip ──▶ blind.py ──▶ scores ──▶ p2/log.csv
page:       p2/log.csv ──▶ validate_p2.py ──▶ summarize_p2.py ──▶ results_p2.json ──▶ case study
```

## Build routes and models

One route: an eye-level Astra still, rendered from the same spot as a new 16:9 real photo, animated with image-to-video into a 5 s slow push toward the hallway. The earlier video-to-video route on Aleph is dropped: no Astra walkthrough recording exists.

| Input | Made how | Given to the models? |
|---|---|---|
| Start frame: eye-level Astra render, 16:9, daylight, ceiling on, no cutaway | Astra, from the taped spot | Yes, every model |
| End frame: Astra render from about 1.5 m further along the path | Astra | Only if every scored model takes a last frame |
| Real photo A, 16:9, 1x lens, from the taped spot | Phone, EXIF stripped | Only as a materials reference, and only if every model takes one |
| Real photo B and a 5 s phone walk from A to B | Phone | Never: ground truth for scoring |

| Model | Role | Credits per 5 s at 720p (verify in app) |
|---|---|---|
| Gen-4.5 | Scored, Runway; the MVP | About 60 |
| Seedance 2.5 | Scored | About 150 |
| Gemini Omni 1.1 Flash | Scored | About 50 |
| GWM Worlds | Probe, if it passes the upload, export and credit gate | Not published |

Build loop rules:
- Change one thing per iteration: prompt wording, reference image on or off, duration, or camera path. Write what changed in the build log.
- Same 3 iterations for every model, in order: base prompt; add the real photo as reference; one wording fix from what broke. Gen-4.5 runs first. Extra demo tries beyond 3 are logged as demo only and left out of the comparison.
- Pick models by hand in the video picker, not through Agent. In P1, Agent chose the model for me (Nano Banana Pro).
- Prices and the inputs each model accepts are read in the app before the first generation. Nothing here assumes a price.

## Observation log

Every generation during the build gets one row in [`p2/build_log.csv`](../p2/build_log.csv) within 5 minutes, in my own words. This is the raw material for the eval design and the case study, so nothing waits until the end.

| Column | What goes in it |
|---|---|
| when | Timestamp |
| model | As the picker names it |
| route | Build iteration (b01 to b03) or demo |
| prompt_id | Saved prompt file, for example `p2/prompts/b03.txt` |
| changed | The one thing changed from the last try |
| credits_shown, balance_after | Cost on screen and balance after |
| minutes | Generate click to finished clip |
| output_file | Saved clip in `evidence/` |
| keep | Yes or no: would I show it |
| tag | broke, surprised, cost, ux, routing or quality |
| observation | One or two sentences: what I saw, with a timestamp in the clip if it broke |

Build rows are never scored and never mixed into the eval log. The existing `demo_log.csv` stays for P1.

## Eval layer, after the build

The eval runs on the same start frame, with the prompt the build settled on, frozen in a commit before the first scored clip. The protocol is drafted in `p2/`: 3 arms x 2 clips, four criteria with 1 to 5 anchors, blind scoring.

How building first stays credible:
- **The freeze rule still holds.** Build clips are exploration. Only clips generated after the freeze commit are scored.
- **The frozen prompt is the best of the 3 build variants across all three models,** so it isn't tuned to Gen-4.5 alone. Gen-4.5's build runs a day earlier than the others, and the write-up says so.
- **Observations from the build can change the protocol, but only before the freeze.** For example, a failure type I keep seeing gets added to [`p2/FAILURE_TYPES.md`](../p2/FAILURE_TYPES.md).
- **What the eval adds over the build:** same input and prompt for every arm, 2 attempts each, scores I can defend, and cost per acceptable clip.

## Budget

Everything runs on Runway credits, so there is one pool: 420 observed on Nov 2, plus a one-month Pro upgrade (about 1,300 credits needed at Runway's listed prices for 5 clips per scored model). The eval reserve is set aside first and the build spends what is left.

- **Eval reserve** = 2 x (price of arm A + B + C) + 3 retries at the most expensive price. Filled once prices are read in the app.
- **Build ceiling** = balance minus eval reserve. When it's reached, the build stops, finished or not.
- **If the reserve alone exceeds the balance:** drop to 2 arms or top up, decided before the first build generation.
- **Tracking:** every spend goes in the build log and the credit ledger. P1 spend so far: 25 pilot, 25 voided attempt, 30 all-in for run 1 (20 on the card).

## Testing, risks and open questions

Scripts are written test-first with fake rows, like P1. Already built and passing at design time: [`p2/validate_p2.py`](../p2/validate_p2.py) and [`p2/blind.py`](../p2/blind.py), 11 tests. Still to build: a build-log check, then the P2 roll-up and a new `p2/results_p2.json` export, so the P1 `results.json` shape the page reads stays untouched.

| Risk | Fallback |
|---|---|
| No model can hold a 5 s push | Fallback ladder frozen before the eval: 3 s push, then a locked-off shot with subtle motion |
| Prices too high for 3 arms | 2 arms, or a top-up, decided before the first build generation |
| A model updates mid-week | Log the date of every clip; the write-up says so |
| Privacy: uploads go to third-party models through Runway, and some photos show the view outside | Only the living room render and photo are used; views outside are blurred or cropped before anything is published |
| The Astra model is AI-generated, not measured | "Kept" means kept from the plan; the write-up says so |

Open at design time:
- Shoot photos A and B and the phone walk from the taped spot
- Re-render Astra at eye level (start, and optionally end frame)
- Re-pick the 8 landmarks on photo A
- Confirm 16:9 for each model; does Gen-4.5 take a last frame or reference image?
- GWM gate: upload, export, credit cost
- Stretch: a bedroom clip, build only?

The work was split into tickets only after this design was approved: inputs, build log, Gen-4.5 build (MVP), Seedance and Gemini builds, GWM probe, rubric rehearsal and freeze, generate, blind score, summary and metric, findings, publish. The PRD was rewritten from this design.
