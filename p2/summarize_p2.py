#!/usr/bin/env python3
"""Summarize the P2 clip log into per-model numbers and p2/results_p2.json. Stdlib only.

Usage: python3 p2/summarize_p2.py [p2/log.csv] [--out p2/results_p2.json]
Refuses to run (exit 1, nothing written) if the log fails validate_p2, including unscored rows.
The P1 results.json is never read or written.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import validate_p2  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_LOG = os.path.join(HERE, "log.csv")
DEFAULT_OUT = os.path.join(HERE, "results_p2.json")
SCORES = validate_p2.SCORES
SCHEMA_VERSION = 1


def _r(x):
    return None if x is None else round(x, 3)


def _mean(values):
    return sum(values) / len(values)


def _count(rows, key):
    out = {}
    for r in rows:
        if r[key]:
            out[r[key]] = out.get(r[key], 0) + 1
    return dict(sorted(out.items()))


def _all_four_4_plus(row):
    return all(int(row[s]) >= 4 for s in SCORES)


def summarize_arm(rows):
    acceptable = sum(int(r["acceptable"]) for r in rows)
    credits = sum(float(r["credits"]) for r in rows)
    minutes = sum(float(r["minutes"]) for r in rows)
    return {
        "model_shown": rows[0]["model_shown"],
        "clips": len(rows),
        "acceptable": acceptable,
        "acceptable_rate": _r(acceptable / len(rows)),
        "scores": {
            s: {"mean": _r(_mean([int(r[s]) for r in rows])), "best": max(int(r[s]) for r in rows)}
            for s in SCORES
        },
        "temporal_events_mean": _r(_mean([int(r["temporal_events"]) for r in rows])),
        "credits_total": _r(credits),
        "minutes_total": _r(minutes),
        "credits_per_acceptable": _r(credits / acceptable) if acceptable else None,
        "minutes_per_acceptable": _r(minutes / acceptable) if acceptable else None,
        "failures_by_type": _count(rows, "failure_type"),
    }


def summarize(rows):
    """rows: validated, fully scored log rows (dicts of strings). Returns the results dict."""
    arms = {a: summarize_arm([r for r in rows if r["arm"] == a])
            for a in sorted({r["arm"] for r in rows})}
    agree = sum((r["acceptable"] == "1") == _all_four_4_plus(r) for r in rows)
    clip_scores = []
    for r in rows:
        clip = {"blind_id": r["blind_id"], "arm": r["arm"], "attempt": int(r["attempt"]),
                "acceptable": int(r["acceptable"])}
        clip.update({s: int(r[s]) for s in SCORES})
        clip.update({
            "temporal_events": int(r["temporal_events"]),
            "all_four_4_plus": _all_four_4_plus(r),
            "failure_type": r["failure_type"] or None,
            "severity": int(r["severity"]) if r["severity"] else None,
        })
        clip_scores.append(clip)
    clip_scores.sort(key=lambda c: c["blind_id"])
    return {
        "schema_version": SCHEMA_VERSION,
        "clips": len(rows),
        "arms": arms,
        "failures_by_type": _count(rows, "failure_type"),
        "gut_call": {
            "clips": len(rows),
            "agree": agree,
            "agreement_rate": _r(agree / len(rows)),
            "acceptable_but_scored_below_4": sum(
                r["acceptable"] == "1" and not _all_four_4_plus(r) for r in rows),
            "unacceptable_but_all_4_plus": sum(
                r["acceptable"] == "0" and _all_four_4_plus(r) for r in rows),
        },
        "clip_scores": clip_scores,
    }


def _fmt(x):
    return "n/a" if x is None else f"{x:g}"


def print_table(results):
    print(f"{'arm':<4}{'model':<24}{'clips':>5}{'accept':>8}"
          f"{'geom':>11}{'plan':>11}{'real':>11}{'temp':>11}{'cred/acc':>10}{'min/acc':>9}")
    for arm, a in results["arms"].items():
        cells = "".join(f"{a['scores'][s]['mean']:>6g}/{a['scores'][s]['best']:<4}" for s in SCORES)
        print(f"{arm:<4}{a['model_shown']:<24}{a['clips']:>5}{a['acceptable_rate']:>8g}"
              f"{cells}{_fmt(a['credits_per_acceptable']):>10}{_fmt(a['minutes_per_acceptable']):>9}")
    print("(scores are mean/best of the arm's clips)")
    print("failures by type:", results["failures_by_type"] or "none")
    g = results["gut_call"]
    print(f"gut call agrees with all-four-at-4+ on {g['agree']} of {g['clips']} clips "
          f"({g['agreement_rate']:g})")


def main(argv):
    args = argv[1:]
    out = DEFAULT_OUT
    if "--out" in args:
        i = args.index("--out")
        if i + 1 >= len(args):
            print(__doc__.strip(), file=sys.stderr)
            return 2
        out = args[i + 1]
        del args[i:i + 2]
    if len(args) > 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    log = args[0] if args else DEFAULT_LOG
    try:
        rows, problems = validate_p2.validate_file(log)
    except OSError as e:
        print(f"cannot read {log}: {e}")
        return 1
    if problems or not rows:
        for p in problems or ["log has no rows"]:
            print(p)
        print("Refusing to summarize an invalid log. Fix it first (python3 p2/validate_p2.py).")
        return 1
    results = summarize(rows)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    print_table(results)
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
