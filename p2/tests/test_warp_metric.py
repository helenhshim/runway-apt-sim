"""Tests for p2/warp_metric.py on synthetic frames (no real clips).

Run: python3 -m unittest discover -s p2/tests -v
"""
import os
import sys
import unittest

import numpy as np

P2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, P2)

import warp_metric as wm  # noqa: E402


def textured(seed=1):
    rng = np.random.default_rng(seed)
    small = rng.integers(0, 255, (36, 64, 3), dtype=np.uint8)
    import cv2
    return cv2.GaussianBlur(cv2.resize(small, (wm.W, wm.H), interpolation=cv2.INTER_CUBIC), (0, 0), 2)


def shift(img, dx):
    return np.roll(img, dx, axis=1)


class WarpMetricTest(unittest.TestCase):
    def test_identical_frames_near_zero(self):
        e, v, f = wm.pair_error(textured(), textured())
        self.assertLess(e, 0.5)
        self.assertLess(f, 0.2)

    def test_smooth_pan_scores_low(self):
        a = textured()
        e, v, f = wm.pair_error(a, shift(a, 3))
        self.assertLess(e, 6.0)
        self.assertGreater(f, 1.5)  # motion was seen

    def test_flicker_scores_higher_than_pan(self):
        a = textured()
        pan, _, _ = wm.pair_error(a, shift(a, 3))
        flick, _, _ = wm.pair_error(a, np.clip(a.astype(int) + 60, 0, 255).astype(np.uint8))
        self.assertGreater(flick, pan + 10)

    def test_unrelated_frames_score_high(self):
        e, _, _ = wm.pair_error(textured(1), textured(2))
        self.assertTrue(np.isnan(e) or e > 20)

    def test_spikes_found(self):
        err = np.full(50, 2.0)
        err += np.random.default_rng(0).normal(0, 0.1, 50)
        err[20] = 15.0
        self.assertEqual(wm.spikes(err), [20])


if __name__ == "__main__":
    unittest.main()
