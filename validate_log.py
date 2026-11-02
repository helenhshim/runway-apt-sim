#!/usr/bin/env python3
"""Validate the staging-eval CSV log. Stdlib only.

Usage: python3 validate_log.py log.csv
Prints one line per problem ("row N: ...", row 1 is the header) and exits 1 if any.
"""
import csv
import sys

COLUMNS = [
    "run_id", "case_id", "room", "attempt", "surface", "model_shown", "prompt_id",
    "credits", "minutes", "acceptable", "landmarks_kept", "scale_error_pct",
    "layout", "lighting", "furniture", "failure_type", "severity", "notes",
]
FAILURE_TYPES = {
    "geometry", "opening", "scale", "placement", "identity",
    "shadow", "reflection", "material", "hallucination", "side_effect",
}
REQUIRED = ["run_id", "case_id", "room", "surface", "model_shown", "prompt_id", "credits"]
SCORES = ["layout", "lighting", "furniture"]


def _number(text):
    try:
        return float(text)
    except ValueError:
        return None


def _int_in(row, field, lo, hi, problems, n):
    text = row[field]
    value = _number(text)
    if value is None or value != int(value) or not lo <= value <= hi:
        problems.append(f"row {n}: {field} must be an integer {lo} to {hi}, got {text!r}")
        return None
    return int(value)


def validate_row(row, n):
    """Return a list of problem strings for one row (n is the CSV line number)."""
    problems = []
    for field in REQUIRED:
        if not row[field]:
            problems.append(f"row {n}: {field} is missing")
    if row["credits"]:
        c = _number(row["credits"])
        if c is None or c < 0:
            problems.append(f"row {n}: credits must be a number >= 0, got {row['credits']!r}")
    m = _number(row["minutes"])
    if m is None or m < 0:
        problems.append(f"row {n}: minutes must be a number >= 0, got {row['minutes']!r}")
    _int_in(row, "attempt", 1, 99, problems, n)
    _int_in(row, "acceptable", 0, 1, problems, n)
    _int_in(row, "landmarks_kept", 0, 8, problems, n)
    for field in SCORES:
        _int_in(row, field, 1, 5, problems, n)
    if row["scale_error_pct"] and _number(row["scale_error_pct"]) is None:
        problems.append(f"row {n}: scale_error_pct must be a number or blank, got {row['scale_error_pct']!r}")
    if row["failure_type"] and row["failure_type"] not in FAILURE_TYPES:
        problems.append(
            f"row {n}: failure_type {row['failure_type']!r} is not one of {sorted(FAILURE_TYPES)}"
        )
    if row["severity"]:
        _int_in(row, "severity", 1, 3, problems, n)
    if bool(row["failure_type"]) != bool(row["severity"]):
        problems.append(f"row {n}: failure_type and severity must both be filled or both blank")
    return problems


def validate_file(path):
    """Return (rows, problems). rows are dicts of stripped strings, only trustworthy if problems is empty."""
    problems, rows = [], []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if header is None:
            return rows, ["header: file is empty"]
        header = [h.strip() for h in header]
        if header != COLUMNS:
            return rows, [f"header: expected {COLUMNS}, got {header}"]
        seen, seen_attempts = {}, {}
        for n, values in enumerate(reader, start=2):
            if not any(v.strip() for v in values):
                continue
            if len(values) != len(COLUMNS):
                problems.append(f"row {n}: expected {len(COLUMNS)} columns, got {len(values)}")
                continue
            row = {c: v.strip() for c, v in zip(COLUMNS, values)}
            problems.extend(validate_row(row, n))
            if row["run_id"] in seen:
                problems.append(f"row {n}: run_id {row['run_id']!r} already used on row {seen[row['run_id']]}")
            seen.setdefault(row["run_id"], n)
            key = (row["case_id"], row["attempt"])
            if key in seen_attempts:
                problems.append(
                    f"row {n}: case_id {key[0]!r} attempt {key[1]} already used on row {seen_attempts[key]}"
                )
            seen_attempts.setdefault(key, n)
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
        print(f"{len(problems)} problem(s) found. Fix the log before rolling up.")
        return 1
    print(f"OK: {len(rows)} rows valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
