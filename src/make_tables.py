#!/usr/bin/env python3
"""Generate the camera-ready LaTeX Table I from strict summary metrics."""
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SUMMARY = ROOT / "results" / "full_summary_metrics.csv"
if not SUMMARY.exists():
    # allow smoke preview
    SUMMARY = ROOT / "results" / "smoke_summary_metrics.csv"
OUTDIR = ROOT / "paper" / "tables"
OUTDIR.mkdir(parents=True, exist_ok=True)
OUT = OUTDIR / "results_table.tex"

if not SUMMARY.exists():
    raise SystemExit("No summary CSV found. Run score_results.py first.")

rows = list(csv.DictReader(open(SUMMARY)))
by_mode = {row["mode"]: row for row in rows}
required = ["m0_freeform", "m1_checklist", "m2_evidence_grounded"]
if set(by_mode) != set(required):
    raise SystemExit(f"Unexpected mode set: {sorted(by_mode)}")


def values(key):
    return [f"{float(by_mode[mode][key]):.3f}" for mode in required]


metric_rows = [
    ("Critical Gap Recall", "critical_gap_recall", None),
    ("False-Ready Rate ($n{=}27$)", "false_ready_rate", None),
    ("False-Block Rate ($n{=}9$)", "false_block_rate", None),
    ("Unsupported Evid.\\ Claims", "unsupported_evidence_rate", None),
    ("Decision Accuracy ($n{=}36$)", "decision_accuracy", None),
]

lines = [
    "\\begin{table}[t]",
    "\\centering",
    "\\caption{Controlled pilot results across review modes.}",
    "\\label{tab:results}",
    "\\footnotesize",
    "\\begin{tabular}{@{}lccc@{}}",
    "\\toprule",
    "\\textbf{Metric} & \\textbf{M0} & \\textbf{M1} & \\textbf{M2} \\\\",
    "\\midrule",
]
for label, key, _ in metric_rows:
    m0, m1, m2 = values(key)
    lines.append(f"{label} & {m0} & {m1} & {m2} \\\\")
lines.extend(["\\bottomrule", "\\end{tabular}", "\\end{table}"])
OUT.write_text("\n".join(lines) + "\n")
print(f"Wrote {OUT}")
