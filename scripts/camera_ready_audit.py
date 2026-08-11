#!/usr/bin/env python3
"""Camera-ready integrity, strict-evidence, and uncertainty audit.

This script uses only the frozen benchmark cases and raw outputs. It never calls
an API. The accepted scorer is invoked for the current-policy comparison, while
strict quote support is implemented independently here.
"""

from __future__ import annotations

import csv
import json
import math
import re
import sys
from collections import Counter, defaultdict
from itertools import product
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src import score_results as accepted  # noqa: E402


RAW_DIR = ROOT / "results" / "raw_outputs"
CAMERA_DIR = ROOT / "camera_ready"
RESULTS_DIR = ROOT / "results"
EXPECTED_MODELS = {
    "openai/gpt-5.5",
    "x-ai/grok-4.3",
    "meta-llama/llama-4-maverick",
}
EXPECTED_MODES = {
    "m0_freeform",
    "m1_checklist",
    "m2_evidence_grounded",
}
VISIBLE_FIELDS = [
    ("Change Summary", "change_summary"),
    ("Diff / Config", "diff_or_config"),
    ("Service Context", "service_context"),
    ("Deployment Plan", "deployment_plan"),
    ("Rollback Plan", "rollback_plan"),
    ("Observability Evidence", "observability_evidence"),
    ("Alerting Evidence", "alerting_evidence"),
    ("Owner / On-Call", "owner_oncall_evidence"),
    ("SLO / Reliability Impact", "slo_reliability_impact"),
    ("Blast Radius", "blast_radius"),
    ("Validation Evidence", "validation_evidence"),
]
IGNORED_QUOTES = {"ready", "fix-before-ship", "pass", "missing_evidence"}
Z_95 = 1.959963984540054


def normalize(value: str) -> str:
    """Apply only the camera-ready harmless normalization policy."""
    return re.sub(r"\s+", " ", value).strip().casefold()


def visible_bundle(case: dict) -> str:
    """Reconstruct the exact bundle representation supplied to the models."""
    return "\n".join(
        f"{label}: {case.get(key, '') or '[not provided]' }"
        for label, key in VISIBLE_FIELDS
    )


def accepted_bundle(case: dict) -> str:
    """Reproduce the accepted scorer's pre-correction bundle representation."""
    return "\n".join(
        value for key, value in case.items()
        if key != "ground_truth" and isinstance(value, str)
    )


def evidence_quotes(response: str) -> list[str]:
    quotes = [q.strip() for q in re.findall(r'"([^"\n]{8,})"', response)]
    return [q for q in quotes if normalize(q) not in IGNORED_QUOTES]


def current_quote_supported(quote: str, case: dict) -> bool:
    """Reproduce the accepted scorer's permissive support test exactly."""
    q_norm = normalize(quote)
    b_norm = normalize(accepted_bundle(case))
    return q_norm in b_norm or q_norm[:40] in b_norm or q_norm[-40:] in b_norm


def strict_quote_supported(quote: str, case: dict) -> bool:
    """Require the complete normalized quote to be a contiguous bundle span."""
    return normalize(quote) in normalize(visible_bundle(case))


def source_context(quote: str, case: dict) -> str:
    bundle = normalize(visible_bundle(case))
    q_norm = normalize(quote)
    pos = bundle.find(q_norm)
    if pos < 0:
        candidates = [q_norm[:40], q_norm[-40:]]
        positions = [(bundle.find(c), c) for c in candidates if c]
        positions = [(p, c) for p, c in positions if p >= 0]
        if not positions:
            return "NO CONTIGUOUS MATCH IN SUPPLIED BUNDLE"
        pos, candidate = positions[0]
        match_end = pos + len(candidate)
    else:
        match_end = pos + len(q_norm)
    lo = max(0, pos - 80)
    hi = min(len(bundle), match_end + 80)
    return bundle[lo:hi]


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    if not rows:
        raise RuntimeError(f"Refusing to write empty CSV: {path}")
    fields = fields or list(rows[0].keys())
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def wilson(successes: int, trials: int) -> tuple[float, float]:
    if trials <= 0:
        return (math.nan, math.nan)
    p = successes / trials
    z2 = Z_95 * Z_95
    denominator = 1 + z2 / trials
    center = (p + z2 / (2 * trials)) / denominator
    half = Z_95 * math.sqrt((p * (1 - p) + z2 / (4 * trials)) / trials) / denominator
    return center - half, center + half


def aggregate(rows: list[dict], mode: str, model: str | None = None) -> dict:
    selected = [
        r for r in rows
        if r["mode"] == mode and (model is None or r["model"] == model)
    ]
    unsafe = [r for r in selected if r["expected_decision"] == "FIX-BEFORE-SHIP"]
    ready = [r for r in selected if r["expected_decision"] == "READY"]
    evidence_claims = sum(int(r["evidence_claim_count"]) for r in selected)
    unsupported = sum(int(r["unsupported_evidence_claim_count"]) for r in selected)
    critical_total = sum(int(r["critical_gap_count"]) for r in unsafe)
    critical_found = sum(int(r["identified_critical_gap_count"]) for r in unsafe)
    return {
        "model": model or "ALL_MODELS",
        "mode": mode,
        "n": len(selected),
        "unsafe_n": len(unsafe),
        "ready_n": len(ready),
        "decision_correct": sum(int(r["decision_accuracy"]) for r in selected),
        "decision_accuracy": round(mean(float(r["decision_accuracy"]) for r in selected), 3),
        "false_ready_count": sum(int(r["false_ready"]) for r in unsafe),
        "false_ready_rate": round(sum(int(r["false_ready"]) for r in unsafe) / len(unsafe), 3),
        "false_block_count": sum(int(r["false_block"]) for r in ready),
        "false_block_rate": round(sum(int(r["false_block"]) for r in ready) / len(ready), 3),
        "evidence_claim_count": evidence_claims,
        "unsupported_evidence_claim_count": unsupported,
        "unsupported_evidence_rate": round(
            mean(float(r["unsupported_evidence_rate"]) for r in selected), 3
        ),
        "unsupported_evidence_pooled_rate": round(unsupported / evidence_claims, 3)
        if evidence_claims else 0.0,
        "critical_gaps_identified": critical_found,
        "critical_gaps_total": critical_total,
        "critical_gap_recall": round(
            mean(float(r["critical_gap_recall"]) for r in unsafe), 3
        ),
        "critical_gap_recall_pooled": round(critical_found / critical_total, 3),
    }


def interval_rows(groups: list[dict]) -> list[dict]:
    out = []
    for group in groups:
        metrics = [
            ("decision_accuracy", group["decision_correct"], group["n"], "correct decisions"),
            ("false_ready_rate", group["false_ready_count"], group["unsafe_n"], "false READY decisions"),
            ("false_block_rate", group["false_block_count"], group["ready_n"], "false blocks"),
            (
                "unsupported_evidence_pooled_rate",
                group["unsupported_evidence_claim_count"],
                group["evidence_claim_count"],
                "unsupported claims; pooled claim-level estimate",
            ),
            (
                "critical_gap_recall_pooled",
                group["critical_gaps_identified"],
                group["critical_gaps_total"],
                "identified critical-gap observations; pooled estimate",
            ),
        ]
        for metric, successes, trials, note in metrics:
            low, high = wilson(successes, trials)
            out.append({
                "model": group["model"],
                "mode": group["mode"],
                "metric": metric,
                "successes": successes,
                "trials": trials,
                "estimate": f"{successes / trials:.6f}" if trials else "NA",
                "wilson_95_low": f"{low:.6f}" if trials else "NA",
                "wilson_95_high": f"{high:.6f}" if trials else "NA",
                "note": note,
            })
    return out


def main() -> None:
    CAMERA_DIR.mkdir(exist_ok=True)
    cases = accepted.load_cases()
    raw_files = sorted(RAW_DIR.glob("*.json"))
    raw_records = [json.loads(path.read_text()) for path in raw_files]

    if len(raw_files) != 108:
        raise SystemExit(f"BLOCKED_DATA_INCONSISTENCY: expected 108 raw files, found {len(raw_files)}")
    if any(r.get("status") == "error" or str(r.get("response", "")).startswith("ERROR") for r in raw_records):
        raise SystemExit("BLOCKED_DATA_INCONSISTENCY: one or more raw outputs are unusable")

    models = {r["model"] for r in raw_records}
    modes = {r["mode"] for r in raw_records}
    if models != EXPECTED_MODELS:
        raise SystemExit(f"BLOCKED_DATA_INCONSISTENCY: models={sorted(models)}")
    if modes != EXPECTED_MODES:
        raise SystemExit(f"BLOCKED_DATA_INCONSISTENCY: modes={sorted(modes)}")

    tuples = [(r["case_id"], r["model"], r["mode"]) for r in raw_records]
    duplicates = [key for key, count in Counter(tuples).items() if count > 1]
    expected_tuples = set(product(cases, EXPECTED_MODELS, EXPECTED_MODES))
    if duplicates or set(tuples) != expected_tuples:
        missing = sorted(expected_tuples - set(tuples))
        extra = sorted(set(tuples) - expected_tuples)
        raise SystemExit(
            "BLOCKED_DATA_INCONSISTENCY: "
            f"duplicates={duplicates}; missing={missing}; extra={extra}"
        )

    current_rows = []
    strict_rows = []
    sensitivity = []
    quote_totals = defaultdict(lambda: {"claims": 0, "current_unsupported": 0, "strict_unsupported": 0})
    pass_totals = defaultdict(int)

    for path, raw in zip(raw_files, raw_records):
        case = cases[raw["case_id"]]
        baseline = accepted.score_file(path, cases)
        if baseline is None:
            raise SystemExit(f"BLOCKED_DATA_INCONSISTENCY: unusable row {path.name}")

        response = raw.get("response", "")
        quotes = evidence_quotes(response)
        strict_unsupported = 0
        for quote_index, quote in enumerate(quotes, 1):
            current_supported = current_quote_supported(quote, case)
            strict_supported = strict_quote_supported(quote, case)
            quote_totals[raw["mode"]]["claims"] += 1
            quote_totals[raw["mode"]]["current_unsupported"] += int(not current_supported)
            quote_totals[raw["mode"]]["strict_unsupported"] += int(not strict_supported)
            strict_unsupported += int(not strict_supported)
            sensitivity.append({
                "case_id": raw["case_id"],
                "model": raw["model"],
                "mode": raw["mode"],
                "raw_file": path.name,
                "quote_index": quote_index,
                "quote": quote,
                "current_supported": int(current_supported),
                "strict_supported": int(strict_supported),
                "classification_changed": int(current_supported != strict_supported),
                "source_context": source_context(quote, case),
            })

        unsupported_passes = accepted.unsupported_gate_passes(
            response, case["ground_truth"].get("seeded_gaps", [])
        )
        pass_totals[raw["mode"]] += unsupported_passes
        evidence_claims = len(quotes) + unsupported_passes
        current_unsupported = sum(
            int(not current_quote_supported(quote, case)) for quote in quotes
        ) + unsupported_passes
        unsupported_claims = strict_unsupported + unsupported_passes
        current = dict(baseline)
        current.update({
            "evidence_claim_count": evidence_claims,
            "unsupported_evidence_claim_count": current_unsupported,
            "unsupported_evidence_rate": round(current_unsupported / evidence_claims, 3)
            if evidence_claims else 0.0,
            "evidence_hallucination_rate": round(current_unsupported / evidence_claims, 3)
            if evidence_claims else 0.0,
        })
        current_rows.append(current)
        strict = dict(baseline)
        strict.update({
            "evidence_claim_count": evidence_claims,
            "unsupported_evidence_claim_count": unsupported_claims,
            "unsupported_evidence_rate": round(unsupported_claims / evidence_claims, 3)
            if evidence_claims else 0.0,
            "evidence_hallucination_rate": round(unsupported_claims / evidence_claims, 3)
            if evidence_claims else 0.0,
        })
        strict_rows.append(strict)

    if len(current_rows) != 108:
        raise SystemExit(f"BLOCKED_DATA_INCONSISTENCY: usable rows={len(current_rows)}")
    if sum(int(r["parse_success"]) for r in current_rows) != 108:
        raise SystemExit("BLOCKED_DATA_INCONSISTENCY: parse-success count is not 108")

    write_csv(CAMERA_DIR / "exact_evidence_sensitivity.csv", sensitivity)
    write_csv(RESULTS_DIR / "camera_ready_strict_scored_results.csv", strict_rows)

    model_groups = [
        aggregate(strict_rows, mode, model)
        for model in sorted(EXPECTED_MODELS)
        for mode in sorted(EXPECTED_MODES)
    ]
    mode_groups = [aggregate(strict_rows, mode) for mode in sorted(EXPECTED_MODES)]
    write_csv(RESULTS_DIR / "camera_ready_model_level_metrics.csv", model_groups)
    write_csv(RESULTS_DIR / "camera_ready_wilson_intervals.csv", interval_rows(mode_groups + model_groups))

    accepted_summary = accepted.summarize(current_rows)
    strict_summary = accepted.summarize(strict_rows)
    write_csv(RESULTS_DIR / "camera_ready_strict_summary_metrics.csv", strict_summary)

    print("Integrity checks: PASS")
    print(f"Raw files: {len(raw_files)}; usable rows: {len(current_rows)}; parse successes: 108")
    print("Models:", ", ".join(sorted(models)))
    print("Modes:", ", ".join(sorted(modes)))
    print("Duplicate tuples: 0; missing tuples: 0; extra tuples: 0")
    print("\nAccepted/current summary:")
    for row in accepted_summary:
        print(row)
    print("\nStrict summary:")
    for row in strict_summary:
        print(row)
    print("\nQuote sensitivity by mode:")
    for mode in sorted(EXPECTED_MODES):
        values = quote_totals[mode]
        print(
            mode,
            f"quoted_claims={values['claims']}",
            f"current_unsupported_quotes={values['current_unsupported']}",
            f"strict_unsupported_quotes={values['strict_unsupported']}",
            f"unsupported_seeded_gate_passes={pass_totals[mode]}",
        )
    changed = [row for row in sensitivity if row["classification_changed"]]
    print(f"Changed quote classifications: {len(changed)}")
    for row in changed:
        print(
            row["case_id"], row["model"], row["mode"],
            repr(row["quote"]), "context=", row["source_context"]
        )


if __name__ == "__main__":
    main()
