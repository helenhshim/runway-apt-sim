# P2 findings: Astra render to real-world video (T34, DRAFT 2026-11-05)

Full record for Helen. The case study page (T35) adapts it for the web. Every number comes from `log.csv` (frozen, blind scored, single pass), `results_p2.json` (`python3 p2/summarize_p2.py p2/log.csv`), `build_log.csv` or `WARP_RESULTS.md`. Protocol frozen at `f589500`, eval prompt `p2v1` (= `b03`). All arms at 720p, 16:9, 5 s, start frame only. The P1 image-staging pilot is summarized in the top-level `README.md` and is not repeated here.

## Headline

For "show me my planned room as a real video", realism isn't the bottleneck. Staying faithful to what the start frame doesn't show is.

- 5 of 6 clips scored realism 4 or higher, but 3 of 6 failed, and all 3 failed at a reveal: an area the start frame only half shows (the left doorway) coming into view.
- The most realistic clip was the most wrong. Gemini's C1 scored realism 5 and plan fidelity 1.
- Acceptable clips by model: Seedance 2.5 2 of 2, Gemini Omni 1.1 Flash 1 of 2, Runway's Gen-4.5 0 of 2. With 2 clips per model this is a signal, not a ranking.

## The proof: realism and fidelity come apart (C1)

Gemini's C1 (blind B06) is the clearest case. By 2.5 s (the frame I picked) a fake nook sits where the left doorway should be. A different chair appears in the wrong place, and furniture from the start frame is gone. Scores: geometry 1, plan 1, temporal 2, severity 3. Realism 5, the only realism 5 in the eval. If you judged this clip on how real it looks, it would win. As a picture of my planned room, it's the worst clip I generated.

## What this means for Gen-4.5 (A2)

Gen-4.5 failed both clips at the same reveal.
- **A2 (blind B03), severity 2, `invented_area`.** By 2.5 s an invented corner replaces the left doorway. An invented painting and wood paneling pop in across from the bench, and the stools morph. Geometry 1, plan 3, realism 3, temporal 2. In my words: it "imagined random things in the corner that replaced the doorway" and "looked more like a 3d render with the fake stuff that popped up".
- **A1 (blind B05), severity 2, `opening`.** At 4.75 s the left doorway's door is closed. Geometry 1 (opening cap). Plan 3, realism 4, temporal 5. A quiet failure, but the same spot.
- **Build pattern.** Gen-4.5 got the stools wrong in b01, b02 and b03. Seedance and Gemini got them right every time.
- **Inputs.** Gen-4.5 was the only model in the test that took neither a reference image nor a last frame, so it had nothing to anchor the doorway to (see Cost and UX).

## Results per model

| | Gen-4.5 (A) | Seedance 2.5 (B) | Gemini Omni 1.1 Flash (C) |
|---|---|---|---|
| Acceptable (gut call) | 0/2 | 2/2 | 1/2 |
| Geometry, mean (best) | 1.0 (1) | 5.0 (5) | 3.0 (5) |
| Plan, mean (best) | 3.0 (3) | 5.0 (5) | 3.0 (5) |
| Realism, mean (best) | 3.5 (4) | 4.0 (4) | 4.5 (5) |
| Temporal, mean (best) | 3.5 (5) | 5.0 (5) | 3.5 (5) |
| Temporal events, mean | 1.0 | 0 | 1.5 |
| Credits spent (2 clips) | 115 | 300 | 102 |
| Credits per acceptable clip | n/a (none) | 150 | 102 |
| Minutes per clip | about 1 | about 2.5 | about 1 |

Scores are 1 to 5 on `RUBRIC.md`. Gut call and "all four at 4 or higher" agreed on 6 of 6 clips.

**Worst failure per model.** Break times are the first frame where I saw the break, picked from stills in `evidence/stills/` (gitignored until the privacy pass).
- **Gen-4.5:** A2 at 2.5 s, invented corner replaces the doorway (severity 2).
- **Seedance 2.5:** no failure. Both clips scored 5/5/4/5 with zero events and passed all three reveal checks. The weakest point is realism 4 on both: no reflection on the TV, and a little softer than the others.
- **Gemini Omni 1.1 Flash:** C1 at 2.5 s, fake nook where the doorway should be (severity 3, the worst in the eval). C2 passed (5/5/4/5), but it had an invented side table beside the couch. That's the same piece that showed up in all three Gemini build clips (square, round, black).

## Hypotheses

I wrote each hypothesis and its kill condition before any scored clip (`README.md`). If the kill condition happens, the hypothesis is killed. I hold myself to the stricter reading. With 2 clips per model, all of this is directional.

**H1: the most realistic-looking model invents more and is less 1:1 (Gemini).** Survives, with a caveat.
- Kill condition: Gemini's plan fidelity is the same as or higher than Seedance's, or Gemini has no more invented pieces than either other model.
- Plan: Gemini 3.0 vs Seedance 5.0, so the first half doesn't fire.
- Invented pieces: Gemini 2 (C1 fake nook, C2 side table) vs Seedance 0, so the second half doesn't fire either.
- Gemini had the highest realism mean (4.5), and C1 is the clearest example of the claim.
- Caveat: Gen-4.5 invented as much as Gemini or more (A2 corner, painting, wood; A1 closed door), with lower realism. Invention isn't unique to the most realistic model.

**H2: the cheap one is close enough (Gemini over Seedance).** Killed.
- Kill condition: Gemini has fewer acceptable clips than Seedance. It did: 1 of 2 vs 2 of 2.
- The same hypothesis also said "1 of 2 counts as close enough". Those two thresholds conflict, and I'm holding to the stricter one.
- On cost alone Gemini still wins: 102 credits per acceptable clip vs 150, at about 1 minute vs 2.5. But its one failure was the severity-3 clip that looked the most real. For judging a plan before I buy, that's the wrong kind of cheap.

**H3: failures start at reveals (something returns, or a new area comes into view).** Killed on the stated measure. The reveal pattern is a new observation.
- Kill condition: most temporal events across the 6 clips are not tied to a return or a new area coming into view.
- Temporal events: 5 in total. 2 are tied to a new area across from the bench (A2 painting and wood, C1 fake nook). 2 are not (A2 stools morph, C1 wrong chair). 1 is unclear (C1 missing furniture). That's 2 of 5, so the kill condition fires. Events weren't tagged by trigger at scoring time, so this split is my reading after the fact.
- New observation, not a rescue: all 3 failed clips failed reveal check 2, the left doorway the start frame only half shows, and no clip failed with the doorway intact. The failures show up in geometry (openings and invented areas), not mainly as temporal pops. Next time, the measure for H3 should be reveal checks, not temporal events.

## Recommendations

Each one is tied to a logged failure.

### Research fixes (for Gen-4.5)
1. **Anchor the reveal.** Logged: all 3 failures were at the left doorway (A1 door closed, A2 invented corner, C1 fake nook). Fix: train and test on frame-edge reveals in interiors, where an area the start frame half shows has to stay what it is. Runway's Gen-4.5 launch post already lists object permanence as a known failure, and this is a concrete, cheap case of it.
2. **Keep in-frame object identity.** Logged: Gen-4.5's stools were wrong in b01 to b03 and morphed in A2, while Seedance and Gemini kept them. Fix: score identity per piece for furniture visible in the start frame, the way criterion 2 does.
3. **Score fidelity separately from realism.** Logged: C1 scored realism 5 and plan 1. Fix: report fidelity next to realism, never folded into one preference score. A blended score would pass C1.
4. **Don't trust warping error as a temporal stand-in.** Logged: it agreed with my temporal score on 3 of 6 clips and missed C1 entirely. Fix: keep a human or reference-grounded check (landmarks and reveal checks against the start frame) until an automated one agrees with it.

### Product fixes
1. **Show cost before Generate.** Logged: every build row's cost had to be inferred from the balance. A1 cost 55 against a listed 60.
2. **Add an "already run" cue.** Logged: an accidental repeat of Seedance b02 (150 credits, unsaved) and an accidental Seedance generation during the eval, accepted as B2. Both happened on the most expensive model, so 300 credits of accidents.
3. **Respect audio off, or say when it can't.** Logged: Seedance defaulted audio on, and Gemini couldn't turn it off (it added footsteps). Neither said so before generating.
4. **Give Gen-4.5 a last frame and a reference image, and show capabilities in the picker.** Logged: Gen-4.5 took neither, so the fairness rule took them away from all three arms. They're the obvious way to anchor the doorway reveal (research fix 1).
5. **Let me edit a piece in the video.** Build observation: the Astra render already drifted from the real pieces, and I wanted to fix the stools in the video model instead of going back to Astra.

## Cost and UX

- **No cost shown before generating.** Every cost in this project is a balance difference. Eval spend was 517 credits (A 115, B 300, C 102) against a plan of 522. Gen-4.5 A1 charged 55, not the listed 60, and nothing in the app explains why.
- **Accidental repeat, because there's no "already run" cue.** In the build I couldn't tell whether Seedance b02 had produced the right output, since the two looked so similar, and nothing said the prompt had already run, so I ran it again (150 credits). In the eval, a navigation mistake produced an extra Seedance clip that I accepted as B2 (settings checked, first output, out of run order).
- **Audio forced on by Seedance and Gemini.** Seedance defaulted to on (turned off from b02 on). Gemini couldn't be turned off at all, so every Gemini clip, scored ones included, has audio. That's a logged deviation from the audio-off rule. It doesn't affect visual scores, but it's a hidden setting.
- **Gen-4.5 takes no reference image and no last frame.** Seedance and Gemini accept both. Runway's own model had the fewest controls in the picker.
- **Speed.** Gen-4.5 and Gemini took about 1 minute per clip, Seedance about 2.5.

## Automated metric (T32)

Flow-based warping error agreed with my temporal score on only **3 of 6** clips: 1 hit (A2), 2 quiet matches (B1, B2), 2 false alarms (A1, C2) and 1 miss (C1). It mostly tracks camera speed and softness. Error rises with mean flow, Seedance (the softest) is lowest everywhere, and spikes bunch at 4 to 5 s where the push speeds up. It missed C1, the worst clip, because a static fake nook stays consistent from frame to frame. Verdict: not worth scaling as a stand-in for the human score. See `WARP_RESULTS.md`.

## Limits

- **n = 6:** 2 clips per model, one room, one start frame, a 5 s forward push. Directional, not statistics.
- **One scorer, single pass.** I scored blind in one sitting. The 24 h re-score (T33) was canceled, so there's no test-retest number. I may recognize a model's style even blind.
- **One room.** Mine, from one Astra render, which is AI-generated from photos, not measured. No hallway walk exists, so reveal checks are judged against photo A and the start frame.
- **Invented-piece rule applied unevenly.** The rubric (settled 2026-11-05) counts an invented piece as a `pop`. C2's side table is in its notes but logged as 0 events and temporal 5. Counted properly, I'd score C2 temporal 4 with 1 event. C2 stays acceptable, but Gemini's temporal mean goes from 3.5 to 3.0 and its events mean from 1.5 to 2.0. The frozen log isn't changed. The rehearsal Temporal re-score (T28) is also still open.
- **Deviations** (T28, T29): A1 cost 55, not 60. B2 was an accidental generation accepted out of run order. Gemini audio was forced on.
- **Break times are single frames I picked**, not logged during scoring. A2's 2.5 s is earlier than the landmark counts suggested (still 8 in view at the 50% pause).
- **GWM deferred.** Runway's world model (T26) wasn't run, so this says nothing about it.
- **Picker only.** Popular models outside Runway's picker aren't covered. Gen-4.5 has no public image-to-video leaderboard rank to compare against (`I2V_RESEARCH.md`).

## Launch proposal

Add a "reveal fidelity" slice to Gen-4.5's eval suite. I don't know what Runway evaluates internally. This is the gap my test exposed, and a cheap way to check whether it's already covered. The slice: interior start frames, each with a few written reveal checks (what has to stay true as areas the start frame half shows come into view), scored for fidelity separately from realism, by a person until an automated check agrees with people. Warping error didn't. The reason: 3 of 6 clips failed, all at a reveal, and C1 shows that a model can look perfectly real while being wrong about the room. The bar: Gen-4.5 passes the reveal checks at least as often as the best third-party model in the picker on the same frames, with no real-looking-but-wrong failures like C1. To get there, I'd start with the four research fixes above: anchor the reveal, keep object identity, score fidelity separately, and keep a human check on temporal quality.
