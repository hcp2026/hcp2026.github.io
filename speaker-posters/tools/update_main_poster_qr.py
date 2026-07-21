#!/usr/bin/env python3
from __future__ import annotations

import shutil
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[2]
POSTER = ROOT / "HCP2026-poster.png"
BACKUP = ROOT / "speaker-posters" / "HCP2026-poster-before-wechat-update.png"
WECHAT = ROOT / "assets" / "wechat-group-qr.png"


def rounded_mask(size: tuple[int, int], radius: int) -> Image.Image:
    mask = Image.new("L", size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, size[0] - 1, size[1] - 1), radius=radius, fill=255)
    return mask


def font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


def update_host_text(poster: Image.Image) -> Image.Image:
    arr = np.array(poster)
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)

    x1, y1, x2, y2 = 350, 1810, 900, 2010
    crop = arr[y1:y2, x1:x2]
    old_text = (crop[:, :, 0] > 150) & (crop[:, :, 1] > 150) & (crop[:, :, 2] > 150)
    mask[y1:y2, x1:x2][old_text] = 255
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=3)

    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), mask, 5, cv2.INPAINT_TELEA)
    poster = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(poster)
    draw.text(
        (426, 1893),
        "山东大学网络空间安全学院",
        fill=(255, 255, 255),
        font=font(70),
    )
    return poster


def update_event_date_text(poster: Image.Image) -> Image.Image:
    arr = np.array(poster)
    mask = np.zeros(arr.shape[:2], dtype=np.uint8)

    x1, y1, x2, y2 = 350, 1510, 1700, 1680
    crop = arr[y1:y2, x1:x2]
    old_text = (crop[:, :, 0] > 150) & (crop[:, :, 1] > 150) & (crop[:, :, 2] > 150)
    mask[y1:y2, x1:x2][old_text] = 255
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=3)

    inpainted = cv2.inpaint(cv2.cvtColor(arr, cv2.COLOR_RGB2BGR), mask, 5, cv2.INPAINT_TELEA)
    poster = Image.fromarray(cv2.cvtColor(inpainted, cv2.COLOR_BGR2RGB))

    draw = ImageDraw.Draw(poster)
    draw.text(
        (424, 1568),
        "2026 年 7 月 31 日 — 8 月 2 日",
        fill=(255, 255, 255),
        font=font(82),
    )
    return poster


def remove_call_for_submissions(poster: Image.Image) -> Image.Image:
    draw = ImageDraw.Draw(poster)
    panel_bg = poster.getpixel((1600, 3150))
    draw.rectangle((450, 3340, 1710, 3505), fill=panel_bg)
    return poster


def main() -> None:
    BACKUP.parent.mkdir(parents=True, exist_ok=True)
    if not BACKUP.exists():
        shutil.copy2(POSTER, BACKUP)

    poster = Image.open(BACKUP).convert("RGB")
    poster = update_event_date_text(poster)
    poster = update_host_text(poster)
    poster = remove_call_for_submissions(poster)
    draw = ImageDraw.Draw(poster)

    # Repaint the third QR area in the bottom card, then place the full WeChat
    # screenshot so that the expiration notice remains visible.
    panel_bg = poster.getpixel((1600, 3150))
    draw.rectangle((1240, 2530, 1880, 3158), fill=panel_bg)

    qr = Image.open(WECHAT).convert("RGB")
    qr_w = 340
    qr_h = round(qr_w * qr.height / qr.width)
    qr = qr.resize((qr_w, qr_h), Image.Resampling.LANCZOS)

    x = 1538 - qr_w // 2
    y = 2532
    shadow = Image.new("RGBA", (qr_w + 46, qr_h + 46), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow)
    shadow_draw.rounded_rectangle((23, 23, qr_w + 23, qr_h + 23), radius=28, fill=(80, 40, 25, 58))
    shadow = shadow.filter(ImageFilter.GaussianBlur(18))
    poster.paste(shadow.convert("RGB"), (x - 23, y - 23), shadow)

    mask = rounded_mask((qr_w, qr_h), 24)
    poster.paste(qr, (x, y), mask)

    label = "参会微信群"
    label_font = font(58)
    bbox = draw.textbbox((0, 0), label, font=label_font)
    label_x = 1538 - (bbox[2] - bbox[0]) // 2
    draw.text((label_x, 3096), label, fill=(167, 25, 48), font=label_font)

    poster.save(POSTER, optimize=True)

    jpg = poster.resize((1080, 1920), Image.Resampling.LANCZOS)
    jpg.save(ROOT / "HCP2026-poster.jpg", quality=95, optimize=True, progressive=True)

    # A single-page PDF keeps the full poster in one page and uses the updated QR.
    poster.save(ROOT / "HCP2026-poster.pdf", "PDF", resolution=144)
    print(POSTER)
    print(ROOT / "HCP2026-poster.jpg")
    print(ROOT / "HCP2026-poster.pdf")


if __name__ == "__main__":
    main()
