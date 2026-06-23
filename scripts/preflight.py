#!/usr/bin/env python3
"""RelGate preflight checks. Runs locally; makes no API calls."""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "configs" / "experiment_config.json"
CASES_DIR = ROOT / "benchmark" / "cases"
PROMPTS_DIR = ROOT / "prompts"

CRITICAL_GATES = {"G1", "G2", "G3", "G4"}
REQUIRED_CASE_FIELDS = [
    "case_id", "case_type", "change_summary", "diff_or_config", "service_context",
    "deployment_plan", "rollback_plan", "observability_evidence", "alerting_evidence",
    "owner_oncall_evidence", "slo_reliability_impact", "blast_radius", "validation_evidence",
    "ground_truth",
]


def fail(msg: str) -> None:
    print(f"ERROR: {msg}")
    sys.exit(1)


def warn(msg: str) -> None:
    print(f"WARNING: {msg}")


def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except Exception as e:
        fail(f"Failed to parse JSON {path}: {e}")


def check_no_macos_metadata():
    bad = []
    for p in ROOT.rglob("*"):
        name = p.name
        if name == ".DS_Store" or name.startswith("._") or "__MACOSX" in p.parts:
            bad.append(str(p.relative_to(ROOT)))
    if bad:
        fail("macOS metadata present: " + ", ".join(bad[:20]))


def check_config():
    cfg = load_json(CONFIG)
    forbidden = [x.lower() for x in cfg.get("forbidden_model_families", [])]
    models = cfg.get("models", [])
    if len(models) != 3:
        fail(f"Expected exactly 3 models, found {len(models)}")
    ids = []
    for m in models:
        mid = m.get("model_id", "")
        ids.append(mid)
        lo = mid.lower()
        if any(f in lo for f in forbidden):
            fail(f"Forbidden model family in model_id: {mid}")
        if not mid or "/" not in mid:
            fail(f"Invalid OpenRouter model_id: {mid}")
    if len(set(ids)) != len(ids):
        fail("Duplicate model IDs in config")
    print("Models:", ", ".join(ids))
    return cfg


def check_prompts(cfg):
    required = ["m0_freeform.txt", "m1_checklist.txt", "m2_evidence_grounded.txt"]
    leak_terms = [x.lower() for x in cfg.get("forbidden_prompt_leak_terms", [])]
    for fname in required:
        p = PROMPTS_DIR / fname
        if not p.exists():
            fail(f"Missing prompt file: {fname}")
        txt = p.read_text().lower()
        if "# === system prompt ===" not in txt or "# === user prompt template ===" not in txt:
            fail(f"Prompt {fname} missing required section headers")
        for term in leak_terms:
            if term in txt:
                fail(f"Prompt {fname} appears to leak forbidden term: {term}")
    m0 = (PROMPTS_DIR / "m0_freeform.txt").read_text().lower()
    if any(g in m0 for g in ["g1", "g2", "g3", "g4", "g5", "g6", "g7", "checklist"]):
        warn("M0 contains gate/checklist language. Confirm this is intentional. M0 should be freeform.")
    m2 = (PROMPTS_DIR / "m2_evidence_grounded.txt").read_text().lower()
    for term in ["exact quote", "missing_evidence", "do not infer", "final decision cannot be ready"]:
        if term not in m2:
            fail(f"M2 missing evidence-grounding rule phrase: {term}")


def check_case(path: Path):
    c = load_json(path)
    for f in REQUIRED_CASE_FIELDS:
        if f not in c:
            fail(f"{path.name} missing required field: {f}")
    if not re.match(r"^case_\d{3}$", c["case_id"]):
        fail(f"{path.name} has invalid case_id {c['case_id']}")
    if c["case_id"] != path.stem:
        fail(f"{path.name} stem does not match case_id {c['case_id']}")
    # No TBD placeholders.
    whole = json.dumps(c).lower()
    if "tbd" in whole or "todo" in whole or "fixme" in whole:
        fail(f"{path.name} contains TBD/TODO/FIXME")
    gt = c.get("ground_truth", {})
    expected = gt.get("expected_decision")
    gaps = gt.get("seeded_gaps", [])
    if expected not in {"READY", "FIX-BEFORE-SHIP"}:
        fail(f"{path.name} invalid expected_decision: {expected}")
    if not isinstance(gaps, list):
        fail(f"{path.name} seeded_gaps must be a list")
    for g in gaps:
        if g.get("gate") not in {f"G{i}" for i in range(1, 8)}:
            fail(f"{path.name} invalid gate in gap: {g}")
        if g.get("severity") not in {"critical", "major", "minor"}:
            fail(f"{path.name} invalid severity in gap: {g}")
    critical = [g for g in gaps if g.get("severity") == "critical"]
    if expected == "FIX-BEFORE-SHIP" and not critical:
        fail(f"{path.name} unsafe case must contain at least one critical seeded gap")
    if expected == "READY" and gaps:
        fail(f"{path.name} READY control must have zero seeded gaps")
    if expected == "READY":
        # All critical and major evidence fields should be non-empty and concrete.
        evidence_fields = [
            "deployment_plan", "rollback_plan", "observability_evidence", "alerting_evidence",
            "owner_oncall_evidence", "slo_reliability_impact", "blast_radius", "validation_evidence",
        ]
        for f in evidence_fields:
            v = str(c.get(f, "")).strip()
            if len(v) < 25:
                fail(f"{path.name} READY control has weak/empty {f}")
            vague = ["should be fine", "can revert", "deploy to prod", "we have monitoring"]
            if any(x in v.lower() for x in vague):
                fail(f"{path.name} READY control has vague evidence in {f}: {v}")
    return c


def bundle_to_text(case: dict) -> str:
    fields = [
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
    return "\n".join(f"{label}: {case.get(key, '') or '[not provided]'}" for label, key in fields)


def check_prompt_leakage(cases, cfg):
    leak_terms = [x.lower() for x in cfg.get("forbidden_prompt_leak_terms", [])]
    for c in cases:
        text = bundle_to_text(c).lower()
        for term in leak_terms:
            if term in text:
                fail(f"Bundle text for {c['case_id']} leaks forbidden term: {term}")
        if "seeded" in text or "ground truth" in text:
            fail(f"Bundle text for {c['case_id']} leaks scoring metadata")


def check_run_profile_counts(cases, cfg):
    unsafe = [c for c in cases if c["ground_truth"]["expected_decision"] == "FIX-BEFORE-SHIP"]
    ready = [c for c in cases if c["ground_truth"]["expected_decision"] == "READY"]
    if len(cases) != 12:
        fail(f"Expected exactly 12 cases, found {len(cases)}")
    if len(unsafe) != cfg.get("unsafe_cases_expected", 9):
        fail(f"Expected {cfg.get('unsafe_cases_expected', 9)} unsafe cases, found {len(unsafe)}")
    if len(ready) != cfg.get("ready_control_cases_expected", 3):
        fail(f"Expected {cfg.get('ready_control_cases_expected', 3)} READY controls, found {len(ready)}")
    smoke = set(cfg.get("smoke_cases", []))
    if len(smoke) != 2:
        fail("smoke_cases must contain exactly two case IDs")
    by_id = {c["case_id"]: c for c in cases}
    for cid in smoke:
        if cid not in by_id:
            fail(f"Smoke case {cid} not found")
    smoke_expected = {by_id[cid]["ground_truth"]["expected_decision"] for cid in smoke}
    if smoke_expected != {"READY", "FIX-BEFORE-SHIP"}:
        fail("Smoke cases must include one unsafe and one READY control case")


def main():
    print("=== RelGate Preflight ===")
    check_no_macos_metadata()
    cfg = check_config()
    check_prompts(cfg)
    cases = [check_case(p) for p in sorted(CASES_DIR.glob("case_*.json"))]
    check_prompt_leakage(cases, cfg)
    check_run_profile_counts(cases, cfg)
    print(f"Cases: {len(cases)} total")
    print("Unsafe cases:", sum(c["ground_truth"]["expected_decision"] == "FIX-BEFORE-SHIP" for c in cases))
    print("READY controls:", sum(c["ground_truth"]["expected_decision"] == "READY" for c in cases))
    print("Preflight PASS. No API calls were made.")


if __name__ == "__main__":
    main()
