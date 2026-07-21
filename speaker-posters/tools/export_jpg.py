#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
PNG_DIR = ROOT / "speaker-posters" / "png"
JPG_DIR = ROOT / "speaker-posters" / "jpg"


def main() -> None:
    JPG_DIR.mkdir(parents=True, exist_ok=True)
    for old in JPG_DIR.glob("*.jpg"):
        old.unlink()
    for png in sorted(PNG_DIR.glob("*.png")):
        img = Image.open(png).convert("RGB")
        out = JPG_DIR / f"{png.stem}.jpg"
        img.save(out, quality=94, optimize=True, progressive=True)
        print(out)


if __name__ == "__main__":
    main()
