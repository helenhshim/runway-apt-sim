# P2: Astra render to real-world video (DRAFT, not frozen)

P1 (`protocol/`, frozen at 1e24e9e) tested image staging and stopped after one formal run. P2 is the headline. Nothing in `protocol/` changes.

- **Question:** starting from one eye-level Astra render of my planned living room, which image-to-video model turns it into a walkthrough that looks like my real apartment while keeping the plan and the room intact as the camera moves, and what does one acceptable clip cost?
- **Why this test:** I want to see my real apartment with the furniture I planned, as real-world video. Going from a 3D plan straight to video tests scene understanding, which is where Runway is heading (GWM).
- **Surface:** Runway's video model picker, model chosen by hand. Not Agent: in P1, Agent picked the model (Nano Banana Pro), and here the model is the variable.
- **Arms (locked 2026-11-03):** A = Runway Gen-4.5, B = Seedance 2.5, C = Gemini Omni 1.1 Flash. All at 720p, 16:9, 5 s, start frame only. Picked functional first (takes a start image), then by image-to-video leaderboard rank, then in the picker; see `I2V_RESEARCH.md`.
- **Probe, not scored against the arms:** GWM Worlds, Runway's world model built on Gen-4.5. Gate before the freeze: the Astra still uploads as the first frame, a 5 s clip exports, and a credit cost shows. If any fails, that is a finding and GWM stays out.
- **Design:** build first (3 iterations per arm, logged, never scored), then a frozen eval of 3 arms x 2 attempts = 6 scored clips. Same start frame, prompt, settings and duration for every arm. Interleaved run order. Shuffled, renamed clips for scoring.
- **Rule:** the rubric, prompt, inventory and log schema are committed and pushed to a public repo before the first scored clip.
- **Status:** draft. One scorer, one room, n = 2 per arm.

The Astra render is AI-generated from photos, not measured.

## Files
| File | What |
|---|---|
| `PROMPT.md` | Inputs, build prompts, eval prompt slot, settings per arm, run order, GWM probe |
| `INVENTORY.md` | Landmarks and furniture read off the Astra start frame, the input baseline check, ground-truth files |
| `RUBRIC.md` | Four criteria, 1 to 5 anchors, acceptable gut call, severity |
| `FAILURE_TYPES.md` | Failure types, including temporal ones (must match `validate_p2.py`) |
| `schema.sql`, `validate_p2.py` | 24-column log, one row per scored clip, and its validator |
| `blind.py` | Copies clips to random ids for scoring, key kept in `evidence/` |
| `build_log.csv`, `validate_build_log.py` | One row per build generation (never scored) and its check |
| `prompts/` | Build prompts `b01`, `b02` (and `b03` once chosen), exactly as pasted into the app |
| `I2V_RESEARCH.md` | Current model research (image to video, GWM, failure modes) |
| `MODEL_SELECTION.md`, `EVAL_RESEARCH.md` | Earlier research pass (video editing, eval methods, world models) |
| `tests/` | Fake rows only: `python3 -m unittest discover -s p2/tests -v` |
| `warp_metric.py` | Automated flow-based warping error per clip, with floor and spike times (T32); test in `tests/test_warp_metric.py` |

## Logging a build generation
Within 5 minutes of each generation, add one row to `build_log.csv` (or tell Claude in this session and it adds the row), then run:

```bash
python3 p2/validate_build_log.py p2/build_log.csv
```

| Column | What goes in it |
|---|---|
| when | `2026-11-03 18:05` |
| model | As the picker names it, for example `Gen-4.5` |
| iteration | `b01`, `b02`, `b03`, `demo` or `draft` |
| prompt_id | The prompt file used, for example `b01` |
| changed | The one thing changed from the last try (blank on the first) |
| credits_shown, balance_after | The cost on screen and the balance after; at least one is required |
| minutes | Generate click to finished clip |
| output_file | The clip's file name in `evidence/`, unique per row |
| keep | `yes` or `no`: would I show it |
| tag | `broke`, `surprised`, `cost`, `ux`, `routing` or `quality` |
| observation | One or two sentences in my words, with a timestamp in the clip if something broke |

## Hypotheses
Written 2026-11-04, in Helen's own words, before any scored clip. Measures are from `RUBRIC.md`. The "why" column is high-level reasoning from the PRD and Research tab, not from the build clips; I have seen these models on this exact frame, so a confirmed hypothesis is a replication and a kill is the more informative result. Same text as the PRD. With 2 clips per model, results are directional, not statistics.

| # | Hypothesis (my words) | Why I think so (high level, before scoring) | Measure | Kill condition (what would disprove it) |
|---|---|---|---|---|
| H1 | The model that looks most like real footage is not 1:1 with the render I provide and is more prone to making up furniture (Gemini). | For this job a wrong room is worse than a less pretty clip. A model rewarded for looking like real footage fills gaps with plausible furniture instead of matching my plan. (From the PRD and Research tab framing, confirmed by Helen.) | Plan fidelity (criterion 2) against realism (criterion 3), mean of 2 clips per model, plus a count of pieces in the clip that are not in the render (for example the side table). | Gemini's plan fidelity is the same as or higher than Seedance's, or Gemini has no more invented pieces than either other model. |
| H2 | The cheap one is close enough. I would have used Gemini over the 150 credits, and it was faster. | The job is to judge a plan before I buy, so a clip only has to be good enough to decide on. Paying about 3x for the top-ranked model only makes sense if the extra quality changes that decision. (Listed credits, not build results.) | Gut-call acceptable rate and credits per acceptable clip (credits spent divided by acceptable clips), at 51 (Gemini), 60 (Gen-4.5) and 150 (Seedance) credits. | Gemini has fewer acceptable clips than Seedance. 1 of 2 acceptable counts as close enough; 0 of 2 does not. |
| H3 | Failures start when something is hidden and comes back, or when an area the start frame never showed comes into view and the model makes something up (the side table). | A model that repaints each frame instead of holding one room has nothing to anchor to once something leaves the frame or a new area enters it. That is where I expect a scene-understanding failure. (From the Research tab questions on scene understanding and when it breaks.) | Pop and morph events in criterion 4, plus invented pieces, split by whether they follow something returning from behind an object or a new area entering the frame, against drift or flicker with no such trigger. | Most temporal events across the 6 clips are not tied to something returning or an area newly coming into view. |

**Scope note (Helen):** the test is a 5 s clip. On a longer clip, matching the render 1:1 would matter much more than realism, especially for this task, and that could vary task by task. H1 and H2 are claims about 5 s only.

Stools: in the build, Gen-4.5's stools were wrong in b01 to b03 and Gemini's matched the real thing, so stools do not count against Gemini in H1.

Build-phase observation, not a hypothesis (the prompt is frozen at the freeze): changing the prompt and the model made the clips look more like my room, but I would want to edit the pieces in the video model to match the original pieces, since the Astra render did not get them 1:1.

## Fairness rules
- Same start frame (`evidence/p2_astra_start.png`), prompt text and settings for every arm.
- A reference image or a last frame is used only if every scored arm accepts it; otherwise no arm gets it.
- 720p, 16:9, 5 s for every arm; anything a model forces is logged in `notes`.
- Model defaults otherwise. Audio off. Any prompt enhancer off.
- Run order interleaved: A, B, C for attempt 1, then the same for attempt 2.
- First outputs only. No prompt changes after the freeze; a changed prompt is a new version, committed before use, never mixed.
- Scoring in a separate pass, on clips renamed by `blind.py`. I may recognize a model's style; the page says so.

## Stop rules and fallback ladder
- Exactly 2 scored clips per arm, acceptable or not.
- An error, refusal or timeout gets one retry with nothing changed. Not scored; credits logged in `notes` and the ledger.
- Fallback ladder, decided now: if the build shows no arm can hold a 5 s push, the eval uses a 3 s push; if that fails too, a locked-off shot with subtle motion. The step is chosen at the freeze from build evidence, never mid-eval.
- If prices put the plan over the cap, drop an arm before the freeze, never mid-run.

## Budget (from Runway's pages; fill from the app before the freeze)
| Arm | Model | Credits per 5 s at 720p (listed) | From the app |
|---|---|---|---|
| A | Gen-4.5 | about 60 | FILL |
| B | Seedance 2.5 | about 150 (80 minimum) | FILL |
| C | Gemini Omni 1.1 Flash | about 50 | FILL |

5 clips per arm (3 build, 2 eval) is about 1,300 credits plus drafts and retries. Runway Pro for one month.

## Filled before the freeze
1. Prices and input support per arm (tables above and in `PROMPT.md`).
2. Start frame saved, its landmarks and pieces written in `INVENTORY.md`, and the input baseline check done.
3. The eval prompt chosen from the build iterations, with the reason.
4. The fallback ladder step chosen from build evidence.
5. Hypotheses copied in.
6. Rubric rehearsed on one build clip; fixes logged.

## What is reused from P1 and what changed
- Reused: frozen-first rule, anchors decidable without gut feel, typed failure log with severity 1 to 3, acceptable gut call before scoring, CSV then validate, fake-row tests.
- Changed: image to video instead of image editing; criteria are real-room fidelity, plan fidelity, realism and temporal and scene consistency; new failure types; a 24-column log with `arm` and `blind_id`. The column names `geometry` and `temporal` keep their names but follow the new definitions in `RUBRIC.md`.
- Not yet built: the build log check and the P2 summary script that writes `p2/results_p2.json` (the P1 `results.json` shape is untouched).
