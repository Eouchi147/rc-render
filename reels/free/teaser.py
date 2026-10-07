#!/usr/bin/env python3
"""A vertical teaser (1080 x 1920, YouTube Shorts / Reels) cut from a long film: the film's cold open in a window, a big
question above it, "Full deep dive on the channel" below, over a blurred, darkened copy of the same picture.

  python3 teaser.py --src lf-under-giza.mp4 (or the release URL) --end 33.5 --title "What's really|*under* Giza?" \
                    --kicker "Deep dive" --foot "Full 11-minute film on the channel" --out teaser.mp4

--end: where the teaser stops (just after the film's title card appears: the first chapter's start time is a good cut).
The title's "|" breaks the line; *stars* set a word in the warm accent. Fonts are the films' own (Inter, Newsreader).
"""
import argparse, asyncio, base64, html, os, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
W, H, VW, VH = 1080, 1920, 1080, 760       # the film is scaled to 1351 x 760 and its centre 1080 kept
VY = 560                                   # top of the film window


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


def overlay_html(a):
    f = lambda n: b64(os.path.join(FONTS, n))
    lines = "".join("<div>" + re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(x.strip())) + "</div>" for x in a.title.split("|"))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:I;font-weight:700;src:url(data:font/woff2;base64,{f('inter-latin-700-normal.woff2')}) format('woff2')}}
@font-face{{font-family:I;font-weight:600;src:url(data:font/woff2;base64,{f('inter-latin-600-normal.woff2')}) format('woff2')}}
@font-face{{font-family:N;font-weight:500;font-style:italic;src:url(data:font/woff2;base64,{f('newsreader-latin-500-italic.woff2')}) format('woff2')}}
@font-face{{font-family:I;font-weight:700;src:url(data:font/woff2;base64,{f('inter-latin-ext-700-normal.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:I;font-weight:600;src:url(data:font/woff2;base64,{f('inter-latin-ext-600-normal.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:N;font-weight:500;font-style:italic;src:url(data:font/woff2;base64,{f('newsreader-latin-ext-500-italic.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
html,body{{margin:0;width:{W}px;height:{H}px;background:transparent;overflow:hidden}}
.top{{position:absolute;left:70px;right:70px;bottom:{H - VY + 56}px;text-align:center}}
.k{{font:600 30px I;letter-spacing:.22em;color:#e8b87a;text-transform:uppercase;margin-bottom:26px}}
.t{{font:700 {a.size}px/1.04 I;color:#fbf6ee;letter-spacing:-.02em;text-shadow:0 6px 30px rgba(0,0,0,.7)}}
.t em{{font-style:normal;color:#f2c98e}}
.win{{position:absolute;left:0;top:{VY}px;width:{VW}px;height:{VH}px;box-shadow:0 30px 80px rgba(0,0,0,.6);outline:2px solid rgba(242,201,142,.35)}}
.bot{{position:absolute;left:70px;right:70px;top:{VY + VH + 70}px;text-align:center}}
.f{{font:600 38px I;color:#fbf6ee;text-shadow:0 4px 20px rgba(0,0,0,.7)}}
.f b{{color:#f2c98e;font-weight:700}}
.m{{margin-top:26px;font:500 34px N;font-style:italic;color:rgba(251,246,238,.85)}}
</style></head><body>
<div class="top"><div class="k">{html.escape(a.kicker)}</div><div class="t">{lines}</div></div>
<div class="win"></div>
<div class="bot"><div class="f">{re.sub(r"\*(.+?)\*", r"<b>\1</b>", html.escape(a.foot))}</div><div class="m">Residual Continuum · Weigh it yourself.</div></div>
</body></html>"""


async def overlay_png(a, out):
    from playwright.async_api import async_playwright
    tmp = out + ".html"
    open(tmp, "w", encoding="utf-8").write(overlay_html(a))
    async with async_playwright() as pw:
        br = await pw.chromium.launch(args=["--no-sandbox"])
        pg = await br.new_page(viewport={"width": W, "height": H})
        await pg.goto("file://" + tmp)
        await pg.wait_for_timeout(400)
        await pg.screenshot(path=out, omit_background=True)
        await br.close()
    os.remove(tmp)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True); p.add_argument("--end", type=float, required=True); p.add_argument("--start", type=float, default=0)
    p.add_argument("--title", required=True); p.add_argument("--kicker", default="Deep dive")
    p.add_argument("--foot", default="Full deep dive on the *channel*"); p.add_argument("--size", type=int, default=96)
    p.add_argument("--out", required=True)
    a = p.parse_args()
    png = os.path.abspath(a.out) + ".overlay.png"
    asyncio.run(overlay_png(a, png))
    d = a.end - a.start
    fo = max(0.0, d - 0.6)
    vf = (f"[0:v]split[a][b];[a]scale=-2:{H},crop={W}:{H},boxblur=28:2,eq=brightness=-0.22:saturation=0.85[bg];"
          f"[b]scale=-2:{VH},crop={VW}:{VH}[fg];[bg][fg]overlay=0:{VY}[v1];[v1][1:v]overlay=0:0,fade=t=in:st=0:d=0.3,fade=t=out:st={fo:.2f}:d=0.6,format=yuv420p[v]")
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a.start}", "-t", f"{d:.3f}", "-i", a.src, "-i", png,
           "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-af", f"afade=t=out:st={fo:.2f}:d=0.6",
           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", "30", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    os.remove(png)
    print(a.out, os.path.getsize(a.out), "bytes,", f"{d:.1f} s")


if __name__ == "__main__":
    main()
