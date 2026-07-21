#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "speaker-posters"
HTML_DIR = OUT / "html"

POSTER_ORDER = [
    "yuhong-dai",
    "naijun-zhan",
    "xiaoming-sun",
    "qilong-feng",
    "mingxuan-yuan",
    "zhaoguo-wang",
    "min-li",
    "yixin-cao",
    "zhendong-lei",
    "shengxin-liu",
    "hu-qin",
    "yixiao-huang",
    "emanuele-bellini",
    "chunning-zhou",
    "xindi-zhang",
    "yanhong-fan",
]

KEYNOTE_IDS = {"yuhong-dai", "naijun-zhan", "xiaoming-sun", "qilong-feng"}

TOPIC_LABELS = {
    "mingxuan-yuan": "人工智能专题",
    "zhaoguo-wang": "人工智能专题",
    "min-li": "人工智能专题",
    "yixin-cao": "组合优化专题",
    "zhendong-lei": "组合优化专题",
    "shengxin-liu": "组合优化专题",
    "hu-qin": "组合优化专题",
    "yixiao-huang": "组合优化专题",
    "emanuele-bellini": "密码分析专题",
    "chunning-zhou": "密码分析专题",
    "xindi-zhang": "密码分析专题",
    "yanhong-fan": "密码分析专题",
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
    return value.strip()


def paragraphs(value: str) -> str:
    value = normalize_text(value) or "待定"
    chunks = [part.strip() for part in re.split(r"\n\s*\n", value) if part.strip()]
    if not chunks:
        chunks = [value]
    return "\n".join(f"<p>{esc(part)}</p>" for part in chunks)


def label_for(key: str) -> str:
    if key in KEYNOTE_IDS:
        return "KEYNOTE 特邀报告"
    return TOPIC_LABELS.get(key, "专题报告")


CSS = """
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; background: #130710; }
body {
  display: flex;
  justify-content: center;
  padding: 32px 0;
  color: #fff;
  font-family: "Noto Sans SC", "PingFang SC", "Microsoft YaHei", Arial, sans-serif;
}
.poster {
  position: relative;
  width: 1080px;
  min-height: 1920px;
  overflow: hidden;
  background:
    linear-gradient(180deg, rgba(42, 29, 69, .90) 0%, rgba(92, 35, 55, .88) 44%, rgba(80, 4, 18, .96) 100%),
    url("../../assets/sdu-qingdao-library-hero.jpg") center / cover no-repeat;
  box-shadow: 0 22px 80px rgba(0,0,0,.38);
}
.poster::before {
  content: "";
  position: absolute;
  inset: 0;
  background:
    radial-gradient(circle at 22% 16%, rgba(255, 226, 163, .18), transparent 30%),
    linear-gradient(180deg, rgba(12, 9, 26, .18), rgba(63, 4, 16, .46));
  pointer-events: none;
}
.top-rule {
  position: absolute;
  inset: 0 0 auto 0;
  height: 14px;
  background: linear-gradient(90deg, #a71930, #d8b15f);
}
.inner {
  position: relative;
  z-index: 1;
  padding: 82px 78px 62px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 22px;
  color: rgba(255,255,255,.90);
}
.brand img {
  width: 252px;
  height: auto;
  filter: brightness(0) invert(1);
}
.brand .tag {
  margin-left: auto;
  color: #f7dfaa;
  font-size: 22px;
  font-weight: 800;
  letter-spacing: 8px;
}
.event {
  margin-top: 72px;
}
.event .kicker {
  color: #f7dfaa;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 16px;
}
.event h1 {
  margin: 24px 0 0;
  font-family: Georgia, "Times New Roman", serif;
  font-size: 132px;
  line-height: .92;
  letter-spacing: 4px;
}
.event .subtitle {
  margin-top: 22px;
  font-size: 33px;
  font-weight: 800;
  line-height: 1.35;
}
.event .en {
  margin-top: 10px;
  max-width: 780px;
  color: rgba(255,255,255,.78);
  font-size: 20px;
  line-height: 1.45;
}
.speaker-head {
  display: grid;
  grid-template-columns: 272px minmax(0, 1fr);
  gap: 34px;
  margin-top: 66px;
  align-items: start;
}
.photo {
  width: 272px;
  aspect-ratio: 4 / 5;
  object-fit: cover;
  object-position: center 48%;
  border: 1px solid rgba(255,255,255,.24);
  border-radius: 16px;
  box-shadow: 0 16px 44px rgba(0,0,0,.36);
}
.speaker-info {
  padding-top: 6px;
}
.speaker-info .label {
  display: inline-flex;
  padding: 8px 14px;
  color: #fff;
  background: #a71930;
  border-radius: 6px;
  font-size: 17px;
  font-weight: 800;
  letter-spacing: 3px;
}
.speaker-info h2 {
  margin: 18px 0 0;
  font-size: 52px;
  line-height: 1.16;
}
.aff {
  margin-top: 12px;
  color: rgba(255,255,255,.76);
  font-size: 22px;
  font-weight: 700;
  line-height: 1.45;
}
.title-box {
  margin-top: 26px;
  padding: 22px 26px;
  background: rgba(255,255,255,.10);
  border-left: 7px solid #f7dfaa;
  border-radius: 0 12px 12px 0;
}
.title-box .lab {
  color: #f7dfaa;
  font-size: 15px;
  font-weight: 900;
  letter-spacing: 4px;
}
.title-box .title {
  margin-top: 10px;
  color: #fff;
  font-size: 30px;
  font-weight: 900;
  line-height: 1.38;
}
.section {
  margin-top: 46px;
}
.section-head {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 18px;
}
.section-head .cn {
  color: #fff;
  font-size: 30px;
  font-weight: 900;
}
.section-head .en {
  color: rgba(255,255,255,.52);
  font-size: 16px;
  font-weight: 800;
  letter-spacing: 5px;
  text-transform: uppercase;
}
.section-head::after {
  content: "";
  flex: 1;
  height: 1px;
  background: rgba(255,255,255,.22);
}
.prose {
  color: rgba(255,255,255,.92);
  font-size: 22px;
  line-height: 1.9;
  text-align: justify;
}
.prose p { margin: 0 0 14px; }
.bio-card {
  padding: 24px 28px;
  background: rgba(255,255,255,.08);
  border: 1px solid rgba(255,255,255,.16);
  border-radius: 16px;
}
.footer {
  position: relative;
  z-index: 1;
  margin-top: 54px;
  padding: 30px 78px 44px;
  border-top: 1px solid rgba(255,255,255,.20);
  text-align: center;
}
.footer .meta {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
  color: #f7dfaa;
  font-size: 20px;
  font-weight: 800;
}
.footer .url {
  margin-top: 12px;
  color: rgba(255,255,255,.86);
  font-size: 20px;
  font-family: Georgia, "Times New Roman", serif;
  font-weight: 800;
  letter-spacing: 2px;
}
"""


def poster_html(index: int, key: str, speaker: dict) -> str:
    name = pick(speaker["name"])
    aff = pick(speaker["aff"])
    title = pick(speaker["title"])
    abstract = pick(speaker.get("abstract", {}))
    bio = pick(speaker.get("bio", {}))
    photo = "../../" + speaker["photo"]
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>HCP 2026 · {esc(name)}</title>
  <style>{CSS}</style>
</head>
<body>
  <article class="poster">
    <div class="top-rule"></div>
    <div class="inner">
      <header class="brand">
        <img src="../../assets/sdu-logo.svg" alt="山东大学" />
        <div class="tag">报告海报</div>
      </header>

      <section class="event">
        <div class="kicker">第 九 届</div>
        <h1>HCP 2026</h1>
        <div class="subtitle">难解问题的理论、算法与应用研讨会</div>
      </section>

      <section class="speaker-head">
        <img class="photo" src="{photo}" alt="{esc(name)}" />
        <div class="speaker-info">
          <div class="label">{esc(label_for(key))}</div>
          <h2>{esc(name)}</h2>
          <div class="aff">{esc(aff)}</div>
          <div class="title-box">
            <div class="lab">报告题目</div>
            <div class="title">{esc(title)}</div>
          </div>
        </div>
      </section>

      <section class="section">
        <div class="section-head"><span class="cn">报告摘要</span></div>
        <div class="prose">{paragraphs(abstract)}</div>
      </section>

      <section class="section">
        <div class="section-head"><span class="cn">个人简介</span></div>
        <div class="bio-card"><div class="prose">{paragraphs(bio)}</div></div>
      </section>
    </div>
    <footer class="footer">
      <div class="meta"><span>2026.07.31 – 08.02</span><span>山东大学青岛校区</span></div>
      <div class="url">hcp2026.sincst.cn</div>
    </footer>
  </article>
</body>
</html>
"""


def main() -> None:
    HTML_DIR.mkdir(parents=True, exist_ok=True)
    for old in HTML_DIR.glob("*.html"):
        old.unlink()
    speakers = extract_speakers()
    for idx, key in enumerate(POSTER_ORDER, 1):
        speaker = speakers[key]
        name = pick(speaker["name"])
        path = HTML_DIR / f"{idx:02d}-{name}-{key}.html"
        path.write_text(poster_html(idx, key, speaker), encoding="utf-8")
        print(path)


if __name__ == "__main__":
    main()
