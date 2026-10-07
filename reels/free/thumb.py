#!/usr/bin/env python3
"""YouTube thumbnail (1280 x 720 JPEG) for a long film: a frame of the film, a big title, an optional verdict chip.

  python3 thumb.py --img frame.png --kicker "Deep dive" --title "What's really|*under* Giza?" --side right --out thumb.jpg
                   [--verdict "Mixed record" --vcol "#d8c7a8"] [--size 92]

The title's "|" breaks the line; words wrapped in *stars* are set in the warm accent. Fonts are the films' own (Inter, Newsreader).
Crop the frame first so the HUD (top ~11%) and the captions (bottom ~20%) are not in it.
"""
import argparse, asyncio, base64, html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


def page(a):
    img = b64(a.img)
    mime = "image/png" if a.img.lower().endswith(".png") else "image/jpeg"
    f = lambda n: b64(os.path.join(FONTS, n))
    lines = []
    for ln in a.title.split("|"):
        t = html.escape(ln.strip())
        t = re.sub(r"\*(.+?)\*", r"<em>\1</em>", t)
        lines.append(f"<div>{t}</div>")
    right = a.side == "right"
    grad = ("linear-gradient(270deg, rgba(14,10,8,.92) 0%, rgba(14,10,8,.72) 38%, rgba(14,10,8,0) 66%)" if right else
            "linear-gradient(90deg, rgba(14,10,8,.92) 0%, rgba(14,10,8,.72) 38%, rgba(14,10,8,0) 66%)")
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:I;font-weight:700;src:url(data:font/woff2;base64,{f('inter-latin-700-normal.woff2')}) format('woff2')}}
@font-face{{font-family:I;font-weight:600;src:url(data:font/woff2;base64,{f('inter-latin-600-normal.woff2')}) format('woff2')}}
@font-face{{font-family:N;font-weight:500;font-style:italic;src:url(data:font/woff2;base64,{f('newsreader-latin-500-italic.woff2')}) format('woff2')}}
@font-face{{font-family:I;font-weight:700;src:url(data:font/woff2;base64,{f('inter-latin-ext-700-normal.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:I;font-weight:600;src:url(data:font/woff2;base64,{f('inter-latin-ext-600-normal.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:N;font-weight:500;font-style:italic;src:url(data:font/woff2;base64,{f('newsreader-latin-ext-500-italic.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
html,body{{margin:0;width:1280px;height:720px;overflow:hidden;background:#120d0a}}
.bg{{position:absolute;inset:0;background:url(data:{mime};base64,{img}) center/cover no-repeat;filter:saturate(1.15) contrast(1.06)}}
.sh{{position:absolute;inset:0;background:{grad}}}
.vg{{position:absolute;inset:0;box-shadow:inset 0 0 160px rgba(0,0,0,.55)}}
.box{{position:absolute;top:0;bottom:0;{'right' if right else 'left'}:64px;width:640px;display:flex;flex-direction:column;justify-content:center;
      align-items:{'flex-end' if right else 'flex-start'};text-align:{'right' if right else 'left'}}}
.k{{font:600 26px I;letter-spacing:.2em;color:#e8b87a;text-transform:uppercase;margin-bottom:18px}}
.t{{font:700 {a.size}px/1.0 I;color:#fbf6ee;letter-spacing:-.02em;text-shadow:0 4px 28px rgba(0,0,0,.65)}}
.t em{{font-style:normal;color:#f2c98e}}
.v{{margin-top:30px;font:600 28px I;color:{a.vcol};border:3px solid {a.vcol};border-radius:999px;padding:8px 26px;background:rgba(14,10,8,.55)}}
.m{{position:absolute;{'left' if right else 'right'}:34px;bottom:28px;font:500 24px N;font-style:italic;color:rgba(251,246,238,.82);text-shadow:0 2px 12px rgba(0,0,0,.8)}}
</style></head><body><div class="bg"></div><div class="sh"></div><div class="vg"></div>
<div class="box"><div class="k">{html.escape(a.kicker)}</div><div class="t">{''.join(lines)}</div>
{f'<div class="v">{html.escape(a.verdict)}</div>' if a.verdict else ''}</div>
<div class="m">Residual Continuum</div></body></html>"""


async def shoot(a):
    from playwright.async_api import async_playwright
    tmp = os.path.abspath(a.out) + ".html"
    open(tmp, "w", encoding="utf-8").write(page(a))
    async with async_playwright() as pw:
        exe = os.environ.get("RC_CHROME") or None
        br = await (pw.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else pw.chromium.launch(args=["--no-sandbox"]))
        pg = await br.new_page(viewport={"width": 1280, "height": 720})
        await pg.goto("file://" + tmp)
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=a.out, type="jpeg", quality=90)
        await br.close()
    os.remove(tmp)
    print(a.out, os.path.getsize(a.out), "bytes")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--img", required=True); p.add_argument("--title", required=True); p.add_argument("--kicker", default="Deep dive")
    p.add_argument("--verdict", default=""); p.add_argument("--vcol", default="#d8c7a8"); p.add_argument("--side", default="left")
    p.add_argument("--size", type=int, default=92); p.add_argument("--out", required=True)
    asyncio.run(shoot(p.parse_args()))
