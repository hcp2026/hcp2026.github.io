#!/usr/bin/env python3
from __future__ import annotations

import zipfile
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "speaker-posters"
SOURCE_PNG_DIR = OUT / "png"
SOURCE_JPG_DIR = OUT / "jpg"
SET_PNG_DIR = OUT / "海报合集-9张"
SET_JPG_DIR = OUT / "海报合集-9张-jpg"

TARGET_WIDTH = 1080
GAP = 24
GAP_COLOR = (19, 7, 16)

SINGLE_POSTERS = {
    "1-主海报.png": ROOT / "promo-posters" / "png" / "01-main-poster.png",
    "2-大会议程.png": ROOT / "promo-posters" / "png" / "02-agenda-poster.png",
    "3-戴彧虹.png": SOURCE_PNG_DIR / "01-戴彧虹-yuhong-dai.png",
    "4-詹乃军.png": SOURCE_PNG_DIR / "02-詹乃军-naijun-zhan.png",
    "5-孙晓明.png": SOURCE_PNG_DIR / "03-孙晓明-xiaoming-sun.png",
    "6-冯启龙.png": SOURCE_PNG_DIR / "04-冯启龙-qilong-feng.png",
}

POSTER_GROUPS = {
    "7-人工智能专题.png": [
        "05-袁明轩-mingxuan-yuan.png",
        "06-王肇国-zhaoguo-wang.png",
        "07-李旻-min-li.png",
    ],
    "8-组合优化专题.png": [
        "08-操宜新-yixin-cao.png",
        "09-雷震东-zhendong-lei.png",
        "10-刘圣鑫-shengxin-liu.png",
        "11-秦虎-hu-qin.png",
        "12-黄一潇-yixiao-huang.png",
    ],
    "9-密码分析专题.png": [
        "13-Emanuele Bellini-emanuele-bellini.png",
        "14-周春宁-chunning-zhou.png",
        "15-张昕荻-xindi-zhang.png",
        "16-樊燕红-yanhong-fan.png",
    ],
}


def flatten_to_rgb(path: Path) -> Image.Image:
    if not path.is_file():
        raise FileNotFoundError(path)
    with Image.open(path) as image:
        image.load()
        if image.mode == "RGB":
            return image.copy()
        if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
            rgba = image.convert("RGBA")
            background = Image.new("RGBA", rgba.size, (*GAP_COLOR, 255))
            background.alpha_composite(rgba)
            return background.convert("RGB")
        return image.convert("RGB")


def resized_to_width(image: Image.Image, width: int = TARGET_WIDTH) -> Image.Image:
    if image.width == width:
        return image
    height = round(image.height * width / image.width)
    return image.resize((width, height), Image.Resampling.LANCZOS)


def save_single(output_name: str, source: Path) -> None:
    image = resized_to_width(flatten_to_rgb(source))
    image.save(SET_PNG_DIR / output_name, optimize=True)


def merge_vertical(output_name: str, source_names: list[str]) -> None:
    images = [resized_to_width(flatten_to_rgb(SOURCE_PNG_DIR / name)) for name in source_names]
    total_height = sum(image.height for image in images) + GAP * (len(images) - 1)
    merged = Image.new("RGB", (TARGET_WIDTH, total_height), GAP_COLOR)
    y = 0
    for image in images:
        merged.paste(image, (0, y))
        y += image.height + GAP
    merged.save(SET_PNG_DIR / output_name, optimize=True)


def export_jpgs() -> None:
    for old in SET_JPG_DIR.glob("*.jpg"):
        old.unlink()
    for png in sorted(SET_PNG_DIR.glob("*.png")):
        with Image.open(png) as image:
            image.convert("RGB").save(
                SET_JPG_DIR / f"{png.stem}.jpg",
                quality=94,
                optimize=True,
                progressive=True,
            )


def zip_dir(zip_name: str, directory: Path, pattern: str) -> None:
    zip_path = OUT / zip_name
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for file in sorted(directory.glob(pattern)):
            zf.write(file, arcname=file.name)


def clean_outputs() -> None:
    SET_PNG_DIR.mkdir(parents=True, exist_ok=True)
    SET_JPG_DIR.mkdir(parents=True, exist_ok=True)
    expected_pngs = set(SINGLE_POSTERS) | set(POSTER_GROUPS)
    for png in SET_PNG_DIR.glob("*.png"):
        if png.name not in expected_pngs:
            png.unlink()


def main() -> None:
    clean_outputs()
    for output_name, source in SINGLE_POSTERS.items():
        save_single(output_name, source)
    for output_name, source_names in POSTER_GROUPS.items():
        merge_vertical(output_name, source_names)
    export_jpgs()
    zip_dir("HCP2026-speaker-posters-png.zip", SOURCE_PNG_DIR, "*.png")
    zip_dir("HCP2026-speaker-posters-jpg.zip", SOURCE_JPG_DIR, "*.jpg")
    zip_dir("HCP2026-poster-set-9-png.zip", SET_PNG_DIR, "*.png")
    zip_dir("HCP2026-poster-set-9-jpg.zip", SET_JPG_DIR, "*.jpg")
    for png in sorted(SET_PNG_DIR.glob("*.png")):
        with Image.open(png) as image:
            print(f"{png.relative_to(ROOT)}\t{image.width}x{image.height}")


if __name__ == "__main__":
    main()
