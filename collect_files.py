#!/usr/bin/env python3
from pathlib import Path
import argparse, shutil, sys

p=argparse.ArgumentParser()
p.add_argument("i",type=Path)
p.add_argument("o",type=Path)
p.add_argument("-d","--max_depth",type=int,default=None)
a=p.parse_args(); r,n=a.i,a.o; m=a.max_depth
if not r.is_dir(): sys.exit(1)
u=set()
def uniq(x):
    if x not in u: u.add(x); return x
    s=Path(x).stem; e=Path(x).suffix; c=1
    while True:
        y=f"{s}{c}{e}"
        if y not in u: u.add(y); return y
        c+=1
for f in r.rglob("*"):
    if not f.is_file(): continue
    rel=f.relative_to(r)
    d=len(rel.parts)-1
    tgt_dir=n.joinpath(*rel.parts[:min(d,m) if m is not None else 0])
    tgt_dir.mkdir(parents=True,exist_ok=True)
    shutil.copy2(f,tgt_dir/uniq(f.name))
