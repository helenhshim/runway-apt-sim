# staging-eval

A small eval of Runway's image staging on three rooms of one apartment, compared with Astra renders, scored against the real photo.

- **Question:** does Runway keep a room's layout, light and scale intact while adding furniture, and what does one acceptable image cost?
- **Design:** 3 rooms x 2 attempts, one frozen prompt template, three criteria scored 1 to 5 (layout fidelity, lighting and material realism, furniture accuracy), a typed failure log.
- **Rule:** the rubric, prompt template and CSV schema are committed before the first generation. The commit history shows it.
- **Status:** preliminary. One scorer, one pass, three rooms.

Astra renders are AI-generated from photos, not measured models.

Tickets: Linear project "Runway staging eval (P1)". Board: `.scratch/staging-eval/BOARD.md`.
PRD: https://claude.ai/artifact/PN7G29thMiNKNDmedyiSn6
Case study: https://www.helenshim.me/projects/astra-room-models

Scaffolding (validation script, SQL roll-up) was written with Claude Code.
