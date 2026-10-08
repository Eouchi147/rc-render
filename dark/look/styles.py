"""Ten looks rendered from the same 2.5D scenes."""
import math
import numpy as np
import cv2
from core import (base_render, make_particles, draw_particles, luminance, fbm, value_noise, smoothstep, rng,
                  bloom, godrays, dof, chroma, vignette, grain, anamorphic, flare_ghosts, filmic, edges_from_id, DW, DH)


# ------------------------------------------------------------------ shared helpers
def paper(H, W, base=(0.93, 0.9, 0.83), fiber=0.06, mottle=0.05, seed=1, S=1.0):
    img = np.ones((H, W, 3), np.float32) * np.array(base, np.float32)
    m = fbm(H, W, 180 * S, 5, seed) - 0.5
    img *= (1 + m * mottle * 2)[..., None]
    # fibres
    r = rng(seed + 1)
    fib = np.zeros((H, W), np.float32)
    for i in range(int(900 * S * S) + 200):
        x, y = r.random() * W, r.random() * H
        a = r.random() * math.pi
        L = r.uniform(8, 40) * S
        pts = np.array([[x, y], [x + math.cos(a) * L * 0.5 + r.normal(0, 3), y + math.sin(a) * L * 0.5 + r.normal(0, 3)],
                        [x + math.cos(a) * L, y + math.sin(a) * L]], np.float32)
        cv2.polylines(fib, [(pts * 16).astype(np.int32)], False, float(r.uniform(0.3, 1.0)), 1, cv2.LINE_AA, 4)
    fine = value_noise(H, W, 1.6 * S + 0.6, seed + 3) - 0.5
    img *= (1 - fib * fiber)[..., None]
    img *= (1 + fine * 0.035)[..., None]
    return img


def hatch_angle_map(buf, sc, default=0.0):
    idm = buf['id']
    ang = np.full(idm.shape, default + 90.0, np.float32)
    for i, it in enumerate(sc.items):
        if it.hatch is not None:
            ang[idm == i] = it.hatch + 90.0
    sky = idm < 0
    ang[sky] = 90.0
    return np.radians(ang)


def stripes(H, W, ang, spacing, warp=0.0, seed=0, S=1.0):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    ph = (xx * np.cos(ang) + yy * np.sin(ang)) / spacing
    if warp:
        ph += (fbm(H, W, 120 * S, 4, seed) - 0.5) * warp
    f = ph - np.floor(ph)
    return np.abs(f - 0.5) * 2  # 0 at line centre, 1 between lines


def mask_of(buf, sc, pred):
    idm = buf['id']
    m = np.zeros(idm.shape, bool)
    for i, it in enumerate(sc.items):
        if pred(it):
            m |= idm == i
    return m


def emissive_mask(buf):
    e = buf['emit']
    return np.clip(e / 1.5, 0, 1)


def lens_cine(img, buf, sc, S, rays=0.5, blo=0.6, focus=None, aperture=30, ca=0.0018, vig=0.35, gr=0.03, flare=0.25,
              streak=0.25, maxr=14):
    if focus is None:
        focus = sc.focus
    img = dof(img, buf['depth'], focus, aperture=aperture, maxr=maxr, S=S)
    if sc.sun is not None and rays > 0:
        lum = luminance(img)
        src = img * (smoothstep(0.55, 1.2, lum) * (buf['depth'] < 0.3))[..., None]
        img = godrays(img, src, sc.sun[0], sc.sun[1], strength=rays, S=S)
    img = bloom(img, thr=0.75, strength=blo, S=S)
    if streak:
        img = anamorphic(img, thr=1.0, strength=streak, S=S)
    if flare and sc.sun is not None:
        img = flare_ghosts(img, sc.sun[0], sc.sun[1], strength=flare * 0.25, S=S)
    if ca:
        img = chroma(img, ca)
    img = vignette(img, vig)
    img = grain(img, gr)
    return img


# ================================================================== 1. INK SCROLL
def gold_leaf(H, W, S, seed=3):
    base = np.array([0.84, 0.68, 0.4], np.float32)
    n = fbm(H, W, 90 * S + 1, 4, seed)
    speck = (value_noise(H, W, 1.2 * S + 0.4, seed + 5) > 0.93).astype(np.float32)
    sheen = fbm(H, W, 500 * S + 1, 3, seed + 9)
    g = base * (0.9 + 0.14 * n[..., None]) * (0.88 + 0.24 * sheen[..., None])
    g += speck[..., None] * np.array([0.12, 0.1, 0.05], np.float32)
    # leaf squares
    sq = (np.mod(np.mgrid[0:H, 0:W][0] + 3, int(70 * S) + 1) < 1) | (np.mod(np.mgrid[0:H, 0:W][1] + 7, int(70 * S) + 1) < 1)
    g *= (1 - sq * 0.12)[..., None]
    return g


def cloud_band(H, W, S, y, h, seed, x0=-50, x1=None):
    """kasumi: a scalloped band built from rounded lobes."""
    x1 = DW + 50 if x1 is None else x1
    m = np.zeros((H, W), np.float32)
    r = rng(seed)
    x = x0
    while x < x1:
        w = r.uniform(120, 260)
        hh = h * r.uniform(0.7, 1.0)
        yy = y + r.uniform(-h * 0.15, h * 0.15)
        cv2.ellipse(m, (int((x + w / 2) * S * 16), int(yy * S * 16)), (int(w / 2 * S * 16), int(hh / 2 * S * 16)), 0, 0, 360,
                    1.0, -1, cv2.LINE_AA, 4)
        for k in range(3):
            lx = x + r.uniform(0, w)
            cv2.ellipse(m, (int(lx * S * 16), int((yy - hh * 0.35) * S * 16)), (int(r.uniform(30, 70) * S * 16), int(hh * 0.4 * S * 16)),
                        0, 0, 360, 1.0, -1, cv2.LINE_AA, 4)
        x += w * r.uniform(0.6, 0.9)
    m = cv2.GaussianBlur(m, (0, 0), 1.2 * S)
    return np.clip(m, 0, 1)


def style_ink(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    img = buf['img']
    lum = luminance(img)
    # how dark is each place, normalised so the scene keeps paper in its lights
    lo, hi = np.percentile(lum, 2), np.percentile(lum, 99.5)
    d = 1 - np.clip((lum - lo) / (hi - lo + 1e-6), 0, 1)
    d = d ** 1.15
    # depth: far things paler (classic ink perspective)
    depth = buf['depth']
    far = np.clip(1 - depth, 0, 1)
    d = d * (1 - 0.45 * far ** 1.5 * (buf['id'] >= 0))
    # layered washes with wobbly boundaries and dried edges
    wob = (fbm(H, W, 70 * S, 4, 11) - 0.5) * 0.12
    wash = np.zeros_like(d)
    for t, a in ((0.12, 0.18), (0.32, 0.22), (0.55, 0.25), (0.78, 0.3)):
        layer = smoothstep(t - 0.03, t + 0.03, d + wob)
        edge = layer - cv2.GaussianBlur(layer, (0, 0), 2.2 * S)
        wash += a * layer + 0.35 * np.clip(edge, 0, 1)
    # brush streaks follow each object's hatch direction
    ang = hatch_angle_map(buf, sc, 0)
    streak = stripes(H, W, ang, 5.5 * S, warp=5, seed=12, S=S)
    dry = value_noise(H, W, 30 * S, 13, cy=3 * S)
    wash *= (0.8 + 0.25 * streak) * (0.88 + 0.24 * dry)
    # bleed into the fibres
    bleed = cv2.GaussianBlur(wash, (0, 0), 1.6 * S)
    fibre = fbm(H, W, 6 * S, 3, 14)
    wash = np.maximum(wash, bleed * smoothstep(0.35, 0.75, fibre))
    # outlines: brush contours, heavier near the camera, broken by dry brush
    e = edges_from_id(buf, 1)
    e = cv2.dilate(e, np.ones((2, 2), np.uint8)) if S > 0.7 else e
    near = np.clip(depth * 1.3 - 0.15, 0.25, 1)
    wv = value_noise(H, W, 60 * S, 15)
    brk = value_noise(H, W, 9 * S, 16, cy=9 * S) > 0.22
    line = cv2.GaussianBlur(e * near * (0.6 + 0.6 * wv) * brk, (0, 0), 0.7 * S)
    line = np.clip(line * 1.6, 0, 1)
    ink = np.clip(wash + line * 0.85, 0, 1.1)
    # rain as fine diagonal strokes
    parts = make_particles(sc)
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a, z) in parts['rain'][::2]:
            cv2.line(rl, (int(x0 * S * 16), int(y0 * S * 16)), (int(x1 * S * 16), int(y1 * S * 16)), float(a * 0.8), 1, cv2.LINE_AA, 4)
        ink = np.clip(ink + rl * 0.5, 0, 1.1)
    pap = paper(H, W, (0.94, 0.91, 0.84), S=S, seed=2)
    inkcol = np.array([0.09, 0.08, 0.075], np.float32)
    out = pap * (1 - ink[..., None]) + inkcol * ink[..., None] * pap
    # vermilion and gold for fire and light
    em = cv2.GaussianBlur(emissive_mask(buf), (0, 0), 2 * S)
    glow = cv2.GaussianBlur(em, (0, 0), 22 * S) * 0.7
    warm = np.clip(em * 1.2 + glow, 0, 1)
    red = np.array([0.82, 0.27, 0.13], np.float32)
    out = out * (1 - warm[..., None] * 0.75) + red * pap * warm[..., None] * 0.75
    for l in sc.lights:
        pass
    # gold mist bands (kasumi)
    gold = gold_leaf(H, W, S, seed=4)
    bands = getattr(sc, 'ink_bands', None) or [(DH * 0.17, 120, 41), (DH * 0.86, 140, 42)]
    for (y, h, s_) in bands:
        m = cloud_band(H, W, S, y, h, s_)
        out = out * (1 - m[..., None]) + gold * m[..., None]
        edge = np.clip(m - cv2.GaussianBlur(m, (0, 0), 2.5 * S), 0, 1)
        out *= (1 - edge * 0.25)[..., None]
    # seal
    sx, sy, ss = int(930 * S), int(1700 * S), int(64 * S)
    seal = np.zeros((H, W), np.float32)
    cv2.rectangle(seal, (sx, sy), (sx + ss, sy + ss), 1.0, -1)
    cut = np.zeros((H, W), np.float32)
    cv2.rectangle(cut, (sx + ss // 5, sy + ss // 5), (sx + ss - ss // 5, sy + ss - ss // 5), 1.0, max(1, int(5 * S)))
    cv2.line(cut, (sx + ss // 2, sy + ss // 5), (sx + ss // 2, sy + ss - ss // 5), 1.0, max(1, int(5 * S)))
    seal = seal * (1 - cut) * (0.75 + 0.25 * (value_noise(H, W, 3 * S + 0.5, 17) > 0.3))
    out = out * (1 - seal[..., None] * 0.85) + np.array([0.75, 0.16, 0.1], np.float32) * seal[..., None] * 0.85
    out = vignette(out, 0.18, col=(0.55, 0.48, 0.38))
    return np.clip(out, 0, 1)


# ================================================================== 2. SHADOW THEATRE
def style_shadow(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    from core import sky_render
    sky = sky_render(sc, W, H, S)
    lum_sky = luminance(sky)
    # richer, warmer theatre sky
    sky = sky * 1.15
    depth = buf['depth']
    cov = buf['cover']
    idm = buf['id']
    out = sky.copy()
    # depth tint: near = black, far = tinted by the sky colour at the horizon
    hz_col = sky[int(H * 0.62)].mean(0)
    items = sorted(enumerate(sc.items), key=lambda t: (t[1].z, t[0]))
    for idx, it in items:
        if idx not in buf['masks']:
            continue
        x0, y0, m = buf['masks'][idx]
        from core import paste
        sl = paste(depth, x0, y0, m)
        if sl is None:
            continue
        (dy, dx), (sy_, sx_) = sl
        a = m[sy_, sx_] * it.alpha
        if it.mat in ('fire', 'window', 'glint') and it.emit > 0:
            col = it.col * (1.4 + it.emit * 0.5)
        else:
            t = np.clip((it.z - 0.08) / 0.45, 0, 1) ** 0.9
            col = hz_col * (1 - t) * 0.85 + np.array([0.02, 0.018, 0.02], np.float32) * t
            if it.mat in ('water',):
                col = col * 0.9
        out[dy, dx] = out[dy, dx] * (1 - a[..., None]) + col * a[..., None]
    # haze between planes
    for f in sc.fog:
        pass
    # rim light: silhouette edges facing the light glow
    sil = (idm >= 0).astype(np.float32)
    rim = np.clip(sil - cv2.erode(sil, np.ones((3, 3), np.uint8)), 0, 1)
    rim = cv2.GaussianBlur(rim, (0, 0), 1.2 * S)
    if sc.sun is not None:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt((xx - sc.sun[0] * S) ** 2 + (yy - sc.sun[1] * S) ** 2) / (900 * S)
        rimw = np.exp(-d * 1.4)
        out += rim[..., None] * rimw[..., None] * np.array([1.0, 0.75, 0.5], np.float32) * 0.6
    # lights: glow in the air
    for l in sc.lights:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d2 = ((xx - l.x * S) ** 2 + (yy - l.y * S) ** 2) / (l.r * 1.1 * S) ** 2
        out += l.col * (0.25 * l.I * np.exp(-d2))[..., None]
    parts = make_particles(sc)
    out = draw_particles(out, parts, S, lights=sc.lights, rain_col=(0.55, 0.55, 0.6))
    # paper-cut fibre on the black
    tex = fbm(H, W, 8 * S, 3, 21)
    out *= (0.94 + 0.12 * tex * sil)[..., None]
    out = lens_cine(out, buf, sc, S, rays=0.55, blo=0.7, aperture=18, ca=0.0015, vig=0.4, gr=0.028, flare=0.3, streak=0.2, maxr=8)
    return filmic(out, exposure=1.05, sat=1.1)


# ================================================================== 3. WOODCUT CHRONICLE
def style_woodcut(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    img = buf['img']
    lum = luminance(img)
    lo, hi = np.percentile(lum, 1.5), np.percentile(lum, 99.5)
    t = np.clip((lum - lo) / (hi - lo + 1e-6), 0, 1)
    dark = (1 - t) ** 1.05
    ang = hatch_angle_map(buf, sc, 0)
    sp = 6.0 * S + 1.2
    s1 = stripes(H, W, ang, sp, warp=3.5, seed=31, S=S)
    s2 = stripes(H, W, ang + math.radians(62), sp * 1.15, warp=3.5, seed=32, S=S)
    ink = (s1 < dark * 1.08).astype(np.float32)
    ink = np.maximum(ink, (s2 < np.clip(dark - 0.55, 0, 1) * 1.6).astype(np.float32))
    ink[dark > 0.93] = 1.0
    # carved edges
    e = edges_from_id(buf, 1)
    e = cv2.dilate(e, np.ones((max(2, int(3 * S)), max(2, int(3 * S))), np.uint8))
    ink = np.maximum(ink, e)
    # rough the cuts and leave chisel specks in solid black
    rough = value_noise(H, W, 2.5 * S + 0.5, 33)
    ink = np.where((ink > 0.5) & (rough > 0.93) & (dark < 0.97), 0.0, ink)
    ink = cv2.GaussianBlur(ink, (0, 0), 0.55 * S + 0.2)
    ink = smoothstep(0.35, 0.65, ink)
    # rain as carved lines
    parts = make_particles(sc)
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a, z) in parts['rain'][::3]:
            cv2.line(rl, (int(x0 * S * 16), int(y0 * S * 16)), (int(x1 * S * 16), int(y1 * S * 16)), 1.0, max(1, int(1.2 * S)), cv2.LINE_AA, 4)
        ink = np.where(dark > 0.5, ink * (1 - rl * 0.9), np.maximum(ink, rl * 0.8))
    pap = paper(H, W, (0.9, 0.86, 0.76), fiber=0.05, S=S, seed=34)
    black = np.array([0.07, 0.065, 0.06], np.float32)
    out = pap * (1 - ink[..., None]) + black * ink[..., None]
    # second block: vermilion for fire and light, slightly off register
    em = emissive_mask(buf)
    warm = cv2.GaussianBlur(em, (0, 0), 3 * S)
    for l in sc.lights:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d2 = ((xx - l.x * S) ** 2 + (yy - l.y * S) ** 2) / (l.r * 0.9 * S) ** 2
        warm = np.maximum(warm, np.exp(-d2) * min(l.I, 1.2) * 0.8)
    warm = (warm > 0.25).astype(np.float32) * (0.85 + 0.15 * (value_noise(H, W, 40 * S, 35, cy=3 * S)))
    M = np.float32([[1, 0, 2.5 * S], [0, 1, -1.5 * S]])
    warm = cv2.warpAffine(warm, M, (W, H))
    red = np.array([0.78, 0.2, 0.12], np.float32)
    out = out * (1 - warm[..., None] * (1 - ink[..., None]) * 0.85) + red * pap * warm[..., None] * (1 - ink[..., None]) * 0.85
    out = vignette(out, 0.12, col=(0.6, 0.55, 0.45))
    return np.clip(out, 0, 1)


# ================================================================== 4. CANDLELIT OIL
def style_oil(sc, W, H, buf=None, work=720):
    WW, HH = work, work * 16 // 9
    b2 = base_render(sc, WW, HH)
    S2 = b2['S']
    ref = b2['img'].copy()
    parts = make_particles(sc)
    ref = draw_particles(ref, parts, S2, lights=sc.lights)
    ref = filmic(ref, exposure=1.25, contrast=1.08, sat=1.15, gamma=(1.0, 0.98, 0.95))
    r = rng(51)
    canvas = np.ones_like(ref) * np.array([0.22, 0.16, 0.11], np.float32)
    height = np.zeros((HH, WW), np.float32)
    lum_ref = luminance(ref)
    for R in (14, 8, 4, 2):
        blur = cv2.GaussianBlur(ref, (0, 0), R * 0.6)
        lb = luminance(blur)
        gx = cv2.Sobel(lb, cv2.CV_32F, 1, 0, ksize=3)
        gy = cv2.Sobel(lb, cv2.CV_32F, 0, 1, ksize=3)
        gm = np.sqrt(gx * gx + gy * gy)
        diff = np.abs(canvas - blur).sum(2)
        thr = 0.08 if R > 2 else 0.11
        cells = []
        for y in range(0, HH, R):
            for x in range(0, WW, R):
                y1, x1 = min(y + R, HH), min(x + R, WW)
                region = diff[y:y1, x:x1]
                if region.mean() > thr:
                    k = np.argmax(region)
                    cells.append((y + k // (x1 - x), x + k % (x1 - x)))
        r.shuffle(cells)
        for (cy, cx) in cells:
            col = blur[cy, cx] * (1 + r.normal(0, 0.035, 3)).astype(np.float32)
            pts = [(cx, cy)]
            x, y = float(cx), float(cy)
            dxp, dyp = 0.0, 0.0
            L = 10 if R > 2 else 5
            for step in range(L):
                xi, yi = int(min(max(x, 0), WW - 1)), int(min(max(y, 0), HH - 1))
                if step > 1 and np.abs(blur[yi, xi] - col).sum() > 0.16:
                    break
                if gm[yi, xi] < 1e-3:
                    break
                dx, dy = -gy[yi, xi], gx[yi, xi]
                if dxp * dx + dyp * dy < 0:
                    dx, dy = -dx, -dy
                n = math.hypot(dx, dy) + 1e-9
                dx, dy = dx / n, dy / n
                if step:
                    dx, dy = 0.6 * dx + 0.4 * dxp, 0.6 * dy + 0.4 * dyp
                    n = math.hypot(dx, dy) + 1e-9
                    dx, dy = dx / n, dy / n
                x, y = x + dx * R, y + dy * R
                pts.append((x, y))
                dxp, dyp = dx, dy
            q = (np.array(pts) * 16).astype(np.int32)
            th = max(1, int(R * 1.15))
            cv2.polylines(canvas, [q], False, tuple(float(c) for c in col), th, cv2.LINE_AA, 4)
            cv2.polylines(height, [q], False, float(0.6 + 0.4 * r.random()), max(1, th - 1), cv2.LINE_AA, 4)
    # impasto light
    hb = cv2.GaussianBlur(height, (0, 0), 0.8)
    bristle = value_noise(HH, WW, 1.5, 52, cy=1.5)
    hb = hb + bristle * 0.15
    em = cv2.Sobel(hb, cv2.CV_32F, 1, 0, ksize=3) * -0.6 + cv2.Sobel(hb, cv2.CV_32F, 0, 1, ksize=3) * -0.6
    canvas = canvas * (1 + np.clip(em, -0.4, 0.4)[..., None] * 0.35)
    img = cv2.resize(canvas, (W, H), interpolation=cv2.INTER_CUBIC)
    S = W / DW
    weave = (np.sin(np.mgrid[0:H, 0:W][1] * 1.9) * np.sin(np.mgrid[0:H, 0:W][0] * 1.9)).astype(np.float32)
    img *= (1 + weave * 0.02)[..., None]
    bufd = base_render(sc, W, H) if buf is None else buf
    em_m = emissive_mask(bufd)
    img = bloom(img, thr=0.7, strength=0.45, S=S, tint=(1.0, 0.8, 0.6))
    if sc.sun is not None:
        lum = luminance(img)
        src = img * (smoothstep(0.6, 1.1, lum) * (bufd['depth'] < 0.3))[..., None]
        img = godrays(img, src, sc.sun[0], sc.sun[1], strength=0.35, S=S)
    img = vignette(img, 0.45, col=(0.05, 0.03, 0.02))
    img = grain(img, 0.015)
    return np.clip(img * np.array([1.03, 1.0, 0.94], np.float32), 0, 1)


# ================================================================== 5. UKIYO-E
UKI = np.array([[0.11, 0.13, 0.2], [0.17, 0.27, 0.44], [0.36, 0.52, 0.66], [0.7, 0.78, 0.8], [0.93, 0.88, 0.76],
                [0.86, 0.36, 0.22], [0.92, 0.62, 0.36], [0.55, 0.4, 0.26], [0.33, 0.22, 0.16], [0.47, 0.55, 0.38],
                [0.64, 0.6, 0.52], [0.2, 0.17, 0.16], [0.97, 0.85, 0.55]], np.float32)


def style_ukiyoe(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    lit = filmic(buf['img'], exposure=1.4, sat=1.2)
    alb = buf['alb'] * 0.55 + lit * 0.45
    # flatten within each object, keep a two-step value split (bokashi-like)
    lab = cv2.cvtColor(np.clip(alb, 0, 1).astype(np.float32), cv2.COLOR_RGB2Lab)
    pal_lab = cv2.cvtColor(UKI[None], cv2.COLOR_RGB2Lab)[0]
    d = ((lab[..., None, :] - pal_lab[None, None]) ** 2 * np.array([0.6, 1.0, 1.0], np.float32)).sum(-1)
    q = UKI[np.argmin(d, -1)]
    q = cv2.medianBlur((q * 255).astype(np.uint8), max(3, int(5 * S) | 1)).astype(np.float32) / 255
    # sky and water bokashi: graded bands
    sky = buf['id'] < 0
    grad = np.linspace(0, 1, H, dtype=np.float32)[:, None]
    top = np.array([0.12, 0.17, 0.33], np.float32)
    if sc.mood == 'dusk':
        top = np.array([0.4, 0.22, 0.32], np.float32)
    bok = np.clip((0.42 - grad) / 0.42, 0, 1) ** 1.3
    q = np.where(sky[..., None], q * (1 - bok[..., None] * 0.85) + top * bok[..., None] * 0.85, q)
    # stars stay as white dots
    lum = luminance(buf['img'])
    stars = (sky & (lum > 0.75)).astype(np.float32)
    q = q * (1 - stars[..., None]) + np.array([0.97, 0.94, 0.85], np.float32) * stars[..., None]
    # wood grain and baren texture
    grain_ = value_noise(H, W, 90 * S, 61, cy=2.2 * S)
    q *= (0.94 + 0.1 * grain_)[..., None]
    q *= (0.97 + 0.06 * fbm(H, W, 14 * S, 3, 62))[..., None]
    # key block
    e = edges_from_id(buf, 1)
    e = cv2.dilate(e, np.ones((max(2, int(3 * S)), max(2, int(3 * S))), np.uint8)).astype(np.float32)
    e = cv2.GaussianBlur(e, (0, 0), 0.6 * S)
    M = np.float32([[1, 0, 1.5 * S], [0, 1, 1.0 * S]])
    q = cv2.warpAffine(q, M, (W, H), borderMode=cv2.BORDER_REFLECT)
    keycol = np.array([0.12, 0.11, 0.13], np.float32)
    out = q * (1 - e[..., None] * 0.92) + keycol * e[..., None] * 0.92
    parts = make_particles(sc)
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a, z) in parts['rain'][::2]:
            L = 2.4
            cv2.line(rl, (int(x0 * S * 16), int(y0 * S * 16)), (int((x0 + (x1 - x0) * L) * S * 16), int((y0 + (y1 - y0) * L) * S * 16)),
                     1.0, 1, cv2.LINE_AA, 4)
        out = out * (1 - rl[..., None] * 0.75) + keycol * rl[..., None] * 0.75
    if parts['embers']:
        for (x, y, r_, b) in parts['embers']:
            cv2.circle(out, (int(x * S), int(y * S)), max(1, int(r_ * S)), (0.92, 0.45, 0.2), -1, cv2.LINE_AA)
    pap = paper(H, W, (1.0, 0.97, 0.9), fiber=0.08, mottle=0.04, S=S, seed=63)
    out = out * pap
    out = vignette(out, 0.15, col=(0.55, 0.48, 0.4))
    return np.clip(out, 0, 1)


# ================================================================== 6. PAPER DIORAMA (macro lens)
def style_paper(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    from core import sky_render, paste
    sky = sky_render(sc, W, H, S)
    sky = cv2.GaussianBlur(sky, (0, 0), 6 * S)
    out = sky * 0.95
    pap_tex = 0.94 + 0.1 * fbm(H, W, 5 * S, 3, 71)
    kx, ky = sc.key_dir
    items = sorted(enumerate(sc.items), key=lambda t: (t[1].z, t[0]))
    layers = {}
    for idx, it in items:
        if idx not in buf['masks']:
            continue
        key = round(it.z * 14) / 14
        layers.setdefault(key, []).append((idx, it))
    acc_shadow = np.zeros((H, W), np.float32)
    for key in sorted(layers):
        lay = np.zeros((H, W), np.float32)
        colimg = np.zeros((H, W, 3), np.float32)
        emit_l = np.zeros((H, W), np.float32)
        for idx, it in layers[key]:
            x0, y0, m = buf['masks'][idx]
            sl = paste(lay, x0, y0, m)
            if sl is None:
                continue
            (dy, dx), (sy_, sx_) = sl
            a = m[sy_, sx_] * min(it.alpha * 1.4, 1.0)
            c = np.array(it.col, np.float32)
            lum_c = float(luminance(c[None, None])[0, 0])
            # paper colours: lift darks, keep hue, matte
            if sc.mood == 'dusk':
                c = c * 0.85 + lum_c * 0.05 + 0.05
            else:
                c = c * 0.55 + lum_c * 0.15 + 0.12
            if sc.mood in ('night', 'storm'):
                c = c * np.array([0.72, 0.76, 0.95], np.float32)
            if it.emit > 0:
                c = np.array(it.col, np.float32) * 1.3
                emit_l[dy, dx] = np.maximum(emit_l[dy, dx], a)
            colimg[dy, dx] = colimg[dy, dx] * (1 - a[..., None]) + c * a[..., None]
            lay[dy, dx] = np.maximum(lay[dy, dx], a)
        # shadow cast by this layer onto what is behind (already in out)
        off = 10 * S
        M = np.float32([[1, 0, -kx * off * 1.4], [0, 1, -ky * off * 1.4]])
        sh = cv2.warpAffine(lay, M, (W, H))
        sh = cv2.GaussianBlur(sh, (0, 0), 9 * S)
        out = out * (1 - sh[..., None] * 0.45)
        # lit by the lights, edge highlight
        light = np.ones((H, W), np.float32) * 0.85
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        warm = np.zeros((H, W, 3), np.float32)
        for l in sc.lights:
            d2 = ((xx - l.x * S) ** 2 + (yy - l.y * S) ** 2) / (l.r * 1.5 * S) ** 2
            warm += l.col * (l.I * 0.5 * np.exp(-d2))[..., None]
        er = cv2.erode(lay, np.ones((3, 3), np.uint8))
        edge = np.clip(lay - er, 0, 1)
        Mx = np.float32([[1, 0, kx * 2 * S], [0, 1, ky * 2 * S]])
        lit_edge = np.clip(edge - cv2.warpAffine(edge, Mx, (W, H)), 0, 1)
        col_l = colimg * pap_tex[..., None] * (light[..., None] + warm)
        col_l += lit_edge[..., None] * 0.25
        col_l = col_l * (1 - emit_l[..., None]) + colimg * emit_l[..., None] * 1.2
        out = out * (1 - lay[..., None]) + col_l * lay[..., None]
    for l in sc.lights:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d2 = ((xx - l.x * S) ** 2 + (yy - l.y * S) ** 2) / (l.r * 0.8 * S) ** 2
        out += l.col * (0.22 * l.I * np.exp(-d2))[..., None]
    parts = make_particles(sc)
    if parts['rain']:
        parts['rain'] = parts['rain'][::3]
    out = draw_particles(out, parts, S, lights=sc.lights, rain_col=(0.6, 0.62, 0.7))
    out = lens_cine(out, buf, sc, S, rays=0.25, blo=0.55, aperture=55, maxr=22, ca=0.002, vig=0.42, gr=0.02, flare=0.0, streak=0.0)
    return filmic(out, exposure=1.1, sat=1.05)


# ================================================================== 7. STAINED GLASS
def style_glass(sc, W, H, buf=None):
    from skimage.segmentation import slic
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    src = filmic(buf['img'], exposure=1.5, sat=1.4)
    src = src * 0.7 + buf['alb'] * 0.3
    small = cv2.resize(src, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    seg = slic(small, n_segments=1100, compactness=14, start_label=0, channel_axis=-1)
    seg = cv2.resize(seg.astype(np.int32).astype(np.float32), (W, H), interpolation=cv2.INTER_NEAREST).astype(np.int64)
    idm = buf['id'].astype(np.int64) + 1
    lab = seg * 4096 + idm
    _, lab = np.unique(lab, return_inverse=True)
    lab = lab.reshape(H, W)
    n = lab.max() + 1
    cnt = np.bincount(lab.ravel(), minlength=n).astype(np.float32) + 1e-6
    mean = np.stack([np.bincount(lab.ravel(), weights=src[..., c].ravel(), minlength=n) / cnt for c in range(3)], 1)
    # jewel tones: saturate and deepen
    lumv = mean @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    mean = lumv[:, None] + (mean - lumv[:, None]) * 1.6
    mean = np.clip(mean, 0.02, 1.2)
    r = rng(81)
    mean *= (0.85 + 0.3 * r.random((n, 1))).astype(np.float32)
    glass = mean[lab].astype(np.float32)
    # piece shading: brighter centre, darker rims; streaks and seeds
    edges = np.zeros((H, W), np.float32)
    edges[:, 1:] += lab[:, 1:] != lab[:, :-1]
    edges[1:, :] += lab[1:, :] != lab[:-1, :]
    edges = np.clip(edges, 0, 1)
    dist = cv2.distanceTransform((1 - edges).astype(np.uint8), cv2.DIST_L2, 3)
    shade = np.clip(dist / (9 * S), 0, 1) ** 0.5
    glass *= (0.55 + 0.6 * shade)[..., None]
    streak = value_noise(H, W, 60 * S, 82, cy=4 * S)
    glass *= (0.85 + 0.3 * streak)[..., None]
    seeds = (value_noise(H, W, 1.8 * S + 0.4, 83) > 0.9).astype(np.float32)
    glass += seeds[..., None] * 0.08
    # lead cames
    lead = cv2.dilate(edges, np.ones((max(3, int(5 * S)), max(3, int(5 * S))), np.uint8)).astype(np.float32)
    lead = cv2.GaussianBlur(lead, (0, 0), 0.7 * S)
    bead = np.clip(1 - np.abs(cv2.GaussianBlur(edges, (0, 0), 1.0 * S) * 3 - 1), 0, 1)
    leadcol = np.array([0.06, 0.06, 0.065], np.float32)
    out = glass * (1 - lead[..., None]) + (leadcol + bead[..., None] * 0.12) * lead[..., None]
    # saddle bars
    for yb in np.arange(320, DH, 480):
        cv2.rectangle(out, (0, int(yb * S)), (W, int((yb + 9) * S)), (0.05, 0.05, 0.055), -1)
    # grisaille painting on figures: their own edges drawn finer
    e = edges_from_id(buf, 1) * (buf['depth'] > 0.5)
    out *= (1 - cv2.GaussianBlur(e, (0, 0), 0.6 * S) * 0.6)[..., None]
    out = bloom(out, thr=0.65, strength=0.75, S=S)
    if sc.sun is not None:
        lum = luminance(out)
        srcg = out * smoothstep(0.7, 1.1, lum)[..., None]
        out = godrays(out, srcg, sc.sun[0], sc.sun[1], strength=0.3, S=S)
    out = vignette(out, 0.3)
    return filmic(out, exposure=1.2, sat=1.0)


# ================================================================== 8. GILDED MOSAIC
def style_mosaic(sc, W, H, buf=None):
    from scipy.spatial import cKDTree
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    src = filmic(buf['img'], exposure=1.4, sat=1.15)
    r = rng(91)
    sp = 12 * S
    gy, gx = np.mgrid[0:H:sp, 0:W:sp]
    pts = np.stack([gx.ravel() + r.uniform(-sp * 0.35, sp * 0.35, gx.size), gy.ravel() + r.uniform(-sp * 0.35, sp * 0.35, gx.size)], 1)
    e = edges_from_id(buf, 1)
    ey, ex = np.nonzero(e)
    pick = r.random(len(ex)) < 0.06
    pts = np.vstack([pts, np.stack([ex[pick] + r.normal(0, 1.5, pick.sum()), ey[pick] + r.normal(0, 1.5, pick.sum())], 1)])
    tree = cKDTree(pts)
    yy, xx = np.mgrid[0:H, 0:W]
    _, lab = tree.query(np.stack([xx.ravel(), yy.ravel()], 1), workers=2)
    lab = lab.reshape(H, W)
    n = len(pts)
    cnt = np.bincount(lab.ravel(), minlength=n).astype(np.float32) + 1e-6
    mean = np.stack([np.bincount(lab.ravel(), weights=src[..., c].ravel(), minlength=n) / cnt for c in range(3)], 1)
    skyfrac = np.bincount(lab.ravel(), weights=(buf['id'] < 0).ravel().astype(np.float32), minlength=n) / cnt
    # tessera palette
    pal = np.array([[0.93, 0.9, 0.82], [0.75, 0.7, 0.62], [0.5, 0.45, 0.4], [0.25, 0.22, 0.22], [0.08, 0.08, 0.1],
                    [0.12, 0.2, 0.42], [0.25, 0.38, 0.62], [0.55, 0.15, 0.12], [0.78, 0.38, 0.2], [0.2, 0.35, 0.26],
                    [0.55, 0.6, 0.45], [0.62, 0.45, 0.3], [0.42, 0.28, 0.2]], np.float32)
    dd = ((mean[:, None, :] - pal[None]) ** 2).sum(-1)
    tcol = pal[np.argmin(dd, 1)] * (0.9 + 0.2 * r.random((n, 1))).astype(np.float32)
    gold = np.array([0.95, 0.74, 0.36], np.float32)
    gmask = skyfrac > 0.5
    gl = (0.7 + 0.5 * r.random((n, 1))).astype(np.float32)
    lum_sky = mean @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    tcol = np.where(gmask[:, None], gold * gl * (0.7 + 0.5 * np.clip(lum_sky[:, None] * 1.5, 0, 1)), tcol)
    img = tcol[lab].astype(np.float32)
    # grout and bevel
    edges = np.zeros((H, W), np.float32)
    edges[:, 1:] += lab[:, 1:] != lab[:, :-1]
    edges[1:, :] += lab[1:, :] != lab[:-1, :]
    dist = cv2.distanceTransform((edges == 0).astype(np.uint8), cv2.DIST_L2, 3)
    grout = smoothstep(0.6 * S + 0.3, 1.6 * S + 0.6, dist)
    gxh = cv2.Sobel(dist, cv2.CV_32F, 1, 0, ksize=3)
    gyh = cv2.Sobel(dist, cv2.CV_32F, 0, 1, ksize=3)
    bevel = np.clip(-(gxh * 0.7 + gyh * 0.7) * 0.12, -0.25, 0.25) * (dist < 4 * S)
    img = img * (1 + bevel[..., None])
    img = img * grout[..., None] + np.array([0.28, 0.26, 0.24], np.float32) * (1 - grout[..., None])
    # gold glints
    tilt = (r.random(n) > 0.86).astype(np.float32)
    glint = tilt[lab] * gmask[lab] * grout
    img += glint[..., None] * np.array([0.4, 0.3, 0.15], np.float32)
    img = bloom(img, thr=0.8, strength=0.5, S=S, tint=(1.0, 0.85, 0.6))
    img = vignette(img, 0.3)
    img = grain(img, 0.012)
    return np.clip(img, 0, 1)


# ================================================================== 9. CHARCOAL AND CHALK
def style_charcoal(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    img = buf['img']
    parts = make_particles(sc)
    img = draw_particles(img.copy(), parts, S, lights=sc.lights)
    lum = luminance(img)
    lo, hi = np.percentile(lum, 1.5), np.percentile(lum, 99.7)
    t = np.clip((lum - lo) / (hi - lo + 1e-6), 0, 1)
    tooth = value_noise(H, W, 1.4 * S + 0.4, 101)
    tooth2 = fbm(H, W, 6 * S, 3, 102)
    ang = hatch_angle_map(buf, sc, 0) + math.radians(35)
    st = stripes(H, W, ang, 7 * S + 1, warp=6, seed=103, S=S)
    dark = (1 - t) ** 1.2
    char = smoothstep(0.15, 0.95, dark + (0.5 - st) * 0.35)
    char = char * smoothstep(0.15, 0.6, tooth * 0.6 + tooth2 * 0.6 + dark * 0.4)
    smudge = cv2.GaussianBlur(dark, (0, 0), 6 * S) * 0.45
    char = np.clip(np.maximum(char, smudge), 0, 1)
    e = edges_from_id(buf, 1)
    e = cv2.GaussianBlur(cv2.dilate(e, np.ones((2, 2), np.uint8)), (0, 0), 0.8 * S)
    brk = value_noise(H, W, 14 * S, 104) > 0.3
    char = np.clip(char + e * 0.9 * brk * (buf['depth'] > 0.3), 0, 1)
    chalk = smoothstep(0.62, 0.95, t) * smoothstep(0.25, 0.7, tooth * 0.7 + tooth2 * 0.5)
    pap = paper(H, W, (0.6, 0.56, 0.5), fiber=0.04, mottle=0.06, S=S, seed=105)
    out = pap * (1 - char[..., None] * 0.92) + np.array([0.05, 0.045, 0.045], np.float32) * char[..., None] * 0.92
    warmchalk = np.array([0.98, 0.94, 0.85], np.float32)
    em = cv2.GaussianBlur(emissive_mask(buf), (0, 0), 4 * S)
    out = out * (1 - chalk[..., None] * 0.85) + warmchalk * chalk[..., None] * 0.85
    out = out * (1 - em[..., None] * 0.5) + np.array([0.95, 0.55, 0.25], np.float32) * em[..., None] * 0.5
    out = vignette(out, 0.25, col=(0.3, 0.28, 0.25))
    return np.clip(out, 0, 1)


# ================================================================== 10. WATERCOLOUR AND INK
def style_watercolor(sc, W, H, buf=None):
    buf = buf or base_render(sc, W, H)
    S = buf['S']
    img = filmic(buf['img'], exposure=1.6, sat=1.1)
    parts = make_particles(sc)
    base = cv2.edgePreservingFilter((np.clip(img, 0, 1) * 255).astype(np.uint8), flags=1, sigma_s=40, sigma_r=0.35).astype(np.float32) / 255
    # pigment: pull towards paper white in lights, granulate in darks
    pap = paper(H, W, (0.97, 0.95, 0.9), fiber=0.04, mottle=0.03, S=S, seed=111)
    lum = luminance(base)
    gran = fbm(H, W, 3 * S, 3, 112)
    wet = fbm(H, W, 120 * S, 4, 113)
    pig = 1 - base
    pig *= (0.85 + 0.35 * gran[..., None] * (lum[..., None] < 0.6)) * (0.88 + 0.24 * wet[..., None])
    # edge darkening of washes
    bl = cv2.GaussianBlur(pig, (0, 0), 3 * S)
    pig = np.clip(pig + np.clip(pig - bl, 0, None) * 1.4, 0, 1)
    out = pap * (1 - pig)
    # pen line
    e = edges_from_id(buf, 1) * (buf['depth'] > 0.25)
    wob = value_noise(H, W, 30 * S, 114) > 0.25
    e = cv2.GaussianBlur(e * wob, (0, 0), 0.6 * S)
    out *= (1 - np.clip(e * 1.1, 0, 0.8))[..., None] * np.array([1, 0.97, 0.95], np.float32) + 0.0
    if parts['rain']:
        rl = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a, z) in parts['rain'][::3]:
            cv2.line(rl, (int(x0 * S * 16), int(y0 * S * 16)), (int(x1 * S * 16), int(y1 * S * 16)), float(a), 1, cv2.LINE_AA, 4)
        out *= (1 - rl * 0.4)[..., None]
    out = draw_particles(out, dict(rain=[], embers=parts['embers'], dust=parts['dust']), S, lights=sc.lights)
    em = cv2.GaussianBlur(emissive_mask(buf), (0, 0), 10 * S)
    out = out + em[..., None] * np.array([0.5, 0.3, 0.1], np.float32) * 0.6
    out = vignette(out, 0.15, col=(0.7, 0.65, 0.58))
    return np.clip(out, 0, 1)


STYLES = dict(ink=style_ink, shadow=style_shadow, woodcut=style_woodcut, oil=style_oil, ukiyoe=style_ukiyoe,
              paper=style_paper, glass=style_glass, mosaic=style_mosaic, charcoal=style_charcoal, watercolor=style_watercolor)
