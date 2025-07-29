#!/usr/bin/env python3

import argparse
import random
import subprocess
from os import getenv
from pathlib import Path
from typing import Any


def dedupe(lst: list[Any]) -> list[Any]:
    return list(set(lst))


def ensure_exists(file: Path) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.touch(exist_ok=True)


def find(path: Path, exts: list[str]) -> list[Path]:
    files: list[Path] = []
    for ext in exts:
        for file in path.glob(f"**/*.{ext}"):
            files.append(file)
    return files


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="swaywall", description="Intelligent wallpaper switcher for swaywm"
    )
    parser.add_argument("dir", help="path to wallpaper directory", type=str)
    parser.add_argument(
        "-r", "--restore", help="restore latest wallpaper", action="store_true"
    )

    exts = ["png", "jpg", "jpeg"]
    parser.add_argument(
        "-e",
        "--extensions",
        nargs="+",
        default=exts,
        metavar="EXT",
        help=f"image file extensions to look for (default: {' '.join(exts)})",
    )
    return parser.parse_args()


def get_history(hst_file: Path) -> list[Path]:
    ensure_exists(hst_file)
    hst: list[Path] = []
    for wall in hst_file.read_text().splitlines():
        wall = wall.strip()
        if not Path(wall).exists():
            continue
        hst.append(Path(wall))
    return hst


def get_new(walls: list[Path], hst: list[Path]) -> Path:
    new_walls: list[Path] = []
    for wall in walls:
        if wall not in hst:
            new_walls.append(wall)
    return random.choice(new_walls)


def remember(new: Path, walls: list[Path], hst: list[Path], hst_file: Path) -> None:
    hst = dedupe(hst)
    random.shuffle(hst)  # avoid cycling through walls in the same order

    hst.insert(0, new)
    del hst[len(walls) - 1 :]
    with hst_file.open("w") as f:
        for wall in hst:
            f.write(f"{wall}\n")


def set_wall(wall: Path) -> None:
    subprocess.run(["swaymsg", "output", "*", "bg", str(wall), "fill"], check=True)


def main() -> None:
    args = parse_args()
    walls_dir = Path(args.dir)
    if not walls_dir.is_dir():
        raise FileNotFoundError(f"directory not found: {walls_dir}")

    state = getenv("XDG_STATE_HOME") or Path.home() / ".local" / "state"
    hst_file = Path(state) / "wallpaperhst"
    hst = get_history(hst_file)

    if args.restore and hst:
        previous_wall = Path(hst[0])
        if not previous_wall.exists():
            raise FileNotFoundError(f"wallpaper not found: {previous_wall}")
        set_wall(previous_wall)
        exit(0)

    walls = find(walls_dir, args.extensions)
    if not walls:
        raise FileNotFoundError(f"no wallpapers found in {walls_dir}")

    new = get_new(walls, hst)
    if new:
        remember(new, walls, hst, hst_file)
        set_wall(new)


if __name__ == "__main__":
    main()
