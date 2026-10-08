"""Core for the style-frame lookbook: geometry, noise, 2.5D scene, base render, lens effects.
Design space is 1080 x 1920 (9:16). Everything is drawn in that space and scaled at raster time."""
import math
import numpy as np
import cv2

DW, DH = 1080, 1920


def rng(seed):
    return np.random.default_rng(seed)


# ------------------------------------------------------------------ noise
def value_noise(h, w, cell, seed, cy=None):
    """Smooth value noise. cell = feature size in px (x); cy = feature size in y (anisotropic)."""
    cy = cell if cy is None else cy
    r = rng(seed)
    gw, gh = int(w / cell) + 4, int(h / cy) + 4
    g = r.random((gh, gw)).astype(np.float32)
    big = cv2.resize(g, (int(gw * cell), int(gh * cy)), interpolation=cv2.INTER_CUBIC)
    return big[:h, :w]


def fbm(h, w, cell, octaves=5, seed=0, gain=0.5, cy=None):
    tot = np.zeros((h, w), np.float32)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        c = max(cell / (2 ** o), 1.5)
        c2 = None if cy is None else max(cy / (2 ** o), 1.5)
        tot += amp * value_noise(h, w, c, seed + o * 101, c2)
        norm += amp
        amp *= gain
    return tot / norm


def fbm1d(n, seed, octaves=6, gain=0.5, base_cells=3):
    r = rng(seed)
    tot = np.zeros(n)
    amp, norm = 1.0, 0.0
    for o in range(octaves):
        cells = base_cells * 2 ** o
        g = r.random(cells + 2)
        xs = np.linspace(0, cells, n)
        i = np.clip(np.floor(xs).astype(int), 0, cells)
        f = xs - i
        f = f * f * (3 - 2 * f)
        tot += amp * (g[i] * (1 - f) + g[i + 1] * f)
        norm += amp
        amp *= gain
    return tot / norm


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a + 1e-9), 0, 1)
    return t * t * (3 - 2 * t)


# ------------------------------------------------------------------ geometry (design space)
def P(pts):
    return np.asarray(pts, np.float64)


def rect(x0, y0, x1, y1):
    return P([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])


def ellipse(cx, cy, rx, ry, n=48, a0=0.0, a1=2 * math.pi):
    full = abs(a1 - a0) >= 2 * math.pi - 1e-6
    t = np.linspace(a0, a1, n, endpoint=not full)
    return np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], 1)


def catmull(points, n=10, closed=False):
    Q = P(points)
    if closed:
        Q = np.vstack([Q[-1], Q, Q[0], Q[1]])
    else:
        Q = np.vstack([Q[0], Q, Q[-1]])
    out = []
    for i in range(1, len(Q) - 2):
        p0, p1, p2, p3 = Q[i - 1], Q[i], Q[i + 1], Q[i + 2]
        for t in np.linspace(0, 1, n, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    if not closed:
        out.append(Q[-2])
    return P(out)


def ridge(x0, x1, base, amp, seed, n=300, octaves=7, gain=0.55, ybottom=DH + 40, env=None, cells=3):
    xs = np.linspace(x0, x1, n)
    f = fbm1d(n, seed, octaves, gain, cells)
    f = (f - f.min()) / (f.max() - f.min() + 1e-9)
    if env is not None:
        f = f * env(np.linspace(0, 1, n))
    ys = base - amp * f
    pts = np.stack([xs, ys], 1)
    return np.vstack([pts, [(x1, ybottom), (x0, ybottom)]])


def T(poly, dx=0.0, dy=0.0, s=1.0, ox=0.0, oy=0.0, rot=0.0, sx=None, sy=None):
    """scale about (ox, oy), rotate (deg), then translate."""
    Q = P(poly).copy()
    sx = s if sx is None else sx
    sy = s if sy is None else sy
    Q[:, 0] = (Q[:, 0] - ox) * sx
    Q[:, 1] = (Q[:, 1] - oy) * sy
    if rot:
        a = math.radians(rot)
        c, s_ = math.cos(a), math.sin(a)
        Q = np.stack([Q[:, 0] * c - Q[:, 1] * s_, Q[:, 0] * s_ + Q[:, 1] * c], 1)
    Q[:, 0] += ox + dx
    Q[:, 1] += oy + dy
    return Q


def stroke_poly(pts, w0, w1=None, n=None):
    """A tapered ribbon polygon around a polyline (width w0 at start to w1 at end)."""
    Q = P(pts)
    if n:
        Q = catmull(Q, n)
    w1 = w0 if w1 is None else w1
    d = np.gradient(Q, axis=0)
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    w = np.linspace(w0, w1, len(Q))[:, None] / 2
    return np.vstack([Q + nrm * w, (Q - nrm * w)[::-1]])


# ------------------------------------------------------------------ scene
class Item:
    def __init__(self, polys=None, lines=None, z=0.5, col=(0.5, 0.5, 0.5), mat='solid', key=1.0, recv=1.0,
                 emit=0.0, outline=True, hatch=None, name='', shade=None, alpha=1.0, glow=0.0, wline=None,
                 detail=False):
        self.polys = [P(p) for p in (polys or [])]
        self.lines = [(P(p), w) for (p, w) in (lines or [])]
        self.z = z
        self.col = np.array(col, np.float32)
        self.mat = mat
        self.key = key          # exposure to the key light
        self.recv = recv        # how much point lights reach it
        self.emit = emit        # self light (windows, fire)
        self.outline = outline
        self.hatch = hatch      # preferred hatch angle in degrees (None = auto)
        self.name = name
        self.shade = shade      # optional (top_mult, bottom_mult) vertical shading
        self.alpha = alpha
        self.glow = glow        # extra glow around emissive items
        self.wline = wline      # for water: the reflection line y
        self.detail = detail    # small detail line (drawn as line in line styles)

    def bbox(self):
        pts = [p for p in self.polys] + [p for p, _ in self.lines]
        allp = np.vstack(pts)
        pad = max([w for _, w in self.lines], default=0) + 4
        return allp[:, 0].min() - pad, allp[:, 1].min() - pad, allp[:, 0].max() + pad, allp[:, 1].max() + pad


class Light:
    def __init__(self, x, y, col, I=1.0, r=200.0, z=0.5, flare=0.0, air=0.25):
        self.x, self.y, self.col, self.I, self.r, self.z = x, y, np.array(col, np.float32), I, r, z
        self.flare = flare      # lens flare strength
        self.air = air          # glow in the air (volumetric)


class Scene:
    def __init__(self, name):
        self.name = name
        self.items = []
        self.lights = []
        self.sky = {}
        self.amb = np.array([0.3, 0.3, 0.32], np.float32)
        self.key_col = np.array([0.6, 0.65, 0.8], np.float32)
        self.key_dir = (-0.5, -0.8)       # direction TO the key light (screen space)
        self.haze_col = np.array([0.4, 0.45, 0.55], np.float32)
        self.haze = 0.6
        self.haze_pow = 1.6
        self.fog = []          # dicts: y0, y1, z, col, dens, seed
        self.rain = None       # dict
        self.embers = None     # dict
        self.dust = None
        self.focus = 0.6       # depth in focus
        self.sun = None        # (x, y) for god rays
        self.mood = 'night'
        self.ink_bias = 0.0
        self.gold_bands = []   # for scroll styles: (y, height, seed)
        self.title = ''

    def add(self, *items):
        for it in items:
            self.items.append(it)
        return items[0] if len(items) == 1 else items


# ------------------------------------------------------------------ raster
def raster_item(it, S, SS=2):
    """Coverage mask of an item. Returns (x0, y0, mask float32) in output pixels."""
    bx0, by0, bx1, by1 = it.bbox()
    x0 = int(math.floor(bx0 * S)) - 1
    y0 = int(math.floor(by0 * S)) - 1
    x1 = int(math.ceil(bx1 * S)) + 2
    y1 = int(math.ceil(by1 * S)) + 2
    w, h = max(x1 - x0, 1), max(y1 - y0, 1)
    m = np.zeros((h * SS, w * SS), np.uint8)
    k = S * SS * 16.0
    for p in it.polys:
        q = ((p * S - (x0, y0)) * SS * 16.0).round().astype(np.int32)
        one = np.zeros_like(m)
        cv2.fillPoly(one, [q], 255, lineType=cv2.LINE_AA, shift=4)
        np.maximum(m, one, out=m)
    for p, wd in it.lines:
        q = ((p * S - (x0, y0)) * SS * 16.0).round().astype(np.int32)
        th = max(int(round(wd * S * SS)), 1)
        cv2.polylines(m, [q], False, 255, thickness=th, lineType=cv2.LINE_AA, shift=4)
    if SS > 1:
        m = cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA)
    return x0, y0, m.astype(np.float32) / 255.0


def paste(dst, x0, y0, src):
    """returns slices for overlapping region of src placed at (x0, y0) into dst (2D shapes)."""
    H, W = dst.shape[:2]
    h, w = src.shape[:2]
    ax0, ay0 = max(x0, 0), max(y0, 0)
    ax1, ay1 = min(x0 + w, W), min(y0 + h, H)
    if ax1 <= ax0 or ay1 <= ay0:
        return None
    return (slice(ay0, ay1), slice(ax0, ax1)), (slice(ay0 - y0, ay1 - y0), slice(ax0 - x0, ax1 - x0))


def gradient_stops(H, stops):
    ys = np.array([s[0] for s in stops]) * H
    cols = np.array([s[1] for s in stops], np.float32)
    yy = np.arange(H)
    return np.stack([np.interp(yy, ys, cols[:, c]) for c in range(3)], 1).astype(np.float32)


def sky_render(scene, W, H, S):
    sk = scene.sky
    grad = gradient_stops(H, sk.get('stops', [(0, (0.1, 0.12, 0.2)), (1, (0.4, 0.4, 0.5))]))
    img = np.repeat(grad[:, None, :], W, 1)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for g in sk.get('glow', []):
        x, y, rad, col, st = g
        d2 = ((xx - x * S) ** 2 + (yy - y * S) ** 2) / (rad * S) ** 2
        img += np.array(col, np.float32) * st * np.exp(-d2)[..., None]
    if sk.get('milky'):
        mx = sk['milky']   # (x0, y0, x1, y1, width, strength)
        x0, y0, x1, y1, wd, st = mx
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx, ny = -dy / L, dx / L
        dist = ((xx / S - x0) * nx + (yy / S - y0) * ny)
        band = np.exp(-(dist / wd) ** 2)
        n1 = fbm(H, W, 220 * S, 6, 77)
        n2 = fbm(H, W, 60 * S, 4, 78)
        neb = band * smoothstep(0.35, 0.8, n1 * 0.7 + n2 * 0.3)
        dark = band * smoothstep(0.55, 0.75, fbm(H, W, 90 * S, 5, 79)) * 0.6
        img += (st * (neb - dark * neb))[..., None] * np.array([0.55, 0.55, 0.62], np.float32)
    if sk.get('stars'):
        n, ymax = sk['stars']
        r = rng(5)
        sl = np.zeros((H, W), np.float32)
        xs = r.random(n) * W
        ys = r.random(n) * ymax * S
        if sk.get('milky'):
            x0, y0, x1, y1, wd, st = sk['milky']
            t = r.random(n // 2)
            off = r.normal(0, wd * 0.45, n // 2)
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            mxs = (x0 + dx * t - dy / L * off) * S
            mys = (y0 + dy * t + dx / L * off) * S
            xs = np.concatenate([xs, mxs])
            ys = np.concatenate([ys, mys])
        b = r.pareto(2.2, len(xs)) * 0.18 + 0.05
        b = np.clip(b, 0, 2.5)
        ok = (xs >= 0) & (xs < W) & (ys >= 0) & (ys < H)
        xi, yi = xs[ok].astype(int), ys[ok].astype(int)
        np.add.at(sl, (yi, xi), b[ok])
        sl = cv2.GaussianBlur(sl, (0, 0), 0.6 * S + 0.3) * 2.2 + cv2.GaussianBlur(sl, (0, 0), 2.2 * S) * 1.6
        img += np.array([0.9, 0.93, 1.0], np.float32) * sl[..., None]
    if sk.get('bright'):
        bl = np.zeros((H, W), np.float32)
        for (bx, by, bb) in sk['bright']:
            if 0 <= bx * S < W and 0 <= by * S < H:
                bl[int(by * S), int(bx * S)] += bb
        bl = cv2.GaussianBlur(bl, (0, 0), 0.9 * S + 0.3) * 6 + cv2.GaussianBlur(bl, (0, 0), 4 * S) * 3
        img += np.array([0.95, 0.96, 1.0], np.float32) * bl[..., None]
    if sk.get('moon'):
        x, y, rad, col = sk['moon']
        m = np.zeros((H, W), np.float32)
        cv2.circle(m, (int(x * S * 16), int(y * S * 16)), int(rad * S * 16), 1.0, -1, cv2.LINE_AA, 4)
        tex = 0.85 + 0.15 * fbm(H, W, 30 * S, 4, 9)
        img = img * (1 - m[..., None]) + (np.array(col, np.float32) * tex[..., None]) * m[..., None]
    for c in sk.get('clouds', []):
        # dict: y0, y1, cell, seed, cov, col_top, col_bot, dens, xstretch
        h0, h1 = int(c['y0'] * S), int(c['y1'] * S)
        hh = h1 - h0
        n = fbm(hh, W, c.get('cell', 260) * S, 6, c.get('seed', 1), cy=c.get('cell', 260) * S * c.get('ystretch', 0.45))
        cut = max(0, -h0)
        cov = c.get('cov', 0.5)
        m = smoothstep(cov, cov + c.get('soft', 0.18), n)
        env = np.sin(np.linspace(0, math.pi, hh))[:, None] ** c.get('envp', 0.8)
        m = m * env * c.get('dens', 1.0)
        # light from above: shade by local noise derivative
        shade = np.clip((n - np.roll(n, int(14 * S), 0)) * 6 + 0.5, 0, 1)
        top = np.array(c['col_top'], np.float32)
        bot = np.array(c['col_bot'], np.float32)
        col = bot + (top - bot) * shade[..., None]
        m, col = m[cut:], col[cut:]
        h0 = max(h0, 0)
        h1 = min(h1, H)
        m, col = m[:h1 - h0], col[:h1 - h0]
        region = img[h0:h1]
        img[h0:h1] = region * (1 - m[..., None]) + col * m[..., None]
    return img


def material_noise(H, W, S):
    return dict(f18=fbm(H, W, 18 * S + 1, 4, 501), f4=fbm(H, W, 4 * S + 1, 2, 502), f40=fbm(H, W, 40 * S + 1, 4, 503),
                f10=fbm(H, W, 10 * S + 1, 3, 504), sx=value_noise(H, W, 80 * S + 1, 505, cy=3 * S + 1),
                sy=value_noise(H, W, 3 * S + 1, 506, cy=80 * S + 1))


def material_tex(it, TX, dy, dx, ys, xs, S):
    m = it.mat
    f18, f4, f40, f10 = TX['f18'][dy, dx], TX['f4'][dy, dx], TX['f40'][dy, dx], TX['f10'][dy, dx]
    if m == 'stone':
        return 1 + 0.22 * (f18 - 0.5) + 0.12 * (f4 - 0.5)
    if m == 'plaster':
        return 1 + 0.14 * (f40 - 0.5) + 0.06 * (f4 - 0.5)
    if m == 'wood':
        return 1 + 0.18 * (TX['sy'][dy, dx] - 0.5) + 0.06 * (f4 - 0.5)
    if m == 'roof':
        rows = 0.5 + 0.5 * np.sin(ys / (7 * S + 0.5) * math.pi)
        return 1 + 0.16 * (rows - 0.5) + 0.14 * (f18 - 0.5)
    if m in ('sand', 'ground', 'road', 'mountain'):
        return 1 + 0.2 * (f10 - 0.5) + 0.1 * (f40 - 0.5)
    if m == 'foliage':
        return 1 + 0.4 * (f10 - 0.5)
    if m in ('figure', 'animal', 'cloth'):
        return 1 + 0.18 * (f10 - 0.5)
    if m == 'tent':
        return 1 + 0.12 * np.sin(ys / (6 * S + 0.5) * math.pi) + 0.1 * (f10 - 0.5)
    if m == 'sail':
        return 1 + 0.12 * (TX['sy'][dy, dx] - 0.5) + 0.08 * (f40 - 0.5)
    return np.ones(f4.shape, np.float32)


def light_field(scene, xs, ys, S, it):
    """Lighting multiplier for an item over a pixel grid (xs, ys in output px)."""
    L = np.zeros(xs.shape + (3,), np.float32) + scene.amb
    # key light: gradient across the item toward the light direction
    bx0, by0, bx1, by1 = it.bbox()
    cx, cy = (bx0 + bx1) / 2 * S, (by0 + by1) / 2 * S
    size = max(bx1 - bx0, by1 - by0) * S + 1
    kx, ky = scene.key_dir
    g = ((xs - cx) * kx + (ys - cy) * ky) / size
    kf = np.clip(0.6 + g * 1.2, 0.15, 1.4) * it.key
    L += scene.key_col * kf[..., None]
    for l in scene.lights:
        if it.recv <= 0:
            break
        d2 = ((xs - l.x * S) ** 2 + (ys - l.y * S) ** 2) / (l.r * S) ** 2
        f = l.I / (1 + d2) ** 1.25
        dz = abs(it.z - l.z)
        f = f * math.exp(-(dz / 0.35) ** 2)
        L += l.col * (f * it.recv)[..., None]
    if it.shade is not None:
        t0, t1 = it.shade
        yy = np.clip((ys - by0 * S) / ((by1 - by0) * S + 1), 0, 1)
        L *= (t0 + (t1 - t0) * yy)[..., None]
    return L


def base_render(scene, W=DW, H=DH, SS=2):
    S = W / DW
    img = sky_render(scene, W, H, S)
    alb = img.copy()
    depth = np.zeros((H, W), np.float32)
    idmap = np.full((H, W), -1, np.int32)
    emit = np.zeros((H, W), np.float32)
    cover = np.zeros((H, W), np.float32)
    items = sorted(enumerate(scene.items), key=lambda t: (t[1].z, t[0]))
    masks = {}
    TX = material_noise(H, W, S)
    for k, (idx, it) in enumerate(items):
        x0, y0, m = raster_item(it, S, SS)
        sl = paste(depth, x0, y0, m)
        if sl is None:
            continue
        (dy, dx), (sy, sx) = sl
        a = m[sy, sx] * it.alpha
        ys, xs = np.mgrid[dy, dx]
        Lf = light_field(scene, xs.astype(np.float32), ys.astype(np.float32), S, it)
        tx = material_tex(it, TX, dy, dx, ys, xs, S)
        col = it.col * tx[..., None] * Lf + it.col * it.emit
        rimk = getattr(scene, 'rim', 0.0)
        if rimk > 0 and it.emit <= 0 and it.z > 0.3:
            er = cv2.erode(m, np.ones((3, 3), np.uint8))
            bandm = cv2.GaussianBlur(np.clip(m - er, 0, 1), (0, 0), 1.0 * S + 0.3)[sy, sx]
            gx = cv2.Sobel(m, cv2.CV_32F, 1, 0, ksize=3)[sy, sx]
            gy = cv2.Sobel(m, cv2.CV_32F, 0, 1, ksize=3)[sy, sx]
            nn = np.sqrt(gx * gx + gy * gy) + 1e-6
            kx, ky = scene.key_dir
            facing = np.clip(-(gx * kx + gy * ky) / nn, 0, 1)
            col = col + scene.key_col[None, None] * (rimk * 2.2 * bandm * facing)[..., None]
        hz = scene.haze * (1 - it.z) ** scene.haze_pow
        col = col * (1 - hz) + scene.haze_col * hz
        a3 = a[..., None]
        img[dy, dx] = img[dy, dx] * (1 - a3) + col * a3
        acol = it.col * (1 - hz * 0.8) + scene.haze_col * hz * 0.8
        alb[dy, dx] = alb[dy, dx] * (1 - a3) + acol * a3
        hit = a > 0.5
        depth[dy, dx] = np.where(hit, it.z, depth[dy, dx])
        idmap[dy, dx] = np.where(hit, idx, idmap[dy, dx])
        emit[dy, dx] = emit[dy, dx] * (1 - a) + it.emit * a
        cover[dy, dx] = np.maximum(cover[dy, dx], a)
        masks[idx] = (x0, y0, m)
    buf = dict(img=img, alb=alb, depth=depth, id=idmap, emit=emit, cover=cover, S=S, W=W, H=H, masks=masks)
    water_reflect(scene, buf)
    fog_layers(scene, buf)
    air_glow(scene, buf)
    return buf


def water_reflect(scene, buf):
    img = buf['img']
    H, W = img.shape[:2]
    S = buf['S']
    for idx, it in enumerate(scene.items):
        if it.mat != 'water' or it.wline is None:
            continue
        sel = buf['id'] == idx
        if not sel.any():
            continue
        wl = it.wline * S
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        rip = (fbm(H, W, 90 * S, 4, 31, cy=6 * S) - 0.5) * 26 * S
        ry = 2 * wl - yy + (fbm(H, W, 60 * S, 3, 32, cy=4 * S) - 0.5) * 6 * S
        rx = xx + rip * np.clip((yy - wl) / (300 * S), 0.2, 1.5)
        refl = cv2.remap(img, rx, np.clip(ry, 0, H - 1), cv2.INTER_LINEAR)
        k = it.col
        mixf = getattr(it, 'refl', 0.55)
        if getattr(it, 'rblur', 0):
            refl = cv2.GaussianBlur(refl, (0, 0), sigmaX=it.rblur * S * 0.3, sigmaY=it.rblur * S)
        out = refl * (0.62 + 0.38 * k) * mixf + img * (1 - mixf)
        img[sel] = out[sel]


def fog_layers(scene, buf):
    img = buf['img']
    H, W = img.shape[:2]
    S = buf['S']
    for f in scene.fog:
        y0, y1 = int(f['y0'] * S), int(f['y1'] * S)
        hh = y1 - y0
        n = fbm(hh, W, f.get('cell', 300) * S, 5, f.get('seed', 3), cy=f.get('cell', 300) * S * 0.25)
        env = np.sin(np.linspace(0, math.pi, hh))[:, None] ** 1.2
        m = smoothstep(f.get('cov', 0.35), 0.85, n) * env * f.get('dens', 0.6)
        behind = buf['depth'][y0:y1] <= f['z']
        m = m * np.where(behind, 1.0, f.get('front', 0.25))
        col = np.array(f['col'], np.float32)
        img[y0:y1] = img[y0:y1] * (1 - m[..., None]) + col * m[..., None]


def air_glow(scene, buf):
    img = buf['img']
    H, W = img.shape[:2]
    S = buf['S']
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    for l in scene.lights:
        if l.air <= 0:
            continue
        d2 = ((xx - l.x * S) ** 2 + (yy - l.y * S) ** 2) / (l.r * 1.2 * S) ** 2
        img += l.col * (l.air * l.I * np.exp(-d2))[..., None]


def edges_from_id(buf, thick=1):
    idm = buf['id']
    e = np.zeros(idm.shape, np.float32)
    e[:, 1:] += idm[:, 1:] != idm[:, :-1]
    e[1:, :] += idm[1:, :] != idm[:-1, :]
    e = np.clip(e, 0, 1)
    if thick > 1:
        e = cv2.dilate(e, np.ones((thick, thick), np.uint8))
    return e


def luminance(img):
    return img[..., 0] * 0.2126 + img[..., 1] * 0.7152 + img[..., 2] * 0.0722


# ------------------------------------------------------------------ lens & grade
def bloom(img, thr=0.8, strength=0.6, radii=(4, 12, 30, 70), S=1.0, tint=None):
    lum = luminance(img)
    bright = img * (np.clip(lum - thr, 0, None) / (lum + 1e-6))[..., None]
    acc = np.zeros_like(img)
    for r in radii:
        acc += cv2.GaussianBlur(bright, (0, 0), r * S)
    acc /= len(radii)
    if tint is not None:
        acc *= np.array(tint, np.float32)
    return img + acc * strength


def godrays(img, src, lx, ly, strength=0.5, decay=0.965, n=40, span=0.6, S=1.0):
    """radial blur of src (bright sky/light mask image) toward (lx, ly) in design coords."""
    H, W = img.shape[:2]
    cx, cy = lx * S, ly * S
    acc = np.zeros_like(src)
    w = 1.0
    tot = 0
    for i in range(n):
        sc = 1 - span * i / n
        M = np.float32([[sc, 0, cx * (1 - sc)], [0, sc, cy * (1 - sc)]])
        acc += cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT) * w
        tot += w
        w *= decay
    acc /= tot
    return img + acc * strength


def dof(img, depth, focus, aperture=40.0, maxr=26, S=1.0, bokeh=True):
    """Depth of field: blend between blurred copies by circle of confusion."""
    coc = np.clip(np.abs(depth - focus) * aperture * S, 0, maxr * S)
    levels = [0, 1.5, 3, 6, 10, 16, 26]
    levels = [l * S for l in levels if l <= maxr]
    stack = []
    for r in levels:
        if r < 0.5:
            stack.append(img)
        elif bokeh and r >= 5:
            k = int(r) * 2 + 1
            ker = np.zeros((k, k), np.float32)
            cv2.circle(ker, (k // 2, k // 2), int(r), 1.0, -1, cv2.LINE_AA)
            ker /= ker.sum()
            stack.append(cv2.filter2D(img, -1, ker))
        else:
            stack.append(cv2.GaussianBlur(img, (0, 0), r / 2))
    out = np.zeros_like(img)
    lv = np.array(levels)
    idx = np.clip(np.searchsorted(lv, coc) - 1, 0, len(lv) - 2)
    lo = lv[idx]
    hi = lv[idx + 1]
    t = np.clip((coc - lo) / (hi - lo + 1e-6), 0, 1)
    for i in range(len(lv) - 1):
        sel = (idx == i)
        if not sel.any():
            continue
        tt = t[..., None]
        blend = stack[i] * (1 - tt) + stack[i + 1] * tt
        out[sel] = blend[sel]
    return out


def chroma(img, amt=0.002):
    H, W = img.shape[:2]
    out = img.copy()
    for c, s in ((0, 1 + amt), (2, 1 - amt)):
        M = np.float32([[s, 0, W / 2 * (1 - s)], [0, s, H / 2 * (1 - s)]])
        out[..., c] = cv2.warpAffine(img[..., c], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return out


def vignette(img, strength=0.35, power=2.2, col=(0, 0, 0)):
    H, W = img.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    r = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 * 0.8 + ((yy - H / 2) / (H / 2)) ** 2 * 0.6)
    v = np.clip(r, 0, 1.6) ** power * strength
    v = np.clip(v, 0, 1)[..., None]
    return img * (1 - v) + np.array(col, np.float32) * v


def grain(img, amt=0.035, seed=1, size=1.0):
    H, W = img.shape[:2]
    r = rng(seed)
    n = r.normal(0, 1, (int(H / size) + 1, int(W / size) + 1)).astype(np.float32)
    if size != 1.0:
        n = cv2.resize(n, (W, H), interpolation=cv2.INTER_LINEAR)
    n = n[:H, :W]
    lum = luminance(np.clip(img, 0, 1))
    w = (0.35 + 0.65 * (1 - np.abs(lum - 0.45) * 1.6)).clip(0.15, 1)
    return img + (n * amt * w)[..., None]


def anamorphic(img, thr=1.0, strength=0.35, length=260, tint=(0.6, 0.8, 1.0), S=1.0):
    lum = luminance(img)
    bright = np.clip(lum - thr, 0, None)
    k = int(length * S) | 1
    ker = np.exp(-np.linspace(-3, 3, k) ** 2)
    ker = (ker / ker.sum()).astype(np.float32)[None, :]
    st = cv2.filter2D(bright, -1, ker)
    st = cv2.GaussianBlur(st, (0, 0), 1.5 * S)
    return img + st[..., None] * np.array(tint, np.float32) * strength


def flare_ghosts(img, lx, ly, strength=0.25, S=1.0, seed=3):
    H, W = img.shape[:2]
    cx, cy = W / 2, H / 2
    x, y = lx * S, ly * S
    out = img.copy()
    r = rng(seed)
    for k in range(5):
        t = -0.4 - k * 0.35
        gx, gy = cx + (x - cx) * t, cy + (y - cy) * t
        rad = (20 + 60 * r.random()) * S
        m = np.zeros((H, W), np.float32)
        cv2.circle(m, (int(gx), int(gy)), int(rad), 1.0, -1, cv2.LINE_AA)
        m = cv2.GaussianBlur(m, (0, 0), rad * 0.25)
        tint = np.array([0.5 + 0.5 * r.random(), 0.6 + 0.3 * r.random(), 0.8 + 0.2 * r.random()], np.float32)
        out += m[..., None] * tint * strength * (0.4 + 0.6 * r.random())
    return out


def filmic(img, exposure=1.0, contrast=1.0, sat=1.0, lift=(0, 0, 0), gain=(1, 1, 1), gamma=(1, 1, 1)):
    x = np.clip(img * exposure, 0, None)
    # ACES-ish
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    x = np.clip((x * (a * x + b)) / (x * (c * x + d) + e), 0, 1)
    if contrast != 1.0:
        x = np.clip((x - 0.5) * contrast + 0.5, 0, 1)
    lum = luminance(x)[..., None]
    x = lum + (x - lum) * sat
    x = np.clip(x, 0, 1)
    x = x * np.array(gain, np.float32) + np.array(lift, np.float32) * (1 - x)
    x = np.clip(x, 0, 1) ** (1 / np.array(gamma, np.float32))
    return np.clip(x, 0, 1)


def to8(img, seed=0):
    r = rng(seed)
    d = (r.random(img.shape[:2]).astype(np.float32) - 0.5) / 255.0
    return (np.clip(img + d[..., None], 0, 1) * 255 + 0.5).astype(np.uint8)


def save(img, path):
    cv2.imwrite(path, cv2.cvtColor(to8(img), cv2.COLOR_RGB2BGR))


# ------------------------------------------------------------------ particles
def make_particles(scene):
    """Particle geometry in design space, so each style can draw it its own way."""
    out = dict(rain=[], embers=[], dust=[])
    if scene.rain:
        rd = scene.rain
        r = rng(rd.get('seed', 11))
        n = rd.get('n', 2000)
        ang = math.radians(rd.get('angle', 12))
        x0, y0, x1, y1 = rd.get('box', (0, 0, DW, DH))
        for i in range(n):
            z = r.random()
            L = (rd.get('len', (30, 70))[0] + (rd.get('len', (30, 70))[1] - rd.get('len', (30, 70))[0]) * r.random()) * (0.4 + z)
            x = r.uniform(x0 - 200, x1)
            y = r.uniform(y0, y1)
            dx, dy = math.sin(ang) * L, math.cos(ang) * L
            out['rain'].append((x, y, x + dx, y + dy, rd.get('alpha', 0.3) * (0.3 + 0.7 * z), z))
        for cur in rd.get('curtains', []):
            cx0, cx1, cy0, cy1, dens = cur
            for i in range(int(dens)):
                z = r.random() * 0.4
                L = r.uniform(40, 120)
                x = r.uniform(cx0, cx1)
                y = r.uniform(cy0, cy1)
                out['rain'].append((x, y, x + math.sin(ang) * L, y + math.cos(ang) * L, rd.get('alpha', 0.3) * 0.6, z))
    if scene.embers:
        e = scene.embers
        r = rng(e.get('seed', 12))
        for i in range(e.get('n', 60)):
            t = r.random()
            x = e['x'] + r.normal(0, e.get('spread', 40)) * (0.4 + t) + math.sin(t * 9 + r.random() * 6) * 20 * t
            y = e['y'] - t * e.get('rise', 400)
            out['embers'].append((x, y, r.uniform(1.2, 3.2) * (1 - t * 0.5), (1 - t) ** 1.5 * r.uniform(0.5, 1.0)))
    if scene.dust:
        d = scene.dust
        r = rng(d.get('seed', 13))
        x0, y0, x1, y1 = d['box']
        for i in range(d.get('n', 300)):
            out['dust'].append((r.uniform(x0, x1), r.uniform(y0, y1), r.uniform(0.8, 2.6), r.uniform(0.2, 1.0)))
    return out


def draw_particles(img, parts, S, buf=None, rain_col=(0.75, 0.8, 0.9), lights=(), ember_col=(1.0, 0.6, 0.25),
                   dust_col=(1.0, 0.85, 0.6), dust_light=None):
    H, W = img.shape[:2]
    if parts['rain']:
        layer = np.zeros((H, W), np.float32)
        for (x0, y0, x1, y1, a, z) in parts['rain']:
            cv2.line(layer, (int(x0 * S * 16), int(y0 * S * 16)), (int(x1 * S * 16), int(y1 * S * 16)), float(a),
                     max(1, int(round((0.6 + z) * S))), cv2.LINE_AA, 4)
        boost = np.ones((H, W), np.float32)
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        tint = np.zeros((H, W, 3), np.float32)
        for l in lights:
            d2 = ((xx - l.x * S) ** 2 + (yy - l.y * S) ** 2) / (l.r * 1.4 * S) ** 2
            f = l.I * np.exp(-d2)
            boost += f * 1.5
            tint += l.col * f[..., None]
        col = np.array(rain_col, np.float32) + tint
        img += layer[..., None] * col * boost[..., None] * 0.4
    if parts['embers']:
        layer = np.zeros((H, W), np.float32)
        for (x, y, r_, b) in parts['embers']:
            cv2.circle(layer, (int(x * S * 16), int(y * S * 16)), max(1, int(r_ * S * 16)), float(b), -1, cv2.LINE_AA, 4)
        glow = cv2.GaussianBlur(layer, (0, 0), 3 * S)
        img += (layer * 2.0 + glow * 3.0)[..., None] * np.array(ember_col, np.float32)
    if parts['dust']:
        layer = np.zeros((H, W), np.float32)
        for (x, y, r_, b) in parts['dust']:
            cv2.circle(layer, (int(x * S * 16), int(y * S * 16)), max(1, int(r_ * S * 16)), float(b), -1, cv2.LINE_AA, 4)
        layer = cv2.GaussianBlur(layer, (0, 0), 0.8 * S)
        if dust_light is not None:
            layer *= dust_light
        img += layer[..., None] * np.array(dust_col, np.float32) * 0.6
    return img
