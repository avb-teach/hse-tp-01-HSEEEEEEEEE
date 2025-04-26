#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, sys

p = argparse.ArgumentParser()
p.add_argument("i", type=Path)               # input_dir
p.add_argument("o", type=Path)               # output_dir
p.add_argument("-d", "--max_depth", type=int, default=None)
a = p.parse_args()
I, O, M = a.i, a.o, a.max_depth

if not I.is_dir():
    sys.exit(1)
O.mkdir(parents=True, exist_ok=True)

used = set()
def uniq(name):
    if name not in used:
        used.add(name); return name
    s = Path(name).stem; e = Path(name).suffix; c = 1
    while True:
        new = f"{s}{c}{e}"
        if new not in used:
            used.add(new); return new
        c += 1

for f in I.rglob("*"):
    if not f.is_file():
        continue
    depth = len(f.relative_to(I).parts) - 1
    if M is not None and depth > M:
        continue
    shutil.copy2(f, O / uniq(f.name))
