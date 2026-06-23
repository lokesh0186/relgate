#!/usr/bin/env python3
"""RelGate scoring script.

Scores raw model outputs against pre-registered seeded gaps and READY controls.
Designed for small ISSRE FA/PH pilot; outputs auditable CSVs.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
CASES_DIR = ROOT / "benchmark" / "cases"
RESULTS_DIR = ROOT / "results"
GATES = [f"G{i}" for i in range(1, 8)]
CRITICAL_GATES = {"G1", "G2", "G3", "G4"}

KEY_CONCEPTS = {
    "G1": ["observability", "dashboard", "metric", "monitor", "log", "trace", "grafana", "cloudwatch", "datadog"],
    "G2": ["alert", "alerting", "pagerduty", "alarm", "notification"],
    "G3": ["rollout", "canary", "staged", "gradual", "blast", "feature flag", "maxunavailable", "phased"],
    "G4": ["rollback", "revert", "undo", "recovery", "trigger"],
    "G5": ["owner", "on-call", "oncall", "escalation", "contact", "team"],
    "G6": ["slo", "sli", "error budget", "customer impact", "reliability impact", "latency", "availability"],
    "G7": ["test", "validation", "staging", "dry-run", "integration", "load test", "backtest", "promtool"],
}
ABSENCE_MARKERS = [
    "missing", "absent", "not provided", "no ", "lack", "without", "does not include",
    "not specified", "not mentioned", "empty", "missing_evidence", "fail", "insufficient",
    "vague", "unclear", "not enough", "no evidence",
]
PASS_MARKERS = ["pass", "passes", "satisfied", "sufficient", "provided", "present", "included", "configured"]


def load_cases():
    cases = {}
    for p in sorted(CASES_DIR.glob("case_*.json")):
        c = json.loads(p.read_text())
        cases[c["case_id"]] = c
    return cases


def bundle_text(case: dict) -> str:
    parts = []
    for k, v in case.items():
        if k != "ground_truth" and isinstance(v, str):
            parts.append(v)
    return "\n".join(parts)


def extract_decision(text: str) -> str:
    t = text.upper()
    # Prefer explicit final decision line.
    m = re.search(r"FINAL\s+DECISION\s*:\s*(READY|FIX[-\s]?BEFORE[-\s]?SHIP)", t)
    if m:
        val = m.group(1).replace(" ", "-")
        return "FIX-BEFORE-SHIP" if "FIX" in val else "READY"
    if "FIX-BEFORE-SHIP" in t or "FIX BEFORE SHIP" in t:
        return "FIX-BEFORE-SHIP"
    if "NOT READY" in t or "NOT PRODUCTION READY" in t or "BLOCK" in t:
        return "FIX-BEFORE-SHIP"
    if re.search(r"\bREADY\b", t) or "READY FOR PRODUCTION" in t:
        return "READY"
    return "UNPARSED"


def extract_gate_verdicts(text: str) -> dict:
    verdicts = {}
    for gate in GATES:
        # Matches: G1: PASS, Gate: G1 ... Verdict: PASS, etc.
        pat1 = re.search(rf"\b{gate}\b\s*[:\-]\s*(PASS|FAIL|MISSING_EVIDENCE|MISSING EVIDENCE)", text, re.I)
        if pat1:
            verdicts[gate] = pat1.group(1).upper().replace(" ", "_")
            continue
        # Look for local window around gate.
        idx = text.upper().find(gate)
        if idx >= 0:
            window = text[idx:idx+350].lower()
            if "missing_evidence" in window or "missing evidence" in window or "fail" in window:
                verdicts[gate] = "MISSING_EVIDENCE" if "missing" in window else "FAIL"
            elif "pass" in window:
                verdicts[gate] = "PASS"
    return verdicts


def gap_identified(text: str, gap: dict) -> bool:
    tl = text.lower()
    gate = gap["gate"]
    gate_mentioned = gate.lower() in tl
    concept_found = any(c in tl for c in KEY_CONCEPTS.get(gate, []))
    if not (gate_mentioned or concept_found):
        return False
    # Strong evidence: any absence marker near any concept or gate.
    anchors = [gate.lower()] + KEY_CONCEPTS.get(gate, [])
    for a in anchors:
        pos = tl.find(a)
        if pos >= 0:
            window = tl[max(0, pos-140):pos+200]
            if any(m in window for m in ABSENCE_MARKERS):
                return True
    # Fallback: whole response says missing and concept is present.
    return concept_found and any(m in tl for m in ABSENCE_MARKERS)


def count_identified_gaps(text: str, seeded_gaps: list) -> tuple[int, int]:
    total = 0
    critical = 0
    for gap in seeded_gaps:
        if gap_identified(text, gap):
            total += 1
            if gap.get("severity") == "critical":
                critical += 1
    return total, critical


def exact_quote_support(text: str, case: dict) -> tuple[int, int]:
    """Return (quoted_evidence_claims, unsupported_quotes)."""
    quotes = [q.strip() for q in re.findall(r'"([^"\n]{8,})"', text)]
    btxt = re.sub(r"\s+", " ", bundle_text(case)).lower()
    total = 0
    unsupported = 0
    for q in quotes:
        q_norm = re.sub(r"\s+", " ", q).lower()
        # Ignore quoted labels/formatting that are not evidence claims.
        if q_norm in {"ready", "fix-before-ship", "pass", "missing_evidence"}:
            continue
        total += 1
        if q_norm not in btxt and q_norm[:40] not in btxt and q_norm[-40:] not in btxt:
            unsupported += 1
    return total, unsupported


def unsupported_gate_passes(text: str, seeded_gaps: list) -> int:
    """Count cases where model marks a seeded-missing gate as PASS/satisfied."""
    verdicts = extract_gate_verdicts(text)
    count = 0
    missing_gates = {g["gate"] for g in seeded_gaps}
    for gate in missing_gates:
        if verdicts.get(gate) == "PASS":
            count += 1
    return count


def actionability_score(text: str) -> float:
    tl = text.lower()
    # Split on bullets and recommendation-like clauses.
    chunks = re.split(r"\n\s*[-*]|recommendation:|recommended_actions:|should |must |need to |add |include ", tl)
    recs = [c.strip()[:240] for c in chunks if len(c.strip()) > 25]
    if not recs:
        return 0.0
    scores = []
    for r in recs:
        specific = any(x in r for x in ["trigger", "threshold", "pagerduty", "grafana", "rollback", "canary", "staging", "slo", "p99", "%", ">", "<", "within", "if "])
        if specific and len(r) > 50:
            scores.append(2.0)
        elif len(r) > 35:
            scores.append(1.0)
        else:
            scores.append(0.5)
    return round(mean(scores), 2)


def score_file(path: Path, cases: dict) -> dict | None:
    raw = json.loads(path.read_text())
    if raw.get("status") == "error" or str(raw.get("response", "")).startswith("ERROR"):
        return None
    case = cases[raw["case_id"]]
    gt = case["ground_truth"]
    expected = gt["expected_decision"]
    seeded = gt.get("seeded_gaps", [])
    critical_gaps = [g for g in seeded if g.get("severity") == "critical"]
    response = raw.get("response", "")

    decision = extract_decision(response)
    id_total, id_crit = count_identified_gaps(response, seeded)
    quote_total, quote_unsupported = exact_quote_support(response, case)
    unsupported_pass = unsupported_gate_passes(response, seeded)
    halluc_claims = quote_unsupported + unsupported_pass
    evidence_claims = quote_total + unsupported_pass
    halluc_rate = round(halluc_claims / evidence_claims, 3) if evidence_claims else 0.0

    is_unsafe = expected == "FIX-BEFORE-SHIP"
    is_ready_control = expected == "READY"
    false_ready = 1 if is_unsafe and decision == "READY" else 0
    false_block = 1 if is_ready_control and decision == "FIX-BEFORE-SHIP" else 0
    decision_accuracy = 1 if decision == expected else 0
    parse_success = 1 if decision in {"READY", "FIX-BEFORE-SHIP"} else 0

    usage = raw.get("usage", {}) or {}
    return {
        "case_id": raw["case_id"],
        "case_type": raw.get("case_type", case.get("case_type", "")),
        "expected_decision": expected,
        "model": raw["model"],
        "mode": raw["mode"],
        "decision": decision,
        "parse_success": parse_success,
        "seeded_gap_count": len(seeded),
        "critical_gap_count": len(critical_gaps),
        "identified_gap_count": id_total,
        "identified_critical_gap_count": id_crit,
        "gap_recall": round(id_total / len(seeded), 3) if seeded else "NA",
        "critical_gap_recall": round(id_crit / len(critical_gaps), 3) if critical_gaps else "NA",
        "false_ready": false_ready,
        "false_block": false_block,
        "evidence_claim_count": evidence_claims,
        "unsupported_evidence_claim_count": halluc_claims,
        "evidence_hallucination_rate": halluc_rate,
        "actionability_score_mean": actionability_score(response),
        "decision_accuracy": decision_accuracy,
        "latency_seconds": raw.get("latency_seconds", 0),
        "tokens_in": usage.get("prompt_tokens") or usage.get("input_tokens") or 0,
        "tokens_out": usage.get("completion_tokens") or usage.get("output_tokens") or 0,
        "cost_usd": raw.get("estimated_or_reported_cost_usd", ""),
        "raw_file": path.name,
        "notes": "",
    }


def avg(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    return round(mean(vals), 3) if vals else "NA"


def summarize(rows: list) -> list:
    out = []
    modes = ["m0_freeform", "m1_checklist", "m2_evidence_grounded"]
    for mode in modes:
        mr = [r for r in rows if r["mode"] == mode]
        unsafe = [r for r in mr if r["expected_decision"] == "FIX-BEFORE-SHIP"]
        ready = [r for r in mr if r["expected_decision"] == "READY"]
        if not mr:
            continue
        out.append({
            "mode": mode,
            "n": len(mr),
            "unsafe_n": len(unsafe),
            "ready_control_n": len(ready),
            "gap_recall": avg([r["gap_recall"] for r in unsafe]),
            "critical_gap_recall": avg([r["critical_gap_recall"] for r in unsafe]),
            "false_ready_rate": round(sum(r["false_ready"] for r in unsafe) / len(unsafe), 3) if unsafe else "NA",
            "false_block_rate": round(sum(r["false_block"] for r in ready) / len(ready), 3) if ready else "NA",
            "evidence_hallucination_rate": avg([r["evidence_hallucination_rate"] for r in mr]),
            "actionability_mean": avg([r["actionability_score_mean"] for r in mr]),
            "decision_accuracy": round(sum(r["decision_accuracy"] for r in mr) / len(mr), 3),
            "parse_success_rate": round(sum(r["parse_success"] for r in mr) / len(mr), 3),
            "cost_usd_total": round(sum(float(r["cost_usd"] or 0) for r in mr), 4),
        })
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="results/raw_outputs", help="Raw output directory relative to repo root")
    parser.add_argument("--output-prefix", default="full", help="Prefix for scored/summary CSV")
    args = parser.parse_args()

    raw_dir = ROOT / args.input_dir
    if not raw_dir.exists():
        sys.exit(f"Raw dir not found: {raw_dir}")
    cases = load_cases()
    raw_files = sorted(raw_dir.glob("*.json"))
    if not raw_files:
        sys.exit(f"No raw JSON files found in {raw_dir}")

    rows = []
    for p in raw_files:
        r = score_file(p, cases)
        if r:
            rows.append(r)
    if not rows:
        sys.exit("No scoreable rows")

    scored_path = RESULTS_DIR / f"{args.output_prefix}_relgate_scored_results.csv"
    summary_path = RESULTS_DIR / f"{args.output_prefix}_summary_metrics.csv"
    fieldnames = list(rows[0].keys())
    with open(scored_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    summary = summarize(rows)
    with open(summary_path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(summary[0].keys()))
        w.writeheader()
        w.writerows(summary)

    print(f"Scored rows: {len(rows)} -> {scored_path}")
    print(f"Summary -> {summary_path}")
    print("\n=== Summary by mode ===")
    for r in summary:
        print(r)


if __name__ == "__main__":
    main()
