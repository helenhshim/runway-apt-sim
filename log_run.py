#!/usr/bin/env python3
"""Add one generation to the CSV log by answering prompts. Stdlib only.

Usage: python3 log_run.py [log.csv]      (default log.csv; created with the header if missing)
Press Enter to accept a [default]. run_id is filled automatically; surface, model_shown and
prompt_id default to the previous row. A bad answer is explained and asked again. Nothing is
written until the whole row passes validate_log, and Ctrl-C leaves the file untouched.
"""
import csv
import io
import os
import sys

import validate_log

COLUMNS = validate_log.COLUMNS
CARRY_OVER = ("surface", "model_shown", "prompt_id")
HINTS = {
    "run_id": "blank = next id",
    "model_shown": "type 'not shown' if the app doesn't say",
    "acceptable": "1 = yes, 0 = no; decide before scoring",
    "landmarks_kept": "0 to 8",
    "scale_error_pct": "blank if not measured",
    "layout": "1 to 5", "lighting": "1 to 5", "furniture": "1 to 5",
    "failure_type": "one of " + ", ".join(sorted(validate_log.FAILURE_TYPES)) + "; blank if none",
    "severity": "1 to 3; blank if no failure",
}


def _existing(path):
    if not os.path.exists(path):
        return ""
    with open(path, newline="", encoding="utf-8-sig") as f:
        return f.read()


def _ask(field, default, input_fn):
    hint = f" ({HINTS[field]})" if field in HINTS else ""
    shown = f" [{default}]" if default else ""
    answer = input_fn(f"{field}{hint}{shown}: ").strip()
    return answer or default


def _fields_to_reask(problem):
    # Problems read "row N: <field> ..." so the first word after the row number is the field.
    field = problem.split(": ", 1)[1].split()[0]
    fields = [field] if field in COLUMNS else ["run_id", "case_id", "attempt"]
    if "must both be filled" in problem:
        fields.append("severity")
    return fields


def log_one(path, input_fn=input, output_fn=print):
    """Ask for one row, validate it with the rest of the log, then append it. Returns the row dict."""
    text = _existing(path)
    rows = []
    if text:
        rows, problems = validate_log.validate_file(path)
        if problems:
            raise SystemExit("Existing log has problems, fix them first:\n" + "\n".join(problems))
    previous = rows[-1] if rows else {}
    defaults = {c: previous.get(c, "") if c in CARRY_OVER else "" for c in COLUMNS}

    row = {}
    for c in COLUMNS:
        row[c] = _ask(c, defaults[c], input_fn)
    while True:
        if not row["run_id"]:
            row["run_id"] = f"R{len(rows) + 1}"
        header_line = ",".join(COLUMNS) + "\n"
        buf = io.StringIO()
        csv.writer(buf, lineterminator="\n").writerow([row[c] for c in COLUMNS])
        candidate = (text if text else header_line) + buf.getvalue()
        if text and not text.endswith("\n"):
            candidate = text + "\n" + buf.getvalue()
        tmp = path + ".tmp"
        with open(tmp, "w", newline="", encoding="utf-8") as f:
            f.write(candidate)
        _, problems = validate_log.validate_file(tmp)
        if not problems:
            os.replace(tmp, path)
            output_fn(f"Saved {row['run_id']} ({row['case_id']} attempt {row['attempt']}) to {path}.")
            return row
        os.remove(tmp)
        # Only this row's problems matter; the existing rows were valid when we started.
        for p in problems:
            output_fn(p.replace(f"row {len(rows) + 2}", "this row"))
        if row["run_id"] == f"R{len(rows) + 1}":
            row["run_id"] = ""  # auto id may be the clash; let it be regenerated unless re-asked
        for field in dict.fromkeys(f for p in problems for f in _fields_to_reask(p)):
            row[field] = _ask(field, "", input_fn)


def main(argv):
    path = argv[1] if len(argv) > 1 else "log.csv"
    try:
        while True:
            log_one(path)
            if input("Log another? [y/N]: ").strip().lower() != "y":
                return 0
    except (KeyboardInterrupt, EOFError):
        print("\nStopped. Nothing half-written was saved.")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
