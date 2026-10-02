import os
"""Stills of every shot of a film page, fully built, as one contact sheet (fast visual QA without audio)."""
import asyncio, os, sys
from playwright.async_api import async_playwright
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "free", "fonts")
FF = "".join(f"@font-face{{font-family:'{fam}';font-style:{st};font-weight:{wt};src:url('file://{FONTS}/{fn}')}}" for fam, st, wt, fn in [
    ("Newsreader", "normal", 400, "newsreader-latin-400-normal.woff2"), ("Newsreader", "italic", 400, "newsreader-latin-400-italic.woff2"),
    ("Newsreader", "normal", 500, "newsreader-latin-500-normal.woff2"), ("Inter", "normal", 400, "inter-latin-400-normal.woff2"),
    ("Inter", "normal", 600, "inter-latin-600-normal.woff2"), ("Inter", "normal", 700, "inter-latin-700-normal.woff2")])


async def main(ids, wait=int(os.environ.get("RC_WAIT", "2600"))):
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for sid in ids:
            path = f"{os.environ.get('RC_FILMS_OUT') or HERE + '/out'}/{sid}.html"
            land = '"aspect":"16:9"' in open(path, encoding="utf-8").read(6000)      # a long film (16:9): a landscape viewport
            vw, vh = (960, 540) if land else (540, 960)
            pg = await b.new_page(viewport={"width": vw, "height": vh}, device_scale_factor=float(os.environ.get("RC_DPR", "1")))
            errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
            await pg.goto(f"file://{path}")
            await pg.add_style_tag(content=FF)
            await pg.wait_for_timeout(400)
            n = await pg.evaluate(f"SY.keys('{sid}').length")
            await pg.evaluate(f"window.scrollTo(0,SY.keys('{sid}')[0]+4)")
            ims = []
            for i in range(n):
                await pg.evaluate(f"SY.film('{sid}',{i});SY.snap('{sid}')")
                await pg.wait_for_timeout(wait)
                f = f"/tmp/claude-0/pv_{sid}_{i}.png"; await pg.screenshot(path=f); ims.append(f)
            if errs: print(sid, "ERRORS", errs[:3])
            cols = min(n, 5); rows = (n + cols - 1) // cols
            tw, th = (480, 270) if land else (270, 480)
            sheet = Image.new("RGB", (cols * tw, rows * th), "black")
            for i, f in enumerate(ims):
                im = Image.open(f).resize((tw, th)); sheet.paste(im, ((i % cols) * tw, (i // cols) * th))
            sheet.save(f"/tmp/claude-0/sheet_{sid}.png"); print("sheet", sid, n)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
