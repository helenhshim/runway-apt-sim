"""Tests for p2/validate_build_log.py using fake rows.

Not real build data. Run: python3 -m unittest discover -s p2/tests -v
"""
import csv
import os
import sys
import tempfile
import unittest

P2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, P2)

import validate_build_log as vbl  # noqa: E402

# when, model, iteration, prompt_id, changed, credits_shown, balance_after, minutes,
# output_file, keep, tag, observation
GOOD = [
    ["2026-11-03 18:05", "Gen-4.5", "b01", "b01", "", 60, 2600, 1.5,
     "p2_A_b01.mp4", "no", "broke", "Sofa melts into the rug at 0:03."],
    ["2026-11-03 18:20", "Gen-4.5", "b02", "b02", "added reference photo", "", 2540, 2,
     "p2_A_b02.mp4", "yes", "quality", "Floor grain matches the real photo."],
    ["2026-11-03 18:40", "GWM Worlds", "demo", "gwm-1", "probe", "", 2500, 3,
     "p2_gwm_1.mp4", "no", "ux", "No credit cost shown before generating."],
]


def write_csv(path, rows, header=vbl.COLUMNS):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


class BuildLogTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "build_log.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, rows):
        write_csv(self.path, rows)
        return vbl.validate_file(self.path)[1]

    def test_good_rows_pass(self):
        self.assertEqual(self.check(GOOD), [])

    def test_empty_log_with_header_passes(self):
        self.assertEqual(self.check([]), [])

    def test_shipped_log_is_valid(self):
        rows, problems = vbl.validate_file(os.path.join(P2, "build_log.csv"))
        self.assertEqual(problems, [])

    def test_required_fields(self):
        row = list(GOOD[0])
        row[1], row[11] = "", ""
        problems = " ".join(self.check([row]))
        self.assertIn("model is missing", problems)
        self.assertIn("observation is missing", problems)

    def test_bad_tag_keep_and_iteration(self):
        row = list(GOOD[0])
        row[2], row[9], row[10] = "b9", "maybe", "meh"
        problems = " ".join(self.check([row]))
        for word in ("iteration", "keep", "tag"):
            self.assertIn(word, problems)

    def test_cost_needs_credits_or_balance(self):
        row = list(GOOD[0])
        row[5], row[6] = "", ""
        self.assertTrue(any("credits_shown or balance_after" in p for p in self.check([row])))

    def test_negative_numbers_and_bad_time(self):
        row = list(GOOD[0])
        row[0], row[5], row[7] = "yesterday", -5, "x"
        problems = " ".join(self.check([row]))
        for word in ("when", "credits_shown", "minutes"):
            self.assertIn(word, problems)

    def test_duplicate_output_file(self):
        dup = list(GOOD[0])
        dup[0] = "2026-11-03 19:00"
        self.assertTrue(any("output_file" in p for p in self.check([GOOD[0], dup])))

    def test_bad_header(self):
        write_csv(self.path, GOOD, header=vbl.COLUMNS[:-1])
        self.assertTrue(vbl.validate_file(self.path)[1][0].startswith("header"))


if __name__ == "__main__":
    unittest.main()
