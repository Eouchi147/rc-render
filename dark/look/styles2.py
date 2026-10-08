"""Second pass on the looks: per-object ink and print logic."""
import math
import numpy as np
import cv2
from core import (base_render, make_particles, draw_particles, luminance, fbm, value_noise, smoothstep, rng, paste,
                  sky_render, bloom, godrays, dof, chroma, vignette, grain, anamorphic, flare_ghosts, filmic,
                  edges_from_id, DW, DH)
import styles as S1
from styles import paper, hatch_angle_map, stripes, emissive_mask, lens_cine, gold_leaf, cloud_band

HZ = dict(bamberg=0.56, zong=0.545, arabia=0.69, kleidion=0.6)
MOOD_SKY = dict(night=0.9, storm=0.7, dusk=0.35)


def item_masks(buf, sc):
    for idx, it in sorted(enumerate(sc.items), key=lambda t: (t[1].z, t[0])):
        if idx in buf['masks']:
            yield idx, it, buf['masks'][idx]


def col_lum(c):
    c = np.asarray(c, np.float32)
    return float(c[0] * 0.2126 + c[1] * 0.7152 + c[2] * 0.0722)


def band_of(m, w):
    k = max(1, int(round(w)))
    er = cv2.erode(m, np.ones((2 * k + 1, 2 * k + 1), np.uint8))
    return np.clip(m - er, 0, 1)


# ================================================================== 1. INK SCROLL (sumi-e)
def style_ink(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    sky = sky_render(sc, W, H, S)
    sl = luminance(sky)
    hz = HZ.get(sc.name, 0.6)
    yy = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    skyD = np.clip(1 - sl / (np.percentile(sl, 99.5) + 1e-6), 0, 1) ** 0.9
    mist = smoothstep(hz + 0.02, hz - 0.22, yy)
    skyD = smoothstep(0.05, 0.95, skyD) * (0.1 + 0.9 * mist) * MOOD_SKY.get(sc.mood, 0.6)
    D = skyD.astype(np.float32).copy()
    C = np.zeros((H, W), np.float32)
    texn = fbm(H, W, 30 * S + 1, 4, 201)
    wetn = fbm(H, W, 90 * S + 1, 4, 202)
    for idx, it, (x0, y0, m) in item_masks(buf, sc):
        sl_ = paste(D, x0, y0, m)
        if sl_ is None:
            continue
        (dy, dx), (sy_, sx_) = sl_
        a = m[sy_, sx_] * min(1.0, it.alpha * (1.6 if it.mat in ('smoke', 'rain') else 1.0))
        if it.mat in ('smoke', 'rain'):
            a = a * 0.5
        lc = col_lum(it.col)
        tone = np.clip(1.12 - lc * 1.55, 0.05, 0.97)
        if it.mat in ('window',) and it.emit <= 0:
            tone = 0.97
        if it.emit > 0:
            tone = 0.0
        if it.mat in ('figure', 'animal'):
            tone = 0.82
        tone *= 0.3 + 0.7 * smoothstep(0.0, 0.85, it.z)
        ys = (np.arange(dy.start, dy.stop, dtype=np.float32) / S)[:, None]
        bx0, by0, bx1, by1 = it.bbox()
        if it.z < 0.8 and it.mat not in ('window', 'fire', 'figure', 'animal', 'metal', 'rope', 'water', 'foam', 'glint'):
            span = max(by1 - by0, 1)
            f = smoothstep(by1 - span * 0.05, by1 - span * 0.6, ys)
            tm = tone * (0.08 + 0.92 * f)
        else:
            tm = np.full((dy.stop - dy.start, 1), tone, np.float32)
        tm = tm * (0.8 + 0.4 * texn[dy, dx]) * (0.85 + 0.3 * wetn[dy, dx])
        D[dy, dx] = D[dy, dx] * (1 - a) + tm * a
        if it.outline and it.z > 0.22 and it.emit <= 0 and it.mat not in ('water', 'rain', 'smoke', 'glint'):
            wpx = (0.5 + 1.6 * it.z) * S * (0.8 if it.mat in ('figure', 'animal') else 1.3)
            bandf = band_of(m, wpx)
            if it.mat in ('ground', 'sand', 'road', 'mountain', 'stone', 'roofs', 'foliage') and it.name not in ('portal_frame', 'niche', 'cartouche'):
                k_ = max(2, int(4 * S))
                above = np.zeros_like(m)
                above[k_:] = m[:-k_]
                bandf = bandf * (above < 0.5)
            band = bandf[sy_, sx_]
            C[dy, dx] = np.maximum(C[dy, dx], band * (0.35 + 0.65 * it.z))
        if it.detail and it.emit <= 0:
            k_ = 0.3 if it.mat in ('water', 'foam', 'sand', 'grass') else 1.0
            C[dy, dx] = np.maximum(C[dy, dx], a * (0.5 + 0.5 * it.z) * k_)
    # washes: dried edges, brush grain, bleed
    edge = np.clip(D - cv2.GaussianBlur(D, (0, 0), 2.5 * S + 0.5), 0, 1)
    D = np.clip(D + edge * 0.9, 0, 1)
    ang = hatch_angle_map(buf, sc, 0)
    streak = stripes(H, W, ang, 4.5 * S + 0.8, warp=2.5, seed=203, S=S)
    D = D * (0.88 + 0.16 * streak)
    dry = value_noise(H, W, 26 * S + 1, 204, cy=2.5 * S + 0.5)
    brk = smoothstep(0.12, 0.4, value_noise(H, W, 7 * S + 1, 205, cy=7 * S + 1) * 0.6 + dry * 0.6)
    C = cv2.GaussianBlur(C * brk, (0, 0), 0.6 * S + 0.2)
    fibre = fbm(H, W, 5 * S + 1, 3, 206)
    bleed = cv2.GaussianBlur(D, (0, 0), 1.4 * S + 0.3)
    D = np.maximum(D, bleed * smoothstep(0.45, 0.8, fibre))
    parts = make_particles(sc)
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0r, y0r, x1r, y1r, a_, z) in parts['rain'][::3]:
            cv2.line(rl, (int(x0r * S * 16), int(y0r * S * 16)), (int(x1r * S * 16), int(y1r * S * 16)), float(a_ * 1.3), 1, cv2.LINE_AA, 4)
        C = np.maximum(C, rl * 0.6)
    if parts['embers']:
        pass
    total = np.clip(D * 0.92 + C * 0.95, 0, 1)
    pap = paper(H, W, (0.95, 0.92, 0.85), fiber=0.07, mottle=0.05, S=S, seed=207)
    inkcol = np.array([0.08, 0.075, 0.07], np.float32)
    out = pap * (1 - total[..., None]) + inkcol * pap * total[..., None] * 1.1
    # vermilion: fire, lit windows, and the sun as a red disc
    em = emissive_mask(buf)
    warm = np.clip(cv2.GaussianBlur(em, (0, 0), 1.5 * S + 0.3) * 1.3, 0, 1)
    halo = np.zeros((H, W), np.float32)
    yy2, xx2 = np.mgrid[0:H, 0:W].astype(np.float32)
    for l in sc.lights:
        d2 = ((xx2 - l.x * S) ** 2 + (yy2 - l.y * S) ** 2) / (l.r * 0.7 * S) ** 2
        halo = np.maximum(halo, np.exp(-d2) * min(l.I, 1.5) * 0.45)
    red = np.array([0.8, 0.22, 0.12], np.float32)
    goldc = np.array([0.86, 0.62, 0.3], np.float32)
    out = out * (1 - halo[..., None] * 0.5) + goldc * pap * halo[..., None] * 0.5
    out = out * (1 - warm[..., None]) + red * pap * warm[..., None]
    if sc.mood == 'dusk' and sc.sun is not None:
        disc = np.zeros((H, W), np.float32)
        cv2.circle(disc, (int(sc.sun[0] * S * 16), int(sc.sun[1] * S * 16)), int(54 * S * 16), 1.0, -1, cv2.LINE_AA, 4)
        disc *= (buf['depth'] < 0.07) * (0.85 + 0.15 * fbm(H, W, 12 * S + 1, 3, 208))
        out = out * (1 - disc[..., None] * 0.9) + red * pap * disc[..., None] * 0.9
    # gold mist bands, feathered
    gold = gold_leaf(H, W, S, seed=209) * np.array([0.9, 0.86, 0.78], np.float32)
    bands = dict(bamberg=[(330, 90, 51), (1585, 110, 52)], zong=[(205, 80, 53), (1560, 105, 54)],
                 arabia=[(1220, 80, 55), (1800, 110, 56)], kleidion=[(205, 80, 57), (1520, 95, 58)]).get(sc.name, [])
    for (y, h, s_) in bands:
        mb = cloud_band(H, W, S, y, h, s_)
        mb = mb * 0.94
        out = out * (1 - mb[..., None]) + gold * mb[..., None]
        e2 = np.clip(mb - cv2.erode(mb, np.ones((3, 3), np.uint8)), 0, 1)
        out *= (1 - cv2.GaussianBlur(e2, (0, 0), 0.8 * S + 0.3) * 0.45)[..., None]
    # mounting: silk borders with a gold thread
    bw = int(26 * S)
    silk = np.array([0.25, 0.3, 0.34], np.float32) * (0.9 + 0.2 * value_noise(H, W, 3 * S + 1, 210, cy=40 * S + 1))[..., None]
    for x_a, x_b in ((0, bw), (W - bw, W)):
        out[:, x_a:x_b] = silk[:, x_a:x_b]
    out[:, bw:bw + max(1, int(2 * S))] = np.array([0.8, 0.64, 0.33], np.float32)
    out[:, W - bw - max(1, int(2 * S)):W - bw] = np.array([0.8, 0.64, 0.33], np.float32)
    # seal
    sx, sy, ss = int(905 * S), int(1745 * S), int(60 * S)
    seal = np.zeros((H, W), np.float32)
    cv2.rectangle(seal, (sx, sy), (sx + ss, sy + ss), 1.0, -1)
    cut = np.zeros((H, W), np.float32)
    t = max(1, int(5 * S))
    cv2.rectangle(cut, (sx + ss // 5, sy + ss // 5), (sx + ss - ss // 5, sy + ss - ss // 5), 1.0, t)
    cv2.line(cut, (sx + ss // 2, sy + ss // 5), (sx + ss // 2, sy + ss - ss // 5), 1.0, t)
    cv2.line(cut, (sx + ss // 5, sy + ss // 2), (sx + ss // 2, sy + ss // 2), 1.0, t)
    seal = seal * (1 - cut) * (0.7 + 0.3 * (value_noise(H, W, 2.5 * S + 0.5, 211) > 0.3))
    out = out * (1 - seal[..., None] * 0.85) + np.array([0.74, 0.15, 0.1], np.float32) * seal[..., None] * 0.85
    return np.clip(out, 0, 1)


# ================================================================== 3. WOODCUT CHRONICLE
def style_woodcut(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    lit = buf['img'].copy()
    def norm(v):
        lo, hi = np.percentile(v, 2), np.percentile(v, 99.6)
        return np.clip((v - lo) / (hi - lo + 1e-6), 0, 1)
    t = 0.55 * norm(luminance(lit)) + 0.45 * norm(luminance(buf['alb']))
    dark = 1 - t
    g = math.log(0.5) / math.log(max(min(float(dark.mean()), 0.95), 0.05))
    dark = np.clip(dark ** g * 1.08 - 0.04, 0, 1)
    ang = hatch_angle_map(buf, sc, 0)
    sky = buf['id'] < 0
    ang = np.where(sky, 0.0, ang)
    sp = 8.5 * S + 1.0
    s1 = stripes(H, W, ang, sp, warp=0.8, seed=301, S=S)
    ink = (s1 < dark ** 1.1 * 1.1).astype(np.float32)
    s2 = stripes(H, W, ang + math.radians(90), sp * 1.2, warp=0.8, seed=302, S=S)
    ink = np.maximum(ink, ((s2 < (dark - 0.62) * 2.2) & (dark > 0.62)).astype(np.float32))
    ink[dark > 0.86] = 1.0
    ink[dark < 0.1] = 0.0
    e = edges_from_id(buf, 1)
    near = buf['depth'] > 0.3
    e = cv2.dilate(e * near, np.ones((max(2, int(3 * S)), max(2, int(3 * S))), np.uint8))
    ink = np.maximum(ink, e)
    # gouge flecks in the solid blacks
    r = rng(303)
    fl = np.zeros((H, W), np.float32)
    for i in range(int(2600 * S * S)):
        x, y = r.random() * W, r.random() * H
        a = r.normal(0, 0.25)
        L = r.uniform(3, 11) * S
        cv2.line(fl, (int(x * 16), int(y * 16)), (int((x + math.cos(a) * L) * 16), int((y + math.sin(a) * L) * 16)), 1.0,
                 max(1, int(1.1 * S)), cv2.LINE_AA, 4)
    solid = cv2.erode((dark > 0.9).astype(np.float32), np.ones((5, 5), np.uint8))
    ink = np.where((fl > 0.5) & (solid > 0.5), 0.0, ink)
    ink = smoothstep(0.3, 0.7, cv2.GaussianBlur(ink, (0, 0), 0.55 * S + 0.25))
    parts = make_particles(sc)
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a_, z) in parts['rain'][::4]:
            cv2.line(rl, (int(x0 * S * 16), int(y0 * S * 16)), (int(x1 * S * 16), int(y1 * S * 16)), 1.0, max(1, int(1.3 * S)), cv2.LINE_AA, 4)
        ink = np.where(dark > 0.55, ink * (1 - rl), np.maximum(ink, rl * 0.85))
    pap = paper(H, W, (0.91, 0.87, 0.77), fiber=0.05, mottle=0.06, S=S, seed=304)
    inkv = 0.9 + 0.1 * value_noise(H, W, 20 * S + 1, 305)
    black = np.array([0.06, 0.055, 0.05], np.float32)
    out = pap * (1 - ink[..., None] * inkv[..., None]) + black * (ink * inkv)[..., None]
    # second block in vermilion: the lights, and their glow drawn as red lines
    em = emissive_mask(buf)
    redm = cv2.dilate((em > 0.3).astype(np.float32), np.ones((max(3, int(5 * S)), max(3, int(5 * S))), np.uint8))
    halo = np.zeros((H, W), np.float32)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for l in sc.lights:
        d2 = ((xx - l.x * S) ** 2 + (yy - l.y * S) ** 2) / (l.r * 0.45 * S) ** 2
        halo = np.maximum(halo, np.exp(-d2) * min(l.I, 1.2) * 0.8)
    if sc.mood == 'dusk' and sc.sun is not None:
        d2 = ((xx - sc.sun[0] * S) ** 2 + (yy - sc.sun[1] * S) ** 2) / (330 * S) ** 2
        halo = np.maximum(halo, np.exp(-d2) * sky)
        disc = np.zeros((H, W), np.float32)
        cv2.circle(disc, (int(sc.sun[0] * S), int(sc.sun[1] * S)), int(52 * S), 1.0, -1, cv2.LINE_AA)
        redm = np.maximum(redm, disc * sky)
    hl = stripes(H, W, np.zeros((H, W), np.float32) + math.radians(90), sp, warp=0.5, seed=306, S=S)
    redm = np.maximum(redm, ((hl < halo * 0.9) & (halo > 0.12)).astype(np.float32) * (1 - ink))
    M = np.float32([[1, 0, 2.2 * S], [0, 1, -1.4 * S]])
    redm = cv2.warpAffine(cv2.GaussianBlur(redm, (0, 0), 0.6 * S + 0.2), M, (W, H))
    redm *= 0.85 + 0.15 * value_noise(H, W, 30 * S + 1, 307, cy=2 * S + 1)
    red = np.array([0.76, 0.19, 0.12], np.float32)
    k = (redm * (1 - ink * 0.9))[..., None] * 0.9
    out = out * (1 - k) + red * pap * k
    out = vignette(out, 0.1, col=(0.6, 0.55, 0.45))
    return np.clip(out, 0, 1)


# ================================================================== 4. CANDLELIT OIL (fixed coverage, flow field)
def style_oil(sc, W, H, buf=None, work=720):
    WW, HH = work, work * 16 // 9
    b2 = base_render(sc, WW, HH)
    S2 = b2['S']
    ref = b2['img'].copy()
    parts = make_particles(sc)
    ref = draw_particles(ref, parts, S2, lights=sc.lights)
    ref = filmic(ref, exposure=1.75 if sc.name == 'arabia' else 1.3, contrast=1.1, sat=1.25)
    lumr = luminance(ref)[..., None]
    # teal shadows, warm lights
    ref = ref + (1 - lumr) * np.array([-0.02, 0.01, 0.04], np.float32) * 1.2 + lumr * np.array([0.04, 0.01, -0.03], np.float32)
    ref = np.clip(ref, 0, 1)
    r = rng(51)
    canvas = np.ones_like(ref) * np.array([0.25, 0.17, 0.11], np.float32)
    height = np.zeros((HH, WW), np.float32)
    lb0 = cv2.GaussianBlur(luminance(ref), (0, 0), 2)
    gx = cv2.Sobel(lb0, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(lb0, cv2.CV_32F, 0, 1, ksize=3)
    Jxx, Jyy, Jxy = [cv2.GaussianBlur(v, (0, 0), 7) for v in (gx * gx, gy * gy, gx * gy)]
    theta = 0.5 * np.arctan2(2 * Jxy, Jxx - Jyy) + math.pi / 2   # along edges
    coh = np.sqrt((Jxx - Jyy) ** 2 + 4 * Jxy ** 2) / (Jxx + Jyy + 1e-6)
    ang0 = np.radians(hatch_angle_map(b2, sc, 0) * 180 / math.pi * 0)  # zeros
    flat = coh < 0.25
    theta = np.where(flat, np.radians(8) + (fbm(HH, WW, 60, 3, 52) - 0.5) * 0.8, theta)
    for li, R in enumerate((14, 8, 4, 2)):
        blur = cv2.GaussianBlur(ref, (0, 0), R * 0.55)
        diff = np.abs(canvas - blur).sum(2)
        thr = -1 if li == 0 else (0.07 if R > 2 else 0.1)
        cells = []
        for y in range(0, HH, R):
            for x in range(0, WW, R):
                y1, x1 = min(y + R, HH), min(x + R, WW)
                region = diff[y:y1, x:x1]
                if region.mean() > thr:
                    k = np.argmax(region)
                    cells.append((y + k // (x1 - x), x + k % (x1 - x)))
        r.shuffle(cells)
        L = 9 if R > 4 else (6 if R > 2 else 4)
        for (cy, cx) in cells:
            col = blur[cy, cx] * (1 + r.normal(0, 0.04, 3)).astype(np.float32)
            pts = [(cx, cy)]
            x, y = float(cx), float(cy)
            th0 = theta[cy, cx]
            dx, dy = math.cos(th0), math.sin(th0)
            if r.random() < 0.5:
                dx, dy = -dx, -dy
            for step in range(L):
                x, y = x + dx * R * 0.9, y + dy * R * 0.9
                xi, yi = int(min(max(x, 0), WW - 1)), int(min(max(y, 0), HH - 1))
                pts.append((x, y))
                if step > 0 and np.abs(blur[yi, xi] - col).sum() > 0.18:
                    break
                th = theta[yi, xi]
                nx, ny = math.cos(th), math.sin(th)
                if nx * dx + ny * dy < 0:
                    nx, ny = -nx, -ny
                dx, dy = 0.55 * nx + 0.45 * dx, 0.55 * ny + 0.45 * dy
                n = math.hypot(dx, dy) + 1e-9
                dx, dy = dx / n, dy / n
            q = (np.array(pts) * 16).astype(np.int32)
            th_ = max(1, int(R * 1.25))
            cv2.polylines(canvas, [q], False, tuple(float(c) for c in col), th_, cv2.LINE_AA, 4)
            cv2.polylines(height, [q], False, float(0.5 + 0.5 * r.random()), max(1, th_ - 1), cv2.LINE_AA, 4)
    hb = cv2.GaussianBlur(height, (0, 0), 0.7)
    hb = hb + value_noise(HH, WW, 1.4, 53, cy=1.4) * 0.18
    em = cv2.Sobel(hb, cv2.CV_32F, 1, 0, ksize=3) * -0.5 + cv2.Sobel(hb, cv2.CV_32F, 0, 1, ksize=3) * -0.5
    canvas = canvas * (1 + np.clip(em, -0.4, 0.4)[..., None] * 0.4)
    img = cv2.resize(canvas, (W, H), interpolation=cv2.INTER_CUBIC)
    S = W / DW
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    weave = np.sin(xx * 1.7) * np.sin(yy * 1.7)
    img *= (1 + weave * 0.018)[..., None]
    bufd = buf if buf is not None else base_render(sc, W, H)
    img = bloom(img, thr=0.72, strength=0.5, S=S, tint=(1.0, 0.8, 0.6))
    if sc.sun is not None:
        lum = luminance(img)
        src = img * (smoothstep(0.62, 1.05, lum) * (bufd['depth'] < 0.3))[..., None]
        img = godrays(img, src, sc.sun[0], sc.sun[1], strength=0.38, S=S)
    img = vignette(img, 0.5, col=(0.04, 0.025, 0.02))
    img = grain(img, 0.014)
    return np.clip(img * np.array([1.03, 1.0, 0.95], np.float32), 0, 1)


# ================================================================== 5. UKIYO-E (per-object flat colour)
UKI = np.array([[0.11, 0.13, 0.2], [0.17, 0.27, 0.44], [0.36, 0.52, 0.66], [0.7, 0.78, 0.8], [0.93, 0.88, 0.76],
                [0.86, 0.36, 0.22], [0.92, 0.62, 0.36], [0.55, 0.4, 0.26], [0.33, 0.22, 0.16], [0.47, 0.55, 0.38],
                [0.64, 0.6, 0.52], [0.2, 0.17, 0.16], [0.97, 0.85, 0.55], [0.6, 0.62, 0.66], [0.38, 0.4, 0.46]], np.float32)
SKY_UKI = dict(night=[(0, (0.08, 0.1, 0.2)), (0.35, (0.15, 0.22, 0.38)), (0.6, (0.62, 0.7, 0.76)), (1, (0.8, 0.82, 0.8))],
               storm=[(0, (0.2, 0.22, 0.27)), (0.3, (0.38, 0.42, 0.48)), (0.55, (0.86, 0.82, 0.7)), (1, (0.9, 0.86, 0.78))],
               dusk=[(0, (0.3, 0.2, 0.36)), (0.25, (0.62, 0.36, 0.38)), (0.5, (0.93, 0.6, 0.36)), (0.62, (0.97, 0.86, 0.6)), (1, (0.95, 0.9, 0.75))])


def style_ukiyoe(sc, W, H, buf=None):
    from core import gradient_stops
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    out = np.repeat(gradient_stops(H, SKY_UKI.get(sc.mood, SKY_UKI['night']))[:, None], W, 1)
    if sc.name == 'arabia':
        out = np.repeat(gradient_stops(H, [(0, (0.05, 0.06, 0.14)), (0.45, (0.1, 0.14, 0.3)), (0.68, (0.36, 0.4, 0.52)),
                                            (1, (0.5, 0.5, 0.55))])[:, None], W, 1)
    # clouds as flat shapes with outlines
    sk = sky_render(sc, W, H, S)
    skl = luminance(sk)
    base_l = cv2.GaussianBlur(skl, (0, 0), 60 * S)
    cl = smoothstep(0.02, 0.06, skl - base_l) * (buf['id'] < 0) * (np.arange(H)[:, None] < HZ.get(sc.name, 0.6) * H)
    cl = (cv2.GaussianBlur(cl, (0, 0), 2 * S) > 0.5).astype(np.float32)
    k_ = max(3, int(9 * S) | 1)
    cl = cv2.morphologyEx(cl, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_, k_)))
    if sc.name == 'arabia':
        mw = cv2.GaussianBlur(skl, (0, 0), 14 * S)
        mwb = smoothstep(0.012, 0.03, mw - cv2.GaussianBlur(skl, (0, 0), 120 * S)) * (buf['id'] < 0)
        cl = (mwb > 0.5).astype(np.float32)
        cl = cv2.morphologyEx(cl, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k_, k_)))
    ccol = np.array([0.95, 0.92, 0.84], np.float32) if sc.mood != 'night' else (np.array([0.3, 0.36, 0.55], np.float32) if sc.name == 'arabia' else np.array([0.48, 0.55, 0.68], np.float32))
    out = out * (1 - cl[..., None] * 0.85) + ccol * cl[..., None] * 0.85
    lines = band_of(cl, 1.0 * S + 0.5)
    # stars and milky way
    if sc.name == 'arabia':
        st = (skl > np.percentile(skl, 99.2)) & (buf['id'] < 0)
        st = cv2.dilate(st.astype(np.uint8), np.ones((2, 2), np.uint8)).astype(bool)
        starmask = st
    lit = buf['img']
    for idx, it, (x0, y0, m) in item_masks(buf, sc):
        sl_ = paste(out[..., 0], x0, y0, m)
        if sl_ is None:
            continue
        (dy, dx), (sy_, sx_) = sl_
        a = m[sy_, sx_] * it.alpha
        if it.mat in ('rain',):
            continue
        c = np.array(it.col, np.float32)
        if it.emit > 0:
            pc = np.array([0.98, 0.78, 0.4], np.float32) if it.mat != 'fire' else np.array([0.9, 0.35, 0.18], np.float32)
        else:
            boost = 1.6 if sc.mood in ('night', 'storm') else 1.15
            cc = np.clip(c * boost, 0, 1)
            lab = cv2.cvtColor(cc[None, None], cv2.COLOR_RGB2Lab)[0, 0]
            pl = cv2.cvtColor(UKI[None], cv2.COLOR_RGB2Lab)[0]
            pc = UKI[np.argmin(((pl - lab) ** 2 * np.array([0.5, 1, 1], np.float32)).sum(1))]
        # two-step shading from the lit render
        L = luminance(lit[dy, dx])
        lm = float(np.median(L[a > 0.5])) if (a > 0.5).any() else 0.5
        shade = np.where(L < lm * 0.75, 0.78, 1.0).astype(np.float32)
        if it.mat in ('water',):
            yy = np.arange(dy.start, dy.stop, dtype=np.float32)[:, None] / H
            pc_img = np.array([0.15, 0.27, 0.45], np.float32) * (1.15 - 0.6 * (yy - yy.min()) / (yy.max() - yy.min() + 1e-6))[..., None]
            pc_img = np.broadcast_to(pc_img, (dy.stop - dy.start, dx.stop - dx.start, 3))
        else:
            pc_img = pc * shade[..., None]
        out[dy, dx] = out[dy, dx] * (1 - a[..., None]) + pc_img * a[..., None]
    # sun or moon disc
    if sc.sun is not None and sc.mood != 'storm':
        disc = np.zeros((H, W), np.float32)
        rad = 54 if sc.mood == 'dusk' else 44
        cv2.circle(disc, (int(sc.sun[0] * S * 16), int(sc.sun[1] * S * 16)), int(rad * S * 16), 1.0, -1, cv2.LINE_AA, 4)
        disc *= buf['depth'] < 0.07
        dc = np.array([0.88, 0.3, 0.18], np.float32) if sc.mood == 'dusk' else np.array([0.98, 0.92, 0.7], np.float32)
        out = out * (1 - disc[..., None]) + dc * disc[..., None]
    if sc.name == 'arabia':
        out[starmask & (buf['id'] < 0)] = np.array([0.97, 0.95, 0.86], np.float32)
    grain_ = value_noise(H, W, 90 * S + 1, 501, cy=2.2 * S + 0.5)
    out *= (0.95 + 0.09 * grain_)[..., None]
    out *= (0.97 + 0.06 * fbm(H, W, 12 * S + 1, 3, 502))[..., None]
    e = edges_from_id(buf, 1)
    e = np.maximum(e, lines)
    e = cv2.dilate(e, np.ones((max(2, int(2.5 * S)), max(2, int(2.5 * S))), np.uint8)).astype(np.float32)
    e = cv2.GaussianBlur(e, (0, 0), 0.5 * S + 0.2)
    M = np.float32([[1, 0, 1.6 * S], [0, 1, 1.1 * S]])
    out = cv2.warpAffine(out, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    keycol = np.array([0.1, 0.1, 0.14], np.float32)
    out = out * (1 - e[..., None] * 0.9) + keycol * e[..., None] * 0.9
    parts = make_particles(sc)
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a_, z) in parts['rain'][::2]:
            cv2.line(rl, (int(x0 * S * 16), int(y0 * S * 16)), (int((x0 + (x1 - x0) * 2.6) * S * 16), int((y0 + (y1 - y0) * 2.6) * S * 16)),
                     1.0, 1, cv2.LINE_AA, 4)
        out = out * (1 - rl[..., None] * 0.7) + keycol * rl[..., None] * 0.7
    if parts['embers']:
        for (x, y, r_, b) in parts['embers']:
            cv2.circle(out, (int(x * S), int(y * S)), max(1, int(r_ * S)), (0.92, 0.5, 0.22), -1, cv2.LINE_AA)
    pap = paper(H, W, (1.0, 0.97, 0.9), fiber=0.08, mottle=0.04, S=S, seed=503)
    out = out * pap
    # margin and cartouche, as on a print
    mw = int(22 * S)
    out[:mw] = pap[:mw]
    out[-mw:] = pap[-mw:]
    out[:, :mw] = pap[:, :mw]
    out[:, -mw:] = pap[:, -mw:]
    cv2.rectangle(out, (mw, mw), (W - mw, H - mw), (0.12, 0.11, 0.13), max(1, int(2 * S)))
    cx0, cy0 = int(W - mw - 70 * S), int(mw + 30 * S)
    cv2.rectangle(out, (cx0, cy0), (cx0 + int(44 * S), cy0 + int(190 * S)), (0.9, 0.8, 0.55), -1)
    cv2.rectangle(out, (cx0, cy0), (cx0 + int(44 * S), cy0 + int(190 * S)), (0.12, 0.11, 0.13), max(1, int(2 * S)))
    for k in range(5):
        y = cy0 + int((22 + k * 34) * S)
        cv2.line(out, (cx0 + int(12 * S), y), (cx0 + int(32 * S), y + int(14 * S)), (0.12, 0.11, 0.13), max(1, int(3 * S)), cv2.LINE_AA)
    return np.clip(out, 0, 1)


# ================================================================== 7. STAINED GLASS (shards cut by objects)
def style_glass(sc, W, H, buf=None):
    from scipy.spatial import cKDTree
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    src = filmic(buf['img'], exposure=1.6, sat=1.5)
    src = src * 0.65 + np.clip(buf['alb'] * 1.3, 0, 1) * 0.35
    r = rng(601)
    depth = buf['depth']
    pts = []
    for (sp, zsel) in ((78, lambda d: d < 0.05), (34, lambda d: (d >= 0.05) & (d < 0.5)), (20, lambda d: d >= 0.5)):
        s = sp * S
        gy, gx = np.mgrid[0:H:s, 0:W:s]
        p = np.stack([gx.ravel() + r.uniform(-s * 0.45, s * 0.45, gx.size), gy.ravel() + r.uniform(-s * 0.45, s * 0.45, gx.size)], 1)
        p = p[(p[:, 0] >= 0) & (p[:, 0] < W) & (p[:, 1] >= 0) & (p[:, 1] < H)]
        dd = depth[p[:, 1].astype(int), p[:, 0].astype(int)]
        pts.append(p[zsel(dd)])
    pts = np.vstack(pts)
    tree = cKDTree(pts)
    yy, xx = np.mgrid[0:H, 0:W]
    _, vor = tree.query(np.stack([xx.ravel(), yy.ravel()], 1), workers=2)
    vor = vor.reshape(H, W).astype(np.int64)
    lab = vor * 4096 + (buf['id'].astype(np.int64) + 1)
    _, lab = np.unique(lab, return_inverse=True)
    lab = lab.reshape(H, W)
    n = lab.max() + 1
    cnt = np.bincount(lab.ravel(), minlength=n).astype(np.float32) + 1e-6
    mean = np.stack([np.bincount(lab.ravel(), weights=src[..., c].ravel(), minlength=n) / cnt for c in range(3)], 1)
    lumv = mean @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    mean = lumv[:, None] + (mean - lumv[:, None]) * 1.7
    mean = np.clip(mean * (0.8 + 0.4 * r.random((n, 1))), 0.02, 1.25).astype(np.float32)
    glass = mean[lab]
    edges = np.zeros((H, W), np.float32)
    edges[:, 1:] += lab[:, 1:] != lab[:, :-1]
    edges[1:, :] += lab[1:, :] != lab[:-1, :]
    edges = np.clip(edges, 0, 1)
    dist = cv2.distanceTransform((1 - edges).astype(np.uint8), cv2.DIST_L2, 3)
    shade = np.clip(dist / (10 * S), 0, 1) ** 0.5
    glass *= (0.6 + 0.55 * shade)[..., None]
    glass *= (0.86 + 0.28 * value_noise(H, W, 70 * S + 1, 602, cy=5 * S + 1))[..., None]
    glass += (value_noise(H, W, 1.8 * S + 0.4, 603) > 0.92).astype(np.float32)[..., None] * 0.07
    # grisaille: painted detail lines on near objects
    e = edges_from_id(buf, 1) * (depth > 0.55)
    glass *= (1 - cv2.GaussianBlur(e, (0, 0), 0.8 * S + 0.2) * 0.55)[..., None]
    lead = cv2.dilate(edges, np.ones((max(3, int(6 * S)), max(3, int(6 * S))), np.uint8)).astype(np.float32)
    lead = cv2.GaussianBlur(lead, (0, 0), 0.7 * S + 0.2)
    bead = cv2.GaussianBlur(edges, (0, 0), 1.0 * S + 0.3)
    out = glass * (1 - lead[..., None]) + (np.array([0.05, 0.05, 0.055], np.float32) + bead[..., None] * 0.1) * lead[..., None]
    for yb in np.arange(400, DH, 480):
        cv2.rectangle(out, (0, int(yb * S)), (W, int((yb + 10) * S)), (0.04, 0.04, 0.045), -1)
    out = bloom(out, thr=0.62, strength=0.8, S=S)
    if sc.sun is not None:
        lum = luminance(out)
        srcg = out * smoothstep(0.7, 1.15, lum)[..., None]
        out = godrays(out, srcg, sc.sun[0], sc.sun[1], strength=0.32, S=S)
    out = vignette(out, 0.35)
    return filmic(out, exposure=1.25, sat=1.0)


# ================================================================== 8. GILDED MOSAIC (bigger tesserae, contour rows)
def style_mosaic(sc, W, H, buf=None):
    from scipy.spatial import cKDTree
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    src = filmic(buf['img'], exposure=1.5, sat=1.2)
    r = rng(701)
    sp = 17 * S
    gy, gx = np.mgrid[0:H:sp, 0:W:sp]
    gx = gx.astype(np.float32) + (np.arange(gx.shape[0])[:, None] % 2) * sp * 0.5
    pts = np.stack([gx.ravel() + r.uniform(-sp * 0.2, sp * 0.2, gx.size), gy.ravel() + r.uniform(-sp * 0.2, sp * 0.2, gx.size)], 1)
    # contour rows: seeds along both sides of every edge
    e = edges_from_id(buf, 1)
    ey, ex = np.nonzero(e)
    sel = r.random(len(ex)) < (1.0 / (7 * S + 1))
    ex, ey = ex[sel].astype(np.float32), ey[sel].astype(np.float32)
    idm = buf['id']
    gxi = cv2.Sobel(idm.astype(np.float32), cv2.CV_32F, 1, 0, ksize=3)[ey.astype(int), ex.astype(int)]
    gyi = cv2.Sobel(idm.astype(np.float32), cv2.CV_32F, 0, 1, ksize=3)[ey.astype(int), ex.astype(int)]
    nn = np.sqrt(gxi ** 2 + gyi ** 2) + 1e-6
    off = 4.5 * S
    pts = np.vstack([pts, np.stack([ex + gxi / nn * off, ey + gyi / nn * off], 1), np.stack([ex - gxi / nn * off, ey - gyi / nn * off], 1)])
    # thin the grid near edges so rows dominate
    tree = cKDTree(pts)
    yy, xx = np.mgrid[0:H, 0:W]
    _, lab = tree.query(np.stack([xx.ravel(), yy.ravel()], 1), workers=2)
    lab = lab.reshape(H, W)
    n = len(pts)
    cnt = np.bincount(lab.ravel(), minlength=n).astype(np.float32) + 1e-6
    mean = np.stack([np.bincount(lab.ravel(), weights=src[..., c].ravel(), minlength=n) / cnt for c in range(3)], 1)
    skyfrac = np.bincount(lab.ravel(), weights=(idm < 0).ravel().astype(np.float32), minlength=n) / cnt
    edgefrac = np.bincount(lab.ravel(), weights=e.ravel(), minlength=n) / cnt
    pal = np.array([[0.94, 0.91, 0.84], [0.76, 0.71, 0.63], [0.52, 0.47, 0.42], [0.28, 0.25, 0.24], [0.1, 0.1, 0.12],
                    [0.13, 0.22, 0.45], [0.27, 0.4, 0.64], [0.58, 0.16, 0.13], [0.8, 0.42, 0.22], [0.22, 0.37, 0.27],
                    [0.56, 0.61, 0.46], [0.64, 0.47, 0.32], [0.44, 0.3, 0.22], [0.42, 0.3, 0.45]], np.float32)
    dd = ((mean[:, None, :] - pal[None]) ** 2).sum(-1)
    tcol = pal[np.argmin(dd, 1)] * (0.88 + 0.24 * r.random((n, 1))).astype(np.float32)
    tcol = np.where((edgefrac > 0.05)[:, None] & (skyfrac < 0.5)[:, None], tcol * 0.45, tcol)
    gold = np.array([0.96, 0.76, 0.38], np.float32)
    lum_sky = mean @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    gl = (0.78 + 0.34 * r.random((n, 1))).astype(np.float32) * (0.75 + 0.45 * np.clip(lum_sky[:, None] * 1.4, 0, 1))
    tcol = np.where((skyfrac > 0.5)[:, None], gold * gl, tcol)
    img = tcol[lab].astype(np.float32)
    edges = np.zeros((H, W), np.float32)
    edges[:, 1:] += lab[:, 1:] != lab[:, :-1]
    edges[1:, :] += lab[1:, :] != lab[:-1, :]
    dist = cv2.distanceTransform((edges == 0).astype(np.uint8), cv2.DIST_L2, 3)
    grout = smoothstep(0.8 * S + 0.4, 2.0 * S + 0.8, dist)
    gxh = cv2.Sobel(dist, cv2.CV_32F, 1, 0, ksize=3)
    gyh = cv2.Sobel(dist, cv2.CV_32F, 0, 1, ksize=3)
    bevel = np.clip(-(gxh + gyh) * 0.09, -0.22, 0.22) * (dist < 4 * S + 1)
    img = img * (1 + bevel[..., None])
    img = img * grout[..., None] + np.array([0.3, 0.28, 0.25], np.float32) * (1 - grout[..., None])
    tilt = (r.random(n) > 0.85).astype(np.float32)
    img += (tilt[lab] * (skyfrac[lab] > 0.5) * grout)[..., None] * np.array([0.35, 0.27, 0.12], np.float32)
    img = bloom(img, thr=0.82, strength=0.45, S=S, tint=(1.0, 0.85, 0.6))
    img = vignette(img, 0.3)
    img = grain(img, 0.01)
    return np.clip(img, 0, 1)


# ================================================================== 9. CHARCOAL AND CHALK (grain, smudge)
def style_charcoal(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    img = buf['img'].copy()
    parts = make_particles(sc)
    img = draw_particles(img, parts, S, lights=sc.lights)
    lum = luminance(img)
    lo, hi = np.percentile(lum, 1.5), np.percentile(lum, 99.7)
    t = np.clip((lum - lo) / (hi - lo + 1e-6), 0, 1)
    dark = (1 - t) ** 1.1
    tooth = value_noise(H, W, 1.5 * S + 0.4, 801)
    ang = hatch_angle_map(buf, sc, 0) + math.radians(30)
    # directional grain: average tooth along the stroke direction
    k = int(9 * S) | 1
    strokes = np.zeros((H, W), np.float32)
    for a in np.radians([0, 30, 60, 90, 120, 150]):
        ker = np.zeros((k, k), np.float32)
        c = k // 2
        cv2.line(ker, (int(c - math.cos(a) * c), int(c - math.sin(a) * c)), (int(c + math.cos(a) * c), int(c + math.sin(a) * c)), 1.0, 1)
        ker /= ker.sum()
        f = cv2.filter2D(tooth, -1, ker)
        w = np.cos(ang - a) ** 16
        strokes += f * w
    strokes /= np.maximum(sum(np.cos(ang - a) ** 16 for a in np.radians([0, 30, 60, 90, 120, 150])), 1e-3)
    d_eff = dark + (strokes - 0.5) * 0.9 + (tooth - 0.5) * 0.25
    char = smoothstep(0.32, 0.78, d_eff)
    smudge = cv2.GaussianBlur(dark, (0, 0), 7 * S + 1) * 0.5
    char = np.clip(np.maximum(char, smudge * smoothstep(0.3, 0.7, dark)), 0, 1)
    e = edges_from_id(buf, 1) * (buf['depth'] > 0.3)
    e = cv2.GaussianBlur(cv2.dilate(e, np.ones((2, 2), np.uint8)), (0, 0), 0.9 * S + 0.2)
    brk = smoothstep(0.2, 0.45, value_noise(H, W, 12 * S + 1, 802))
    char = np.clip(char + e * 0.85 * brk, 0, 1)
    chalk = smoothstep(0.6, 0.95, t + (tooth - 0.5) * 0.3)
    pap = paper(H, W, (0.62, 0.58, 0.52), fiber=0.04, mottle=0.07, S=S, seed=803)
    out = pap * (1 - char[..., None] * 0.94) + np.array([0.045, 0.04, 0.04], np.float32) * char[..., None] * 0.94
    out = out * (1 - chalk[..., None] * 0.8) + np.array([0.97, 0.93, 0.84], np.float32) * chalk[..., None] * 0.8
    em = cv2.GaussianBlur(emissive_mask(buf), (0, 0), 3 * S + 0.5)
    out = out * (1 - em[..., None] * 0.6) + np.array([0.95, 0.52, 0.22], np.float32) * em[..., None] * 0.6
    out = vignette(out, 0.28, col=(0.28, 0.26, 0.23))
    return np.clip(out, 0, 1)


# ================================================================== 6. PAPER DIORAMA (richer colour)
def style_paper(sc, W, H, buf=None):
    sc.haze = sc.haze * 0.55
    b2 = base_render(sc, W, H)
    return S1.style_paper(sc, W, H, buf=b2)


# ================================================================== 2. SHADOW THEATRE (richer skies)
SHADOW_SKY = dict(bamberg=[(0, (0.02, 0.03, 0.07)), (0.3, (0.04, 0.08, 0.17)), (0.5, (0.09, 0.19, 0.3)), (0.58, (0.18, 0.3, 0.36)), (1, (0.03, 0.04, 0.07))],
                  zong=[(0, (0.1, 0.08, 0.14)), (0.3, (0.32, 0.2, 0.26)), (0.48, (0.85, 0.45, 0.25)), (0.545, (1.0, 0.72, 0.4)), (0.56, (0.55, 0.35, 0.3)), (1, (0.12, 0.1, 0.14))],
                  kleidion=[(0, (0.12, 0.06, 0.13)), (0.25, (0.45, 0.15, 0.15)), (0.45, (0.92, 0.42, 0.18)), (0.56, (1.0, 0.76, 0.4)), (0.62, (0.85, 0.45, 0.25)), (1, (0.25, 0.1, 0.1))])


def style_shadow(sc, W, H, buf=None):
    if sc.name in SHADOW_SKY:
        sc.sky = dict(sc.sky)
        sc.sky['stops'] = SHADOW_SKY[sc.name]
        if sc.name == 'bamberg':
            sc.sky['glow'] = [(250, 300, 300, (0.4, 0.5, 0.7), 0.25)]
    b2 = base_render(sc, W, H)
    return S1.style_shadow(sc, W, H, buf=b2)


# ================================================================== 10. WATERCOLOUR (deeper)
def style_watercolor(sc, W, H, buf=None):
    sc.haze = sc.haze * 0.8
    b2 = base_render(sc, W, H)
    S = b2['S']
    img = filmic(b2['img'], exposure=1.45, sat=1.25, contrast=1.06)
    parts = make_particles(sc)
    base = cv2.edgePreservingFilter((np.clip(img, 0, 1) * 255).astype(np.uint8), flags=1, sigma_s=30, sigma_r=0.3).astype(np.float32) / 255
    pap = paper(H, W, (0.97, 0.95, 0.9), fiber=0.04, mottle=0.03, S=S, seed=901)
    lum = luminance(base)
    gran = fbm(H, W, 2.5 * S + 0.5, 3, 902)
    wet = fbm(H, W, 110 * S + 1, 4, 903)
    bloom_n = smoothstep(0.55, 0.75, fbm(H, W, 50 * S + 1, 4, 904))
    pig = 1 - base
    pig *= (0.82 + 0.4 * gran[..., None] * (lum[..., None] < 0.7)) * (0.85 + 0.3 * wet[..., None])
    pig *= (1 - bloom_n[..., None] * 0.18)
    bl = cv2.GaussianBlur(pig, (0, 0), 3.5 * S + 0.5)
    pig = np.clip(pig + np.clip(pig - bl, 0, None) * 1.8, 0, 1)
    out = pap * (1 - pig * 1.02)
    e = edges_from_id(b2, 1) * (b2['depth'] > 0.3)
    wob = value_noise(H, W, 30 * S + 1, 905) > 0.3
    e = cv2.GaussianBlur(e * wob, (0, 0), 0.6 * S + 0.2)
    out *= (1 - np.clip(e * 0.9, 0, 0.7))[..., None]
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a, z) in parts['rain'][::3]:
            cv2.line(rl, (int(x0 * S * 16), int(y0 * S * 16)), (int(x1 * S * 16), int(y1 * S * 16)), float(a), 1, cv2.LINE_AA, 4)
        out *= (1 - rl * 0.35)[..., None]
    out = draw_particles(out, dict(rain=[], embers=parts['embers'], dust=parts['dust']), S, lights=sc.lights)
    em = cv2.GaussianBlur(emissive_mask(b2), (0, 0), 8 * S + 1)
    out = out + em[..., None] * np.array([0.5, 0.3, 0.1], np.float32) * 0.5
    out = vignette(out, 0.15, col=(0.7, 0.65, 0.58))
    return np.clip(out, 0, 1)


STYLES = dict(S1.STYLES)
STYLES.update(ink=style_ink, woodcut=style_woodcut, oil=style_oil, ukiyoe=style_ukiyoe, glass=style_glass,
              mosaic=style_mosaic, charcoal=style_charcoal, paper=style_paper, shadow=style_shadow, watercolor=style_watercolor)
