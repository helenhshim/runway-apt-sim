-- P2 log: one row per scored clip, 24 columns in log order (matches validate_p2.COLUMNS).
DROP TABLE IF EXISTS clips;
CREATE TABLE clips (
    run_id          TEXT PRIMARY KEY,
    case_id         TEXT NOT NULL,      -- astra_walk
    arm             TEXT NOT NULL,      -- A, B or C (model in PROMPT.md)
    attempt         INTEGER NOT NULL,
    surface         TEXT NOT NULL,      -- video picker
    model_shown     TEXT NOT NULL,      -- as the picker names it
    prompt_id       TEXT NOT NULL,      -- p2v1 or p2v1-noref
    ref_images      INTEGER NOT NULL,   -- reference images attached, 0 or 1
    duration_s      REAL NOT NULL,      -- output length in seconds
    aspect_ratio    TEXT NOT NULL,      -- as set, for example 16:9
    credits         REAL NOT NULL,
    minutes         REAL NOT NULL,
    acceptable      INTEGER NOT NULL,   -- gut call, 0 or 1
    blind_id        TEXT,               -- from blind.py
    geometry_checks INTEGER,            -- visible (landmark, frame) pairs
    geometry_kept   INTEGER,
    geometry        INTEGER,            -- 1 to 5
    plan            INTEGER,
    realism         INTEGER,
    temporal        INTEGER,
    temporal_events INTEGER,
    failure_type    TEXT,
    severity        INTEGER,
    notes           TEXT
);
