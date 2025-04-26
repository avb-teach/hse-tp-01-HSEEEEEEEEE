#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, sys, collections

p = argparse.ArgumentParser()
p.add_argument("i", type=Path)          # input_dir
p.add_argument("o", type=Path)          # output_dir
p.add_argument("-d", "--max_depth", type=int)
a = p.parse_args()
S, O, M = a.i, a.o, a.max_depth         # src, out, max_depth

if not S.is_dir():
    sys.exit(1)
O.mkdir(parents=True, exist_ok=True)

used = collections.defaultdict(set)     # dir → {names}

def uniq(t, n):                         # уникальное имя внутри dir t
    s = used[t]
    if n not in s:
        s.add(n); return n
    stem, suf, c = Path(n).stem, Path(n).suffix, 1
    while True:
        m = f"{stem}{c}{suf}"
        if m not in s:
            s.add(m); return m
        c += 1

for f in S.rglob("*"):
    if not f.is_file():
        continue
    rel = f.relative_to(S)
    depth = len(rel.parts) - 1          # 0 — файл прямо в S
    if M is not None and depth > M:
        keep = rel.parts[:M]            # обрезаем до M каталогов
    elif M is not None:
        keep = rel.parts[:depth]        # оставить фактическую глубину (≤ M)
    else:
        keep = ()                       # без --max_depth: всё в корень
    T = O.joinpath(*keep)               # целевая директория
    T.mkdir(parents=True, exist_ok=True)
    shutil.copy2(f, T / uniq(T, f.name))
