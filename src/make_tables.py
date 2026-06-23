#!/usr/bin/env python3
"""Generate LaTeX results table from RelGate summary CSV."""
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

label = {
    "m0_freeform": "M0 Freeform",
    "m1_checklist": "M1 Checklist",
    "m2_evidence_grounded": "M2 RelGate",
}

if not SUMMARY.exists():
    raise SystemExit("No summary CSV found. Run score_results.py first.")

rows = list(csv.DictReader(open(SUMMARY)))
lines = []
lines.append("\\begin{table}[t]")
lines.append("\\centering")
lines.append("\\caption{RelGate pilot results aggregated across models. Lower is better for false-ready, false-block, and evidence hallucination; higher is better for recall, accuracy, and actionability.}")
lines.append("\\small")
lines.append("\\begin{tabular}{lrrrrrr}")
lines.append("\\toprule")
lines.append("Mode & Crit. Recall & False Ready & False Block & Evid. Halluc. & Accuracy & Action. \\")
lines.append("\\midrule")
for r in rows:
    lines.append(
        f"{label.get(r['mode'], r['mode'])} & {r['critical_gap_recall']} & {r['false_ready_rate']} & {r['false_block_rate']} & {r['evidence_hallucination_rate']} & {r['decision_accuracy']} & {r['actionability_mean']} \\")
lines.append("\\bottomrule")
lines.append("\\end{tabular}")
lines.append("\\end{table}")
OUT.write_text("\n".join(lines) + "\n")
print(f"Wrote {OUT}")
