"""Procedural surfaces and light for the film plates: stone, wood, paper, cloth, skin, metal, glass; silhouettes
inflated into relief and lit by point lights (candles, lanterns) and a cool key (moonlight). Everything returns
float32 images in 0..1 (or HDR above 1 for emitters) that the oil painter then turns into brushwork."""
import math
import numpy as np
import cv2
from scipy.spatial import cKDTree


# ------------------------------------------------------------------ noise
def vnoise(h, w, cell, seed):
    r = np.random.default_rng(seed)
    gh, gw = int(h / cell) + 3, int(w / cell) + 3
    g = r.random((gh, gw)).astype(np.float32)
    return cv2.resize(g, (int(gw * cell), int(gh * cell)), interpolation=cv2.INTER_CUBIC)[:h, :w]


def fbm(h, w, cell, octaves=5, seed=0, gain=0.5, lac=2.0):
    out = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        c = max(cell / (lac ** o), 1.5)
        out += vnoise(h, w, c, seed + o * 17) * amp
        tot += amp; amp *= gain
    return out / tot


def ridged(h, w, cell, octaves=4, seed=0):
    n = fbm(h, w, cell, octaves, seed)
    return 1 - np.abs(n - 0.5) * 2


def warp(img, dx, dy):
    h, w = dx.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    return cv2.remap(img, xx + dx, yy + dy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


# ------------------------------------------------------------------ relief and light
def normals(hmap, strength=1.0):
    gx = cv2.Sobel(hmap, cv2.CV_32F, 1, 0, ksize=3) * strength
    gy = cv2.Sobel(hmap, cv2.CV_32F, 0, 1, ksize=3) * strength
    n = np.stack([-gx, -gy, np.ones_like(gx)], -1)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def inflate(mask, radius, power=0.5):
    """A silhouette becomes a dome: height from the distance to its edge (so any shape can be lit like a solid)."""
    m = (mask > 0.5).astype(np.uint8)
    d = cv2.distanceTransform(m, cv2.DIST_L2, 5).astype(np.float32)
    h = np.clip(d / max(radius, 1e-3), 0, 1) ** power
    return cv2.GaussianBlur(h, (0, 0), max(radius * 0.08, 0.6))


class PLight:
    """A point light in plate pixels: position (x, y) and height z above the surface plane (pixels)."""
    def __init__(self, x, y, z, col, I=1.0, r=600.0, spec=0.0):
        self.x, self.y, self.z, self.col, self.I, self.r, self.spec = x, y, z, np.array(col, np.float32), I, r, spec


def light(n, lights, amb=(0.05, 0.05, 0.06), key=None, key_col=(0.3, 0.35, 0.5), shininess=24.0, spec=0.0, y0=0, x0=0,
          wrap=0.0, occl=None):
    """Lambert (+ optional wrap and Blinn specular) for point lights and one directional key. n: HxWx3 normals."""
    h, w = n.shape[:2]
    yy, xx = np.mgrid[y0:y0 + h, x0:x0 + w].astype(np.float32)
    out = np.zeros((h, w, 3), np.float32) + np.array(amb, np.float32)
    sp = np.zeros((h, w, 3), np.float32)
    for L in lights:
        lx, ly, lz = L.x - xx, L.y - yy, np.full_like(xx, L.z)
        d = np.sqrt(lx * lx + ly * ly + lz * lz) + 1e-6
        lx, ly, lz = lx / d, ly / d, lz / d
        ndl = n[..., 0] * lx + n[..., 1] * ly + n[..., 2] * lz
        ndl = np.clip((ndl + wrap) / (1 + wrap), 0, 1)
        fall = L.I / (1 + (d / L.r) ** 2)
        if occl is not None:
            fall = fall * occl
        out += (ndl * fall)[..., None] * L.col
        if spec > 0 or L.spec > 0:
            hx, hy, hz = lx, ly, lz + 1
            hn = np.sqrt(hx * hx + hy * hy + hz * hz) + 1e-6
            ndh = np.clip((n[..., 0] * hx + n[..., 1] * hy + n[..., 2] * hz) / hn, 0, 1)
            sp += ((ndh ** shininess) * fall * max(spec, L.spec))[..., None] * L.col
    if key is not None:
        kx, ky, kz = key
        kn = math.sqrt(kx * kx + ky * ky + kz * kz)
        ndl = np.clip((n[..., 0] * kx + n[..., 1] * ky + n[..., 2] * kz) / kn, 0, 1)
        out += ndl[..., None] * np.array(key_col, np.float32)
    return out, sp


# ------------------------------------------------------------------ materials
def stone_wall(h, w, seed=0, course=95, length=150, mortar=5.0, col=(0.42, 0.38, 0.33), var=0.12, rough=1.0):
    """Coursed rubble masonry: irregular blocks in rough rows. Returns (albedo, height)."""
    r = np.random.default_rng(seed)
    pts, rows = [], int(h / course) + 3
    for ri in range(-1, rows):
        y = ri * course + r.normal(0, course * 0.08)
        x = r.uniform(-length, 0)
        while x < w + length:
            L = length * r.uniform(0.6, 1.4)
            pts.append((x + L / 2, y + course / 2 + r.normal(0, course * 0.12)))
            x += L
    pts = np.array(pts, np.float32)
    # anisotropic distance: stretch x so blocks are wider than tall
    sx = course / length
    tree = cKDTree(np.stack([pts[:, 0] * sx, pts[:, 1]], 1))
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    jx = (fbm(h, w, 40, 3, seed + 1) - 0.5) * course * 0.5
    jy = (fbm(h, w, 40, 3, seed + 2) - 0.5) * course * 0.5
    q = np.stack([(xx + jx).ravel() * sx, (yy + jy).ravel()], 1)
    d, idx = tree.query(q, k=2)
    edge = (d[:, 1] - d[:, 0]).reshape(h, w)
    cid = idx[:, 0].reshape(h, w)
    tint = r.normal(0, var, (len(pts), 3)).astype(np.float32)
    tint[:, 1:] = tint[:, :1] * 0.85 + tint[:, 1:] * 0.15
    alb = np.array(col, np.float32) * (1 + tint[cid])
    grit = fbm(h, w, 6, 3, seed + 3)
    stain = fbm(h, w, 300, 4, seed + 4)
    alb *= (0.85 + 0.3 * grit)[..., None]
    alb *= (0.8 + 0.35 * stain)[..., None]
    mort = np.clip(1 - edge / mortar, 0, 1)
    alb = alb * (1 - mort[..., None] * 0.55)
    bulge = np.clip(edge / (course * 0.35), 0, 1) ** 0.5
    height = bulge * (0.8 + 0.4 * fbm(h, w, 25, 4, seed + 5) * rough) - mort * 0.4
    return np.clip(alb, 0, 1).astype(np.float32), height.astype(np.float32)


def wood(h, w, seed=0, plank=180, col=(0.36, 0.24, 0.15), along='x', gap=3.0, var=0.18, knots=4):
    """Rough planks with grain; along='x' means the grain runs horizontally. Returns (albedo, height)."""
    r = np.random.default_rng(seed)
    hh, ww = (h, w) if along == 'x' else (w, h)
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    pid = (yy // plank).astype(np.int32)
    n = int(hh / plank) + 2
    ptint = r.normal(0, var, (n, 3)).astype(np.float32)
    off = r.uniform(0, 1000, n).astype(np.float32)
    lowf = fbm(hh, ww, 220, 3, seed + 1)
    grain_coord = (yy + lowf * 60) * 0.9
    g1 = np.sin(grain_coord * 0.35 + fbm(hh, ww, 90, 4, seed + 2) * 9) * 0.5 + 0.5
    streak = cv2.resize(r.random((max(2, hh // 3), max(2, ww // 120))).astype(np.float32), (ww, hh), interpolation=cv2.INTER_CUBIC)
    grain = 0.6 * g1 + 0.4 * streak
    alb = np.array(col, np.float32) * (1 + ptint[pid]) * (0.75 + 0.4 * grain)[..., None]
    for k in range(knots):
        cx, cy = r.uniform(0, ww), r.uniform(0, hh)
        rr = r.uniform(8, 22)
        dd = np.sqrt(((xx - cx) / 2.2) ** 2 + (yy - cy) ** 2)
        alb *= (1 - 0.45 * np.exp(-(dd / rr) ** 2))[..., None]
    py = yy - pid * plank
    edge = np.minimum(py, plank - py)
    gapm = np.clip(1 - edge / gap, 0, 1)
    alb *= (1 - 0.8 * gapm)[..., None]
    height = (0.5 + 0.3 * grain - gapm * 0.8 + 0.2 * np.clip(edge / 12, 0, 1)).astype(np.float32)
    wear = fbm(hh, ww, 140, 4, seed + 7)
    alb *= (0.85 + 0.25 * wear)[..., None]
    if along != 'x':
        alb, height = alb.transpose(1, 0, 2), height.T
    return np.clip(alb, 0, 1).astype(np.float32), np.ascontiguousarray(height).astype(np.float32)


def paper(h, w, seed=0, col=(0.86, 0.8, 0.66), age=0.5, folds=((0.5, 'h'),), deckle=6.0):
    """Rag paper: fibres, mottling, foxing, fold lines; returns (albedo, height, alpha with a soft deckle edge)."""
    r = np.random.default_rng(seed)
    alb = np.ones((h, w, 3), np.float32) * np.array(col, np.float32)
    mott = fbm(h, w, 120, 5, seed)
    fib = fbm(h, w, 3, 2, seed + 1)
    alb *= (0.9 + 0.16 * mott)[..., None] * (0.96 + 0.06 * fib)[..., None]
    # edges darker (handling, age)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    e = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    alb *= (1 - age * 0.25 * np.exp(-e / (0.06 * min(h, w))))[..., None]
    alb *= np.array([1.0, 0.97, 0.9], np.float32) ** (age * 2)
    # foxing spots
    for k in range(int(30 * age)):
        cx, cy, rr = r.uniform(0, w), r.uniform(0, h), r.uniform(2, 9)
        dd = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        alb *= (1 - 0.18 * np.exp(-(dd / rr) ** 2))[..., None] * np.array([1, 0.97, 0.92], np.float32) + \
               (1 - (1 - 0.18 * np.exp(-(dd / rr) ** 2))[..., None]) * 0
    height = 0.5 + 0.05 * fib + 0.05 * mott
    for pos, ori in folds:
        if ori == 'h':
            d = np.abs(yy - pos * h)
        else:
            d = np.abs(xx - pos * w)
        crease = np.exp(-(d / 2.0) ** 2)
        height = height - crease * 0.05 + np.exp(-((d - 4) / 6) ** 2) * 0.015
        alb *= (1 - crease * 0.025)[..., None]
    jag = (fbm(h, w, 6, 3, seed + 9) - 0.5) * deckle
    a = np.clip((e + jag) / 1.5, 0, 1)
    return np.clip(alb, 0, 1).astype(np.float32), height.astype(np.float32), a.astype(np.float32)


def cloth(h, w, seed=0, col=(0.8, 0.76, 0.68), fold_cell=60, folds=6):
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    hgt = np.zeros((h, w), np.float32)
    for k in range(folds):
        a = r.uniform(0, math.pi)
        fr = r.uniform(0.6, 1.6) / fold_cell
        ph = r.uniform(0, 6.28)
        hgt += np.sin((xx * math.cos(a) + yy * math.sin(a)) * fr * 6.28 + ph + fbm(h, w, 80, 3, seed + k) * 3) / folds
    weave = (np.sin(xx * 1.6) * np.sin(yy * 1.6)) * 0.03
    alb = np.ones((h, w, 3), np.float32) * np.array(col, np.float32) * (0.9 + 0.15 * fbm(h, w, 50, 4, seed + 20))[..., None]
    return alb, (hgt * 0.5 + 0.5 + weave).astype(np.float32)


# ------------------------------------------------------------------ helpers
def poly_mask(h, w, pts, ss=4):
    m = np.zeros((h * ss, w * ss), np.uint8)
    q = (np.asarray(pts, np.float32) * ss * 16).round().astype(np.int32)
    cv2.fillPoly(m, [q], 255, cv2.LINE_AA, shift=4)
    return cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA).astype(np.float32) / 255.0


def catmull(points, n=12, closed=True):
    p = np.asarray(points, np.float64)
    if closed:
        p = np.vstack([p[-1:], p, p[:2]])
    else:
        p = np.vstack([p[:1], p, p[-1:]])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(p[-2])
    return np.array(out, np.float32)


def over(dst, src_rgb, src_a):
    a = src_a[..., None]
    return dst * (1 - a) + src_rgb * a


def ellipse_pts(cx, cy, rx, ry, n=64, a0=0.0, a1=2 * math.pi, rot=0.0):
    t = np.linspace(a0, a1, n)
    x, y = rx * np.cos(t), ry * np.sin(t)
    c, s = math.cos(rot), math.sin(rot)
    return np.stack([cx + x * c - y * s, cy + x * s + y * c], 1).astype(np.float32)
