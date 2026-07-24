#!/usr/bin/env python3
from __future__ import annotations

import html
import shutil
import subprocess
import textwrap
import zipfile
from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "panel-posters"
HTML_DIR = OUT / "html"
PNG_DIR = OUT / "png"
JPG_DIR = OUT / "jpg"
PDF_DIR = OUT / "pdf"
ZIP_DIR = OUT / "zip"
TMP_DIR = OUT / "tmp"

POSTER_SIZE = (2160, 3840)
JPG_SIZE = (1080, 1920)

PHOTO = "../../assets/speakers/pinyan-lu.jpg"
LOGO = "../../assets/sdu-logo.svg"
BG = "../../assets/sdu-qingdao-library-hero.jpg"

PANELISTS = [
    ("詹乃军", "北京大学计算机学院", "assets/speakers/naijun-zhan.jpeg"),
    ("孙晓明", "中国科学院计算技术研究所", "assets/speakers/xiaoming-sun.png"),
    ("冯启龙", "中南大学计算机学院", "assets/speakers/qilong-feng.jpeg"),
    (
        "袁明轩",
        "华为诺亚方舟实验室 / 香港诺亚方舟实验室",
        "assets/speakers/mingxuan-yuan.jpg",
    ),
    ("王肇国", "上海交通大学", "assets/speakers/zhaoguo-wang.jpeg"),
    ("李旻", "东南大学集成电路学院", "assets/speakers/min-li.png"),
]

CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
]

FONT_SANS = Path("/System/Library/Fonts/STHeiti Light.ttc")
FONT_SERIF = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")
FONT_FALLBACK = Path("/System/Library/Fonts/Supplemental/Arial Unicode.ttf")

RED = (111, 11, 28)
DARK = (25, 7, 18)
GOLD = (247, 223, 170)
CREAM = (250, 241, 230)
WHITE = (255, 255, 255)
INK = (26, 28, 34)


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    selected = path if path.exists() else FONT_FALLBACK
    return ImageFont.truetype(str(selected), size)


def text_size(
    draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont
) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font_obj)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


def draw_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font_obj: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = WHITE,
    spacing: int = 0,
) -> None:
    draw.text(xy, text, font=font_obj, fill=fill, spacing=spacing)


def wrap_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    font_obj: ImageFont.FreeTypeFont,
    max_width: int,
) -> list[str]:
    units = text.split(" ") if " " in text else list(text)
    lines: list[str] = []
    current = ""
    for unit in units:
        candidate = (
            unit if not current else (current + (" " if " " in text else "") + unit)
        )
        if text_size(draw, candidate, font_obj)[0] <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = unit
    if current:
        lines.append(current)
    return lines


def draw_wrapped(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font_obj: ImageFont.FreeTypeFont,
    max_width: int,
    line_height: int,
    fill: tuple[int, int, int] | tuple[int, int, int, int] = WHITE,
) -> int:
    x, y = xy
    for line in wrap_text(draw, text, font_obj, max_width):
        draw.text((x, y), line, font=font_obj, fill=fill)
        y += line_height
    return y


def cover_image(
    path: Path, size: tuple[int, int], position: tuple[float, float] = (0.5, 0.5)
) -> Image.Image:
    with Image.open(path) as img:
        return ImageOps.fit(
            img.convert("RGB"),
            size,
            method=Image.Resampling.LANCZOS,
            centering=position,
        )


def rounded_overlay(
    base: Image.Image,
    box: tuple[int, int, int, int],
    fill: tuple[int, int, int, int],
    radius: int,
    outline: tuple[int, int, int, int] | None = None,
    width: int = 1,
) -> None:
    layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle(box, radius=radius, fill=fill, outline=outline, width=width)
    base.alpha_composite(layer)


def make_background() -> Image.Image:
    bg = cover_image(
        ROOT / "assets/sdu-qingdao-library-hero.jpg", POSTER_SIZE, (0.5, 0.65)
    ).convert("RGBA")
    overlay = Image.new("RGBA", POSTER_SIZE, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for y in range(POSTER_SIZE[1]):
        t = y / POSTER_SIZE[1]
        r = int(42 * (1 - t) + 93 * t)
        g = int(29 * (1 - t) + 4 * t)
        b = int(69 * (1 - t) + 18 * t)
        a = int(222 + 18 * t)
        od.line((0, y, POSTER_SIZE[0], y), fill=(r, g, b, a))
    glow = Image.new("RGBA", POSTER_SIZE, (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-420, -280, 920, 780), fill=(247, 223, 170, 42))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    bg.alpha_composite(overlay)
    bg.alpha_composite(glow)
    top = Image.new("RGBA", POSTER_SIZE, (0, 0, 0, 0))
    td = ImageDraw.Draw(top)
    td.rectangle((0, 0, POSTER_SIZE[0], 32), fill=(167, 25, 48, 255))
    td.rectangle(
        (POSTER_SIZE[0] - 520, 0, POSTER_SIZE[0], 32), fill=(216, 177, 95, 255)
    )
    bg.alpha_composite(top)
    return bg


def draw_brand(draw: ImageDraw.ImageDraw) -> None:
    draw_text(draw, (144, 136), "山东大学", font(FONT_SANS, 70), WHITE)
    draw_text(
        draw,
        (148, 220),
        "SHANDONG UNIVERSITY",
        font(FONT_SERIF, 28),
        (255, 255, 255, 230),
    )
    draw_text(draw, (1760, 140), "专题海报", font(FONT_SANS, 44), GOLD)


def draw_event(draw: ImageDraw.ImageDraw, y: int = 360) -> None:
    draw_text(draw, (144, y), "第  九  届", font(FONT_SANS, 48), GOLD)
    draw_text(draw, (144, y + 106), "HCP 2026", font(FONT_SERIF, 210), WHITE)
    draw_text(
        draw,
        (144, y + 350),
        "难解问题的理论、算法与应用研讨会",
        font(FONT_SANS, 62),
        WHITE,
    )


def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    y = 3630
    draw.line((144, y, 2016, y), fill=(255, 255, 255, 70), width=2)
    draw_text(
        draw,
        (144, y + 46),
        "2026.07.31 – 08.02 · 山东大学青岛校区",
        font(FONT_SANS, 38),
        GOLD,
    )
    draw_text(draw, (1608, y + 46), "hcp2026.sincst.cn", font(FONT_SERIF, 39), GOLD)


def draw_pill(
    draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str
) -> None:
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=(244, 223, 176))
    tw, th = text_size(draw, label, font(FONT_SANS, 42))
    draw_text(
        draw,
        (
            box[0] + (box[2] - box[0] - tw) // 2,
            box[1] + (box[3] - box[1] - th) // 2 - 8,
        ),
        label,
        font(FONT_SANS, 42),
        RED,
    )


def draw_panelist_card(
    img: Image.Image,
    box: tuple[int, int, int, int],
    name: str,
    aff: str,
    photo_path: str,
) -> None:
    rounded_overlay(img, box, (255, 255, 255, 232), 28)
    x1, y1, _, _ = box
    photo = cover_image(ROOT / photo_path, (170, 212), (0.5, 0.45)).convert("RGBA")
    mask = Image.new("L", photo.size, 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle((0, 0, *photo.size), radius=22, fill=255)
    img.paste(photo, (x1 + 24, y1 + 24), mask)
    draw = ImageDraw.Draw(img)
    draw_text(draw, (x1 + 220, y1 + 38), name, font(FONT_SANS, 48), RED)
    draw_wrapped(
        draw,
        (x1 + 220, y1 + 112),
        aff,
        font(FONT_SANS, 27),
        330,
        42,
        (89, 96, 108),
    )


def save_panel_png(path: Path) -> None:
    img = make_background()
    draw = ImageDraw.Draw(img)
    draw_brand(draw)
    draw_event(draw, 300)

    rounded_overlay(
        img, (144, 820, 2016, 1320), (255, 255, 255, 30), 44, (255, 255, 255, 54), 2
    )
    draw = ImageDraw.Draw(img)
    draw.rectangle((144, 820, 164, 1320), fill=GOLD)
    draw_text(draw, (214, 870), "PANEL DISCUSSION", font(FONT_SERIF, 40), GOLD)
    draw_text(draw, (214, 950), "Panel Discussion", font(FONT_SANS, 104), WHITE)
    draw_text(draw, (214, 1095), "AI时代的算法研究", font(FONT_SANS, 72), WHITE)
    draw_pill(draw, (214, 1200, 620, 1288), "2026年8月1日")
    draw_pill(draw, (652, 1200, 1010, 1288), "15:45-16:45")

    rounded_overlay(img, (144, 1380, 2016, 2160), (255, 255, 255, 230), 44)
    photo = cover_image(
        ROOT / "assets/speakers/pinyan-lu.jpg", (420, 525), (0.52, 0.43)
    ).convert("RGBA")
    mask = Image.new("L", photo.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, *photo.size), radius=34, fill=255)
    img.paste(photo, (204, 1440), mask)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((670, 1440, 860, 1504), radius=12, fill=(167, 25, 48))
    draw_text(draw, (702, 1448), "主持人", font(FONT_SANS, 34), WHITE)
    draw_text(draw, (670, 1550), "陆品燕", font(FONT_SANS, 82), RED)
    draw_text(draw, (670, 1660), "上海财经大学", font(FONT_SANS, 42), (89, 96, 108))
    draw_text(draw, (670, 1735), "个人简介", font(FONT_SANS, 29), (162, 120, 60))
    draw_wrapped(draw, (670, 1785), BIO, font(FONT_SANS, 25), 1260, 42, (51, 56, 68))

    draw_text(draw, (144, 2230), "嘉宾", font(FONT_SANS, 62), WHITE)
    draw_text(draw, (310, 2248), "PANELISTS", font(FONT_SERIF, 38), GOLD)
    card_positions = [
        (144, 2325, 748, 2745),
        (778, 2325, 1382, 2745),
        (1412, 2325, 2016, 2745),
        (144, 2775, 748, 3195),
        (778, 2775, 1382, 3195),
        (1412, 2775, 2016, 3195),
    ]
    for panelist, box in zip(PANELISTS, card_positions, strict=True):
        draw_panelist_card(img, box, *panelist)

    draw = ImageDraw.Draw(img)
    draw_text(
        draw,
        (144, 3290),
        "地点：山东大学青岛校区淦昌苑D座305会议厅",
        font(FONT_SANS, 38),
        (255, 255, 255, 220),
    )
    draw_footer(draw)
    img.convert("RGB").save(path, optimize=True)


def save_person_png(path: Path) -> None:
    img = make_background()
    draw = ImageDraw.Draw(img)
    draw_brand(draw)
    draw_event(draw, 280)

    photo = cover_image(
        ROOT / "assets/speakers/pinyan-lu.jpg", (560, 700), (0.52, 0.43)
    ).convert("RGBA")
    mask = Image.new("L", photo.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, *photo.size), radius=38, fill=255)
    img.paste(photo, (144, 860), mask)

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((770, 900, 1281, 972), radius=12, fill=(167, 25, 48))
    draw_text(draw, (800, 912), "PANEL DISCUSSION 主持人", font(FONT_SANS, 35), WHITE)
    draw_text(draw, (770, 1040), "陆品燕", font(FONT_SANS, 112), WHITE)
    draw_text(
        draw, (770, 1185), "上海财经大学", font(FONT_SANS, 50), (255, 255, 255, 210)
    )

    rounded_overlay(img, (770, 1320, 2016, 1560), (255, 255, 255, 32), 22)
    draw = ImageDraw.Draw(img)
    draw.rectangle((770, 1320, 786, 1560), fill=GOLD)
    draw_text(draw, (822, 1360), "专题讨论", font(FONT_SANS, 34), GOLD)
    draw_wrapped(
        draw, (822, 1425), "AI时代的算法研究", font(FONT_SANS, 58), 1080, 76, WHITE
    )

    draw_text(draw, (144, 1660), "个人简介", font(FONT_SANS, 54), WHITE)
    draw.line((380, 1695, 2016, 1695), fill=(255, 255, 255, 70), width=2)
    rounded_overlay(
        img, (144, 1760, 2016, 2390), (255, 255, 255, 28), 34, (255, 255, 255, 54), 2
    )
    draw = ImageDraw.Draw(img)
    draw_wrapped(
        draw, (214, 1830), BIO, font(FONT_SANS, 40), 1730, 70, (255, 255, 255, 236)
    )

    draw_text(draw, (144, 2490), "Panel 嘉宾", font(FONT_SANS, 54), WHITE)
    draw.line((440, 2525, 2016, 2525), fill=(255, 255, 255, 70), width=2)
    guest_positions = [
        (144, 2590, 1050, 2770),
        (1110, 2590, 2016, 2770),
        (144, 2810, 1050, 2990),
        (1110, 2810, 2016, 2990),
        (144, 3030, 1050, 3210),
        (1110, 3030, 2016, 3210),
    ]
    for (name, aff, _), box in zip(PANELISTS, guest_positions, strict=True):
        rounded_overlay(img, box, (255, 255, 255, 28), 24, (255, 255, 255, 50), 2)
        draw = ImageDraw.Draw(img)
        draw_text(draw, (box[0] + 30, box[1] + 28), name, font(FONT_SANS, 42), GOLD)
        draw_wrapped(
            draw,
            (box[0] + 210, box[1] + 34),
            aff,
            font(FONT_SANS, 28),
            650,
            42,
            (255, 255, 255, 220),
        )
    draw_footer(draw)
    img.convert("RGB").save(path, optimize=True)


def chrome_path() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    from_path = (
        shutil.which("google-chrome")
        or shutil.which("chromium")
        or shutil.which("chromium-browser")
    )
    if from_path:
        return Path(from_path)
    raise RuntimeError("Cannot find Chrome or Chromium for rendering.")


def html_file_url(path: Path) -> str:
    return "file://" + quote(str(path.resolve()))


COMMON_CSS = f"""
* {{ box-sizing: border-box; }}
html, body {{
  margin: 0;
  padding: 0;
  width: 1080px;
  height: 1920px;
  overflow: hidden;
  color: #fff;
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  background: #14070d;
}}
.poster {{
  position: relative;
  width: 1080px;
  height: 1920px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(42, 29, 69, .90) 0%, rgba(92, 35, 55, .88) 42%, rgba(80, 4, 18, .98) 100%),
    url("{BG}") center / cover no-repeat;
}}
.poster::before {{
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 22% 13%, rgba(255, 226, 163, .22), transparent 28%),
    linear-gradient(135deg, rgba(255,255,255,.09), transparent 34%),
    linear-gradient(180deg, rgba(20, 7, 13, .08), rgba(60, 4, 17, .54));
  pointer-events: none;
}}
.top-rule {{
  position: absolute;
  inset: 0 0 auto 0;
  height: 16px;
  background: linear-gradient(90deg, #a71930, #d8b15f, #fff1bf);
}}
.inner {{
  position: relative;
  z-index: 1;
  height: 100%;
  padding: 72px 72px 58px;
}}
.brand {{
  display: flex;
  align-items: center;
  gap: 22px;
}}
.brand img {{
  width: 250px;
  height: auto;
  filter: brightness(0) invert(1);
}}
.brand .tag {{
  margin-left: auto;
  color: #f7dfaa;
  font-size: 22px;
  font-weight: 900;
  letter-spacing: 7px;
}}
.event {{
  margin-top: 58px;
}}
.event .kicker {{
  color: #f7dfaa;
  font-size: 25px;
  font-weight: 900;
  letter-spacing: 14px;
}}
.event h1 {{
  margin: 20px 0 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 122px;
  line-height: .92;
  letter-spacing: 4px;
}}
.event .subtitle {{
  margin-top: 18px;
  font-size: 31px;
  line-height: 1.36;
  font-weight: 900;
}}
.pill-row {{
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  margin-top: 30px;
}}
.pill {{
  padding: 12px 18px;
  color: #5b0e19;
  background: #f4dfb0;
  border-radius: 999px;
  font-size: 22px;
  font-weight: 900;
}}
.section-label {{
  color: #f7dfaa;
  font-size: 19px;
  font-weight: 900;
  letter-spacing: 6px;
}}
.footer {{
  position: absolute;
  left: 72px;
  right: 72px;
  bottom: 46px;
  display: flex;
  justify-content: space-between;
  gap: 24px;
  color: #f7dfaa;
  border-top: 1px solid rgba(255,255,255,.24);
  padding-top: 24px;
  font-size: 21px;
  font-weight: 900;
}}
.footer .url {{
  font-family: Georgia, "Times New Roman", serif;
  letter-spacing: 2px;
}}
"""


PANEL_CSS = (
    COMMON_CSS
    + """
.panel-main {
  margin-top: 40px;
  padding: 28px 34px;
  background: rgba(255,255,255,.11);
  border: 1px solid rgba(255,255,255,.20);
  border-left: 9px solid #f7dfaa;
  border-radius: 0 24px 24px 0;
  box-shadow: 0 24px 70px rgba(0,0,0,.26);
}
.panel-main h2 {
  margin: 10px 0 0;
  color: #fff;
  font-size: 62px;
  line-height: 1.08;
  font-weight: 900;
}
.panel-main .topic {
  margin-top: 14px;
  color: #fff;
  font-size: 38px;
  line-height: 1.28;
  font-weight: 900;
}
.panel-main .pill-row {
  margin-top: 16px;
}
.host-card {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
  gap: 26px;
  align-items: center;
  margin-top: 32px;
  padding: 22px;
  background: rgba(255,255,255,.90);
  color: #17191f;
  border-radius: 22px;
  box-shadow: 0 18px 50px rgba(0,0,0,.22);
}
.host-card img {
  width: 220px;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  object-position: center 42%;
  border-radius: 18px;
  border: 1px solid rgba(118,17,32,.18);
}
.host-role {
  display: inline-flex;
  padding: 9px 15px;
  color: #fff;
  background: #a71930;
  border-radius: 7px;
  font-size: 16px;
  font-weight: 900;
  letter-spacing: 4px;
}
.host-name {
  margin-top: 10px;
  color: #761120;
  font-size: 44px;
  font-weight: 900;
}
.host-aff {
  margin-top: 6px;
  color: #59606c;
  font-size: 22px;
  line-height: 1.35;
  font-weight: 800;
}
.host-bio-label {
  margin-top: 12px;
  color: #a2783c;
  font-size: 16px;
  font-weight: 900;
  letter-spacing: 4px;
}
.host-bio {
  margin-top: 5px;
  color: #333844;
  font-size: 15.5px;
  line-height: 1.42;
  text-align: justify;
}
.guest-box {
  margin-top: 24px;
  padding: 20px;
  background: rgba(247, 223, 170, .16);
  border: 1px solid rgba(247, 223, 170, .30);
  border-radius: 18px;
}
.guest-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
  margin-top: 12px;
}
.guest-card {
  display: grid;
  grid-template-columns: 86px minmax(0, 1fr);
  grid-template-rows: auto 1fr;
  gap: 4px 10px;
  min-width: 0;
  padding: 9px;
  color: #17191f;
  background: rgba(255,255,255,.92);
  border-radius: 12px;
}
.guest-card img {
  grid-row: 1 / 3;
  width: 86px;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  object-position: center 42%;
  border-radius: 8px;
}
.guest-card .name {
  margin-top: 3px;
  color: #761120;
  font-size: 19px;
  font-weight: 900;
}
.guest-card .aff {
  margin-top: 0;
  color: #59606c;
  font-size: 11px;
  line-height: 1.3;
  font-weight: 800;
}
"""
)


PERSON_CSS = (
    COMMON_CSS
    + """
.person-head {
  display: grid;
  grid-template-columns: 330px minmax(0, 1fr);
  gap: 38px;
  align-items: center;
  margin-top: 78px;
}
.portrait {
  width: 330px;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  object-position: center 42%;
  border: 1px solid rgba(255,255,255,.26);
  border-radius: 20px;
  box-shadow: 0 18px 52px rgba(0,0,0,.36);
}
.person-label {
  display: inline-flex;
  padding: 9px 16px;
  color: #fff;
  background: #a71930;
  border-radius: 7px;
  font-size: 18px;
  font-weight: 900;
  letter-spacing: 4px;
}
.person-name {
  margin-top: 20px;
  font-size: 66px;
  line-height: 1.1;
  font-weight: 900;
}
.person-aff {
  margin-top: 14px;
  color: rgba(255,255,255,.78);
  font-size: 25px;
  line-height: 1.42;
  font-weight: 800;
}
.topic-box {
  margin-top: 30px;
  padding: 24px 28px;
  background: rgba(255,255,255,.11);
  border-left: 7px solid #f7dfaa;
  border-radius: 0 14px 14px 0;
}
.topic-box .small {
  color: #f7dfaa;
  font-size: 16px;
  font-weight: 900;
  letter-spacing: 4px;
}
.topic-box .topic {
  margin-top: 10px;
  font-size: 31px;
  line-height: 1.35;
  font-weight: 900;
}
.bio-section {
  margin-top: 64px;
}
.bio-section h3 {
  margin: 0;
  color: #fff;
  font-size: 34px;
  font-weight: 900;
}
.bio-section h3::after {
  content: "";
  display: inline-block;
  width: 560px;
  height: 1px;
  margin-left: 18px;
  vertical-align: middle;
  background: rgba(255,255,255,.22);
}
.bio-card {
  margin-top: 24px;
  padding: 34px 38px;
  background: rgba(255,255,255,.09);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 18px;
}
.bio-card p {
  margin: 0;
  color: rgba(255,255,255,.92);
  font-size: 26px;
  line-height: 1.82;
  text-align: justify;
}
.person-guests {
  margin-top: 34px;
}
.person-guests h3 {
  margin: 0;
  color: #fff;
  font-size: 30px;
}
.person-guest-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
  margin-top: 18px;
}
.person-guest {
  padding: 14px 18px;
  background: rgba(255,255,255,.09);
  border: 1px solid rgba(255,255,255,.18);
  border-radius: 12px;
}
.person-guest strong {
  color: #f7dfaa;
  font-size: 18px;
}
.person-guest span {
  display: block;
  margin-top: 4px;
  color: rgba(255,255,255,.84);
  font-size: 13px;
  line-height: 1.4;
}
"""
)


BIO = (
    "陆品燕，上海财经大学“长江学者”特聘教授，计算机与人工智能学院创院院长，"
    "华为泰勒实验室首席科学家。他的主要研究方向是理论计算机，并注重与其它学科的交叉，"
    "近年来也关注求解器算法与大模型机理的研究。曾荣获ACM杰出科学家奖、"
    "第八届世界华人数学家大会ICCM数学奖（原晨兴数学奖）银奖、中国计算机学会青年科学家（2014）等荣誉。"
)


def shell(title: str, css: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <style>{css}</style>
</head>
<body>
  <article class="poster">
    <div class="top-rule"></div>
    <div class="inner">
      <header class="brand">
        <img src="{LOGO}" alt="山东大学" />
        <div class="tag">专题海报</div>
      </header>
      <section class="event">
        <div class="kicker">第 九 届</div>
        <h1>HCP 2026</h1>
        <div class="subtitle">难解问题的理论、算法与应用研讨会</div>
      </section>
      {body}
      <footer class="footer">
        <span>2026.07.31 – 08.02 · 山东大学青岛校区</span>
        <span class="url">hcp2026.sincst.cn</span>
      </footer>
    </div>
  </article>
</body>
</html>
"""


def panel_html() -> str:
    guest_cards = "".join(
        f"""<article class="guest-card">
          <img src="../../{esc(photo)}" alt="{esc(name)}" />
          <div class="name">{esc(name)}</div>
          <div class="aff">{esc(aff)}</div>
        </article>"""
        for name, aff, photo in PANELISTS
    )
    body = f"""
      <section class="panel-main">
        <div class="section-label">PANEL DISCUSSION</div>
        <h2>Panel Discussion</h2>
        <div class="topic">AI时代的算法研究</div>
        <div class="pill-row">
          <span class="pill">2026年8月1日</span>
          <span class="pill">15:45-16:45</span>
        </div>
      </section>
      <section class="host-card">
        <img src="{PHOTO}" alt="陆品燕" />
        <div>
          <div class="host-role">主持人</div>
          <div class="host-name">陆品燕</div>
          <div class="host-aff">上海财经大学</div>
          <div class="host-bio-label">个人简介</div>
          <div class="host-bio">{esc(BIO)}</div>
        </div>
      </section>
      <section class="guest-box">
        <div class="section-label">PANELISTS</div>
        <div class="guest-grid">{guest_cards}</div>
      </section>
    """
    return shell("HCP 2026 · Panel Discussion", PANEL_CSS, body)


def person_html() -> str:
    guests = "".join(
        f'<div class="person-guest"><strong>{esc(name)}</strong><span>{esc(aff)}</span></div>'
        for name, aff, _ in PANELISTS
    )
    body = f"""
      <section class="person-head">
        <img class="portrait" src="{PHOTO}" alt="陆品燕" />
        <div>
          <div class="person-label">PANEL DISCUSSION 主持人</div>
          <div class="person-name">陆品燕</div>
          <div class="person-aff">上海财经大学</div>
          <div class="topic-box">
            <div class="small">专题讨论</div>
            <div class="topic">AI时代的算法研究</div>
          </div>
        </div>
      </section>
      <section class="bio-section">
        <h3>个人简介</h3>
        <div class="bio-card"><p>{esc(BIO)}</p></div>
      </section>
      <section class="person-guests">
        <h3>Panel 嘉宾</h3>
        <div class="person-guest-grid">{guests}</div>
      </section>
    """
    return shell("HCP 2026 · 陆品燕", PERSON_CSS, body)


def clean_outputs() -> None:
    for directory in [HTML_DIR, PNG_DIR, JPG_DIR, PDF_DIR, ZIP_DIR, TMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    for directory, pattern in [
        (HTML_DIR, "*.html"),
        (PNG_DIR, "*.png"),
        (JPG_DIR, "*.jpg"),
        (PDF_DIR, "*.pdf"),
    ]:
        for path in directory.glob(pattern):
            path.unlink()
    for path in ZIP_DIR.glob("*.zip"):
        path.unlink()


def write_html() -> list[Path]:
    pages = [
        ("01-panel-discussion.html", panel_html()),
        ("02-陆品燕-pinyan-lu.html", person_html()),
    ]
    paths = []
    for filename, contents in pages:
        path = HTML_DIR / filename
        path.write_text(contents, encoding="utf-8")
        paths.append(path)
    return paths


def render_html(path: Path, png_out: Path) -> None:
    user_data_dir = TMP_DIR / f"chrome-{path.stem}"
    shutil.rmtree(user_data_dir, ignore_errors=True)
    cmd = [
        str(chrome_path()),
        "--headless=new",
        "--disable-gpu",
        "--disable-background-networking",
        "--disable-component-update",
        "--disable-default-apps",
        "--disable-extensions",
        "--disable-features=MediaRouter,OptimizationHints,Translate",
        "--disable-logging",
        "--disable-sync",
        "--hide-scrollbars",
        "--log-level=3",
        "--metrics-recording-only",
        "--mute-audio",
        "--no-first-run",
        "--no-default-browser-check",
        "--run-all-compositor-stages-before-draw",
        f"--user-data-dir={user_data_dir}",
        "--virtual-time-budget=3000",
        "--window-size=1080,1920",
        "--force-device-scale-factor=2",
        f"--screenshot={png_out}",
        html_file_url(path),
    ]
    subprocess.run(
        cmd,
        check=True,
        timeout=40,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    shutil.rmtree(user_data_dir, ignore_errors=True)
    with Image.open(png_out) as img:
        if img.size != POSTER_SIZE:
            img = img.convert("RGB").resize(POSTER_SIZE, Image.Resampling.LANCZOS)
            img.save(png_out, optimize=True)


def export_from_png(png_path: Path) -> tuple[Path, Path]:
    jpg_path = JPG_DIR / f"{png_path.stem}.jpg"
    pdf_path = PDF_DIR / f"{png_path.stem}.pdf"
    with Image.open(png_path) as img:
        rgb = img.convert("RGB")
        jpg = rgb.resize(JPG_SIZE, Image.Resampling.LANCZOS)
        jpg.save(jpg_path, quality=94, optimize=True, progressive=True)
        rgb.save(pdf_path, "PDF", resolution=216)
    return jpg_path, pdf_path


def zip_dir(zip_name: str, directory: Path, pattern: str) -> None:
    with zipfile.ZipFile(
        ZIP_DIR / zip_name, "w", compression=zipfile.ZIP_DEFLATED
    ) as zf:
        for file in sorted(directory.glob(pattern)):
            zf.write(file, arcname=file.name)


def write_readme() -> None:
    readme = textwrap.dedent(
        """\
        # HCP 2026 Panel Posters

        Generated poster set:

        1. `01-panel-discussion`
        2. `02-陆品燕-pinyan-lu`

        PNG files are 2160 x 3840. JPG files are 1080 x 1920 for WeChat sharing.
        PDF files are single-page posters generated from the high-resolution PNGs.
        """
    )
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    clean_outputs()
    html_paths = write_html()
    png_paths = [
        PNG_DIR / html_paths[0].name.replace(".html", ".png"),
        PNG_DIR / html_paths[1].name.replace(".html", ".png"),
    ]
    save_panel_png(png_paths[0])
    save_person_png(png_paths[1])
    for png_path in png_paths:
        export_from_png(png_path)
    zip_dir("HCP2026-panel-posters-png.zip", PNG_DIR, "*.png")
    zip_dir("HCP2026-panel-posters-jpg.zip", JPG_DIR, "*.jpg")
    zip_dir("HCP2026-panel-posters-pdf.zip", PDF_DIR, "*.pdf")
    write_readme()
    for path in png_paths:
        print(path.relative_to(ROOT))
    for path in sorted(ZIP_DIR.glob("*.zip")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
