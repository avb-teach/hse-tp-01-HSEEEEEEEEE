#!/usr/bin/env python3

import os
import shutil
import sys

if len(sys.argv) != 3:
    sys.exit("Usage: collect_files.py <input_dir> <output_dir>")

src_root = os.path.abspath(sys.argv[1])
dst_root = os.path.abspath(sys.argv[2])

if not os.path.isdir(src_root):
    sys.exit(f"Input directory '{src_root}' does not exist")

os.makedirs(dst_root, exist_ok=True)

for root, _, files in os.walk(src_root):
    for filename in files:
        src_path = os.path.join(root, filename)
        name, ext = os.path.splitext(filename)
        dst_path = os.path.join(dst_root, filename)

        counter = 1
        while os.path.exists(dst_path):
            dst_path = os.path.join(dst_root, f"{name}_{counter}{ext}")
            counter += 1

        shutil.copy2(src_path, dst_path)
