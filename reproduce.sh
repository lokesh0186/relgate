#!/usr/bin/env bash
set -euo pipefail

printf "=== RelGate local preflight ===\n"
python3 scripts/preflight.py

printf "\n=== Strict-scoring regression tests ===\n"
python3 -m unittest discover -s tests -v

printf "\n=== Camera-ready frozen-output audit ===\n"
python3 scripts/camera_ready_audit.py

printf "\n=== Regenerate final metrics and table from frozen outputs ===\n"
python3 src/score_results.py --input-dir results/raw_outputs --output-prefix full
python3 src/make_tables.py

printf "\nReproduction PASS. No model or API calls were made.\n"
