#!/usr/bin/env python3

from pathlib import Path
import shutil
import argparse
import sys

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Collect all files into one directory.")
    p.add_argument("input_dir", type=Path, help="Исходная директория")
    p.add_argument("output_dir", type=Path, help="Целевая директория")
    p.add_argument(
        "--max_depth",
        type=int,
        default=None,
        help="Максимальная глубина (1 = только input_dir)",
    )
    return p.parse_args()


def iter_files(root: Path, max_depth: int | None):
    start_depth = len(root.parts)
    for path in root.rglob("*"):
        if path.is_file():
            depth = len(path.parts) - start_depth
            if max_depth is None or depth <= max_depth:
                yield path


def unique_name(name: str, occupied: set[str]) -> str:
    if name not in occupied:
        occupied.add(name)
        return name
    stem, suffix = Path(name).stem, Path(name).suffix
    counter = 1
    while True:
        new_name = f"{stem}{counter}{suffix}"
        if new_name not in occupied:
            occupied.add(new_name)
            return new_name
        counter += 1


def main() -> None:
    args = parse_args()
    src, dst = args.input_dir, args.output_dir

    if not src.is_dir():
        sys.exit(f"ERROR: {src} not found or not a directory")
    dst.mkdir(parents=True, exist_ok=True)

    occupied: set[str] = set()
    for file in iter_files(src, args.max_depth):
        target = unique_name(file.name, occupied)
        shutil.copy2(file, dst / target)

    print(f"Copied {len(occupied)} files → {dst}")


if __name__ == "__main__":
    main()
