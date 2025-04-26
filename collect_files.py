#!/usr/bin/env python3
"""
collect_files.py
────────────────
* Без --max_depth           → всё дерево «расплющивается» в корень <output_dir>.
* С   --max_depth N (N ≥ 0) → сохраняются первые N уровней каталога.
                              Пример:  in/a/b/c/d.txt  + --max_depth 2
                                       → out/a/b/d.txt
При совпадении имён добавляется суффикс: report.txt → report_1.txt → …
"""

from __future__ import annotations
import os
import shutil
import sys
from pathlib import Path


def die(msg: str, code: int = 1) -> None:
    sys.stderr.write(msg + "\n")
    sys.exit(code)


# ── разбор аргументов ────────────────────────────────────────────────────────
args = sys.argv[1:]
max_depth: int | None = None

# --max_depth можно писать где угодно; поддерживаем --max_depth=2 и --max_depth 2
i = 0
while i < len(args):
    arg = args[i]
    if arg.startswith("--max_depth"):
        if arg == "--max_depth":
            if i + 1 >= len(args):
                die("ERROR: --max_depth требует число")
            max_depth_str = args.pop(i + 1)
        else:                        # форма --max_depth=2
            _, _, max_depth_str = arg.partition("=")
            if not max_depth_str:
                die("ERROR: --max_depth=NUMBER — число отсутствует")
        args.pop(i)                  # убираем сам флаг
        try:
            max_depth = int(max_depth_str)
            if max_depth < 0:
                die("ERROR: --max_depth must be ≥ 0")
        except ValueError:
            die("ERROR: --max_depth must be an integer")
    else:
        i += 1

if len(args) != 2:
    die("Usage: collect_files.py [--max_depth N] <input_dir> <output_dir>")

src_root = Path(args[0]).resolve()
dst_root = Path(args[1]).resolve()

if not src_root.is_dir():
    die(f"ERROR: '{src_root}' is not a directory")

dst_root.mkdir(parents=True, exist_ok=True)

# ── копирование ──────────────────────────────────────────────────────────────
for cur_dir, _, files in os.walk(src_root):
    cur_path = Path(cur_dir)
    rel = cur_path.relative_to(src_root)              # '.' для корня

    # куда кладём файлы из cur_path?
    if max_depth is None:
        target_dir = dst_root
    else:
        keep = rel.parts[:max_depth]                  # () если rel == '.'
        target_dir = dst_root.joinpath(*keep)
        target_dir.mkdir(parents=True, exist_ok=True)

    for fname in files:
        src_file = cur_path / fname
        base, ext = os.path.splitext(fname)
        dst_file = target_dir / fname

        # дубликаты: report.txt → report_1.txt, …
        cnt = 1
        while dst_file.exists():
            dst_file = target_dir / f"{base}_{cnt}{ext}"
            cnt += 1

        shutil.copy2(src_file, dst_file)
