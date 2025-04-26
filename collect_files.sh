#!/usr/bin/env bash
# Проксюет все аргументы в Python-утилиту.
python3 "$(dirname "$0")/collect_files.py" "$@"
