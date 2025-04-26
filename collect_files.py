#!/usr/bin/env python3


from __future__ import annotations
import argparse
import os
import shutil
from pathlib import Path

parser = argparse.ArgumentParser(prog="collect_files.py")
parser.add_argument("input_dir", type=Path)
parser.add_argument("output_dir", type=Path)
parser.add_argument("--max_depth", type=int, default=None)

args = parser.parse_intermixed_args()

src_root: Path = args.input_dir.resolve()
dst_root: Path = args.output_dir.resolve()
max_depth = args.max_depth

if not src_root.is_dir():
    parser.error(f"'{src_root}' is not a directory")

dst_root.mkdir(parents=True, exist_ok=True)

for cur_root, _, files in os.walk(src_root):
    cur_root = Path(cur_root)
    rel_root = cur_root.relative_to(src_root) 

    # куда копировать файлы из этой директории?
    if max_depth is None:
        target_root = dst_root
    else:
        # оставляем первые N компонентов пути
        parts = rel_root.parts[:max_depth] if rel_root != Path('.') else ()
        target_root = dst_root.joinpath(*parts)
        target_root.mkdir(parents=True, exist_ok=True)

    for fname in files:
        src_path = cur_root / fname
        name, ext = os.path.splitext(fname)
        dst_path = target_root / fname

        counter = 1
        while dst_path.exists():
            dst_path = target_root / f"{name}_{counter}{ext}"
            counter += 1

        shutil.copy2(src_path, dst_path)
