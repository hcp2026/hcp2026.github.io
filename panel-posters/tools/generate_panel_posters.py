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


def text_size(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont) -> tuple[int, int]:
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


def wrap_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    units = text.split(" ") if " " in text else list(text)
    lines: list[str] = []
    current = ""
    for unit in units:
        candidate = unit if not current else (current + (" " if " " in text else "") + unit)
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


def cover_image(path: Path, size: tuple[int, int], position: tuple[float, float] = (0.5, 0.5)) -> Image.Image:
    with Image.open(path) as img:
        return ImageOps.fit(img.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=position)


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
    bg = cover_image(ROOT / "assets/sdu-qingdao-library-hero.jpg", POSTER_SIZE, (0.5, 0.65)).convert("RGBA")
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
    td.rectangle((POSTER_SIZE[0] - 520, 0, POSTER_SIZE[0], 32), fill=(216, 177, 95, 255))
    bg.alpha_composite(top)
    return bg


def draw_brand(draw: ImageDraw.ImageDraw) -> None:
    draw_text(draw, (144, 136), "山东大学", font(FONT_SANS, 70), WHITE)
    draw_text(draw, (148, 220), "SHANDONG UNIVERSITY", font(FONT_SERIF, 28), (255, 255, 255, 230))
    draw_text(draw, (1760, 140), "专题海报", font(FONT_SANS, 44), GOLD)


def draw_event(draw: ImageDraw.ImageDraw, y: int = 360) -> None:
    draw_text(draw, (144, y), "第  九  届", font(FONT_SANS, 48), GOLD)
    draw_text(draw, (144, y + 106), "HCP 2026", font(FONT_SERIF, 210), WHITE)
    draw_text(draw, (144, y + 350), "难解问题的理论、算法与应用研讨会", font(FONT_SANS, 62), WHITE)


def draw_footer(draw: ImageDraw.ImageDraw) -> None:
    y = 3630
    draw.line((144, y, 2016, y), fill=(255, 255, 255, 70), width=2)
    draw_text(draw, (144, y + 46), "2026.07.31 – 08.02 · 山东大学青岛校区", font(FONT_SANS, 38), GOLD)
    draw_text(draw, (1608, y + 46), "hcp2026.sincst.cn", font(FONT_SERIF, 39), GOLD)


def draw_pill(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], label: str) -> None:
    draw.rounded_rectangle(box, radius=(box[3] - box[1]) // 2, fill=(244, 223, 176))
    tw, th = text_size(draw, label, font(FONT_SANS, 42))
    draw_text(draw, (box[0] + (box[2] - box[0] - tw) // 2, box[1] + (box[3] - box[1] - th) // 2 - 8), label, font(FONT_SANS, 42), RED)


def save_panel_png(path: Path) -> None:
    img = make_background()
    draw = ImageDraw.Draw(img)
    draw_brand(draw)
    draw_event(draw)

    rounded_overlay(img, (144, 1060, 2016, 1780), (255, 255, 255, 30), 44, (255, 255, 255, 54), 2)
    draw = ImageDraw.Draw(img)
    draw.rectangle((144, 1060, 164, 1780), fill=GOLD)
    draw_text(draw, (214, 1148), "PANEL DISCUSSION", font(FONT_SERIF, 44), GOLD)
    draw_text(draw, (214, 1240), "Panel Discussion", font(FONT_SANS, 130), WHITE)
    draw_text(draw, (214, 1430), "AI时代的算法研究", font(FONT_SANS, 94), WHITE)
    draw_pill(draw, (214, 1606, 620, 1700), "2026年8月1日")
    draw_pill(draw, (652, 1606, 1010, 1700), "15:45-16:45")

    rounded_overlay(img, (144, 1910, 2016, 2840), (255, 255, 255, 230), 44)
    photo = cover_image(ROOT / "assets/speakers/pinyan-lu.jpg", (520, 650), (0.52, 0.43)).convert("RGBA")
    mask = Image.new("L", photo.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, *photo.size), radius=34, fill=255)
    img.paste(photo, (204, 1965), mask)
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((800, 2016, 990, 2080), radius=12, fill=(167, 25, 48))
    draw_text(draw, (832, 2024), "主持人", font(FONT_SANS, 34), WHITE)
    draw_text(draw, (800, 2150), "陆品燕", font(FONT_SANS, 112), RED)
    draw_text(draw, (800, 2296), "上海财经大学", font(FONT_SANS, 52), (89, 96, 108))
    draw_text(draw, (800, 2388), "个人简介", font(FONT_SANS, 31), (162, 120, 60))
    draw_wrapped(draw, (800, 2444), BIO, font(FONT_SANS, 25), 1100, 43, (51, 56, 68))

    rounded_overlay(img, (144, 2890, 2016, 3130), (247, 223, 170, 42), 34, (247, 223, 170, 90), 2)
    draw = ImageDraw.Draw(img)
    draw_text(draw, (214, 2938), "PANELISTS", font(FONT_SERIF, 42), GOLD)
    draw_text(draw, (214, 3024), "嘉宾待定", font(FONT_SANS, 82), WHITE)
    draw_text(draw, (214, 3230), "地点：山东大学青岛校区淦昌苑D座305会议厅", font(FONT_SANS, 42), (255, 255, 255, 220))
    draw_footer(draw)
    img.convert("RGB").save(path, optimize=True)


def save_person_png(path: Path) -> None:
    img = make_background()
    draw = ImageDraw.Draw(img)
    draw_brand(draw)
    draw_event(draw, 340)

    photo = cover_image(ROOT / "assets/speakers/pinyan-lu.jpg", (660, 825), (0.52, 0.43)).convert("RGBA")
    mask = Image.new("L", photo.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle((0, 0, *photo.size), radius=38, fill=255)
    img.paste(photo, (144, 1010), mask)

    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle((884, 1060, 1395, 1132), radius=12, fill=(167, 25, 48))
    draw_text(draw, (914, 1072), "PANEL DISCUSSION 主持人", font(FONT_SANS, 35), WHITE)
    draw_text(draw, (884, 1218), "陆品燕", font(FONT_SANS, 128), WHITE)
    draw_text(draw, (884, 1380), "上海财经大学", font(FONT_SANS, 54), (255, 255, 255, 210))

    rounded_overlay(img, (884, 1532, 2016, 1778), (255, 255, 255, 32), 22)
    draw = ImageDraw.Draw(img)
    draw.rectangle((884, 1532, 900, 1778), fill=GOLD)
    draw_text(draw, (936, 1575), "专题讨论", font(FONT_SANS, 34), GOLD)
    draw_wrapped(draw, (936, 1640), "AI时代的算法研究", font(FONT_SANS, 60), 980, 80, WHITE)

    draw_text(draw, (144, 1988), "个人简介", font(FONT_SANS, 62), WHITE)
    draw.line((420, 2026, 2016, 2026), fill=(255, 255, 255, 70), width=2)
    rounded_overlay(img, (144, 2125, 2016, 3210), (255, 255, 255, 28), 34, (255, 255, 255, 54), 2)
    draw = ImageDraw.Draw(img)
    draw_wrapped(draw, (214, 2205), BIO, font(FONT_SANS, 51), 1730, 92, (255, 255, 255, 236))
    draw_footer(draw)
    img.convert("RGB").save(path, optimize=True)


def chrome_path() -> Path:
    for candidate in CHROME_CANDIDATES:
        if candidate.exists():
            return candidate
    from_path = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
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


PANEL_CSS = COMMON_CSS + """
.panel-main {
  margin-top: 88px;
  padding: 46px 48px 44px;
  background: rgba(255,255,255,.11);
  border: 1px solid rgba(255,255,255,.20);
  border-left: 9px solid #f7dfaa;
  border-radius: 0 24px 24px 0;
  box-shadow: 0 24px 70px rgba(0,0,0,.26);
}
.panel-main h2 {
  margin: 16px 0 0;
  color: #fff;
  font-size: 76px;
  line-height: 1.08;
  font-weight: 900;
}
.panel-main .topic {
  margin-top: 28px;
  color: #fff;
  font-size: 48px;
  line-height: 1.28;
  font-weight: 900;
}
.host-card {
  display: grid;
  grid-template-columns: 280px minmax(0, 1fr);
  gap: 34px;
  align-items: center;
  margin-top: 62px;
  padding: 28px;
  background: rgba(255,255,255,.90);
  color: #17191f;
  border-radius: 22px;
  box-shadow: 0 18px 50px rgba(0,0,0,.22);
}
.host-card img {
  width: 280px;
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
  font-size: 18px;
  font-weight: 900;
  letter-spacing: 4px;
}
.host-name {
  margin-top: 18px;
  color: #761120;
  font-size: 56px;
  font-weight: 900;
}
.host-aff {
  margin-top: 10px;
  color: #59606c;
  font-size: 25px;
  line-height: 1.35;
  font-weight: 800;
}
.host-bio-label {
  margin-top: 22px;
  color: #a2783c;
  font-size: 16px;
  font-weight: 900;
  letter-spacing: 4px;
}
.host-bio {
  margin-top: 8px;
  color: #333844;
  font-size: 18px;
  line-height: 1.62;
  text-align: justify;
}
.guest-box {
  margin-top: 44px;
  padding: 34px 38px;
  background: rgba(247, 223, 170, .16);
  border: 1px solid rgba(247, 223, 170, .30);
  border-radius: 18px;
}
.guest-box .text {
  margin-top: 12px;
  font-size: 38px;
  font-weight: 900;
}
"""


PERSON_CSS = COMMON_CSS + """
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
"""


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
        <div class="text">嘉宾待定</div>
      </section>
    """
    return shell("HCP 2026 · Panel Discussion", PANEL_CSS, body)


def person_html() -> str:
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
    """
    return shell("HCP 2026 · 陆品燕", PERSON_CSS, body)


def clean_outputs() -> None:
    for directory in [HTML_DIR, PNG_DIR, JPG_DIR, PDF_DIR, ZIP_DIR, TMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    for directory, pattern in [(HTML_DIR, "*.html"), (PNG_DIR, "*.png"), (JPG_DIR, "*.jpg"), (PDF_DIR, "*.pdf")]:
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
    subprocess.run(cmd, check=True, timeout=40, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
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
    with zipfile.ZipFile(ZIP_DIR / zip_name, "w", compression=zipfile.ZIP_DEFLATED) as zf:
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
