#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
HTML_DIR = ROOT / "speaker-posters" / "html"
PNG_DIR = ROOT / "speaker-posters" / "png"
TMP_DIR = ROOT / "speaker-posters" / "tmp"

BODY_BG = (19, 7, 16)
BG_TOLERANCE = 3
VIEWPORT = (1080, 5200)

CHROME_CANDIDATES = [
    Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"),
    Path("/Applications/Chromium.app/Contents/MacOS/Chromium"),
    Path("/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"),
]


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


def row_is_body_background(image: Image.Image, y: int) -> bool:
    pixels = image.load()
    width = image.width
    for x in range(0, width, 8):
        rgb = pixels[x, y][:3]
        if any(abs(channel - target) > BG_TOLERANCE for channel, target in zip(rgb, BODY_BG)):
            return False
    return True


def crop_body_padding(path: Path) -> None:
    with Image.open(path) as raw:
        image = raw.convert("RGB")
    top = 0
    while top < image.height and row_is_body_background(image, top):
        top += 1
    bottom = image.height
    while bottom > top and row_is_body_background(image, bottom - 1):
        bottom -= 1
    cropped = image.crop((0, top, image.width, bottom))
    cropped.save(path, optimize=True)


def render_html(html_path: Path, png_path: Path) -> None:
    user_data_dir = TMP_DIR / "chrome-profile"
    if user_data_dir.exists():
        shutil.rmtree(user_data_dir)
    raw_png = TMP_DIR / f"{png_path.stem}.raw.png"
    if raw_png.exists():
        raw_png.unlink()

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
        f"--window-size={VIEWPORT[0]},{VIEWPORT[1]}",
        "--force-device-scale-factor=1",
        f"--screenshot={raw_png}",
        html_file_url(html_path),
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    deadline = time.monotonic() + 90
    last_size = -1
    stable_count = 0
    while time.monotonic() < deadline:
        if raw_png.exists():
            size = raw_png.stat().st_size
            if size > 0 and size == last_size:
                stable_count += 1
            else:
                stable_count = 0
                last_size = size
            if stable_count >= 2:
                break
        if proc.poll() is not None:
            break
        time.sleep(0.25)
    else:
        proc.kill()
        proc.wait(timeout=5)
        raise TimeoutError(f"Chrome timed out while rendering {html_path}")

    if proc.poll() is None:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
            proc.wait(timeout=5)

    if not raw_png.exists() or raw_png.stat().st_size == 0:
        raise subprocess.CalledProcessError(proc.returncode or 1, cmd)
    raw_png.replace(png_path)
    crop_body_padding(png_path)


def main() -> None:
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    for old in PNG_DIR.glob("*.png"):
        old.unlink()

    for html_path in sorted(HTML_DIR.glob("*.html")):
        png_path = PNG_DIR / html_path.name.replace(".html", ".png")
        render_html(html_path, png_path)
        with Image.open(png_path) as image:
            print(f"{png_path.relative_to(ROOT)}\t{image.width}x{image.height}")


if __name__ == "__main__":
    main()
