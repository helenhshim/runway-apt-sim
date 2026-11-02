-- Roll-up views over `runs` (see schema.sql). Re-runnable: views are dropped first.
-- Scores are 1 to 5. "Best of 2" is the best attempt per case (max of its attempts).

DROP VIEW IF EXISTS case_stats;
CREATE VIEW case_stats AS
SELECT case_id, room,
       MIN(rowid)            AS first_row,
       COUNT(*)              AS n,
       AVG(layout)           AS mean_layout,
       AVG(lighting)         AS mean_lighting,
       AVG(furniture)        AS mean_furniture,
       MAX(layout)           AS best_layout,
       MAX(lighting)         AS best_lighting,
       MAX(furniture)        AS best_furniture
FROM runs GROUP BY case_id, room;

DROP VIEW IF EXISTS summary;
CREATE VIEW summary AS
SELECT COUNT(*)                                        AS generations,
       SUM(acceptable)                                 AS acceptable,
       SUM(acceptable) * 1.0 / COUNT(*)                AS acceptable_rate,
       SUM(credits)                                    AS credits_total,
       SUM(minutes)                                    AS minutes_total,
       -- NULL when nothing was acceptable (division by NULL)
       SUM(credits) / NULLIF(SUM(acceptable), 0)       AS credits_per_acceptable,
       SUM(minutes) / NULLIF(SUM(acceptable), 0)       AS minutes_per_acceptable
FROM runs;

DROP VIEW IF EXISTS failures_by_type_severity;
CREATE VIEW failures_by_type_severity AS
SELECT failure_type, severity, COUNT(*) AS n
FROM runs WHERE failure_type IS NOT NULL
GROUP BY failure_type, severity;

DROP VIEW IF EXISTS failures_by_type;
CREATE VIEW failures_by_type AS
SELECT failure_type, COUNT(*) AS n
FROM runs WHERE failure_type IS NOT NULL
GROUP BY failure_type;

-- H1: share of generations with landmarks_kept >= 6 (threshold frozen in the protocol).
DROP VIEW IF EXISTS h1_landmarks;
CREATE VIEW h1_landmarks AS
SELECT COUNT(*) AS generations,
       SUM(landmarks_kept >= 6) AS kept_6_plus,
       SUM(landmarks_kept >= 6) * 1.0 / COUNT(*) AS share
FROM runs;

-- H2: scale vs layout. share_scale_over_10 uses scale_error_pct (rows with it blank are skipped);
-- share_layout_broken counts layout score <= 2 (rubric: 4+ landmarks displaced or opening changed).
-- Scale has no score of its own, so furniture accuracy (which includes the +-10% ruler check) is shown beside layout.
DROP VIEW IF EXISTS h2_scale_vs_layout;
CREATE VIEW h2_scale_vs_layout AS
SELECT AVG(CASE WHEN scale_error_pct IS NULL THEN NULL WHEN ABS(scale_error_pct) > 10 THEN 1.0 ELSE 0.0 END) AS share_scale_over_10,
       AVG(CASE WHEN layout <= 2 THEN 1.0 ELSE 0.0 END) AS share_layout_broken,
       AVG(layout)    AS mean_layout,
       AVG(furniture) AS mean_furniture
FROM runs;

-- H3: lighting and material realism vs layout.
DROP VIEW IF EXISTS h3_lighting_vs_layout;
CREATE VIEW h3_lighting_vs_layout AS
SELECT AVG(lighting) AS mean_lighting, AVG(layout) AS mean_layout,
       AVG(lighting) - AVG(layout) AS lighting_minus_layout
FROM runs;

-- H4: best-of-2 minus mean, averaged across rooms, per criterion.
DROP VIEW IF EXISTS h4_best_minus_mean;
CREATE VIEW h4_best_minus_mean AS
SELECT AVG(best_layout    - mean_layout)    AS layout_gap,
       AVG(best_lighting  - mean_lighting)  AS lighting_gap,
       AVG(best_furniture - mean_furniture) AS furniture_gap
FROM case_stats;

-- H5: results by model_shown, only where the model is known ("not shown"/"unknown"/"n/a" excluded).
DROP VIEW IF EXISTS h5_by_model;
CREATE VIEW h5_by_model AS
SELECT model_shown,
       COUNT(*)        AS generations,
       SUM(acceptable) AS acceptable,
       SUM(credits)    AS credits,
       AVG(layout)     AS mean_layout,
       AVG(lighting)   AS mean_lighting,
       AVG(furniture)  AS mean_furniture
FROM runs
WHERE LOWER(TRIM(model_shown)) NOT IN ('not shown', 'unknown', 'n/a', 'na', 'none')
GROUP BY model_shown;
