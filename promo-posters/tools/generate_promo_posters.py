#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
import textwrap
import zipfile
from pathlib import Path
from urllib.parse import quote

import qrcode
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "promo-posters"
HTML_DIR = OUT / "html"
PNG_DIR = OUT / "png"
JPG_DIR = OUT / "jpg"
PDF_DIR = OUT / "pdf"
ZIP_DIR = OUT / "zip"
TMP_DIR = OUT / "tmp"

CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
]

POSTER_SIZE = (2160, 3840)
JPG_SIZE = (1080, 1920)
POSTER_CSS_HEIGHTS = {
    "03-keynote-poster.html": 2400,
    "04-ai-topic-poster.html": 1700,
    "05-combinatorial-optimization-topic-poster.html": 2400,
    "06-cryptanalysis-topic-poster.html": 2400,
}


def extract_speakers() -> dict[str, dict]:
    text = (ROOT / "script.js").read_text(encoding="utf-8")
    start = text.index("const SPEAKERS =")
    start = text.index("{", start)
    depth = 0
    for idx, char in enumerate(text[start:], start):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : idx + 1])
    raise ValueError("Cannot find SPEAKERS object in script.js")


def pick(value: str | dict[str, str], lang: str = "zh") -> str:
    if isinstance(value, str):
        return value
    return value.get(lang) or value.get("zh") or value.get("en") or ""


def esc(value: str) -> str:
    return html.escape(value, quote=False)


def normalize_text(value: str) -> str:
    value = value.replace("$", "")
    value = value.replace("’", "'").replace("“", "「").replace("”", "」")
    value = value.replace("—", "-").replace("–", "-")
    return value.strip()


def paragraphs(value: str) -> str:
    value = normalize_text(value) or "待定"
    chunks = [part.strip() for part in re.split(r"\n\s*\n", value) if part.strip()]
    return "".join(f"<p>{esc(chunk)}</p>" for chunk in chunks)


def speaker(speakers: dict[str, dict], sid: str) -> dict:
    if sid not in speakers:
        raise KeyError(f"Missing speaker: {sid}")
    return speakers[sid]


def photo_path(s: dict) -> str:
    return "../../" + s["photo"]


COMMON_CSS = """
* { box-sizing: border-box; }
html, body {
  margin: 0;
  padding: 0;
  background: #14090d;
  font-family: "Hiragino Sans GB", "STHeiti", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
  color: #17191f;
}
body {
  width: 1080px;
  height: 1920px;
  overflow: hidden;
}
.poster {
  position: relative;
  width: 1080px;
  height: 1920px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(80, 12, 23, .92) 0%, rgba(124, 20, 39, .90) 38%, rgba(248, 241, 231, .96) 38.1%, rgba(255, 250, 243, 1) 100%),
    url("../../assets/sdu-qingdao-library-hero.jpg") center top / cover no-repeat;
}
.poster::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 18% 8%, rgba(216, 177, 95, .22), transparent 26%),
    linear-gradient(135deg, rgba(255,255,255,.08), transparent 42%),
    linear-gradient(180deg, rgba(79, 12, 23, .10), rgba(79, 12, 23, .02));
  pointer-events: none;
}
.top-rule {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 16px;
  background: linear-gradient(90deg, #a71930 0%, #d8b15f 78%, #fff2cc 100%);
}
.inner {
  position: relative;
  z-index: 1;
  height: 100%;
  padding: 54px 58px 48px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 22px;
  color: rgba(255,255,255,.92);
}
.brand img {
  width: 236px;
  filter: brightness(0) invert(1);
}
.brand .series {
  margin-left: auto;
  color: #f7dfaa;
  font-size: 22px;
  font-weight: 900;
  letter-spacing: 6px;
}
.hero-title {
  margin-top: 34px;
  color: #fff;
}
.hero-title .kicker {
  color: #f7dfaa;
  font-size: 23px;
  font-weight: 900;
  letter-spacing: 12px;
}
.hero-title h1 {
  margin: 16px 0 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 104px;
  line-height: .9;
  letter-spacing: 2px;
}
.hero-title .cn {
  margin-top: 14px;
  font-size: 30px;
  line-height: 1.35;
  font-weight: 900;
}
.hero-title .en {
  margin-top: 6px;
  width: 850px;
  color: rgba(255,255,255,.74);
  font-size: 18px;
  line-height: 1.42;
}
.meta-strip {
  display: flex;
  gap: 12px;
  margin-top: 22px;
}
.meta-pill {
  padding: 10px 16px;
  color: #4f0c17;
  background: #f4dfb0;
  border-radius: 999px;
  font-size: 19px;
  font-weight: 900;
}
.content {
  position: absolute;
  left: 58px;
  right: 58px;
  top: 520px;
  bottom: 94px;
}
.footer {
  position: absolute;
  left: 58px;
  right: 58px;
  bottom: 35px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #761120;
  border-top: 2px solid rgba(167,25,48,.24);
  padding-top: 18px;
  font-size: 20px;
  font-weight: 900;
}
.footer .url {
  font-family: Georgia, "Times New Roman", serif;
  letter-spacing: 1px;
}
.section-title {
  display: flex;
  align-items: baseline;
  gap: 16px;
  color: #761120;
}
.section-title h2 {
  margin: 0;
  color: #fff;
  font-size: 46px;
  line-height: 1;
  font-weight: 900;
  text-shadow: 0 6px 18px rgba(0,0,0,.22);
}
.section-title .en {
  color: #d8b15f;
  font-size: 18px;
  font-weight: 900;
  letter-spacing: 4px;
  text-transform: uppercase;
}
.tag {
  display: inline-flex;
  align-items: center;
  height: 28px;
  padding: 0 10px;
  color: #fff;
  background: #a71930;
  border-radius: 5px;
  font-size: 15px;
  font-weight: 900;
  letter-spacing: .5px;
}
.muted {
  color: #69707d;
}
"""


AGENDA_CSS = """
.agenda-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 20px;
  font-family: "Songti SC", "STSong", "SimSong", "LiSong Pro", serif;
}
.content {
  top: 500px;
}
.agenda-card {
  overflow: hidden;
  background: rgba(255,255,255,.88);
  border: 1px solid rgba(167,25,48,.17);
  border-radius: 16px;
  box-shadow: 0 12px 34px rgba(79,12,23,.10);
}
.agenda-card.full {
  grid-column: 1 / -1;
}
.agenda-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  padding: 14px 18px;
  color: #fff;
  background: #861224;
}
.agenda-head h3 {
  margin: 0;
  font-size: 27px;
  font-weight: 900;
}
.agenda-head .place {
  color: rgba(255,255,255,.76);
  font-size: 15px;
  font-weight: 800;
  text-align: right;
}
.agenda-table {
  width: 100%;
  border-collapse: collapse;
}
.agenda-table td {
  padding: 9px 12px;
  border-top: 1px solid #eadfd4;
  vertical-align: top;
  font-size: 18px;
  line-height: 1.32;
}
.agenda-table td.time {
  width: 126px;
  color: #a71930;
  font-family: "Songti SC", "STSong", "SimSong", "LiSong Pro", serif;
  font-weight: 900;
  white-space: nowrap;
}
.agenda-table strong {
  display: block;
  color: #17191f;
  font-size: 19px;
  line-height: 1.26;
}
.agenda-table .speaker-line {
  display: flex;
  align-items: baseline;
  gap: 8px;
  flex-wrap: wrap;
}
.agenda-table .aff {
  color: #69707d;
  font-size: 14px;
  line-height: 1.22;
  font-weight: 800;
}
.agenda-table .title {
  margin-top: 3px;
  color: #333844;
  font-size: 15px;
  line-height: 1.34;
  font-weight: 700;
}
.agenda-table .break td,
.agenda-table .activity td {
  color: #861224;
  background: #fff2cc;
  font-weight: 900;
  text-align: center;
}
.agenda-table .activity td {
  color: #333844;
  background: #faf1e7;
}
.agenda-table .panel td {
  padding-top: 6px;
  padding-bottom: 6px;
  background: #f6f8fb;
}
.agenda-table .panel-label {
  color: #761120;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 19px;
  line-height: 1.2;
  font-weight: 900;
}
.agenda-table .panel-topic {
  margin-top: 3px;
  color: #17191f;
  font-size: 16px;
  line-height: 1.32;
  font-weight: 900;
}
.agenda-table .panel-meta {
  margin-top: 3px;
  color: #69707d;
  font-size: 12px;
  line-height: 1.24;
  font-weight: 800;
}
.agenda-table .panel-meta span {
  color: #333844;
}
.agenda-card.ai .agenda-head {
  padding-top: 11px;
  padding-bottom: 11px;
}
.agenda-card.ai .agenda-table td {
  padding-top: 6px;
  padding-bottom: 6px;
}
.agenda-card.ai .agenda-table .panel td {
  padding-top: 4px;
  padding-bottom: 4px;
}
.agenda-card.ai .agenda-table .panel-meta {
  font-size: 11px;
  line-height: 1.18;
}
"""


KEYNOTE_CSS = """
.keynote-list {
  display: grid;
  gap: 14px;
  margin-top: 24px;
}
.keynote-card {
  display: grid;
  grid-template-columns: 142px minmax(0, 1fr);
  gap: 16px;
  min-height: 280px;
  padding: 16px;
  background: rgba(255,255,255,.90);
  border: 1px solid rgba(167,25,48,.18);
  border-radius: 17px;
  box-shadow: 0 12px 34px rgba(79,12,23,.10);
}
.keynote-photo {
  width: 142px;
  height: 178px;
  object-fit: cover;
  object-position: center 42%;
  border-radius: 12px;
  border: 1px solid rgba(118,17,32,.18);
}
.keynote-name-row {
  display: flex;
  align-items: center;
  gap: 12px;
}
.keynote-name {
  color: #761120;
  font-size: 29px;
  font-weight: 900;
  line-height: 1.1;
}
.keynote-aff {
  margin-top: 4px;
  color: #69707d;
  font-size: 15px;
  font-weight: 800;
}
.keynote-talk {
  margin-top: 9px;
  color: #17191f;
  font-size: 20px;
  line-height: 1.28;
  font-weight: 900;
}
.abstract-label {
  margin-top: 10px;
  color: #a2783c;
  font-size: 14px;
  font-weight: 900;
  letter-spacing: 3px;
}
.abstract {
  margin-top: 5px;
  color: #333844;
  font-size: 15.8px;
  line-height: 1.42;
  text-align: justify;
}
.abstract p {
  margin: 0;
}
"""

FULL_KEYNOTE_CSS = (
    KEYNOTE_CSS
    + """
body {
  height: auto;
  overflow: visible;
}
.long-keynote-poster {
  height: 2400px;
  background:
    linear-gradient(180deg, rgba(80, 12, 23, .92) 0%, rgba(124, 20, 39, .90) 720px, rgba(248, 241, 231, .96) 722px, rgba(255, 250, 243, 1) 100%),
    url("../../assets/sdu-qingdao-library-hero.jpg") center top / cover no-repeat;
}
.long-keynote-poster .content {
  position: relative;
  inset: auto;
  margin-top: 78px;
}
.long-keynote-poster .keynote-list {
  gap: 18px;
}
.long-keynote-poster .keynote-card {
  grid-template-columns: 170px minmax(0, 1fr);
  min-height: 0;
  gap: 20px;
  padding: 20px;
}
.long-keynote-poster .keynote-photo {
  width: 170px;
  height: 213px;
}
.long-keynote-poster .keynote-name {
  font-size: 30px;
}
.long-keynote-poster .keynote-aff {
  font-size: 16px;
}
.long-keynote-poster .keynote-talk {
  font-size: 21px;
  line-height: 1.32;
}
.long-keynote-poster .abstract {
  font-size: 16.5px;
  line-height: 1.48;
}
"""
)


TOPIC_DETAIL_CSS = (
    KEYNOTE_CSS
    + """
body {
  height: auto;
  overflow: visible;
}
.topic-detail-poster {
  height: 1700px;
  background:
    linear-gradient(180deg, rgba(80, 12, 23, .92) 0%, rgba(124, 20, 39, .90) 720px, rgba(248, 241, 231, .96) 722px, rgba(255, 250, 243, 1) 100%),
    url("../../assets/sdu-qingdao-library-hero.jpg") center top / cover no-repeat;
}
.topic-detail-poster.topic-combo {
  height: 2400px;
}
.topic-detail-poster.topic-crypto {
  height: 2400px;
}
.topic-detail-poster .content {
  position: relative;
  inset: auto;
  margin-top: 78px;
}
.topic-detail-poster .keynote-list {
  gap: 18px;
}
.topic-detail-poster .keynote-card {
  grid-template-columns: 170px minmax(0, 1fr);
  min-height: 0;
  gap: 20px;
  padding: 20px;
}
.topic-detail-poster .keynote-photo {
  width: 170px;
  height: 213px;
}
.topic-detail-poster .keynote-name {
  font-size: 30px;
}
.topic-detail-poster .keynote-aff {
  font-size: 16px;
}
.topic-detail-poster .keynote-talk {
  font-size: 21px;
  line-height: 1.32;
}
.topic-detail-poster .abstract-label {
  margin-top: 12px;
  font-size: 14px;
}
.topic-detail-poster .abstract {
  font-size: 16.5px;
  line-height: 1.48;
}
"""
)


MAIN_CSS = """
.main-panel {
  display: grid;
  grid-template-columns: 1.05fr .95fr;
  gap: 22px;
  margin-top: 24px;
}
.main-info {
  display: grid;
  gap: 16px;
}
.info-box,
.qr-panel {
  padding: 22px;
  background: rgba(255,255,255,.90);
  border: 1px solid rgba(167,25,48,.16);
  border-radius: 17px;
  box-shadow: 0 12px 34px rgba(79,12,23,.10);
}
.info-box .label {
  color: #a2783c;
  font-size: 16px;
  font-weight: 900;
  letter-spacing: 4px;
}
.info-box .value {
  margin-top: 8px;
  color: #17191f;
  font-size: 30px;
  line-height: 1.35;
  font-weight: 900;
}
.info-box .sub {
  margin-top: 8px;
  color: #69707d;
  font-size: 18px;
  line-height: 1.5;
  font-weight: 800;
}
.qr-panel h3 {
  margin: 0 0 18px;
  color: #761120;
  font-size: 30px;
  font-weight: 900;
}
.qr-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}
.qr-item {
  padding: 14px;
  background: #fffaf3;
  border: 1px solid #eadfd4;
  border-radius: 14px;
  text-align: center;
}
.qr-item.wide {
  grid-column: 1 / -1;
}
.qr-item img {
  width: 170px;
  height: 170px;
  object-fit: contain;
  background: #fff;
  border-radius: 10px;
}
.qr-item.wide img {
  width: 190px;
  height: 260px;
}
.qr-item .caption {
  margin-top: 10px;
  color: #761120;
  font-size: 20px;
  font-weight: 900;
}
.main-note {
  margin-top: 20px;
  padding: 22px;
  color: #fff;
  background: linear-gradient(135deg, #a71930, #761120);
  border-radius: 17px;
  font-size: 25px;
  line-height: 1.6;
  font-weight: 900;
}
"""


def poster_shell(
    title_cn: str,
    title_en: str,
    body: str,
    extra_css: str,
    poster_class: str = "",
) -> str:
    title_suffix = f'<span class="en">{esc(title_en)}</span>' if title_en else ""
    class_name = f"poster {poster_class}".strip()
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>HCP 2026 - {esc(title_cn)}</title>
  <style>{COMMON_CSS}{extra_css}</style>
</head>
<body>
  <article class="{esc(class_name)}">
    <div class="top-rule"></div>
    <div class="inner">
      <header class="brand">
        <img src="../../assets/sdu-logo.svg" alt="山东大学" />
        <div class="series">宣传海报</div>
      </header>
      <section class="hero-title">
        <div class="kicker">第 九 届</div>
        <h1>HCP 2026</h1>
        <div class="cn">难解问题的理论、算法与应用研讨会</div>
        <div class="meta-strip">
          <div class="meta-pill">2026年7月31日-8月2日</div>
          <div class="meta-pill">山东大学青岛校区</div>
        </div>
      </section>
      <main class="content">
        <div class="section-title"><h2>{esc(title_cn)}</h2>{title_suffix}</div>
        {body}
      </main>
      <footer class="footer">
        <div>山东大学网络空间安全学院 · 青岛</div>
        <div class="url">hcp2026.sincst.cn</div>
      </footer>
    </div>
  </article>
</body>
</html>
"""


def ensure_generated_assets() -> None:
    qr = qrcode.QRCode(border=1, box_size=12)
    qr.add_data("https://hcp2026.sincst.cn/")
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img.save(TMP_DIR / "website-qr.png")


def main_html() -> str:
    body = """<div class="main-panel">
  <section class="main-info">
    <article class="info-box">
      <div class="label">会议时间</div>
      <div class="value">2026年7月31日-8月2日</div>
      <div class="sub">7月31日报到注册；8月1日-2日大会报告与专题交流。</div>
    </article>
    <article class="info-box">
      <div class="label">会议地点</div>
      <div class="value">山东大学青岛校区淦昌苑D座305会议厅</div>
      <div class="sub">报到地点：青岛蓝谷国际酒店大堂。</div>
    </article>
    <article class="info-box">
      <div class="label">承办单位</div>
      <div class="value">山东大学网络空间安全学院</div>
      <div class="sub">会议聚焦难解计算问题的理论、算法与应用，欢迎参会交流。</div>
    </article>
  </section>
  <section class="qr-panel">
    <h3>扫码获取会议信息</h3>
    <div class="qr-grid">
      <div class="qr-item">
        <img src="../tmp/website-qr.png" alt="会议官网二维码" />
        <div class="caption">会议官网</div>
      </div>
      <div class="qr-item">
        <img src="../../assets/register-qr.png" alt="会议注册二维码" />
        <div class="caption">扫码注册</div>
      </div>
      <div class="qr-item wide">
        <img src="../../assets/wechat-group-qr.png" alt="参会微信群二维码" />
        <div class="caption">参会微信群</div>
      </div>
    </div>
  </section>
</div>"""
    return poster_shell("大会主海报", "", body, MAIN_CSS)


AGENDA_BLOCKS = [
    {
        "cls": "full",
        "date": "7月31日 星期五",
        "place": "青岛蓝谷国际酒店大堂",
        "rows": [
            ("14:00-21:00", "注册", "", "activity"),
            ("交通", "打车导航到「蓝谷国际酒店」", "", "activity"),
            ("17:30-20:30", "欢迎自助餐", "", "activity"),
        ],
    },
    {
        "cls": "",
        "date": "8月1日 上午",
        "place": "山东大学青岛校区淦昌苑D座305会议厅",
        "rows": [
            ("08:50-09:00", "开幕式、致辞", "", "activity"),
            ("09:00-09:45", "戴彧虹", "特邀报告：大规模设施选址问题的精确求解", ""),
            (
                "09:45-10:30",
                "詹乃军",
                "特邀报告：On termination of polynomial programs with equality conditions",
                "",
            ),
            ("10:30-10:45", "茶歇", "", "break"),
            ("10:45-11:30", "孙晓明", "特邀报告：量子线路优化", ""),
            ("11:30-12:15", "冯启龙", "特邀报告：面向大规模数据的机器学习算法优化", ""),
            ("12:15-14:00", "午餐 / 休息", "", "activity"),
        ],
    },
    {
        "cls": "ai",
        "date": "8月1日 下午",
        "place": "人工智能专题",
        "rows": [
            ("14:00-14:30", "袁明轩", "基于大模型的自动算法设计", ""),
            (
                "14:30-15:00",
                "王肇国",
                "FM-Agent：面向大型系统软件的霍尔范式自动化推理智能体及领域实战",
                "",
            ),
            ("15:00-15:30", "李旻", "面向硬件形式化难例求解的智能体路线", ""),
            ("15:30-15:45", "茶歇", "", "break"),
            ("15:45-16:45", "Panel Discussion", "AI时代的算法研究", "panel"),
            ("16:45-17:30", "户外交流", "", "activity"),
            ("17:30-", "晚餐", "", "activity"),
        ],
    },
    {
        "cls": "",
        "date": "8月2日 上午",
        "place": "组合优化专题",
        "rows": [
            ("09:00-09:30", "操宜新", "线性系统的半整数解", ""),
            ("09:30-10:00", "雷震东", "从工业应用看模型表达能力与算法设计", ""),
            ("10:00-10:30", "刘圣鑫", "最大凝聚子图搜索的分支定界算法", ""),
            ("10:30-11:00", "茶歇", "", "break"),
            ("11:00-11:30", "秦虎", "车辆路径优化算法：现状、挑战和实践", ""),
            ("11:30-12:00", "黄一潇", "顺丰智能物流网络规划技术分享", ""),
        ],
    },
    {
        "cls": "",
        "date": "8月2日 下午",
        "place": "密码分析专题",
        "rows": [
            (
                "14:00-14:30",
                "Emanuele Bellini",
                "使用 CLAASP 生成并求解困难的对称密码分析问题",
                "",
            ),
            (
                "14:30-15:00",
                "周春宁",
                "开放密码分析平台（OCP）：面向对称密码的自动化密码分析平台",
                "",
            ),
            ("15:00-15:30", "茶歇", "", "break"),
            ("15:30-16:00", "张昕荻", "SAT求解及其在密码分析中的应用", ""),
            ("16:00-16:30", "樊燕红", "对称密码的自动化分析与设计技术", ""),
            ("16:30-16:40", "闭幕式", "", "activity"),
        ],
    },
]

AGENDA_RENDER_ORDER = [
    "7月31日 星期五",
    "8月1日 上午",
    "8月2日 上午",
    "8月1日 下午",
    "8月2日 下午",
]


def agenda_html(speakers: dict[str, dict]) -> str:
    cards = []
    affiliations = {
        pick(speaker_data["name"]): pick(speaker_data["aff"])
        for speaker_data in speakers.values()
    }
    blocks_by_date = {block["date"]: block for block in AGENDA_BLOCKS}
    for date in AGENDA_RENDER_ORDER:
        block = blocks_by_date[date]
        rows = []
        for time, name, title, row_cls in block["rows"]:
            cls = f' class="{row_cls}"' if row_cls else ""
            if row_cls == "panel":
                label = (
                    '<div class="panel-label">Panel Discussion</div>'
                    '<div class="panel-topic">AI时代的算法研究</div>'
                    '<div class="panel-meta"><span>主持人：</span>陆品燕（上海财经大学）</div>'
                    '<div class="panel-meta"><span>嘉宾：</span>'
                    "詹乃军（北京大学）、孙晓明（中科院计算所）、冯启龙（中南大学）、"
                    "袁明轩（华为诺亚方舟实验室）、王肇国（上海交大）、李旻（东南大学）</div>"
                )
                rows.append(
                    f'<tr class="panel"><td class="time">{esc(time)}</td><td>{label}</td></tr>'
                )
            elif row_cls in {"break", "activity"}:
                label = f"<strong>{esc(name)}</strong>"
                if title:
                    label += f'<div class="title">{esc(title)}</div>'
                rows.append(
                    f'<tr{cls}><td class="time">{esc(time)}</td><td>{label}</td></tr>'
                )
            else:
                aff = affiliations.get(name, "")
                aff_html = f'<span class="aff">{esc(aff)}</span>' if aff else ""
                rows.append(
                    "<tr>"
                    f'<td class="time">{esc(time)}</td>'
                    f'<td><div class="speaker-line"><strong>{esc(name)}</strong>{aff_html}</div>'
                    f'<div class="title">{esc(title)}</div></td>'
                    "</tr>"
                )
        cards.append(
            f"""<article class="agenda-card {block["cls"]}">
  <div class="agenda-head"><h3>{esc(block["date"])}</h3><div class="place">{esc(block["place"])}</div></div>
  <table class="agenda-table"><tbody>{"".join(rows)}</tbody></table>
</article>"""
        )
    body = f'<div class="agenda-grid">{"".join(cards)}</div>'
    return poster_shell("大会议程", "", body, AGENDA_CSS)


KEYNOTE_IDS = ["yuhong-dai", "naijun-zhan", "xiaoming-sun", "qilong-feng"]

POSTER_TITLE_OVERRIDES = {
    "yuhong-dai": "大规模设施选址问题的精确求解",
    "naijun-zhan": "On termination of polynomial programs with equality conditions",
    "yixin-cao": "线性系统的半整数解",
    "shengxin-liu": "最大凝聚子图搜索的分支定界算法",
    "emanuele-bellini": "使用 CLAASP 生成并求解困难的对称密码分析问题",
    "chunning-zhou": "开放密码分析平台（OCP）：面向对称密码的自动化密码分析平台",
}

POSTER_AFF_OVERRIDES = {"emanuele-bellini": "阿联酋技术创新研究院（TII）"}


def keynotes_html(speakers: dict[str, dict]) -> str:
    cards = []
    for sid in KEYNOTE_IDS:
        s = speaker(speakers, sid)
        name = pick(s["name"])
        aff = POSTER_AFF_OVERRIDES.get(sid, pick(s["aff"]))
        title = POSTER_TITLE_OVERRIDES.get(sid, pick(s["title"]))
        abstract = pick(s["abstract"])
        abstract = "待定" if abstract in {"TBA", "待定"} else abstract
        cards.append(
            f"""<article class="keynote-card">
  <img class="keynote-photo" src="{photo_path(s)}" alt="{esc(name)}" />
  <div>
    <div class="keynote-name-row"><span class="tag">特邀报告</span><div class="keynote-name">{esc(name)}</div></div>
    <div class="keynote-aff">{esc(aff)}</div>
    <div class="keynote-talk">{esc(title)}</div>
    <div class="abstract-label">报告摘要</div>
    <div class="abstract">{paragraphs(abstract)}</div>
  </div>
</article>"""
        )
    body = f'<div class="keynote-list">{"".join(cards)}</div>'
    return poster_shell(
        "特邀报告",
        "",
        body,
        FULL_KEYNOTE_CSS,
        "long-keynote-poster",
    )


TOPIC_GROUPS = [
    {
        "slug": "ai",
        "title": "人工智能专题",
        "subtitle": "3 位报告人",
        "filename": "04-ai-topic-poster.html",
        "ids": ["mingxuan-yuan", "zhaoguo-wang", "min-li"],
    },
    {
        "slug": "combo",
        "title": "组合优化专题",
        "subtitle": "5 位报告人",
        "filename": "05-combinatorial-optimization-topic-poster.html",
        "ids": ["yixin-cao", "zhendong-lei", "shengxin-liu", "hu-qin", "yixiao-huang"],
    },
    {
        "slug": "crypto",
        "title": "密码分析专题",
        "subtitle": "4 位报告人",
        "filename": "06-cryptanalysis-topic-poster.html",
        "ids": ["emanuele-bellini", "chunning-zhou", "xindi-zhang", "yanhong-fan"],
    },
]


def topic_detail_card(speakers: dict[str, dict], sid: str) -> str:
    s = speaker(speakers, sid)
    name = pick(s["name"])
    aff = POSTER_AFF_OVERRIDES.get(sid, pick(s["aff"]))
    title = POSTER_TITLE_OVERRIDES.get(sid, pick(s["title"]))
    abstract = pick(s.get("abstract", {}))
    abstract = "待定" if abstract in {"TBA", "待定"} else abstract
    return f"""<article class="keynote-card">
  <img class="keynote-photo" src="{photo_path(s)}" alt="{esc(name)}" />
  <div>
    <div class="keynote-name-row"><span class="tag">专题报告</span><div class="keynote-name">{esc(name)}</div></div>
    <div class="keynote-aff">{esc(aff)}</div>
    <div class="keynote-talk">{esc(title)}</div>
    <div class="abstract-label">报告摘要</div>
    <div class="abstract">{paragraphs(abstract)}</div>
  </div>
</article>"""


def topic_detail_html(speakers: dict[str, dict], group: dict) -> str:
    cards = "".join(topic_detail_card(speakers, sid) for sid in group["ids"])
    body = f'<div class="keynote-list">{"".join(cards)}</div>'
    return poster_shell(
        group["title"],
        group["subtitle"],
        body,
        TOPIC_DETAIL_CSS,
        f"topic-detail-poster topic-{group['slug']}",
    )


def clean_outputs() -> None:
    for directory in [HTML_DIR, PNG_DIR, JPG_DIR, PDF_DIR, ZIP_DIR, TMP_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
    for directory in [HTML_DIR, PNG_DIR, JPG_DIR, PDF_DIR]:
        for path in directory.iterdir():
            if path.is_file() and path.suffix.lower() in {
                ".html",
                ".png",
                ".jpg",
                ".pdf",
            }:
                path.unlink()


def write_html_files(speakers: dict[str, dict]) -> list[Path]:
    files = [
        ("01-main-poster.html", main_html()),
        ("02-agenda-poster.html", agenda_html(speakers)),
        ("03-keynote-poster.html", keynotes_html(speakers)),
    ]
    files.extend(
        (group["filename"], topic_detail_html(speakers, group))
        for group in TOPIC_GROUPS
    )
    paths = []
    for name, text in files:
        path = HTML_DIR / name
        path.write_text(text, encoding="utf-8")
        paths.append(path)
    return paths


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


def render_html(path: Path, png_out: Path) -> None:
    user_data_dir = TMP_DIR / "chrome-profile"
    if user_data_dir.exists():
        shutil.rmtree(user_data_dir)
    css_height = POSTER_CSS_HEIGHTS.get(path.name, 1920)
    output_size = (POSTER_SIZE[0], css_height * 2)
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
        f"--window-size=1080,{css_height}",
        "--force-device-scale-factor=2",
        f"--screenshot={png_out}",
        html_file_url(path),
    ]
    try:
        subprocess.run(
            cmd,
            check=True,
            timeout=60,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.TimeoutExpired:
        if not png_out.exists() or png_out.stat().st_size == 0:
            raise
    with Image.open(png_out) as img:
        if img.size != output_size:
            img = img.convert("RGB").resize(output_size, Image.Resampling.LANCZOS)
            img.save(png_out, optimize=True)


def copy_main_poster() -> Path:
    src = ROOT / "HCP2026-poster.png"
    dst = PNG_DIR / "01-main-poster.png"
    with Image.open(src) as img:
        img = img.convert("RGB")
        if img.size != POSTER_SIZE:
            img = img.resize(POSTER_SIZE, Image.Resampling.LANCZOS)
        img.save(dst, optimize=True)
    return dst


def export_from_png(png_path: Path) -> tuple[Path, Path]:
    stem = png_path.stem
    jpg_path = JPG_DIR / f"{stem}.jpg"
    pdf_path = PDF_DIR / f"{stem}.pdf"
    with Image.open(png_path) as img:
        rgb = img.convert("RGB")
        jpg_height = round(rgb.height * JPG_SIZE[0] / rgb.width)
        jpg = rgb.resize((JPG_SIZE[0], jpg_height), Image.Resampling.LANCZOS)
        jpg.save(jpg_path, quality=94, optimize=True, progressive=True)
        rgb.save(pdf_path, "PDF", resolution=216)
    return jpg_path, pdf_path


def render_all(html_paths: list[Path]) -> list[Path]:
    pngs = []
    for html_path in html_paths:
        png_path = PNG_DIR / html_path.name.replace(".html", ".png")
        render_html(html_path, png_path)
        pngs.append(png_path)
    for png in pngs:
        export_from_png(png)
    return pngs


def zip_outputs() -> None:
    groups = [
        ("HCP2026-promo-posters-png.zip", PNG_DIR, "*.png"),
        ("HCP2026-promo-posters-jpg.zip", JPG_DIR, "*.jpg"),
        ("HCP2026-promo-posters-pdf.zip", PDF_DIR, "*.pdf"),
    ]
    for zip_name, directory, pattern in groups:
        zip_path = ZIP_DIR / zip_name
        if zip_path.exists():
            zip_path.unlink()
        with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for file in sorted(directory.glob(pattern)):
                zf.write(file, arcname=file.name)


def write_readme() -> None:
    readme = textwrap.dedent(
        """\
        # HCP 2026 Promo Posters

        Generated poster set:

        1. `01-main-poster`
        2. `02-agenda-poster`
        3. `03-keynote-poster`
        4. `04-ai-topic-poster`
        5. `05-combinatorial-optimization-topic-poster`
        6. `06-cryptanalysis-topic-poster`

        The main and agenda posters are 2160 x 3840. Posters with full abstracts
        use extended heights. JPG files are exported at 1080 pixels wide.
        PDF files are single-page posters generated from the high-resolution PNGs.
        """
    )
    (OUT / "README.md").write_text(readme, encoding="utf-8")


def main() -> None:
    clean_outputs()
    ensure_generated_assets()
    speakers = extract_speakers()
    html_paths = write_html_files(speakers)
    supporting_paths = [
        path for path in html_paths if path.name != "01-main-poster.html"
    ]
    pngs = render_all(supporting_paths)
    main_poster = copy_main_poster()
    export_from_png(main_poster)
    pngs.insert(0, main_poster)
    zip_outputs()
    write_readme()
    for path in pngs:
        print(path.relative_to(ROOT))
    for path in sorted(ZIP_DIR.glob("*.zip")):
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
