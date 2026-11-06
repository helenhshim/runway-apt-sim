# runway-apt-sim

Can a video model go from my 3D furniture plan straight to a real-world video of my apartment? A small, pre-registered eval of Runway's models against the strongest other models Runway hosts, run on one real living room.

- **Question:** starting from one eye-level render of my planned living room (made in Astra), which image-to-video model turns it into a walkthrough that looks like my real apartment while keeping the plan and the room intact as the camera moves, and what does one acceptable clip cost?
- **Models:** Runway Gen-4.5, Seedance 2.5 and Gemini Omni 1.1 Flash, all at 720p, 16:9, 5 s from the same start frame, chosen by hand in Runway's video picker. GWM Worlds, Runway's world model built on Gen-4.5, runs as a probe on the same still.
- **Design:** build first (3 logged iterations per model), then a frozen eval of 3 models x 2 clips, scored blind on real-room fidelity, plan fidelity, realism, and temporal and scene consistency. Real photos and a phone walk of the same path are the ground truth; the models never see them.
- **Rule:** the rubric, prompt and log schema are committed before the first scored clip. The commit history shows it.
- **Status:** P2 protocol in draft, not frozen. One scorer, one room, n = 2 per model.

The Astra render is AI-generated from photos, not measured.

## What is where

| Folder | What |
|---|---|
| `p2/` | The current eval: protocol (`README`, `PROMPT`, `RUBRIC`, `INVENTORY`, `FAILURE_TYPES`), research (`I2V_RESEARCH`, `MODEL_SELECTION`, `EVAL_RESEARCH`), log schema, validator, blind-scoring script, tests |
| `protocol/` | P1, the image staging pilot, frozen at commit 1e24e9e and never edited |
| root `*.py`, `*.sql`, `tests/` | P1 log, validation, SQL roll-up and JSON export |
| `evidence/` | Inputs, photos and clips; gitignored, only its README is tracked |

## Run it

Python 3 standard library only.

```bash
python3 p2/validate_p2.py p2/log.csv                 # check the P2 log; add --unscored-ok before scoring
python3 p2/blind.py evidence/p2_clips evidence/p2_blind evidence/p2_blind_key.csv   # shuffle clips for blind scoring
python3 -m unittest discover -s p2/tests -v          # P2 tests, fake rows only
python3 -m unittest discover -s tests -v             # P1 tests
```

P1 tools (`log_run.py`, `validate_log.py`, `export_json.py`, `rollup.sql`) are documented in the P1 section below.

## P1: image staging pilot

The project started as a test of Runway image staging: add one chair to a photo of my living room without breaking the room. The protocol was frozen in 1e24e9e before the first run. It stopped after one formal run, because Runway Agent routed the edit to Nano Banana Pro, a third-party image model, so it was testing Runway's product layer rather than Runway's own models. It is reported as a pilot (n = 1), with that routing finding and the card cost (20 credits) against the all-in cost (30).

- `log_run.py` asks for one generation's fields and saves a row only if it validates.
- `validate_log.py` checks the 18-column P1 log.
- `export_json.py` validates, loads SQLite, runs `rollup.sql` and writes `results.json` (shape read by the portfolio page; do not change it without telling Helen).

## Links

- PRD: https://claude.ai/artifact/KJg6jC6r43XgmDL9qmUNJ3 (with Research and Files tabs)
- Technical design: https://claude.ai/artifact/HjRds5ARxNi57dgayN8mLQ
- Tickets: Linear project "Runway eval: Astra render to real-world video (P2)"
- Case study: https://www.helenshim.me/projects/runway-room-video (part 1, the Astra 3D models: https://www.helenshim.me/projects/astra-room-models)

Scaffolding (validators, blind-scoring script, roll-up, tests) was written with Claude Code.
