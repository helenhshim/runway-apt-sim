#!/usr/bin/env python3
"""Validate the CSV log, load it into SQLite, run rollup.sql and write results.json.

Usage: python3 export_json.py log.csv [results.json] [--db eval.db]
The results.json shape is consumed by the portfolio page. Do not change it without telling Helen.
"""
import argparse
import datetime
import json
import os
import sqlite3
import sys

import validate_log

HERE = os.path.dirname(os.path.abspath(__file__))
INT_FIELDS = {"attempt", "landmarks_kept", "acceptable", "layout", "lighting", "furniture", "severity"}
REAL_FIELDS = {"credits", "minutes", "scale_error_pct"}


class InvalidLog(Exception):
    def __init__(self, problems):
        super().__init__("\n".join(problems))
        self.problems = problems


def connect(db_path=":memory:"):
    return sqlite3.connect(db_path)


def _read(name):
    with open(os.path.join(HERE, name), encoding="utf-8") as f:
        return f.read()


def _convert(col, text):
    if text == "":
        return None
    if col in INT_FIELDS:
        return int(float(text))
    if col in REAL_FIELDS:
        return float(text)
    return text


def load(conn, rows):
    conn.executescript(_read("schema.sql"))
    conn.executemany(
        f"INSERT INTO runs ({', '.join(validate_log.COLUMNS)}) "
        f"VALUES ({', '.join('?' * len(validate_log.COLUMNS))})",
        [[_convert(c, r[c]) for c in validate_log.COLUMNS] for r in rows],
    )
    conn.executescript(_read("rollup.sql"))


def _num(x):
    """Round floats for stable JSON; whole numbers become ints."""
    if x is None:
        return None
    x = round(x, 4)
    return int(x) if x == int(x) else x


def build_results(conn, now=None):
    conn.row_factory = sqlite3.Row
    cases = []
    for c in conn.execute("SELECT * FROM case_stats ORDER BY first_row"):
        runs = [
            {
                "attempt": r["attempt"],
                "layout": r["layout"],
                "lighting": r["lighting"],
                "furniture": r["furniture"],
                "landmarks_kept": r["landmarks_kept"],
                "scale_error_pct": _num(r["scale_error_pct"]),
                "acceptable": bool(r["acceptable"]),
                "credits": _num(r["credits"]),
                "minutes": _num(r["minutes"]),
                "failure_type": r["failure_type"],
                "severity": r["severity"],
            }
            for r in conn.execute(
                "SELECT * FROM runs WHERE case_id = ? ORDER BY attempt", (c["case_id"],)
            )
        ]
        cases.append({
            "case_id": c["case_id"],
            "room": c["room"],
            "runs": runs,
            "mean": {k: _num(c[f"mean_{k}"]) for k in ("layout", "lighting", "furniture")},
            "best_of_2": {k: _num(c[f"best_{k}"]) for k in ("layout", "lighting", "furniture")},
        })
    s = conn.execute("SELECT * FROM summary").fetchone()
    failures = {
        r["failure_type"]: r["n"]
        for r in conn.execute("SELECT failure_type, n FROM failures_by_type ORDER BY failure_type")
    }
    now = now or datetime.datetime.now(datetime.timezone.utc)
    return {
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "cases": cases,
        "totals": {
            "acceptable_rate": _num(s["acceptable_rate"]),
            "credits_per_acceptable": _num(s["credits_per_acceptable"]),
            "minutes_per_acceptable": _num(s["minutes_per_acceptable"]),
            "failures_by_type": failures,
        },
    }


def export(csv_path, out_path, db_path=None):
    rows, problems = validate_log.validate_file(csv_path)
    if problems:
        raise InvalidLog(problems)
    if db_path and os.path.exists(db_path):
        os.remove(db_path)
    conn = connect(db_path or ":memory:")
    try:
        load(conn, rows)
        results = build_results(conn)
    finally:
        conn.close()
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
        f.write("\n")
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv")
    ap.add_argument("out", nargs="?", default="results.json")
    ap.add_argument("--db", help="also keep the SQLite file here (for ad-hoc queries on rollup.sql views)")
    args = ap.parse_args(argv)
    try:
        export(args.csv, args.out, args.db)
    except InvalidLog as e:
        for p in e.problems:
            print(p)
        print(f"{len(e.problems)} problem(s) found. results.json not written.")
        return 1
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
