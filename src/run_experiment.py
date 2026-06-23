#!/usr/bin/env python3
"""RelGate Experiment Runner.

Makes controlled OpenRouter calls for ISSRE 2026 RelGate pilot.
Default use:
  python3 scripts/preflight.py
  python3 src/run_experiment.py --profile smoke --estimate-only
  python3 src/run_experiment.py --profile smoke
  # review smoke results before full run
  python3 src/run_experiment.py --profile full
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple

try:
    import requests
except ImportError:
    sys.exit("Install requests: pip install requests")

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "configs" / "experiment_config.json"
CASES_DIR = ROOT / "benchmark" / "cases"
PROMPTS_DIR = ROOT / "prompts"
RESULTS_DIR = ROOT / "results"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Conservative editable estimates. OpenRouter can change pricing; exact billing is authoritative.
# Prices are USD per 1M tokens. Used only for preflight estimates when OpenRouter usage cost is absent.
PRICE_ESTIMATES_PER_MILLION = {
    "openai/gpt-5.5": {"input": 5.00, "output": 30.00},
    "x-ai/grok-4.3": {"input": 1.25, "output": 2.50},
    "meta-llama/llama-4-maverick": {"input": 0.15, "output": 0.60},
}


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def get_api_key() -> str:
    key = os.environ.get("OPENROUTER_API_KEY", "").strip()
    if not key:
        sys.exit("Set OPENROUTER_API_KEY environment variable.")
    return key


def model_ids(cfg: dict) -> List[str]:
    ids = [m["model_id"] for m in cfg["models"]]
    forbidden = [x.lower() for x in cfg.get("forbidden_model_families", [])]
    for mid in ids:
        if any(f in mid.lower() for f in forbidden):
            sys.exit(f"Forbidden model family detected: {mid}")
    if len(set(ids)) != len(ids):
        sys.exit("Duplicate model IDs in config")
    return ids


def load_prompt(mode: str) -> Tuple[str, str]:
    text = (PROMPTS_DIR / f"{mode}.txt").read_text()
    parts = text.split("# === USER PROMPT TEMPLATE ===")
    if len(parts) != 2:
        sys.exit(f"Prompt {mode} missing '# === USER PROMPT TEMPLATE ==='")
    sys_part = parts[0].replace("# === SYSTEM PROMPT ===", "").strip()
    usr_part = parts[1].strip()
    return sys_part, usr_part


def bundle_to_text(case: dict) -> str:
    """Format only visible change-bundle fields. Ground truth is intentionally excluded."""
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


def approx_tokens(text: str) -> int:
    return max(1, int(len(text) / 4))


def estimate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
    rates = PRICE_ESTIMATES_PER_MILLION.get(model, {"input": 5.0, "output": 15.0})
    return (input_tokens / 1_000_000) * rates["input"] + (output_tokens / 1_000_000) * rates["output"]


def usage_cost_usd(model: str, usage: dict) -> float:
    # OpenRouter may include cost in different fields depending on model/provider.
    for key in ["cost", "total_cost", "cost_usd"]:
        if key in usage:
            try:
                return float(usage[key])
            except Exception:
                pass
    inp = usage.get("prompt_tokens") or usage.get("input_tokens") or 0
    out = usage.get("completion_tokens") or usage.get("output_tokens") or 0
    return estimate_cost(model, int(inp), int(out))


def selected_cases(cfg: dict, profile: str) -> List[Path]:
    if profile == "smoke":
        ids = set(cfg.get("smoke_cases", []))
        paths = [CASES_DIR / f"{cid}.json" for cid in ids]
        missing = [p for p in paths if not p.exists()]
        if missing:
            sys.exit(f"Missing smoke case files: {missing}")
        return sorted(paths)
    if profile == "full":
        return sorted(CASES_DIR.glob(cfg.get("full_cases_glob", "case_*.json")))
    raise ValueError(profile)


def build_call_plan(cfg: dict, profile: str) -> List[dict]:
    cases = selected_cases(cfg, profile)
    modes = cfg["modes"]
    models = model_ids(cfg)
    plan = []
    for case_path in cases:
        case = json.loads(case_path.read_text())
        bundle_text = bundle_to_text(case)
        for mode in modes:
            system_prompt, user_template = load_prompt(mode)
            user_prompt = user_template.replace("{change_bundle_text}", bundle_text)
            for model in models:
                plan.append({
                    "case": case,
                    "case_path": case_path,
                    "mode": mode,
                    "model": model,
                    "system_prompt": system_prompt,
                    "user_prompt": user_prompt,
                })
    return plan


def print_estimate(plan: List[dict], cfg: dict) -> float:
    max_out = int(cfg.get("max_tokens", 1800))
    total = 0.0
    by_model: Dict[str, dict] = {}
    for item in plan:
        inp = approx_tokens(item["system_prompt"] + "\n" + item["user_prompt"])
        est = estimate_cost(item["model"], inp, max_out)
        total += est
        d = by_model.setdefault(item["model"], {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cost": 0.0})
        d["calls"] += 1
        d["input_tokens"] += inp
        d["output_tokens"] += max_out
        d["cost"] += est
    print("=== Estimated Cost (conservative max-output estimate) ===")
    for model, d in by_model.items():
        print(f"{model}: calls={d['calls']}, input≈{d['input_tokens']}, output_cap={d['output_tokens']}, cost≈${d['cost']:.4f}")
    print(f"TOTAL estimated cost≈${total:.4f}")
    print(f"Hard budget=${cfg.get('hard_budget_usd', 18.0):.2f}")
    return total


def call_openrouter(api_key: str, item: dict, cfg: dict) -> Tuple[str, dict, float, dict]:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/lokesh0186/relgate",
        "X-Title": "RelGate ISSRE 2026 Pilot",
    }
    payload = {
        "model": item["model"],
        "messages": [
            {"role": "system", "content": item["system_prompt"]},
            {"role": "user", "content": item["user_prompt"]},
        ],
        "temperature": cfg.get("temperature", 0),
        "max_tokens": cfg.get("max_tokens", 1800),
        "top_p": cfg.get("top_p", 1),
    }
    t0 = time.time()
    resp = requests.post(API_URL, headers=headers, json=payload, timeout=180)
    latency = time.time() - t0
    if resp.status_code >= 400:
        raise RuntimeError(f"OpenRouter HTTP {resp.status_code}: {resp.text[:1000]}")
    data = resp.json()
    text = data["choices"][0]["message"]["content"]
    usage = data.get("usage", {}) or {}
    return text, usage, latency, data


def run_profile(profile: str, estimate_only: bool, force: bool):
    cfg = load_config()
    plan = build_call_plan(cfg, profile)
    print(f"Profile={profile}; planned calls={len(plan)}")
    print("Models:", ", ".join(model_ids(cfg)))
    est = print_estimate(plan, cfg)
    if est > float(cfg.get("hard_budget_usd", 18.0)):
        sys.exit(f"Estimated cost ${est:.2f} exceeds hard budget. Stop.")
    if estimate_only:
        print("Estimate-only mode; no API calls made.")
        return

    api_key = get_api_key()
    raw_dir = RESULTS_DIR / ("raw_outputs_smoke" if profile == "smoke" else "raw_outputs")
    raw_dir.mkdir(parents=True, exist_ok=True)
    rows_path = RESULTS_DIR / ("relgate_smoke_results.csv" if profile == "smoke" else "relgate_pilot_results.csv")
    fieldnames = [
        "case_id", "case_type", "expected_decision", "model", "mode", "timestamp",
        "seeded_gap_count", "critical_gap_count", "latency_seconds", "tokens_in",
        "tokens_out", "cost_usd", "raw_file", "status",
    ]
    rows = []
    actual_spend = 0.0

    for idx, item in enumerate(plan, 1):
        case = item["case"]
        case_id = case["case_id"]
        model_short = item["model"].split("/")[-1].replace(":", "_")
        raw_name = f"{model_short}_{item['mode']}_{case_id}.json"
        raw_path = raw_dir / raw_name
        if raw_path.exists() and not force:
            print(f"[{idx}/{len(plan)}] SKIP existing {raw_name}")
            raw = json.loads(raw_path.read_text())
            usage = raw.get("usage", {}) or {}
            actual_spend += usage_cost_usd(item["model"], usage)
            continue

        if actual_spend > float(cfg.get("stop_if_actual_spend_exceeds_usd", 12.0)):
            sys.exit(f"Actual/estimated spend ${actual_spend:.2f} exceeds stop threshold. Stop.")

        print(f"[{idx}/{len(plan)}] {item['model']} | {item['mode']} | {case_id}")
        status = "ok"
        try:
            response, usage, latency, api_response = call_openrouter(api_key, item, cfg)
        except Exception as e:
            response, usage, latency, api_response = f"ERROR: {e}", {}, 0.0, {"error": str(e)}
            status = "error"
            print("  ERROR:", e)

        cost = usage_cost_usd(item["model"], usage)
        actual_spend += cost
        gt = case["ground_truth"]
        seeded = gt.get("seeded_gaps", [])
        critical = [g for g in seeded if g.get("severity") == "critical"]
        raw_data = {
            "case_id": case_id,
            "case_type": case["case_type"],
            "expected_decision": gt["expected_decision"],
            "model": item["model"],
            "mode": item["mode"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "system_prompt": item["system_prompt"],
            "user_prompt": item["user_prompt"],
            "response": response,
            "usage": usage,
            "estimated_or_reported_cost_usd": round(cost, 6),
            "latency_seconds": round(latency, 2),
            "status": status,
            "api_response_id": api_response.get("id"),
        }
        raw_path.write_text(json.dumps(raw_data, indent=2))
        rows.append({
            "case_id": case_id,
            "case_type": case["case_type"],
            "expected_decision": gt["expected_decision"],
            "model": item["model"],
            "mode": item["mode"],
            "timestamp": raw_data["timestamp"],
            "seeded_gap_count": len(seeded),
            "critical_gap_count": len(critical),
            "latency_seconds": round(latency, 2),
            "tokens_in": usage.get("prompt_tokens") or usage.get("input_tokens") or 0,
            "tokens_out": usage.get("completion_tokens") or usage.get("output_tokens") or 0,
            "cost_usd": round(cost, 6),
            "raw_file": raw_name,
            "status": status,
        })
        print(f"  cost≈${cost:.5f}; cumulative≈${actual_spend:.4f}")

    with open(rows_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Done profile={profile}. Raw outputs: {raw_dir}")
    print(f"Rows: {rows_path}")
    print(f"Cumulative estimated/reported cost≈${actual_spend:.4f}")
    if profile == "smoke":
        print("STOP HERE. Score and review smoke results before full run.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=["smoke", "full"], required=True)
    parser.add_argument("--estimate-only", action="store_true")
    parser.add_argument("--force", action="store_true", help="Re-run calls even if raw output files exist")
    args = parser.parse_args()
    run_profile(args.profile, args.estimate_only, args.force)


if __name__ == "__main__":
    main()
