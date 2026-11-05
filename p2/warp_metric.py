"""T32: flow-based warping error per clip (automated temporal check, HEL-94).

For each consecutive frame pair (t, t+1) of the OUTPUT clip: Farneback flow t->t+1 and
t+1->t, drop pixels that fail a forward-backward check or leave the frame, warp frame t+1
back to t, score = mean L1 of the remaining pixels (0 to 255 scale, on a 640x360 copy).
Lower = more consistent. Floor = same pipeline on the start frame held still with small
grain, so it shows what the metric reads on a clip with nothing happening.

Pitfalls (also printed): there is no input-render walkthrough, so flow comes from the
output itself (temporal consistency, not fidelity to a camera path); blur and flat walls
score low; real reflections and new lighting count as error; a frozen clip scores near 0
(read mean_flow beside it); Farneback is a classical flow, not RAFT.

Usage: python3 p2/warp_metric.py CLIP [CLIP ...] --start evidence/p2_astra_start.png --out DIR
Writes DIR/<clip>.csv and DIR/<clip>.png and prints one summary row per clip.
Clips are never copied into the repo.
"""
import argparse
import csv
import os
import sys

import cv2
import numpy as np

W, H = 640, 360


def read_frames(path, size=(W, H)):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        raise ValueError("cannot open " + path)
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(cv2.resize(f, size, interpolation=cv2.INTER_AREA))
    cap.release()
    return frames


def _flow(a, b):
    return cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 4, 21, 3, 5, 1.1, 0)


def _warp(img, flow):
    h, w = flow.shape[:2]
    gx, gy = np.meshgrid(np.arange(w, dtype=np.float32), np.arange(h, dtype=np.float32))
    mx, my = gx + flow[..., 0], gy + flow[..., 1]
    return cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT), mx, my


def pair_error(f0, f1):
    """Return (error, valid_fraction, mean_flow) for one pair of BGR frames."""
    g0 = cv2.cvtColor(f0, cv2.COLOR_BGR2GRAY)
    g1 = cv2.cvtColor(f1, cv2.COLOR_BGR2GRAY)
    fw, bw = _flow(g0, g1), _flow(g1, g0)
    bw_at, mx, my = _warp(bw, fw)  # backward flow sampled where forward flow lands
    inside = (mx >= 0) & (mx <= W - 1) & (my >= 0) & (my <= H - 1)
    d = ((fw + bw_at) ** 2).sum(-1)
    lim = 0.01 * ((fw ** 2).sum(-1) + (bw_at ** 2).sum(-1)) + 0.5
    mask = inside & (d < lim)
    warped, _, _ = _warp(f1.astype(np.float32), fw)
    err = np.abs(warped - f0.astype(np.float32)).mean(-1)
    n = int(mask.sum())
    if n < 0.05 * mask.size:  # nearly everything occluded: no usable measurement
        return float("nan"), n / mask.size, float(np.linalg.norm(fw, axis=-1).mean())
    return float(err[mask].mean()), n / mask.size, float(np.linalg.norm(fw, axis=-1).mean())


def clip_errors(frames):
    rows = [pair_error(frames[i], frames[i + 1]) for i in range(len(frames) - 1)]
    return np.array([r[0] for r in rows]), np.array([r[1] for r in rows]), np.array([r[2] for r in rows])


def floor_frames(start_path, n=121, sigma=1.5, seed=0):
    img = cv2.imread(start_path)
    if img is None:
        raise ValueError("cannot read " + start_path)
    img = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA).astype(np.float32)
    rng = np.random.default_rng(seed)
    return [np.clip(img + rng.normal(0, sigma, img.shape), 0, 255).astype(np.uint8) for _ in range(n)]


def spikes(err, k=3.0):
    """Pair indices whose error is above median + k * MAD (nan ignored)."""
    e = err[~np.isnan(err)]
    if len(e) == 0:
        return []
    med = np.median(e)
    mad = np.median(np.abs(e - med)) or 1e-6
    return [i for i, v in enumerate(err) if not np.isnan(v) and v > med + k * 1.4826 * mad]


def plot(err, floor_mean, title, path):
    w, h = 900, 300
    img = np.full((h, w, 3), 255, np.uint8)
    top = max(np.nanmax(err) if len(err) else 1, floor_mean * 2, 1) * 1.1
    x = lambda i: int(40 + i * (w - 60) / max(len(err) - 1, 1))
    y = lambda v: int(h - 30 - v / top * (h - 60))
    cv2.line(img, (40, y(floor_mean)), (w - 20, y(floor_mean)), (0, 160, 0), 1)
    pts = [(x(i), y(v)) for i, v in enumerate(err) if not np.isnan(v)]
    for a, b in zip(pts, pts[1:]):
        cv2.line(img, a, b, (200, 60, 0), 2)
    cv2.putText(img, f"{title}  green = floor {floor_mean:.2f}  y max {top:.1f}", (40, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
    cv2.putText(img, "frame pair ->", (w // 2, h - 8), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)
    cv2.imwrite(path, img)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("clips", nargs="+")
    ap.add_argument("--start", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    os.makedirs(a.out, exist_ok=True)
    fe, _, _ = clip_errors(floor_frames(a.start))
    floor = float(np.nanmean(fe))
    print(f"floor (start frame held still, grain sigma 1.5): {floor:.3f}")
    print("clip,frames,mean_err,p95_err,max_err,mean_valid,mean_flow,spike_times_s")
    for p in a.clips:
        name = os.path.basename(p).replace("evidence:", "")
        fr = read_frames(p)
        err, valid, flow = clip_errors(fr)
        sp = spikes(err)
        stem = os.path.join(a.out, name)
        with open(stem + ".csv", "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["pair", "t_s", "err", "valid_frac", "mean_flow"])
            for i in range(len(err)):
                w.writerow([i, round(i / 24, 3), round(float(err[i]), 4), round(float(valid[i]), 4), round(float(flow[i]), 4)])
        plot(err, floor, name, stem + ".png")
        print(f"{name},{len(fr)},{np.nanmean(err):.3f},{np.nanpercentile(err, 95):.3f},"
              f"{np.nanmax(err):.3f},{valid.mean():.3f},{flow.mean():.3f},"
              + " ".join(f"{i / 24:.2f}" for i in sp))
    return 0


if __name__ == "__main__":
    sys.exit(main())
