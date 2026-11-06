# PRD: my apartment, furnished, on video (P2)

Helen Shim · written 2026-11-03, updated through the protocol freeze on 2026-11-05

> **About this copy.** This is the public version of the planning doc I worked from. Internal references (ticket numbers, private links, local paths) are removed and cited commits use their current hashes. Otherwise it's as written before the results came in. What actually happened is in [`p2/FINDINGS.md`](../p2/FINDINGS.md); the build plan is in [`TDD.md`](TDD.md).

## The user problem

People furnish rooms they can't preview. A 3D planner like Astra gets the layout right, but the result still looks like a render, so you're judging a sofa, a rug and a lamp in a room that doesn't look like yours. The question I wanted answered is whether a video model can close that gap: take my plan and show it in my real apartment, realistic enough to decide on before I buy.

For that job the failure that matters isn't an ugly clip. It's a wrong room: a moved doorway, a chair that wasn't in the plan, a sofa that morphs. A model can look completely real and still fail the user, because they'd be deciding on furniture that isn't there or a room that isn't theirs.

That's why I evaluated the models myself instead of trusting a leaderboard:
- **Public boards measure general preference, not "keep my room."** They rank on how good a clip looks to voters. Nothing tests whether a model stays faithful to a specific input space.
- **Runway's own model has no public image-to-video rank.** Gen-4.5 isn't on either image-to-video board, so any result here is new evidence.
- **The boards disagree.** Gemini Omni 1.1 Flash is #2 on one and #14 on the other. Disagreeing priors are a reason to test on a real task.
- **Users pay per generation, including rerolls.** The useful number is cost per clip I'd actually use, not the listed price.

## Summary

- **Build first, on all three models:** one eye-level Astra still in, a 5 s photoreal walkthrough out. Gen-4.5, Seedance 2.5 and Gemini Omni 1.1 Flash each get the same 3 iterations in the same order, and every generation is logged as an observation.
- **A world-model probe:** GWM Worlds, which is built on Gen-4.5, runs on the same still, to see what world-model training adds on a real room. (Deferred at the freeze, see the decision log.)
- **Then evaluate:** 3 models x 2 clips on one frozen prompt, scored blind on real-room fidelity, plan fidelity, realism and temporal and scene consistency. The eval is tested too: a re-score, gut call vs scores, and one automated metric.
- **What changed:** this replaces image staging (P1, a one-run pilot) and an earlier video-to-video plan on Aleph, dropped because no Astra walkthrough recording exists.

## Users and jobs to be done

Job: when I'm planning furniture for an apartment I live in, show me my real rooms with that plan, realistic enough that I can judge it before I buy.

| Who | What they need from the output |
|---|---|
| Renter (me, the test user) | Footage that looks like my apartment, not a render, with the planned pieces where I put them. A moved doorway or a morphing sofa is worse than a less pretty clip |
| A model research team | Real outputs on a real task, an honest comparison with other models, and failures typed and tied to fixes they could test |
| Me as practitioner | A build log and a reusable eval setup I can extend to other rooms or a real-photo interaction test |

The headline metric is the rate of clips I'd show as "my apartment with this furniture", not how good the clips look.

## Hypotheses

Each is meant to be disproved. Thresholds freeze with the protocol, before the first scored clip. With 2 clips per model, results are directional, not statistics.

| # | Hypothesis (my words) | Why I think so (before scoring) | Measure | What would disprove it |
|---|---|---|---|---|
| H1 | The model that looks most like real footage is not 1:1 with the render I provide and is more prone to making up furniture (Gemini). | For this job a wrong room is worse than a less pretty clip. A model rewarded for looking like real footage fills gaps with plausible furniture instead of matching my plan. | Plan fidelity (criterion 2) against realism (criterion 3), mean of 2 clips per model, plus a count of pieces in the clip that aren't in the render (for example the side table). | Gemini's plan fidelity is the same as or higher than Seedance's, or Gemini has no more invented pieces than either other model. |
| H2 | The cheap one is close enough. I'd have used Gemini over the 150 credits, and it was faster. | The job is to judge a plan before I buy, so a clip only has to be good enough to decide on. Paying about 3x for the top-ranked model only makes sense if the extra quality changes that decision. | Gut-call acceptable rate and credits per acceptable clip (credits spent divided by acceptable clips), at 51 (Gemini), 60 (Gen-4.5) and 150 (Seedance) credits. | Gemini has fewer acceptable clips than Seedance. 1 of 2 acceptable counts as close enough; 0 of 2 does not. |
| H3 | Failures start when something is hidden and comes back, or when an area the start frame never showed comes into view and the model makes something up (the side table). | A model that repaints each frame instead of holding one room has nothing to anchor to once something leaves the frame or a new area enters it. That's where I expect a scene-understanding failure. | Pop and morph events in criterion 4, plus invented pieces, split by whether they follow something returning from behind an object or a new area entering the frame, against drift or flicker with no such trigger. | Most temporal events across the 6 clips are not tied to something returning or an area newly coming into view. |

Written 2026-11-04 in my own words, before any scored clip; they replace five earlier drafts. Scope: the test is a 5 s clip. On a longer clip, matching the render 1:1 would matter much more than realism, and that could vary task by task, so H1 and H2 are claims about 5 s only. In the build, Gen-4.5's stools were wrong and Gemini's matched the real thing, so stools don't count against Gemini in H1. I'd already seen these models on this exact frame, so a confirmed hypothesis is a replication and a kill is the more informative result.

## Scope

| In | Out for now |
|---|---|
| Living room: one eye-level Astra still, a 5 s slow push toward the hallway | Other rooms |
| Runway's video picker, models chosen by hand, Runway Pro for one month | Agent routing, the Runway API or MCP |
| Gen-4.5, Seedance 2.5, Gemini Omni 1.1 Flash at 720p, 16:9, start frame only | Models outside the picker; Aleph video-to-video (no recording) |
| GWM Worlds as a Runway-only probe, if it passes the upload, export and credit gate | GWM as a scored arm (no outside world model to compare against) |
| Real photos of the same spot as ground truth (never given to the models) | Real-photo interaction test (door opens, stool slides) |
| Symmetric build (3 iterations per model) with a build log | Tagged releases |
| Frozen eval: 3 models x 2 clips, blind scoring | Second human scorer and a rubric-critic agent (descoped) |
| Case study: results, failures, research recommendations, launch proposal, decision log | Lamp relighting, image staging repair pass |

## Model selection

The eval compares Runway's Gen-4.5 with Seedance 2.5 and Gemini Omni 1.1 Flash, all run in Runway's video picker at 720p, 16:9 and 5 s from the same start frame. Models were picked functional first (must take a start image), then by image-to-video leaderboard rank, then by running in the picker. Full research: [`p2/I2V_RESEARCH.md`](../p2/I2V_RESEARCH.md) (current), [`p2/MODEL_SELECTION.md`](../p2/MODEL_SELECTION.md) (the earlier editing pass) and [`p2/EVAL_RESEARCH.md`](../p2/EVAL_RESEARCH.md) (how video models are evaluated).

| Model | Why it's in | Image-to-video leaderboards | Inputs (Runway pages, verify in app) | Credits per 5 s at 720p (verify in app) |
|---|---|---|---|---|
| Gen-4.5 (Runway, scored) | Runway's flagship video model | Not listed on either image-to-video board; Arena text to video #27 | Start image, prompt-only camera | About 60 |
| Seedance 2.5 (ByteDance, scored) | Strongest image-to-video model in the picker | Artificial Analysis #1, Arena #4 | Start and last frame, free reference images, 480p drafts | About 150 (80 minimum) |
| Gemini Omni 1.1 Flash (Google, scored) | Top of Arena; the boards disagree on it | Arena #2 (3.7k votes), Artificial Analysis #14 | Start image, reference images | About 50 |
| GWM Worlds (Runway, probe) | Runway's world model, built on Gen-4.5; real camera control | Not ranked | First frame plus prompt; upload and export not verified | Not published |

What this means for the test:
- **Gen-4.5 has no public image-to-video rank,** and Runway's Dec 2025 "#1" claim no longer matches the boards. My result is new evidence, not a check on an existing number.
- **GWM vs Gen-4.5 is the Runway-specific question:** the same base model with and without world-model training, on a real user task. It also answers which model a "plan to walkthrough" product should use.
- **The boards disagree on Gemini Omni 1.1 Flash** (#2 vs #14). Disagreeing priors are a reason to test on a real task.
- **Stated limits:** top image-to-video models not in the picker (Utopai X, Hyperflow H3, HeyGen Video 1, P-Video-2-Pro); MiniMax H3 and Wan 3.0 may be in tabs not checked.
- **Alternates:** Kling 4.0 (newest, unranked) or MiniMax H3 Max (last-frame support, 768p max).

Sources: [Artificial Analysis image to video](https://artificialanalysis.ai/video/leaderboard/image-to-video), [Arena image to video](https://arena.ai/leaderboard/image-to-video) (Sep 21, 2026), [Runway pricing](https://runway.com/pricing), [Runway API pricing](https://docs.dev.runwayml.com/guides/pricing/), [Gen-4.5](https://runway.com/research/introducing-runway-gen-4.5), [GWM-1](https://runway.com/research/introducing-runway-gwm-1), [GWM Worlds 2](https://runway.com/research/introducing-gwm-worlds-2).

## Success metrics

- **Build:** at least 1 Gen-4.5 clip from my Astra render that passes my gut call, with a build log row for every generation; then the same 3 iterations on Seedance 2.5 and Gemini Omni 1.1 Flash, and a side-by-side of one iteration across all models.
- **Eval:** acceptable rate per model, mean and best-of-2 per criterion, credits and minutes per acceptable clip, failures by type.
- **Eval of the eval:** a rubric rehearsal on one build clip before the freeze, a 24 h blind re-score of 3 clips, gut call vs score agreement, and one automated metric next to my temporal score.
- **Case study:** results per model, worst failures with frame stills, what I'd tell the research team, a launch proposal and a dated decision log.
- **Credibility:** the protocol is committed and pushed before the first scored clip, so the commit date shows it came first.

## Launch proposal (as planned)

A "plan to walkthrough" feature: turn a 3D room plan into photoreal footage of the real space. Primary user: people furnishing their own home (renters and buyers). Go-to-market channel: furniture retailers and real-estate listings. The P2 rubric is the eval gate that would block launch; the case study sets the threshold from the results.

After the results, the proposal I actually made is narrower: a reveal-fidelity slice in Gen-4.5's eval suite. See [`p2/FINDINGS.md`](../p2/FINDINGS.md#launch-proposal).

## Decision log

| Date | Decision | Why | Status |
|---|---|---|---|
| 2026-11-02 | Stop P1 image staging after 1 run; P1 becomes a pilot | Agent routed the edit to Nano Banana Pro, so P1 tested the product layer, not Runway's models | Active |
| 2026-11-02 | Preliminary case study deadline moved | A frozen protocol and real results couldn't both be done by the next morning | Active |
| 2026-11-03 | Switch from video-to-video (Aleph) to image-to-video from the Astra render | No Astra walkthrough recording exists; going from plan straight to real-world video tests what Runway is building toward | Active |
| 2026-11-03 | Arms: Gen-4.5, Seedance 2.5, Gemini Omni 1.1 Flash, all 720p, 16:9, 5 s, start frame only | Start-image support first, then image-to-video rank, then in the picker; Gen-4.5 has no public rank, so my result is new evidence | Active |
| 2026-11-03 | Model selection rule: functional first, then popularity, then in the picker, then cheaper; models outside the picker are a stated limit | A popular model that can't take my input can't do the task; one surface and one credit pool keep the comparison clean | Active |
| 2026-11-03 | All models run in Runway's video picker, chosen by hand, not through Agent | The model is the variable; in P1 Agent chose the model for me | Active |
| 2026-11-03 | GWM Worlds as a Runway-only probe, gated on upload, export and credits | Built on Gen-4.5, so the pair tests what world-model training adds; steered by hand, so not reproducible enough to score | Superseded (deferred, see 2026-11-05) |
| 2026-11-03 | Input prep: eye-level Astra render from the same taped spot as a new 16:9 real photo (1x lens) | Shortens the leap the model has to make, keeps a hard landmark check on frame 1, and gives a real reference for the hallway | Active |
| 2026-11-03 | Failure mitigations: one slow 5 s push with no turns, ceiling on and no cutaway in the render, daylight, a fallback ladder frozen before the eval, a separate demo track | The biggest risk is the model inventing what the still doesn't show; failures become rarer and easier to classify | Active |
| 2026-11-03 | Symmetric build: same 3 iterations per model (base prompt; materials described in words; one fix) | No prompt tuned to one model; triples cross-model observations. Materials went in words because Gen-4.5 takes no reference image (found 2026-11-04), so no arm gets one | Active |
| 2026-11-03 | Keep a frozen eval after the build: 3 models x 2 clips, blind scoring | The build is exploratory; only a fixed prompt with repeats gives defensible scores | Active |
| 2026-11-03 | Test the eval itself: re-score, gut call vs scores, one automated metric | Research teams care whether the rubric is reliable, not only what it says | Active (re-score later cut) |
| 2026-11-03 | Ground the plan in a research pass: leaderboards, eval methods, failure modes | Build, hypotheses and recommendations should rest on sources and first principles | Active |
| 2026-11-03 | Hypotheses are drafts; I rewrite them in my own words, at most three, before the freeze | The bets should be mine, and fewer, sharper bets beat many weak ones | Active |
| 2026-11-03 | Rubric-critic agent descoped; the rubric is rehearsed on one build clip at the freeze instead | Not building a separate agent keeps the build first; a rehearsal still catches coin-flip anchors | Active |
| 2026-11-03 | Scoring written to a CSV and validated on entry, with a notes file | Easiest tracking; the notes keep my words as evidence | Active |
| 2026-11-03 | Cut order if behind: automated metric, then 24 h re-score, then launch proposal shrinks to a paragraph, then narrated video | Protect the build and the core results | Active |
| 2026-11-03 | Runway Pro for one month | About 1,300 credits needed at listed prices. Upgraded 2026-11-04 (2,250 credits): the free plan listed the models but couldn't generate video | Active |
| 2026-11-03 | One scenario only; real-photo interaction (door opens, stool slides) deferred | Small n is the real limit; one scenario fits the week | Active |
| 2026-11-03 | Aleph 2.0 vs Seedance 2.5 vs Gemini Omni Flash, video-to-video at 720p | Top editing models that take an input video | Superseded by the switch to image-to-video |
| 2026-11-04 | Three hypotheses in my own words replace the five drafts (control vs realism, value, when it breaks), each with a rubric measure and a kill condition | Written before any scored clip, from what I saw in the build. Scope limit: 5 s clips only | Active |
| 2026-11-04 | Narrated walkthrough cut | Last in the cut order | Active |
| 2026-11-05 | P2 protocol frozen in commit [`f589500`](https://github.com/helenhshim/runway-apt-sim/commit/f589500) before any scored clip. Eval prompt p2v1 = build prompt b03 (backup b02), picked across all three arms. Fallback ladder: keep the 5 s push. No reference image or last frame for any arm. Credits per clip from the app balance: Gen-4.5 60, Seedance 150, Gemini 51 | All three arms held a 5 s push in b01 to b03; Gen-4.5 takes no reference image or last frame, so none are used (fairness rule). The app shows no cost before generating, so cost is the balance difference | Active |
| 2026-11-05 | GWM Worlds probe deferred and outside the frozen scored protocol | Deprioritized on 2026-11-04 and removed as a blocker of the freeze. Not an arm, not scored | Active |
| 2026-11-05 | The repo was private at freeze time and made public after a privacy pass | The commit dates still order the freeze (13:50) before the commit that logged the six scored clips (14:39) | Active |
| 2026-11-05 | No phone walk exists, so reveal checks, realism and invented_area are judged against the real photo and the start frame | The walk was never recorded. RUBRIC, FAILURE_TYPES, INVENTORY and PROMPT updated to match before the freeze | Active |
| 2026-11-05 | Rubric rehearsed on Gemini b03: 4, 4, 5, 5, gut call yes, no coin flips. Gap found and fixed: an invented piece (the side table) counts as a pop in criterion 4, not in criterion 2 | The rubric didn't say where invented pieces count | Active |
| 2026-11-05 | Audio off on every arm; if a model forces audio on, leave it and log it. Audio isn't scored | Seedance and Gemini defaulted to audio on in the build (footsteps); it doesn't affect the four criteria | Active |
| 2026-11-05 | 24 h re-score canceled | Findings report single-pass scoring and say so in the limits | Active |

## Open questions at the time, and how they resolved

| Question | Resolved |
|---|---|
| Shoot the 16:9 start photo, end photo and phone walk from the taped spot; strip EXIF | Photo A shot and stripped. No end photo or walk, so photo A and the start frame are the ground truth |
| Re-render Astra at eye level from the same spot: ceiling on, no cutaway, daylight, 16:9 | Done; it's the start frame for every arm |
| Re-pick the 8 landmarks on the new photo | Done, in [`p2/INVENTORY.md`](../p2/INVENTORY.md) |
| Does each model accept 16:9? Does Gen-4.5 take a last frame or reference image? | All take 16:9. Gen-4.5 takes neither, so no arm got them |
| GWM gate: upload, export, credit cost | Deferred, not run before the freeze |
| Check the Alibaba, MiniMax and Black Forest Labs tabs | Not checked; models outside the three arms are a stated limit |
