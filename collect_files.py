#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, sys

def g():
    p=argparse.ArgumentParser()
    p.add_argument("i",type=Path)
    p.add_argument("o",type=Path)
    p.add_argument("-d","--max_depth",type=int,default=None)
    return p.parse_args()

def h(r,m):
    s=len(r.parts)
    for f in r.rglob("*"):
        if f.is_file():
            d=len(f.parts)-s-1
            if m is None or d<=m:
                yield f

def n(x,u):
    if x not in u:
        u.add(x);return x
    a=Path(x).stem
    b=Path(x).suffix
    c=1
    while True:
        y=f"{a}{c}{b}"
        if y not in u:
            u.add(y);return y
        c+=1

def main():
    a=g();i,o,m=a.i,a.o,a.max_depth
    if not i.is_dir():sys.exit(1)
    o.mkdir(parents=True,exist_ok=True)
    u=set()
    for f in h(i,m):
        shutil.copy2(f,o/n(f.name,u))

main()
