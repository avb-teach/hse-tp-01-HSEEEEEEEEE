#!/usr/bin/env bash
set -e

if [ "$#" -ne 2 ]; then
  echo "Usage: $(basename "$0") <input_dir> <output_dir>"
  exit 1
fi

python3 "$(dirname "$0")/collect_files.py" "$1" "$2"
