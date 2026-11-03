#!/usr/bin/env python3
"""Validate the P2 build log (p2/build_log.csv). Stdlib only.

Usage: python3 p2/validate_build_log.py p2/build_log.csv
Prints one line per problem ("row N: ...", row 1 is the header) and exits 1 if any.
Build rows are never scored; this only checks that every generation was logged usably.
"""
import csv
import re
import sys

COLUMNS = [
    "when", "model", "iteration", "prompt_id", "changed", "credits_shown",
    "balance_after", "minutes", "output_file", "keep", "tag", "observation",
]
ITERATIONS = {"b01", "b02", "b03", "demo", "draft"}
TAGS = {"broke", "surprised", "cost", "ux", "routing", "quality"}
REQUIRED = ["when", "model", "iteration", "prompt_id", "output_file", "keep", "tag", "observation"]
WHEN = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}$")


def _number(text):
    try:
        return float(text)
    except ValueError:
        return None


def validate_row(row, n):
    """Return a list of problem strings for one row (n is the CSV line number)."""
    problems = []
    for field in REQUIRED:
        if not row[field]:
            problems.append(f"row {n}: {field} is missing")
    if row["when"] and not WHEN.match(row["when"]):
        problems.append(f"row {n}: when must look like 2026-11-03 18:05, got {row['when']!r}")
    if row["iteration"] and row["iteration"] not in ITERATIONS:
        problems.append(f"row {n}: iteration must be one of {sorted(ITERATIONS)}, got {row['iteration']!r}")
    if row["keep"] and row["keep"] not in {"yes", "no"}:
        problems.append(f"row {n}: keep must be yes or no, got {row['keep']!r}")
    if row["tag"] and row["tag"] not in TAGS:
        problems.append(f"row {n}: tag must be one of {sorted(TAGS)}, got {row['tag']!r}")
    for field in ("credits_shown", "balance_after", "minutes"):
        if row[field]:
            value = _number(row[field])
            if value is None or value < 0:
                problems.append(f"row {n}: {field} must be a number >= 0, got {row[field]!r}")
    if not row["minutes"]:
        problems.append(f"row {n}: minutes is missing")
    if not row["credits_shown"] and not row["balance_after"]:
        problems.append(f"row {n}: credits_shown or balance_after is needed to track cost")
    return problems


def validate_file(path):
    """Return (rows, problems). rows are dicts of stripped strings."""
    problems, rows = [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return rows, ["header: file is empty"]
        header = [h.strip() for h in header]
        if header != COLUMNS:
            return rows, [f"header: expected {COLUMNS}, got {header}"]
        seen = {}
        for n, values in enumerate(reader, start=2):
            if not any(v.strip() for v in values):
                continue
            if len(values) != len(COLUMNS):
                problems.append(f"row {n}: expected {len(COLUMNS)} columns, got {len(values)}")
                continue
            row = {c: v.strip() for c, v in zip(COLUMNS, values)}
            problems.extend(validate_row(row, n))
            out = row["output_file"]
            if out and out in seen:
                problems.append(f"row {n}: output_file {out!r} already used on row {seen[out]}")
            seen.setdefault(out, n)
            rows.append(row)
    return rows, problems


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    rows, problems = validate_file(argv[1])
    for p in problems:
        print(p)
    if problems:
        print(f"{len(problems)} problem(s) found.")
        return 1
    print(f"OK: {len(rows)} rows valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
