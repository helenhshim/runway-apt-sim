#!/usr/bin/env python3
"""Copy clips to shuffled random ids for blind scoring. Stdlib only.

Usage: python3 p2/blind.py evidence/p2_clips evidence/p2_blind evidence/p2_blind_key.csv
Copies every video in the clips folder to the blind folder as B01.mp4, B02.mp4, ... in a
random order, and writes the key (blind_id, original file) to the key file. Keep the key
closed until scoring is done, then copy each blind_id into log.csv. Refuses to overwrite.
"""
import csv
import os
import random
import shutil
import sys

VIDEO_EXTS = {".mp4", ".mov", ".webm", ".m4v"}


def blind(clips_dir, out_dir, key_path, rng=None):
    """Return the list of (blind_id, original name) written."""
    rng = rng or random.SystemRandom()
    clips = sorted(f for f in os.listdir(clips_dir) if os.path.splitext(f)[1].lower() in VIDEO_EXTS)
    if not clips:
        raise ValueError(f"no video files in {clips_dir}")
    if os.path.exists(key_path):
        raise FileExistsError(f"{key_path} already exists")
    if os.path.isdir(out_dir) and os.listdir(out_dir):
        raise FileExistsError(f"{out_dir} is not empty")
    os.makedirs(out_dir, exist_ok=True)
    rng.shuffle(clips)
    key = []
    for i, name in enumerate(clips, start=1):
        blind_id = f"B{i:02d}"
        shutil.copy2(os.path.join(clips_dir, name), os.path.join(out_dir, blind_id + os.path.splitext(name)[1].lower()))
        key.append((blind_id, name))
    with open(key_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["blind_id", "original"])
        w.writerows(key)
    return key


def main(argv):
    if len(argv) != 4:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    try:
        key = blind(*argv[1:])
    except (ValueError, FileExistsError) as e:
        print(e)
        return 1
    print(f"copied {len(key)} clips to {argv[2]}; key in {argv[3]} (do not open until scored)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
