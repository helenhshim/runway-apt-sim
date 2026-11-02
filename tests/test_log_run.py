"""Tests for log_run.py, the prompt-and-append helper. Fake data only."""
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import log_run  # noqa: E402
import validate_log  # noqa: E402

# Answers in column order: run_id, case_id, room, attempt, surface, model_shown, prompt_id,
# credits, minutes, acceptable, landmarks_kept, scale_error_pct, layout, lighting, furniture,
# failure_type, severity, notes
FIRST = ["", "L1", "living", "1", "Agent", "not shown", "p1", "20", "4", "0", "5", "12", "2", "4", "3", "scale", "2", ""]


def scripted(answers):
    it = iter(answers)
    return lambda prompt: next(it)


class LogRunTests(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "log.csv")
        self.out = []

    def tearDown(self):
        self.dir.cleanup()

    def run_once(self, answers):
        return log_run.log_one(self.path, scripted(answers), self.out.append)

    def test_creates_file_with_header_and_appends_a_valid_row(self):
        self.run_once(FIRST)
        rows, problems = validate_log.validate_file(self.path)
        self.assertEqual(problems, [])
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_id"], "R1")  # blank run_id takes the next auto id
        self.assertEqual(rows[0]["layout"], "2")

    def test_invalid_answer_is_reasked_and_file_only_gets_the_good_row(self):
        answers = list(FIRST)
        answers[12] = "9"  # layout out of range
        answers += ["4"]  # re-asked layout
        self.run_once(answers)
        rows, problems = validate_log.validate_file(self.path)
        self.assertEqual(problems, [])
        self.assertEqual(rows[0]["layout"], "4")
        self.assertTrue(any("layout" in line for line in self.out))

    def test_blank_answer_keeps_default_from_previous_row(self):
        self.run_once(FIRST)
        second = ["", "L1", "living", "2", "", "", "", "20", "3", "1", "7", "4", "4", "5", "4", "", "", ""]
        self.run_once(second)
        rows, problems = validate_log.validate_file(self.path)
        self.assertEqual(problems, [])
        self.assertEqual(rows[1]["run_id"], "R2")
        self.assertEqual(
            (rows[1]["surface"], rows[1]["model_shown"], rows[1]["prompt_id"]),
            ("Agent", "not shown", "p1"),
        )

    def test_duplicate_case_attempt_is_reasked(self):
        self.run_once(FIRST)
        again = list(FIRST)  # same case_id L1 and attempt 1
        again += ["2"]  # re-asked attempt
        self.run_once(again)
        rows, problems = validate_log.validate_file(self.path)
        self.assertEqual(problems, [])
        self.assertEqual([r["attempt"] for r in rows], ["1", "2"])

    def test_interrupt_leaves_file_unchanged(self):
        self.run_once(FIRST)
        with open(self.path) as f:
            before = f.read()

        def boom(prompt):
            raise KeyboardInterrupt

        with self.assertRaises(KeyboardInterrupt):
            log_run.log_one(self.path, boom, self.out.append)
        with open(self.path) as f:
            self.assertEqual(f.read(), before)


if __name__ == "__main__":
    unittest.main()
