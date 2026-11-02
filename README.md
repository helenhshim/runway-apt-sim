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

## Run it

Python 3 standard library only (SQLite is built in).

```bash
python3 validate_log.py log.csv          # prints "row N: problem" lines, exit 1 if any
python3 export_json.py log.csv results.json   # validates, loads SQLite, rolls up, writes results.json
python3 export_json.py log.csv results.json --db eval.db   # also keep the DB to query the views in rollup.sql
python3 -m unittest discover -s tests -v      # tests use fake rows only, numbers hand-computed in the test file
```

- `schema.sql`: the `runs` table, one row per generation, 18 columns in log order. Row 1 of the CSV is the header, so the first data row is "row 2".
- `validate_log.py`: rejects missing surface, model_shown or credits, bad failure_type (must be one of geometry, opening, scale, placement, identity, shadow, reflection, material, hallucination, side_effect), severity not 1 to 3, scores not 1 to 5, landmarks_kept not 0 to 8, failure_type without severity (or the reverse), duplicate run_id and duplicate case_id + attempt. "model not shown" is a valid model_shown entry.
- `rollup.sql`: views for means and best-of-2 per room, acceptable rate, credits and minutes per acceptable image, failures by type and severity, and H1 to H5 helpers. H5 leaves out rows where model_shown is "not shown", "unknown", "n/a", "na" or "none".
- H2 note: scale has no score of its own, so `h2_scale_vs_layout` compares the share of runs with scale_error_pct above 10 against the share with layout <= 2, and shows mean layout beside mean furniture.
- `results.json` shape is read by the portfolio page. Do not change it without telling Helen. `acceptable` is a boolean there, blank failure_type and severity are null, and `credits_per_acceptable` and `minutes_per_acceptable` are null if nothing was acceptable.

Scaffolding (validation script, SQL roll-up, JSON export, tests) was written with Claude Code.
