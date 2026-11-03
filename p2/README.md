# P2: Astra walkthrough to photoreal video (DRAFT, not frozen)

P1 (`protocol/`, frozen at 1e24e9e) tested image staging and stopped after one formal run. P2 is the headline. Nothing in `protocol/` changes.

- **Question:** given a camera path recorded in my Astra 3D model of the living room, which video model turns it into footage that looks like my real apartment while keeping the Astra layout and furniture intact frame to frame, and what does one acceptable clip cost?
- **Why this test:** I want to see my real apartment with the furniture I have planned, as realistic as possible. The Astra model fixes the plan; the video model's job is to make it look real without breaking it.
- **Surface:** Runway's video model picker, model chosen by hand. Not Agent: in P1, Agent picked the model (Nano Banana Pro), and here the model is the variable.
- **Arms:** Runway Aleph 2.0 against two other edit-video models hosted in the same picker. Chosen in pre-flight from Kling 4.0, Gemini Omni Flash and Grok Imagine, by price and by whether each accepts an input video plus a reference image. Final names go in the table below before the freeze.
- **Design:** 1 scenario x 3 arms x 2 attempts = 6 scored clips. Same input video, prompt, references and duration for every arm. Interleaved run order. Shuffled, renamed clips for scoring.
- **Rule:** the rubric, prompt, inventory and log schema are committed before the first scored clip. The commit history shows it.
- **Status:** draft. One scorer, one pass, one room, n = 2 per arm.

Astra renders and the Astra model are AI-generated from photos, not measured.

## Files
| File | What |
|---|---|
| `PROMPT.md` | Inputs, prompt text, settings, run order |
| `INVENTORY.md` | Landmarks and furniture pieces, read off the input recording before the freeze |
| `RUBRIC.md` | Four criteria, 1 to 5 anchors, acceptable gut call, severity |
| `FAILURE_TYPES.md` | P1 types that still apply plus temporal ones (must match `validate_p2.py`) |
| `schema.sql`, `validate_p2.py` | 24-column log, one row per clip, and its validator |
| `blind.py` | Copies clips to random ids for scoring, key kept in `evidence/` |
| `tests/` | Fake rows only: `python3 -m unittest discover -s p2/tests -v` |

## Hypotheses (each can be disproved; n = 2 per arm, so directional only)
| # | Hypothesis | Disproved if |
|---|---|---|
| H1 | My hunch: Aleph has the highest acceptable rate | Another arm's acceptable rate matches or beats Aleph's |
| H2 | Realism is easier than fidelity: every arm scores lower on the mean of geometry and plan than on realism | Fidelity mean >= realism mean for 2 or more arms |
| H3 | Retries drive cost: best-of-2 beats the mean by more than 0.5 on the four-criterion average | The gap is 0.5 or less, averaged over arms |
| H4 | Credits per acceptable clip differ by more than 2x across arms | All arms with an acceptable clip are within 2x, or fewer than 2 arms have one |

## Fairness rules
- Same input video, prompt text and reference images for every arm. If one chosen arm cannot take a reference image, no arm gets one (the prompt describes the materials in words either way).
- Same output duration and aspect ratio where the model allows; anything forced is logged in `notes`.
- Model defaults otherwise. Audio off. Any prompt enhancer or "improve prompt" toggle off.
- Run order interleaved: arm 1, arm 2, arm 3 for attempt 1, then the same for attempt 2.
- First outputs only. No prompt changes after the freeze; a changed prompt is a new version, committed before use, never mixed.
- Scoring in a separate pass, on clips renamed by `blind.py`. I generated them, so I may recognize a model's style; the page says so.

## Stop rules
- Exactly 2 scored clips per arm, acceptable or not.
- An error, refusal or timeout gets one retry with nothing changed. It is not a scored clip, but its credits are logged in `notes` and counted in the ledger.
- If pre-flight prices put the plan over the cap, drop an arm before the freeze, never mid-run.
- Stop all generation at the cap.

## Budget (fill from the app in pre-flight, before the freeze)
| Arm | Model (as the picker names it) | Credits per clip at the chosen duration |
|---|---|---|
| A | Aleph 2.0 | FILL |
| B | FILL | FILL |
| C | FILL | FILL |

Plan = 2 x (A + B + C) + one pre-flight clip on the cheapest arm + up to 3 retries at the most expensive arm's price. Cap = the observed balance before the first scored clip. Balance observed 2026-11-02: 420.

## Filled before the freeze
1. Arm names and prices (table above).
2. Whether each arm accepts an input video and a reference image, and its duration options (`PROMPT.md`).
3. The input recording saved and its landmarks and pieces written in `INVENTORY.md`.
4. One unscored pre-flight clip, scored with this rubric as a rehearsal; any anchor that is a coin flip gets fixed.

## What is reused from P1 and what changed
- Reused: frozen-first rule, 1 to 5 anchors decidable without gut feel, overlay check, typed failure log with severity 1 to 3, acceptable gut call before scoring, CSV then validate then SQLite roll-up, fake-row tests.
- Changed: new criteria (geometry fidelity to the input path, plan fidelity, realism against the real photos, temporal consistency), new failure types, new 24-column log with `arm`, `blind_id` and clip fields. `validate_log.py`, `rollup.sql` and `export_json.py` stay P1-only.
- Not yet built: the P2 roll-up and JSON export. They do not change what is recorded, so they can come after the freeze. `results.json` is read by the portfolio page; the P2 export will be a new file, `p2/results_p2.json`, so the P1 shape is untouched.
