#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, sys

# аргументы
p = argparse.ArgumentParser()
p.add_argument("i", type=Path)                # input_dir
p.add_argument("o", type=Path)                # output_dir
p.add_argument("-d", "--max_depth", type=int, default=None)
a = p.parse_args()
SRC, DST, MD = a.i, a.o, a.max_depth

if not SRC.is_dir():
    sys.exit(1)
DST.mkdir(parents=True, exist_ok=True)

used = set()                                  # глобальный набор имён
def uniq(n):                                  # name → уникальное name
    if n not in used:
        used.add(n); return n
    s, e, c = Path(n).stem, Path(n).suffix, 1
    while True:
        m = f"{s}{c}{e}"
        if m not in used:
            used.add(m); return m
        c += 1

for f in SRC.rglob("*"):
    if not f.is_file():
        continue
    depth = len(f.relative_to(SRC).parts) - 1     # 0 — в SRC самом
    if MD is not None and depth > MD:
        continue
    shutil.copy2(f, DST / uniq(f.name))
