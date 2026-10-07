#!/usr/bin/env python3
"""A vertical chapter clip (1080 x 1920, YouTube Shorts / Reels) cut from a long film: one chapter in a window, its question
above, the part and the long film below, over a blurred, darkened copy of the same picture (the teaser's frame, teaser.py).

  python3 clip.py --src lf-under-giza.mp4 (or the release URL) --at 33 --to 163 --title "What's hiding|in the *Great Pyramid*?" \
                  --kicker "Under Giza · Part 1 of 4" --foot "Full 11-minute film on the channel" --out lf-under-giza-c1.mp4

--at / --to: where the chapter starts and where the next one starts, in whole seconds as the YouTube chapter list gives them.
The exact cut is found in the sound: a chapter starts on the first word after the long pause that closes the one before
(at least 0.7 s of narrator silence, reel.line_gap), so the clip opens on the chapter's first word and closes in the pause
before the next chapter, with no word cut and no caption of the chapter before.
The title's "|" breaks the line; *stars* set a word in the warm accent; it shrinks to fit two lines.
Prints one JSON line: the cut, the duration, the loudness and the peak.
"""
import argparse, asyncio, base64, html, json, os, re, subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "fonts")
W, H, VW, VH = 1080, 1920, 1080, 760       # the film is scaled to 1351 x 760 and its centre 1080 kept (as the teasers)
VY = 560                                   # top of the film window
SR = 16000


def b64(p):
    return base64.b64encode(open(p, "rb").read()).decode()


# ------------------------------------------------------------------ the cut
def band_db(src, a, d):
    """The narrator's band (300 to 3400 Hz) of the mix from a for d seconds: (times, dB), 10 ms apart."""
    from scipy.signal import butter, sosfiltfilt
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", src, "-vn", "-ac", "1", "-ar", str(SR),
                          "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768.0
    y = sosfiltfilt(butter(4, [300, 3400], btype="band", fs=SR, output="sos"), x)
    hop, win = SR // 100, 3 * SR // 100
    n = max(0, (len(y) - win) // hop)
    e = np.array([np.sqrt(np.mean(y[i * hop:i * hop + win] ** 2)) for i in range(n)])
    return a + (np.arange(n) * hop + win / 2) / SR, 20 * np.log10(e + 1e-9)


def onset(src, T, pre=1.6, post=2.2):
    """The first word of the chapter that YouTube lists at second T (its true start lies in [T, T + 1)): the end of the
    longest narrator pause that ends between T and T + 1.3. Returns (time, pause length) or (None, 0)."""
    a = max(0.0, T - pre)
    t, db = band_db(src, a, pre + post)
    if len(db) < 50:
        return None, 0.0
    # a pause is a stretch with no frame at the voice's level; the music bed and its swells stay well under it
    thr = float(np.clip(np.percentile(db, 85) - 7, -28, -21))
    loud = db > thr
    runs, i, n = [], 0, len(loud)
    while i < n:
        if loud[i]:
            i += 1; continue
        j = i
        while j < n and not loud[j]:
            j += 1
        runs.append((i, j))                       # frames i .. j-1 are quiet; j is the first word's frame
        i = j
    best = None
    for i, j in runs:
        if j >= n:
            continue
        end = float(t[j]); length = float(t[j - 1] - t[i]) + 0.01
        if T - 0.05 <= end <= T + 1.35 and length >= 0.35 and (best is None or length > best[1]):
            best = (end, length)
    return best if best else (None, 0.0)


# ------------------------------------------------------------------ the frame
def overlay_html(a):
    f = lambda n: b64(os.path.join(FONTS, n))
    lines = "".join("<div class='l'>" + re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(x.strip())) + "</div>" for x in a.title.split("|"))
    foot = re.sub(r"\*(.+?)\*", r"<b>\1</b>", html.escape(a.foot))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>
@font-face{{font-family:I;font-weight:700;src:url(data:font/woff2;base64,{f('inter-latin-700-normal.woff2')}) format('woff2')}}
@font-face{{font-family:I;font-weight:600;src:url(data:font/woff2;base64,{f('inter-latin-600-normal.woff2')}) format('woff2')}}
@font-face{{font-family:N;font-weight:500;font-style:italic;src:url(data:font/woff2;base64,{f('newsreader-latin-500-italic.woff2')}) format('woff2')}}
@font-face{{font-family:I;font-weight:700;src:url(data:font/woff2;base64,{f('inter-latin-ext-700-normal.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:I;font-weight:600;src:url(data:font/woff2;base64,{f('inter-latin-ext-600-normal.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
@font-face{{font-family:N;font-weight:500;font-style:italic;src:url(data:font/woff2;base64,{f('newsreader-latin-ext-500-italic.woff2')}) format('woff2');unicode-range:U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF}}
html,body{{margin:0;width:{W}px;height:{H}px;background:transparent;overflow:hidden}}
.top{{position:absolute;left:64px;right:64px;bottom:{H - VY + 54}px;text-align:center}}
.k{{font:600 30px I;letter-spacing:.2em;color:#e8b87a;text-transform:uppercase;margin-bottom:26px}}
.t{{font:700 {a.size}px/1.06 I;color:#fbf6ee;letter-spacing:-.02em;text-shadow:0 6px 30px rgba(0,0,0,.7)}}
.t .l{{white-space:nowrap}}
.t em{{font-style:normal;color:#f2c98e}}
.win{{position:absolute;left:0;top:{VY}px;width:{VW}px;height:{VH}px;box-shadow:0 30px 80px rgba(0,0,0,.6);outline:2px solid rgba(242,201,142,.35)}}
.win:before{{content:'';position:absolute;left:0;right:0;top:0;height:86px;background:linear-gradient(rgba(12,10,8,.93) 0,rgba(12,10,8,.93) 58%,rgba(12,10,8,0) 100%)}}
.win:after{{content:'';position:absolute;left:0;right:0;bottom:0;height:50px;background:linear-gradient(rgba(12,10,8,0) 0,rgba(12,10,8,.93) 42%,rgba(12,10,8,.93) 100%)}}
.n{{position:absolute;left:64px;right:64px;top:{VY + VH + 20}px;text-align:center;font:600 21px I;letter-spacing:.16em;text-transform:uppercase;color:rgba(251,246,238,.5)}}
.bot{{position:absolute;left:64px;right:64px;top:{VY + VH + 92}px;text-align:center}}
.f{{font:600 38px I;color:#fbf6ee;text-shadow:0 4px 20px rgba(0,0,0,.7)}}
.f b{{color:#f2c98e;font-weight:700}}
.m{{margin-top:24px;font:500 34px N;font-style:italic;color:rgba(251,246,238,.85)}}
</style></head><body>
<div class="top"><div class="k">{html.escape(a.kicker)}</div><div class="t">{lines}</div></div>
<div class="win"></div>
<div class="n">{html.escape(a.note)}</div>
<div class="bot"><div class="f">{foot}</div><div class="m">Residual Continuum · Weigh it yourself.</div></div>
<script>
const t=document.querySelector('.t'), box=document.querySelector('.top').clientWidth; let s={a.size};
const wide=()=>Math.max(...[...t.querySelectorAll('.l')].map(l=>l.scrollWidth));
while(s>60 && wide()>box){{ s-=2; t.style.fontSize=s+'px'; }}
document.body.dataset.size=s;
</script>
</body></html>"""


async def overlay_png(a, out):
    from playwright.async_api import async_playwright
    tmp = out + ".html"
    open(tmp, "w", encoding="utf-8").write(overlay_html(a))
    async with async_playwright() as pw:
        br = await pw.chromium.launch(args=["--no-sandbox"])
        pg = await br.new_page(viewport={"width": W, "height": H})
        await pg.goto("file://" + tmp)
        await pg.wait_for_timeout(500)
        size = await pg.evaluate("document.body.dataset.size")
        await pg.screenshot(path=out, omit_background=True)
        await br.close()
    os.remove(tmp)
    return int(size or a.size)


def loudness(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True)
    i = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr); p = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)
    return (float(i[-1]) if i else None), (float(p[-1]) if p else None)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--src", required=True)
    p.add_argument("--at", type=float, required=True, help="the chapter's listed start (s)")
    p.add_argument("--to", type=float, required=True, help="the next chapter's listed start (s)")
    p.add_argument("--title", required=True); p.add_argument("--kicker", required=True)
    p.add_argument("--foot", default="Full film on the *channel*")
    p.add_argument("--note", default="Schematic reconstruction · sources in the description")
    p.add_argument("--size", type=int, default=96)
    p.add_argument("--out", required=True)
    p.add_argument("--max", type=float, default=0, help="test: stop after this many seconds")
    p.add_argument("--preset", default=os.environ.get("RC_PRESET", "medium"))
    a = p.parse_args()
    s0, g0 = onset(a.src, a.at)
    s1, g1 = onset(a.src, a.to)
    start = (s0 - 0.05) if s0 else a.at + 0.45
    end = (s1 - 0.15) if s1 else a.to + 0.2
    d = end - start
    assert 3 < d < 179, ("clip length", d)
    if a.max:
        d = min(d, a.max)
    png = os.path.abspath(a.out) + ".overlay.png"
    size = asyncio.run(overlay_png(a, png))
    fi, fo = 0.25, 0.45
    # the blurred backdrop is made at a quarter size (the same look as the teasers' boxblur=28 at full size, 16 times less work)
    vf = (f"[0:v]split[a][b];[a]scale=-2:{H // 4},crop={W // 4}:{H // 4},boxblur=7:2,scale={W}:{H},eq=brightness=-0.22:saturation=0.85[bg];"
          f"[b]scale=-2:{VH},crop={VW}:{VH}[fg];[bg][fg]overlay=0:{VY}[v1];[v1][1:v]overlay=0:0,"
          f"fade=t=in:st=0:d={fi},fade=t=out:st={d - fo:.3f}:d={fo},format=yuv420p[v]")
    af = f"afade=t=in:st=0:d=0.05,afade=t=out:st={d - fo:.3f}:d={fo},alimiter=limit=0.89:attack=0.5:release=30:level=disabled"
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-t", f"{d:.3f}", "-i", a.src, "-i", png,
           "-filter_complex", vf, "-map", "[v]", "-map", "0:a", "-af", af,
           "-c:v", "libx264", "-preset", a.preset, "-crf", "21", "-maxrate", "4500k", "-bufsize", "9000k", "-g", "60", "-r", "30",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart", a.out]
    subprocess.run(cmd, check=True)
    os.remove(png)
    li, pk = loudness(a.out)
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", a.out],
                               capture_output=True, text=True).stdout.strip() or 0)
    print(json.dumps({"out": os.path.basename(a.out), "start": round(start, 3), "end": round(end, 3), "dur": round(dur, 2),
                      "found": [bool(s0), bool(s1)], "pauses": [round(g0, 2), round(g1, 2)], "title_px": size,
                      "lufs": li, "peak": pk, "bytes": os.path.getsize(a.out)}), flush=True)


if __name__ == "__main__":
    main()
