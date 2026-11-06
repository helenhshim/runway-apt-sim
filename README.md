# runway-apt-sim

Can a video model take my 3D furniture plan and show it in my real apartment? A small, pre-registered, blind-scored eval of Runway's Gen-4.5 against the strongest other image-to-video models Runway hosts, on one real living room.

**Case study:** [helenshim.me/projects/astra-room-models](https://www.helenshim.me/projects/astra-room-models) · **Plan:** [PRD](docs/PRD.md) and [technical design](docs/TDD.md) · **Results:** [`p2/FINDINGS.md`](p2/FINDINGS.md)

## The user problem

People furnish rooms they can't preview. A 3D planner like Astra gets the layout right, but the result still looks like a render, so you end up judging a sofa in a room that doesn't look like yours. I wanted to know whether a video model can close that gap: take one eye-level render of my planned living room and turn it into a walkthrough that looks like my real apartment, realistic enough to decide on before I buy.

For that job, the failure that matters isn't an ugly clip. It's a wrong room: a moved doorway, a chair that wasn't in the plan, a sofa that morphs. So the eval scores fidelity (is this still my room, and my plan?) separately from realism (does it look like real footage?), and counts cost per clip I'd actually use, since users pay for every reroll.

I ran my own eval instead of reading a leaderboard because the public boards rank general preference, not "keep my room." They also disagree with each other (Gemini Omni 1.1 Flash is #2 on one board and #14 on the other), and Gen-4.5 has no public image-to-video rank at all.

## What I found

- **Realism isn't the bottleneck. Fidelity at reveals is.** 5 of 6 clips scored realism 4 or higher, but 3 of 6 failed, and all 3 failed at the same reveal: the left doorway the start frame only half shows.
- **The most realistic clip was the most wrong.** Gemini's C1 scored realism 5 and plan fidelity 1: a fake nook where the doorway should be. Judged on looks alone, it wins.
- **Acceptable clips:** Seedance 2.5 2 of 2, Gemini Omni 1.1 Flash 1 of 2, Gen-4.5 0 of 2. With 2 clips per model this is a signal, not a ranking.
- **Cost per acceptable clip:** Gemini 102 credits, Seedance 150, Gen-4.5 had none. Gemini is cheaper, but its one failure was the real-looking wrong room, the worst kind of cheap for this job.

| | Gen-4.5 | Seedance 2.5 | Gemini Omni 1.1 Flash |
|---|---|---|---|
| Acceptable | 0 of 2 | 2 of 2 | 1 of 2 |
| Real-room fidelity | 1.0 | 5.0 | 3.0 |
| Plan fidelity | 3.0 | 5.0 | 3.0 |
| Realism | 3.5 | 4.0 | 4.5 |
| Temporal consistency | 3.5 | 5.0 | 3.5 |
| Credits spent | 115 | 300 | 102 |

Scores are 1 to 5, mean of 2 clips, from [`p2/results_p2.json`](p2/results_p2.json).

## What I'd hand to a research team

Each recommendation is tied to a logged failure. Full reasoning in [`p2/FINDINGS.md`](p2/FINDINGS.md#recommendations).

1. **Anchor the reveal.** All 3 failures happened at the left doorway (A1 door closed, A2 invented corner, C1 fake nook). Train and test on frame-edge reveals in interiors.
2. **Keep in-frame object identity.** Gen-4.5 got the stools wrong in all 3 build clips and morphed them in A2. Seedance and Gemini kept them every time.
3. **Score fidelity separately from realism.** A blended preference score would have passed C1.
4. **Don't trust warping error as a temporal stand-in.** It agreed with my temporal score on 3 of 6 clips and missed C1 entirely (see below).

The launch proposal that follows: a **reveal-fidelity slice** in Gen-4.5's eval suite. Interior start frames, each with a few written checks for what has to stay true as half-shown areas come into view, scored for fidelity apart from realism, by a person until an automated check agrees with people.

## How the eval is built

- **Pre-registered.** The rubric, prompt, inventory, log schema and three hypotheses (each with a kill condition) were committed in [`f589500`](https://github.com/helenhshim/runway-apt-sim/commit/f589500) at 13:50 on 2026-11-05. The six scored clips were logged at 14:39 and scored after that. The repo was private at freeze time and made public later; the commit dates are unchanged.
- **Build first, then a frozen eval.** Each model got the same 3 logged build iterations in the same order ([`p2/build_log.csv`](p2/build_log.csv)). The eval prompt is the build prompt that worked best across all three models, not tuned to one. Build clips are never scored.
- **Fair by construction.** Same start frame, 720p, 16:9, 5 s, picked by hand in Runway's video picker (not through Agent). Gen-4.5 takes no reference image or last frame, so no arm got one.
- **Blind.** [`p2/blind.py`](p2/blind.py) copies the clips to shuffled ids (B01 to B06). I scored all six in one sitting and opened the key only after the last row.
- **Anchored rubric.** Four criteria with 1 to 5 anchors ([`p2/RUBRIC.md`](p2/RUBRIC.md)). Real-room fidelity is checked against 8 landmarks and written reveal checks from [`p2/INVENTORY.md`](p2/INVENTORY.md). Failures are typed from a 16-type list ([`p2/FAILURE_TYPES.md`](p2/FAILURE_TYPES.md)).
- **Rehearsed.** I rehearsed the rubric on one build clip before the freeze. That caught a gap (it didn't say where an invented piece counts), fixed before the freeze.
- **Gut call as a check.** I logged a yes or no for each clip before scoring it. It agreed with "all four scores at 4 or higher" on 6 of 6.

## Pipeline and tests

```
p2/log.csv ──▶ validate_p2.py ──▶ summarize_p2.py ──▶ results_p2.json ──▶ case study page
p2/build_log.csv ──▶ validate_build_log.py
clips ──▶ blind.py (shuffle for scoring)      clips ──▶ warp_metric.py (automated temporal check)
```

Every script was written test-first with fake rows and hand-computed expected numbers: 40 P2 tests and 25 P1 tests, all passing. The validator checks each row on entry (arm, scores 1 to 5, known failure types, no duplicate ids), so the log can't drift from the schema in [`p2/schema.sql`](p2/schema.sql). The summary refuses to write anything if the log doesn't validate.

## The metric that didn't work

I added one automated temporal metric, flow-based warping error ([`p2/warp_metric.py`](p2/warp_metric.py)), to see if it could stand in for my temporal score. It agreed on 3 of 6 clips: 1 hit, 2 quiet matches, 2 false alarms and 1 miss. It mostly tracks camera speed and softness. It missed C1, the worst clip, because a static fake nook stays consistent from frame to frame. Verdict: not worth scaling. Details in [`p2/WARP_RESULTS.md`](p2/WARP_RESULTS.md).

## Decisions and pivots

| Decision | Why |
|---|---|
| Stopped P1 (image staging) after one formal run | Runway Agent routed my edit to Nano Banana Pro, a third-party model, so P1 was testing Runway's product layer, not Runway's models. Reported as a pilot (n = 1) with the routing finding, and the card cost (20 credits) against the all-in cost (30) |
| Switched to image-to-video from the Astra render | The earlier plan, video-to-video on Aleph, needed an Astra walkthrough recording that doesn't exist |
| Picked models functional first, then by leaderboard, then in the picker | A popular model that can't take a start image can't do the task. One surface and one credit pool keep cost comparable |
| Rewrote the hypotheses myself before the freeze, five drafts down to three | The bets should be mine. Since I'd already seen these models on this frame, a kill is the more informative result |
| Dropped a compare-across-models tool | It works against Runway's router thesis, multiplies compute, and single samples mislead: spread within one model was as large as spread between models |
| Deferred the GWM Worlds probe and canceled the 24 h re-score | Protect the core eval. The limits say so |
| Applied the invented-piece rule unevenly, and logged it instead of editing the frozen log | C2's side table should have counted as a temporal event. Counted properly, Gemini's temporal mean drops from 3.5 to 3.0. The log stays as frozen |

The full dated log is in [`docs/PRD.md`](docs/PRD.md#decision-log).

## Limits

- n = 6: 2 clips per model, one room, one start frame, one 5 s forward push. Directional, not statistics.
- One scorer, single pass, no test-retest number. I may recognize a model's style even blind.
- The Astra render is AI-generated from photos, not measured. No hallway walk was recorded, so reveal checks are judged against a real photo and the start frame.
- Only models in Runway's picker. GWM Worlds wasn't run.
- Deviations are logged: one Gen-4.5 clip cost 55 instead of 60, one Seedance clip was an accidental generation accepted out of run order, and Gemini forced audio on.

## What's where

| Path | What |
|---|---|
| `p2/` | The eval: protocol (`README`, `PROMPT`, `RUBRIC`, `INVENTORY`, `FAILURE_TYPES`), logs, scripts, tests, `FINDINGS`, `WARP_RESULTS`, research notes (`I2V_RESEARCH`, `MODEL_SELECTION`, `EVAL_RESEARCH`) |
| `docs/` | Public copies of the PRD and the technical design |
| `protocol/` | P1, the image staging pilot, frozen at [`1e24e9e`](https://github.com/helenhshim/runway-apt-sim/commit/1e24e9e) and never edited |
| root `*.py`, `*.sql`, `tests/` | P1 log, validation, SQL roll-up and JSON export |
| `evidence/` | Inputs, photos and clips. Gitignored for privacy; only its README is tracked |

## Run it

Python 3. The validators, summary and blind script use the standard library only. `warp_metric.py` also needs OpenCV and NumPy (`pip install opencv-python numpy`).

```bash
python3 p2/validate_p2.py p2/log.csv               # check the scored log
python3 p2/validate_build_log.py p2/build_log.csv  # check the build log
python3 p2/summarize_p2.py p2/log.csv              # write p2/results_p2.json
python3 -m unittest discover -s p2/tests -v        # P2 tests
python3 -m unittest discover -s tests -v           # P1 tests
```

The clips aren't in the repo, so `blind.py` and `warp_metric.py` need your own files in `evidence/`.

Built with Claude Code: the validators, blind-scoring script, summary, metric and tests. The protocol, hypotheses, scores and calls are mine.
