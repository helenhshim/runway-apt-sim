-- One row per Runway generation. Mirrors the CSV log header, in the same order.
-- Optional fields (scale_error_pct, failure_type, severity, notes) are NULL when blank.
CREATE TABLE runs (
    run_id          TEXT PRIMARY KEY,
    case_id         TEXT NOT NULL,
    room            TEXT NOT NULL,
    attempt         INTEGER NOT NULL CHECK (attempt >= 1),
    surface         TEXT NOT NULL CHECK (length(trim(surface)) > 0),
    model_shown     TEXT NOT NULL CHECK (length(trim(model_shown)) > 0),  -- "not shown" is a valid entry
    prompt_id       TEXT NOT NULL,
    credits         REAL NOT NULL CHECK (credits >= 0),
    minutes         REAL NOT NULL CHECK (minutes >= 0),
    acceptable      INTEGER NOT NULL CHECK (acceptable IN (0, 1)),
    landmarks_kept  INTEGER NOT NULL CHECK (landmarks_kept BETWEEN 0 AND 8),
    scale_error_pct REAL,
    layout          INTEGER NOT NULL CHECK (layout BETWEEN 1 AND 5),
    lighting        INTEGER NOT NULL CHECK (lighting BETWEEN 1 AND 5),
    furniture       INTEGER NOT NULL CHECK (furniture BETWEEN 1 AND 5),
    failure_type    TEXT CHECK (failure_type IN (
        'geometry', 'opening', 'scale', 'placement', 'identity',
        'shadow', 'reflection', 'material', 'hallucination', 'side_effect')),
    severity        INTEGER CHECK (severity BETWEEN 1 AND 3),
    notes           TEXT,
    CHECK ((failure_type IS NULL) = (severity IS NULL)),
    UNIQUE (case_id, attempt)
);
