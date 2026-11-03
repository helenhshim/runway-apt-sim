"""Tests for p2/validate_p2.py and p2/blind.py using fake rows and fake files.

Not real eval data. Run: python3 -m unittest discover -s p2/tests -v
"""
import csv
import os
import random
import sys
import tempfile
import unittest

P2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, P2)

import blind  # noqa: E402
import validate_p2  # noqa: E402

# run_id, case, arm, attempt, surface, model, prompt, refs, dur, ratio, credits, minutes, acceptable,
# blind_id, checks, kept, geometry, plan, realism, temporal, events, failure_type, severity, notes
GOOD = [
    ["R1", "astra_walk", "A", 1, "video picker", "ModelA", "p2v1", 1, 5, "16:9", 100, 2.0, 1,
     "B03", 20, 19, 5, 4, 4, 5, 0, "", "", ""],
    ["R2", "astra_walk", "B", 1, "video picker", "ModelB", "p2v1", 1, 5, "16:9", 50, 1.5, 0,
     "B01", 20, 12, 2, 3, 3, 2, 3, "morph", 2, ""],
]
UNSCORED = ["R3", "astra_walk", "C", 1, "video picker", "ModelC", "p2v1", 1, 5, "16:9", 40, 1.0, 0,
            "", "", "", "", "", "", "", "", "", "", ""]


def write_csv(path, rows, header=validate_p2.COLUMNS):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


class ValidateTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.tmp.name, "log.csv")

    def tearDown(self):
        self.tmp.cleanup()

    def check(self, rows, unscored_ok=False):
        write_csv(self.path, rows)
        return validate_p2.validate_file(self.path, unscored_ok)[1]

    def test_columns_match_schema(self):
        with open(os.path.join(P2, "schema.sql")) as f:
            body = f.read().split("CREATE TABLE clips (", 1)[1]
        cols = [line.split()[0] for line in body.splitlines()
                if line.strip() and not line.strip().startswith((")", "--"))]
        self.assertEqual(cols, validate_p2.COLUMNS)

    def test_failure_types_match_doc(self):
        with open(os.path.join(P2, "FAILURE_TYPES.md")) as f:
            doc = {line.split("|")[1].strip() for line in f
                   if line.startswith("| ") and not line.startswith(("| failure_type", "|---"))}
        self.assertEqual(doc, validate_p2.FAILURE_TYPES)

    def test_good_rows_pass(self):
        self.assertEqual(self.check(GOOD), [])

    def test_unscored_needs_flag(self):
        self.assertEqual(len(self.check(GOOD + [UNSCORED])), 1)
        self.assertEqual(self.check(GOOD + [UNSCORED], unscored_ok=True), [])

    def test_partial_scores_rejected(self):
        row = list(GOOD[0])
        row[18] = ""  # realism blank
        self.assertTrue(any("realism is missing" in p for p in self.check([row], unscored_ok=True)))

    def test_kept_over_checks(self):
        row = list(GOOD[0])
        row[15] = 21
        self.assertTrue(any("more than geometry_checks" in p for p in self.check([row])))

    def test_bad_values(self):
        row = list(GOOD[0])
        row[2], row[16], row[21], row[22] = "D", 6, "side_effect", 2
        problems = " ".join(self.check([row]))
        for word in ("arm", "geometry must be", "failure_type 'side_effect'"):
            self.assertIn(word, problems)

    def test_failure_without_severity(self):
        row = list(GOOD[1])
        row[22] = ""
        self.assertTrue(any("both be filled" in p for p in self.check([row])))

    def test_duplicates(self):
        dup = list(GOOD[0])
        dup[0] = "R9"  # new run_id, same arm and attempt, same blind_id
        problems = self.check(GOOD + [dup])
        self.assertTrue(any("attempt" in p for p in problems))
        self.assertTrue(any("blind_id" in p for p in problems))

    def test_bad_header(self):
        write_csv(self.path, GOOD, header=validate_p2.COLUMNS[:-1])
        self.assertTrue(validate_p2.validate_file(self.path)[1][0].startswith("header"))


class BlindTest(unittest.TestCase):
    def test_shuffles_copies_and_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            clips = os.path.join(tmp, "clips")
            os.makedirs(clips)
            for name in ("p2_A_a1.mp4", "p2_B_a1.mp4", "p2_C_a1.MOV", "notes.txt"):
                with open(os.path.join(clips, name), "w") as f:
                    f.write(name)
            out, key_path = os.path.join(tmp, "blind"), os.path.join(tmp, "key.csv")
            key = blind.blind(clips, out, key_path, rng=random.Random(1))
            self.assertEqual(sorted(k[1] for k in key), ["p2_A_a1.mp4", "p2_B_a1.mp4", "p2_C_a1.MOV"])
            for blind_id, name in key:
                ext = os.path.splitext(name)[1].lower()
                with open(os.path.join(out, blind_id + ext)) as f:
                    self.assertEqual(f.read(), name)
            with open(key_path) as f:
                self.assertEqual(len(list(csv.reader(f))), 4)
            with self.assertRaises(FileExistsError):
                blind.blind(clips, out, key_path)


if __name__ == "__main__":
    unittest.main()
