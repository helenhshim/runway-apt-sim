"""Tests for validate_log.py, rollup.sql and export_json.py using fake rows.

All expected numbers below were computed by hand from FAKE_ROWS. They are not
real eval data. Run: python3 -m unittest discover -s tests -v
"""
import csv
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import export_json  # noqa: E402
import validate_log  # noqa: E402

HEADER = [
    "run_id", "case_id", "room", "attempt", "surface", "model_shown", "prompt_id",
    "credits", "minutes", "acceptable", "landmarks_kept", "scale_error_pct",
    "layout", "lighting", "furniture", "failure_type", "severity", "notes",
]

# run_id, case_id, room, attempt, surface, model, prompt, credits, minutes, acceptable,
# landmarks, scale_err, layout, lighting, furniture, failure_type, severity, notes
FAKE_ROWS = [
    ["R1", "L1", "living", 1, "Agent", "ModelA", "p1", 20, 4.0, 0, 5, 12, 2, 4, 3, "scale", 2, ""],
    ["R2", "L1", "living", 2, "Agent", "ModelA", "p1", 20, 3.0, 1, 7, 4, 4, 5, 4, "", "", ""],
    ["R3", "D1", "dining", 1, "Agent", "ModelB", "p1", 8, 2.0, 1, 8, 3, 5, 4, 5, "", "", ""],
    ["R4", "D1", "dining", 2, "Agent", "ModelB", "p1", 8, 2.5, 0, 6, 15, 3, 4, 3, "placement", 1, ""],
    ["R5", "B1", "bedroom", 1, "Agent", "not shown", "p1", 8, 5.0, 0, 5, 20, 2, 3, 2, "geometry", 3, ""],
    ["R6", "B1", "bedroom", 2, "Agent", "not shown", "p1", 8, 4.5, 0, 4, 11, 2, 2, 2, "geometry", 2, ""],
]


def write_csv(path, rows, header=HEADER):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "log.csv")

    def tearDown(self):
        self.dir.cleanup()

    def problems_for(self, **overrides):
        row = dict(zip(HEADER, FAKE_ROWS[0]))
        row.update(overrides)
        write_csv(self.path, [[row[h] for h in HEADER]])
        _, problems = validate_log.validate_file(self.path)
        return problems

    def test_fake_rows_are_valid(self):
        write_csv(self.path, FAKE_ROWS)
        rows, problems = validate_log.validate_file(self.path)
        self.assertEqual(problems, [])
        self.assertEqual(len(rows), 6)

    def test_missing_required_fields_are_rejected_with_row_number(self):
        for field in ("surface", "model_shown", "credits"):
            problems = self.problems_for(**{field: ""})
            self.assertEqual(len(problems), 1, field)
            self.assertIn("row 2", problems[0])
            self.assertIn(field, problems[0])

    def test_invalid_failure_type_severity_scores_landmarks(self):
        cases = {
            "failure_type": "blurry",
            "severity": 4,
            "layout": 0,
            "lighting": 6,
            "furniture": "x",
            "landmarks_kept": 9,
        }
        for field, bad in cases.items():
            problems = self.problems_for(**{field: bad})
            self.assertTrue(any(field in p and "row 2" in p for p in problems), (field, problems))

    def test_failure_type_and_severity_must_come_together(self):
        self.assertTrue(self.problems_for(severity=""))

    def test_bad_header_rejected(self):
        write_csv(self.path, [], header=HEADER[:-1])
        _, problems = validate_log.validate_file(self.path)
        self.assertTrue(problems)
        self.assertIn("header", problems[0])

    def test_duplicate_run_id_rejected(self):
        write_csv(self.path, [FAKE_ROWS[0], FAKE_ROWS[0]])
        _, problems = validate_log.validate_file(self.path)
        self.assertTrue(any("row 3" in p and "run_id" in p for p in problems))

    def test_duplicate_case_attempt_rejected(self):
        dup = list(FAKE_ROWS[1])
        dup[0] = "R9"
        dup[HEADER.index("attempt")] = 1  # L1 attempt 1 already used by R1
        write_csv(self.path, [FAKE_ROWS[0], dup])
        _, problems = validate_log.validate_file(self.path)
        self.assertTrue(any("row 3" in p and "attempt" in p for p in problems))

    def test_problem_row_numbers_count_the_header_as_row_1(self):
        bad = list(FAKE_ROWS[1])
        bad[HEADER.index("layout")] = 9
        write_csv(self.path, [FAKE_ROWS[0], bad])
        _, problems = validate_log.validate_file(self.path)
        self.assertEqual(len(problems), 1)
        self.assertIn("row 3", problems[0])


class ExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dir = tempfile.TemporaryDirectory()
        csv_path = os.path.join(cls.dir.name, "log.csv")
        write_csv(csv_path, FAKE_ROWS)
        cls.out = os.path.join(cls.dir.name, "results.json")
        cls.db = os.path.join(cls.dir.name, "eval.db")
        export_json.export(csv_path, cls.out, db_path=cls.db)
        with open(cls.out) as f:
            cls.data = json.load(f)
        cls.conn = export_json.connect(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()
        cls.dir.cleanup()

    def case(self, case_id):
        return next(c for c in self.data["cases"] if c["case_id"] == case_id)

    def test_top_level_shape(self):
        self.assertEqual(list(self.data), ["generated_at", "cases", "totals"])
        self.assertEqual([c["case_id"] for c in self.data["cases"]], ["L1", "D1", "B1"])
        self.assertEqual(
            list(self.data["cases"][0]), ["case_id", "room", "runs", "mean", "best_of_2"]
        )
        self.assertEqual(
            list(self.data["cases"][0]["runs"][0]),
            ["attempt", "layout", "lighting", "furniture", "landmarks_kept",
             "scale_error_pct", "acceptable", "credits", "minutes",
             "failure_type", "severity"],
        )
        self.assertEqual(
            list(self.data["totals"]),
            ["acceptable_rate", "credits_per_acceptable", "minutes_per_acceptable",
             "failures_by_type"],
        )

    def test_mean_and_best_of_2_per_room(self):
        # living: layout (2+4)/2=3, lighting (4+5)/2=4.5, furniture (3+4)/2=3.5; best 4,5,4
        self.assertEqual(self.case("L1")["mean"], {"layout": 3, "lighting": 4.5, "furniture": 3.5})
        self.assertEqual(self.case("L1")["best_of_2"], {"layout": 4, "lighting": 5, "furniture": 4})
        # dining: means 4,4,4; best 5,4,5
        self.assertEqual(self.case("D1")["mean"], {"layout": 4, "lighting": 4, "furniture": 4})
        self.assertEqual(self.case("D1")["best_of_2"], {"layout": 5, "lighting": 4, "furniture": 5})
        # bedroom: means 2,2.5,2; best 2,3,2
        self.assertEqual(self.case("B1")["mean"], {"layout": 2, "lighting": 2.5, "furniture": 2})
        self.assertEqual(self.case("B1")["best_of_2"], {"layout": 2, "lighting": 3, "furniture": 2})

    def test_run_values_are_carried_through(self):
        run = self.case("L1")["runs"][0]
        self.assertEqual(run["attempt"], 1)
        self.assertIs(run["acceptable"], False)
        self.assertEqual(run["scale_error_pct"], 12)
        self.assertEqual(run["failure_type"], "scale")
        self.assertEqual(run["severity"], 2)
        clean = self.case("L1")["runs"][1]
        self.assertIs(clean["acceptable"], True)
        self.assertIsNone(clean["failure_type"])
        self.assertIsNone(clean["severity"])

    def test_totals(self):
        t = self.data["totals"]
        self.assertAlmostEqual(t["acceptable_rate"], 2 / 6, places=4)  # 2 of 6
        self.assertEqual(t["credits_per_acceptable"], 36)  # 72 credits / 2
        self.assertEqual(t["minutes_per_acceptable"], 10.5)  # 21 minutes / 2
        self.assertEqual(t["failures_by_type"], {"geometry": 2, "placement": 1, "scale": 1})

    def test_no_acceptable_gives_null_cost(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "log.csv")
            rows = [list(r) for r in FAKE_ROWS]
            for r in rows:
                r[HEADER.index("acceptable")] = 0
            write_csv(p, rows)
            out = os.path.join(d, "r.json")
            export_json.export(p, out)
            with open(out) as f:
                t = json.load(f)["totals"]
        self.assertEqual(t["acceptable_rate"], 0)
        self.assertIsNone(t["credits_per_acceptable"])
        self.assertIsNone(t["minutes_per_acceptable"])

    def test_invalid_log_is_not_exported(self):
        with tempfile.TemporaryDirectory() as d:
            p = os.path.join(d, "log.csv")
            bad = [list(r) for r in FAKE_ROWS]
            bad[0][HEADER.index("surface")] = ""
            write_csv(p, bad)
            out = os.path.join(d, "r.json")
            with self.assertRaises(export_json.InvalidLog):
                export_json.export(p, out)
            self.assertFalse(os.path.exists(out))

    def one(self, sql):
        return self.conn.execute(sql).fetchall()

    def test_h1_share_with_landmarks_at_least_6(self):
        # landmarks 5,7,8,6,5,4 -> 7,8,6 qualify -> 3 of 6
        row = self.one("SELECT generations, kept_6_plus, share FROM h1_landmarks")[0]
        self.assertEqual((row[0], row[1]), (6, 3))
        self.assertAlmostEqual(row[2], 0.5)

    def test_h2_scale_vs_layout(self):
        # scale_error_pct > 10: R1 12, R4 15, R5 20, R6 11 -> 4 of 6
        # layout <= 2 (broken): R1, R5, R6 -> 3 of 6
        # mean layout 18/6 = 3; mean furniture 19/6
        r = self.conn.execute(
            "SELECT share_scale_over_10, share_layout_broken, mean_layout, mean_furniture FROM h2_scale_vs_layout"
        ).fetchone()
        self.assertAlmostEqual(r[0], 4 / 6)
        self.assertAlmostEqual(r[1], 3 / 6)
        self.assertAlmostEqual(r[2], 3.0)
        self.assertAlmostEqual(r[3], 19 / 6)

    def test_h3_lighting_vs_layout(self):
        # lighting 4,5,4,4,3,2 = 22/6 ; layout 18/6
        r = self.conn.execute("SELECT mean_lighting, mean_layout FROM h3_lighting_vs_layout").fetchone()
        self.assertAlmostEqual(r[0], 22 / 6)
        self.assertAlmostEqual(r[1], 3.0)

    def test_h4_best_minus_mean(self):
        # per-room gaps layout (1,1,0), lighting (.5,0,.5), furniture (.5,1,0)
        r = self.conn.execute(
            "SELECT layout_gap, lighting_gap, furniture_gap FROM h4_best_minus_mean"
        ).fetchone()
        self.assertAlmostEqual(r[0], 2 / 3)
        self.assertAlmostEqual(r[1], 1 / 3)
        self.assertAlmostEqual(r[2], 0.5)

    def test_h5_by_model_excludes_unknown(self):
        rows = self.one(
            "SELECT model_shown, generations, acceptable, credits, mean_layout, mean_lighting, mean_furniture "
            "FROM h5_by_model ORDER BY model_shown"
        )
        self.assertEqual(
            rows,
            [("ModelA", 2, 1, 40.0, 3.0, 4.5, 3.5), ("ModelB", 2, 1, 16.0, 4.0, 4.0, 4.0)],
        )

    def test_failures_by_type_and_severity(self):
        rows = self.one("SELECT failure_type, severity, n FROM failures_by_type_severity ORDER BY failure_type, severity")
        self.assertEqual(
            rows,
            [("geometry", 2, 1), ("geometry", 3, 1), ("placement", 1, 1), ("scale", 2, 1)],
        )


if __name__ == "__main__":
    unittest.main()
