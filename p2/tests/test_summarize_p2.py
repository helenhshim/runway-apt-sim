"""Tests for p2/summarize_p2.py using fake rows. Not real eval data.

Every expected number below is worked out by hand in the comments, not computed by the code.
Run: python3 -m unittest discover -s p2/tests -v
"""
import contextlib
import csv
import io
import json
import os
import sys
import tempfile
import unittest

P2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, P2)

import summarize_p2  # noqa: E402
import validate_p2  # noqa: E402

# run_id, case, arm, attempt, surface, model, prompt, refs, dur, ratio, credits, minutes, acceptable,
# blind_id, checks, kept, geometry, plan, realism, temporal, events, failure_type, severity, notes
ROWS = [
    ["R1", "astra_walk", "A", 1, "video picker", "Gen-4.5", "b03", 0, 5, "16:9", 60, 2.0, 1,
     "K1", 20, 19, 5, 4, 4, 5, 0, "", "", ""],
    ["R2", "astra_walk", "A", 2, "video picker", "Gen-4.5", "b03", 0, 5, "16:9", 60, 2.5, 1,
     "K2", 20, 15, 4, 4, 3, 4, 1, "identity", 1, ""],
    ["R3", "astra_walk", "B", 1, "video picker", "Seedance 2.5", "b03", 0, 5, "16:9", 150, 3.0, 1,
     "K3", 20, 20, 5, 5, 5, 5, 0, "", "", ""],
    ["R4", "astra_walk", "B", 2, "video picker", "Seedance 2.5", "b03", 0, 5, "16:9", 150, 3.5, 0,
     "K4", 20, 12, 3, 4, 4, 3, 2, "morph", 2, ""],
    ["R5", "astra_walk", "C", 1, "video picker", "Gemini Omni 1.1 Flash", "b03", 0, 5, "16:9", 51, 1.0, 0,
     "K5", 20, 9, 2, 3, 3, 2, 3, "hallucination", 3, ""],
    ["R6", "astra_walk", "C", 2, "video picker", "Gemini Omni 1.1 Flash", "b03", 0, 5, "16:9", 51, 1.2, 1,
     "K6", 20, 17, 4, 2, 4, 4, 1, "hallucination", 2, ""],
]

def write_csv(path, rows, header=validate_p2.COLUMNS):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)


class SummarizeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.log = os.path.join(self.tmp.name, "log.csv")
        self.out = os.path.join(self.tmp.name, "results_p2.json")

    def tearDown(self):
        self.tmp.cleanup()

    def run_cli(self, rows, header=validate_p2.COLUMNS):
        write_csv(self.log, rows, header)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = summarize_p2.main(["summarize_p2.py", self.log, "--out", self.out])
        return code, buf.getvalue()

    def results(self):
        code, _ = self.run_cli(ROWS)
        self.assertEqual(code, 0)
        with open(self.out) as f:
            return json.load(f)

    # --- refusal -------------------------------------------------------------------------

    def test_refuses_invalid_log_and_writes_nothing(self):
        bad = [list(ROWS[0])]
        bad[0][2] = "D"  # arm not A, B or C
        code, out = self.run_cli(bad)
        self.assertEqual(code, 1)
        self.assertIn("arm must be one of", out)
        self.assertFalse(os.path.exists(self.out))

    def test_refuses_unscored_rows(self):
        unscored = list(ROWS[0])
        unscored[13:21] = [""] * 8
        unscored[21:23] = ["", ""]
        code, out = self.run_cli([unscored])
        self.assertEqual(code, 1)
        self.assertIn("not scored yet", out)
        self.assertFalse(os.path.exists(self.out))

    def test_refuses_bad_header(self):
        code, _ = self.run_cli(ROWS, header=validate_p2.COLUMNS[:-1])
        self.assertEqual(code, 1)
        self.assertFalse(os.path.exists(self.out))

    def test_refuses_missing_file(self):
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            code = summarize_p2.main(["summarize_p2.py", os.path.join(self.tmp.name, "nope.csv"),
                                      "--out", self.out])
        self.assertNotEqual(code, 0)
        self.assertFalse(os.path.exists(self.out))

    def test_default_output_is_not_the_p1_results_file(self):
        self.assertEqual(os.path.basename(summarize_p2.DEFAULT_OUT), "results_p2.json")
        self.assertEqual(os.path.basename(os.path.dirname(summarize_p2.DEFAULT_OUT)), "p2")

    # --- per-arm numbers (worked by hand) ------------------------------------------------

    def test_top_level_shape(self):
        r = self.results()
        self.assertEqual(r["schema_version"], 1)
        self.assertEqual(r["clips"], 6)
        self.assertEqual(list(r["arms"]), ["A", "B", "C"])
        self.assertEqual(r["arms"]["A"]["model_shown"], "Gen-4.5")
        self.assertEqual(r["arms"]["B"]["model_shown"], "Seedance 2.5")
        self.assertEqual(r["arms"]["C"]["model_shown"], "Gemini Omni 1.1 Flash")

    def test_arm_a(self):
        a = self.results()["arms"]["A"]
        # 2 clips, both acceptable
        self.assertEqual((a["clips"], a["acceptable"], a["acceptable_rate"]), (2, 2, 1.0))
        # geometry 5,4 -> mean 4.5 best 5 | plan 4,4 -> 4.0, 4 | realism 4,3 -> 3.5, 4 | temporal 5,4 -> 4.5, 5
        self.assertEqual(a["scores"]["geometry"], {"mean": 4.5, "best": 5})
        self.assertEqual(a["scores"]["plan"], {"mean": 4.0, "best": 4})
        self.assertEqual(a["scores"]["realism"], {"mean": 3.5, "best": 4})
        self.assertEqual(a["scores"]["temporal"], {"mean": 4.5, "best": 5})
        # events 0,1 -> mean 0.5
        self.assertEqual(a["temporal_events_mean"], 0.5)
        # credits 60+60=120, minutes 2.0+2.5=4.5; per acceptable: 120/2=60, 4.5/2=2.25
        self.assertEqual((a["credits_total"], a["minutes_total"]), (120, 4.5))
        self.assertEqual((a["credits_per_acceptable"], a["minutes_per_acceptable"]), (60, 2.25))
        self.assertEqual(a["failures_by_type"], {"identity": 1})

    def test_arm_b(self):
        b = self.results()["arms"]["B"]
        self.assertEqual((b["clips"], b["acceptable"], b["acceptable_rate"]), (2, 1, 0.5))
        # geometry 5,3 | plan 5,4 | realism 5,4 | temporal 5,3
        self.assertEqual(b["scores"]["geometry"], {"mean": 4.0, "best": 5})
        self.assertEqual(b["scores"]["plan"], {"mean": 4.5, "best": 5})
        self.assertEqual(b["scores"]["realism"], {"mean": 4.5, "best": 5})
        self.assertEqual(b["scores"]["temporal"], {"mean": 4.0, "best": 5})
        self.assertEqual(b["temporal_events_mean"], 1.0)  # events 0,2
        # credits 300, minutes 6.5, one acceptable clip
        self.assertEqual((b["credits_total"], b["minutes_total"]), (300, 6.5))
        self.assertEqual((b["credits_per_acceptable"], b["minutes_per_acceptable"]), (300, 6.5))
        self.assertEqual(b["failures_by_type"], {"morph": 1})

    def test_arm_c(self):
        c = self.results()["arms"]["C"]
        self.assertEqual((c["clips"], c["acceptable"], c["acceptable_rate"]), (2, 1, 0.5))
        # geometry 2,4 | plan 3,2 | realism 3,4 | temporal 2,4
        self.assertEqual(c["scores"]["geometry"], {"mean": 3.0, "best": 4})
        self.assertEqual(c["scores"]["plan"], {"mean": 2.5, "best": 3})
        self.assertEqual(c["scores"]["realism"], {"mean": 3.5, "best": 4})
        self.assertEqual(c["scores"]["temporal"], {"mean": 3.0, "best": 4})
        self.assertEqual(c["temporal_events_mean"], 2.0)  # events 3,1
        # credits 51+51=102, minutes 1.0+1.2=2.2
        self.assertEqual((c["credits_total"], c["minutes_total"]), (102, 2.2))
        self.assertEqual((c["credits_per_acceptable"], c["minutes_per_acceptable"]), (102, 2.2))
        self.assertEqual(c["failures_by_type"], {"hallucination": 2})

    def test_no_acceptable_clip_gives_null_not_a_crash(self):
        rows = [list(r) for r in ROWS]
        for r in rows:
            if r[2] == "B":
                r[12] = 0
        code, _ = self.run_cli(rows)
        self.assertEqual(code, 0)
        with open(self.out) as f:
            b = json.load(f)["arms"]["B"]
        self.assertEqual((b["acceptable"], b["acceptable_rate"]), (0, 0.0))
        self.assertIsNone(b["credits_per_acceptable"])
        self.assertIsNone(b["minutes_per_acceptable"])

    # --- failures and gut call -----------------------------------------------------------

    def test_failures_by_type_overall(self):
        # identity 1 (R2), morph 1 (R4), hallucination 2 (R5, R6); clips with no failure are not counted
        self.assertEqual(self.results()["failures_by_type"],
                         {"hallucination": 2, "identity": 1, "morph": 1})

    def test_gut_call_agreement(self):
        g = self.results()["gut_call"]
        # "all four scores at 4 or higher": R1 yes, R2 no (realism 3), R3 yes, R4 no, R5 no, R6 no (plan 2)
        # gut call acceptable:               R1 1,      R2 1,           R3 1,      R4 0,  R5 0,  R6 1
        # agree:                             yes        no              yes        yes    yes    no  -> 4 of 6
        self.assertEqual((g["clips"], g["agree"]), (6, 4))
        self.assertEqual(g["agreement_rate"], 0.667)
        self.assertEqual(g["acceptable_but_scored_below_4"], 2)   # R2, R6
        self.assertEqual(g["unacceptable_but_all_4_plus"], 0)

    def test_per_clip_rows_are_listed_by_blind_id(self):
        clips = self.results()["clip_scores"]
        self.assertEqual([c["blind_id"] for c in clips], ["K1", "K2", "K3", "K4", "K5", "K6"])
        self.assertEqual(clips[1], {
            "blind_id": "K2", "arm": "A", "attempt": 2, "acceptable": 1,
            "geometry": 4, "plan": 4, "realism": 3, "temporal": 4, "temporal_events": 1,
            "all_four_4_plus": False, "failure_type": "identity", "severity": 1,
        })

    # --- printed table -------------------------------------------------------------------

    def test_prints_a_line_per_arm(self):
        code, out = self.run_cli(ROWS)
        self.assertEqual(code, 0)
        for model in ("Gen-4.5", "Seedance 2.5", "Gemini Omni 1.1 Flash"):
            self.assertIn(model, out)
        self.assertIn("results_p2.json", out)

    def test_accept_column_prints_count_of_clips_not_a_bare_rate(self):
        # A bare rate ("1" for 2 of 2) reads like a count next to "clips 2". Print "2/2" instead.
        # By hand: A 2 of 2 acceptable, B 1 of 2, C 1 of 2.
        code, out = self.run_cli(ROWS)
        self.assertEqual(code, 0)
        lines = {m: next(l for l in out.splitlines() if m in l)
                 for m in ("Gen-4.5", "Seedance 2.5", "Gemini Omni 1.1 Flash")}
        self.assertIn(" 2/2 ", lines["Gen-4.5"])
        self.assertIn(" 1/2 ", lines["Seedance 2.5"])
        self.assertIn(" 1/2 ", lines["Gemini Omni 1.1 Flash"])
        header = out.splitlines()[0]
        self.assertIn("acc/n", header)
        self.assertNotIn(" accept", header)


if __name__ == "__main__":
    unittest.main()
