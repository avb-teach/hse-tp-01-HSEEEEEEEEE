#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, sys

p = argparse.ArgumentParser()
p.add_argument("i", type=Path)        # input_dir
p.add_argument("o", type=Path)        # output_dir
p.add_argument("-d", "--max_depth", type=int, default=None)
a = p.parse_args()
I, O, M = a.i, a.o, a.max_depth

if not I.is_dir():
    sys.exit(1)
O.mkdir(parents=True, exist_ok=True)

u = {}                                # dir → set(used names)
def uniq(d, n):
    s = u.setdefault(d, set())
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
    k = len(r.parts) - 1              # глубина файла
    m = 0 if M is None else min(k, M) # сколько папок сохранить
    d = O.joinpath(*r.parts[:m])      # целевая директория
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, d / uniq(d, f.name))
