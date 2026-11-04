# Board: Runway eval, Astra render to real-world video (P2)

Linear project P-HEL-6. PRD: https://claude.ai/artifact/KJg6jC6r43XgmDL9qmUNJ3. TDD: https://claude.ai/artifact/HjRds5ARxNi57dgayN8mLQ.
Rules: one writer per file; check `git status` before editing; a session's "done" is a report, verify with git log and the ticket; Done only with evidence in a Linear comment. P1's board stays at `.scratch/staging-eval/BOARD.md`.

## Priority order
1. T19 and T20 in parallel (inputs, build log)
2. T22 Gen-4.5 MVP clip (today)
3. T23, T24 Seedance and Gemini builds, then T25 b03 on all three
4. T21 inventory and baseline, T27 hypotheses
5. T26 GWM probe
6. T31 summary script (any time, agent)
7. T28 freeze
8. T29 generate, then T30 blind scoring
9. T32 automated metric (cut 1st)
10. T33 24 h re-score (cut 2nd)
11. T34 findings and launch proposal (launch proposal shrinks to a paragraph: cut 3rd)
12. T35 case study page (page session)
13. T37 privacy pass and publish
14. T36 narrated walkthrough (cut 4th)

## Tickets
| Ticket | Linear | What | Owner | Status | Blocked by | Due |
|---|---|---|---|---|---|---|
| T19 | HEL-84 | Inputs ready: photos, walk, renders, app checks | Helen | Done 2026-11-04 (all 3 models run on current plan; costs not shown upfront; 16:9, last frame, reference checks moved to T22 to T24) | none | Nov 3 |
| T20 | HEL-85 | Build log, test-first | agent | Done, verified (2bb46cd, 20 P2 tests pass) | none | Nov 3 |
| T22 | HEL-86 | Gen-4.5 build: MVP clip | Helen | Done 2026-11-04 (b01, b02 logged, 975d8d1, 7bfe2b7; hero = b01, iterated not scored; link and 360 demo moved to HEL-103) | T19, T20 | Nov 4 |
| T22b | HEL-103 | Gen-4.5 360 demo and private hero link upload | Helen | Backlog (later, with case study materials) | T22 | Nov 6 |
| T21 | HEL-87 | Inventory and input baseline | agent + Helen | Backlog | T19 | Nov 4 |
| T23 | HEL-88 | Seedance 2.5 build | Helen | Done 2026-11-04 (b01, b02 plus accidental repeat logged, 9bac9f6, de0095c; 150 credits per clip; b01 audio-on deviation accepted) | T19, T20 | Nov 4 |
| T24 | HEL-89 | Gemini Omni 1.1 Flash build | Helen | Done 2026-11-04 (b01, b02 logged, 836de3a, 6d2f3ff, 2851e56; 51 credits per clip; audio on by default for both, deviation accepted; both clips invented a side table beside the couch) | T19, T20 | Nov 4 |
| T25 | HEL-93 | b03 fix on all three, side-by-side | Helen | Done 2026-11-04 (fix 2 iPhone grain line, 11a4ca5; 3 b03 rows logged de188ce, 6753515, e85ed9b; candidate eval prompt b03, backup b02; ladder step: keep 5 s push; Astra wall is in the render, not model invention) | T22, T23, T24 | Nov 4 |
| T26 | HEL-90 | GWM Worlds probe | Helen | Backlog | T19, T20 | Nov 4 |
| T27 | HEL-91 | Hypotheses in my own words | Helen | Todo | none | Nov 4 |
| T28 | HEL-95 | Freeze the P2 protocol | agent + Helen | Backlog | T21, T25, T26, T27 | Nov 5 |
| T29 | HEL-96 | Generate the 6 scored clips | Helen | Backlog | T28 | Nov 5 |
| T30 | HEL-97 | Blind scoring session | Helen + agent | Backlog | T29 | Nov 5 |
| T31 | HEL-92 | Summary script and results JSON | agent | Backlog | none | Nov 5 |
| T32 | HEL-94 | Automated metric (cut 1st) | agent | Backlog | T22 | Nov 5 |
| T33 | HEL-98 | 24 h re-score (cut 2nd) | Helen | Backlog | T30 | Nov 6 |
| T34 | HEL-99 | Findings, recommendations, launch proposal | Helen + agent | Backlog | T30, T31 | Nov 6 |
| T35 | HEL-100 | Case study page | page session | Backlog | T22, T34 | Nov 6 |
| T36 | HEL-101 | Narrated walkthrough (cut 4th) | Helen | Backlog | T35 | Nov 6 |
| T37 | HEL-102 | Privacy pass and publish | Helen + agent | Backlog | T34, T35 | Nov 6 |

Descoped 2026-11-03: rubric-critic agent (Helen: not building a separate agent).
