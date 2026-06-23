#!/usr/bin/env bash
set -euo pipefail

printf "=== RelGate local preflight ===\n"
python3 scripts/preflight.py

printf "\n=== Smoke estimate only; no API calls ===\n"
python3 src/run_experiment.py --profile smoke --estimate-only

printf "\nTo run the smoke test, set OPENROUTER_API_KEY and run:\n"
printf "  python3 src/run_experiment.py --profile smoke\n"
printf "  python3 src/score_results.py --input-dir results/raw_outputs_smoke --output-prefix smoke\n"
printf "\nDo not run the full 108-call experiment until smoke outputs have been reviewed.\n"
