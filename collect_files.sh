#!/usr/bin/env bash
set -euo pipefail

if [[ "$#" -lt 2 ]]; then
  echo "Usage: $0 INPUT_DIR OUTPUT_DIR [--max_depth N]" >&2
  exit 1
fi

python3 "$(dirname "$0")/collect_files.py" "$@"
