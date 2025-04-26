#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, sys
from collections import defaultdict

p = argparse.ArgumentParser()
p.add_argument("i", type=Path)          # input_dir
p.add_argument("o", type=Path)          # output_dir
p.add_argument("-d", "--max_depth", type=int, default=None)
a = p.parse_args()
I, O, M = a.i, a.o, a.max_depth

if not I.is_dir():
    sys.exit(1)
O.mkdir(parents=True, exist_ok=True)

G = set()
D = defaultdict(set)

def u(n, s):
    if n not in s:
        s.add(n); return n
    t, e, c = Path(n).stem, Path(n).suffix, 1
    while True:
        m = f"{t}{c}{e}"
        if m not in s:
            s.add(m); return m
        c += 1

for f in I.rglob("*"):
    if not f.is_file():
        continue
    r = f.relative_to(I)
    k = len(r.parts) - 1
    if M is not None and k > M:
        continue
    T = O / Path(*r.parts[:k])
    T.mkdir(parents=True, exist_ok=True)
    S = G if M is None else D[T]
    shutil.copy2(f, T / u(f.name, S))
