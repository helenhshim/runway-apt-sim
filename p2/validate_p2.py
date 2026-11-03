#!/usr/bin/env python3
"""Validate the P2 clip log (p2/log.csv). Stdlib only.

Usage: python3 p2/validate_p2.py p2/log.csv [--unscored-ok]
Prints one line per problem ("row N: ...", row 1 is the header) and exits 1 if any.
--unscored-ok accepts rows logged at generation time whose score fields are all blank.
"""
import csv
import sys

COLUMNS = [
    "run_id", "case_id", "arm", "attempt", "surface", "model_shown", "prompt_id",
    "ref_images", "duration_s", "aspect_ratio", "credits", "minutes", "acceptable",
    "blind_id", "geometry_checks", "geometry_kept", "geometry", "plan", "realism",
    "temporal", "temporal_events", "failure_type", "severity", "notes",
]
FAILURE_TYPES = {
    "geometry", "opening", "scale", "placement", "identity", "shadow", "reflection",
    "material", "hallucination", "invented_area",
    "flicker", "morph", "pop", "drift", "path_ignored", "render_look",
}
ARMS = {"A", "B", "C"}
REQUIRED = ["run_id", "case_id", "arm", "surface", "model_shown", "prompt_id", "aspect_ratio", "credits"]
SCORES = ["geometry", "plan", "realism", "temporal"]
SCORE_FIELDS = ["blind_id", "geometry_checks", "geometry_kept", *SCORES, "temporal_events"]
MAX_CHECKS = 40  # 8 landmarks x 5 sample frames


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


def _positive(row, field, problems, n, allow_zero=True):
    value = _number(row[field])
    if value is None or value < 0 or (value == 0 and not allow_zero):
        sign = ">= 0" if allow_zero else "> 0"
        problems.append(f"row {n}: {field} must be a number {sign}, got {row[field]!r}")


def validate_row(row, n, unscored_ok=False):
    """Return a list of problem strings for one row (n is the CSV line number)."""
    problems = []
    for field in REQUIRED:
        if not row[field]:
            problems.append(f"row {n}: {field} is missing")
    if row["arm"] and row["arm"] not in ARMS:
        problems.append(f"row {n}: arm must be one of {sorted(ARMS)}, got {row['arm']!r}")
    if row["credits"]:
        _positive(row, "credits", problems, n)
    _positive(row, "minutes", problems, n)
    _positive(row, "duration_s", problems, n, allow_zero=False)
    _int_in(row, "attempt", 1, 99, problems, n)
    _int_in(row, "ref_images", 0, 5, problems, n)
    _int_in(row, "acceptable", 0, 1, problems, n)

    filled = [f for f in SCORE_FIELDS if row[f]]
    if not filled and unscored_ok:
        pass
    elif not filled:
        problems.append(f"row {n}: not scored yet (score fields blank); use --unscored-ok before scoring")
    else:
        for f in SCORE_FIELDS:
            if not row[f]:
                problems.append(f"row {n}: {f} is missing (score fields are all filled or all blank)")
        checks = _int_in(row, "geometry_checks", 1, MAX_CHECKS, problems, n) if row["geometry_checks"] else None
        kept = _int_in(row, "geometry_kept", 0, MAX_CHECKS, problems, n) if row["geometry_kept"] else None
        if checks is not None and kept is not None and kept > checks:
            problems.append(f"row {n}: geometry_kept {kept} is more than geometry_checks {checks}")
        for f in SCORES:
            if row[f]:
                _int_in(row, f, 1, 5, problems, n)
        if row["temporal_events"]:
            _int_in(row, "temporal_events", 0, 99, problems, n)

    if row["failure_type"] and row["failure_type"] not in FAILURE_TYPES:
        problems.append(
            f"row {n}: failure_type {row['failure_type']!r} is not one of {sorted(FAILURE_TYPES)}"
        )
    if row["severity"]:
        _int_in(row, "severity", 1, 3, problems, n)
    if bool(row["failure_type"]) != bool(row["severity"]):
        problems.append(f"row {n}: failure_type and severity must both be filled or both blank")
    return problems


def validate_file(path, unscored_ok=False):
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
        seen = {"run_id": {}, "attempt": {}, "blind_id": {}}
        for n, values in enumerate(reader, start=2):
            if not any(v.strip() for v in values):
                continue
            if len(values) != len(COLUMNS):
                problems.append(f"row {n}: expected {len(COLUMNS)} columns, got {len(values)}")
                continue
            row = {c: v.strip() for c, v in zip(COLUMNS, values)}
            problems.extend(validate_row(row, n, unscored_ok))
            keys = {
                "run_id": row["run_id"],
                "attempt": (row["case_id"], row["arm"], row["attempt"]),
                "blind_id": row["blind_id"] or None,
            }
            for kind, key in keys.items():
                if key is None:
                    continue
                if key in seen[kind]:
                    problems.append(f"row {n}: {kind} {key!r} already used on row {seen[kind][key]}")
                seen[kind].setdefault(key, n)
            rows.append(row)
    return rows, problems


def main(argv):
    args = [a for a in argv[1:] if a != "--unscored-ok"]
    if len(args) != 1:
        print(__doc__.strip(), file=sys.stderr)
        return 2
    rows, problems = validate_file(args[0], unscored_ok="--unscored-ok" in argv)
    for p in problems:
        print(p)
    if problems:
        print(f"{len(problems)} problem(s) found. Fix the log before rolling up.")
        return 1
    print(f"OK: {len(rows)} rows valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
