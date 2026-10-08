"""Film engine: painted plates as depth layers under a moving camera, live elements (flames, dust, rain, smoke,
embers), lens and film (focus, bloom, streaks, aberration, vignette, grain, weave), titles and captions.

Camera model: a pinhole looking down +Z. A layer is a painted plane at depth Z; its pixel (u, v) sits at world
X = (u - u0) * Z / d, where d is the layer's density (layer pixels per frame pixel at the base camera) and (u0, v0) is
the layer pixel on the optical axis at the base camera. Camera: pan (x, y) in frame pixels at depth 1, dolly z,
zoom f, roll (degrees), focus (depth in focus), aperture (blur in pixels per unit of 1/Z)."""
from darkroot import ROOT
import math
import numpy as np
import cv2

W, H, FPS = 1080, 1920, 24


# ------------------------------------------------------------------ timing
def ease(t, kind='inout'):
    t = min(max(t, 0.0), 1.0)
    if kind == 'linear':
        return t
    if kind == 'in':
        return t * t * t
    if kind == 'out':
        return 1 - (1 - t) ** 3
    if kind == 'sine':
        return 0.5 - 0.5 * math.cos(math.pi * t)
    if kind == 'expo':
        return 1 - 2 ** (-10 * t) if t < 1 else 1.0
    return t * t * (3 - 2 * t) if kind == 'smooth' else (4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2)


def keys(t, ks, kind='inout'):
    """ks: [(time, value), ...] (value scalar or tuple); optional per-key easing as a third item."""
    if t <= ks[0][0]:
        return ks[0][1]
    for i in range(len(ks) - 1):
        t0, v0 = ks[i][0], ks[i][1]
        t1, v1 = ks[i + 1][0], ks[i + 1][1]
        if t <= t1:
            k = ks[i + 1][2] if len(ks[i + 1]) > 2 else kind
            u = ease((t - t0) / max(t1 - t0, 1e-6), k)
            if isinstance(v0, (tuple, list)):
                return tuple(a + (b - a) * u for a, b in zip(v0, v1))
            return v0 + (v1 - v0) * u
    return ks[-1][1]


def noise1(t, seed=0, freq=1.0):
    """Smooth 1D noise in -1..1 (sum of incommensurate sines)."""
    r = np.random.default_rng(seed)
    ph = r.uniform(0, 100, 4)
    f = np.array([1.0, 1.731, 2.913, 4.37]) * freq
    a = np.array([0.5, 0.27, 0.15, 0.08])
    return float(np.sum(a * np.sin(2 * math.pi * f * t + ph)) / a.sum())


# ------------------------------------------------------------------ camera and layers
class Cam:
    def __init__(self, x=0.0, y=0.0, z=0.0, f=1.0, roll=0.0, focus=1.0, ap=0.0):
        self.x, self.y, self.z, self.f, self.roll, self.focus, self.ap = x, y, z, f, roll, focus, ap


class Layer:
    def __init__(self, rgb, alpha=None, Z=1.0, d=1.0, anchor=None, name='', lights=None, dyn=None, motion=None, add=False):
        self.rgb = rgb.astype(np.float32)
        self.a = None if alpha is None else alpha.astype(np.float32)
        self.Z, self.d, self.name = Z, d, name
        h, w = rgb.shape[:2]
        self.anchor = anchor if anchor is not None else (w / 2.0, h / 2.0)
        self.lights = lights or []       # [(mask HxW, fn(t) -> gain, colour or None)]
        self.dyn = dyn                   # fn(t, rgb, a) -> (rgb, a)
        self.motion = motion             # fn(t) -> (du, dv, rot_deg, scale, pivot_u, pivot_v)
        self.add = add                   # additive layer (light, glow)
        self.visible = None              # fn(t) -> opacity

    def frame(self, t):
        rgb, a = self.rgb, self.a
        if self.lights:
            rgb = rgb.copy()
            for m, fn, col in self.lights:
                g = fn(t)
                if col is None:
                    rgb *= (1 + (g - 1) * m)[..., None]
                else:
                    rgb += (m * g)[..., None] * np.asarray(col, np.float32)
        if self.dyn is not None:
            rgb, a = self.dyn(t, rgb if self.lights else rgb.copy(), a)
        return rgb, a


def layer_matrix(L, cam, t):
    den = max(L.Z - cam.z, 1e-3)
    s = cam.f * L.Z / (L.d * den)
    u0, v0 = L.anchor
    M = np.array([[s, 0, W / 2 - s * u0 - cam.f * cam.x / den],
                  [0, s, H / 2 - s * v0 - cam.f * cam.y / den],
                  [0, 0, 1]], np.float64)
    if L.motion is not None:
        du, dv, rot, sc, pu, pv = L.motion(t)
        c, sn = math.cos(math.radians(rot)) * sc, math.sin(math.radians(rot)) * sc
        Mm = np.array([[c, -sn, pu - c * pu + sn * pv + du], [sn, c, pv - sn * pu - c * pv + dv], [0, 0, 1]], np.float64)
        M = M @ Mm
    if cam.roll:
        c, sn = math.cos(math.radians(cam.roll)), math.sin(math.radians(cam.roll))
        R = np.array([[c, -sn, W / 2 - c * W / 2 + sn * H / 2], [sn, c, H / 2 - sn * W / 2 - c * H / 2], [0, 0, 1]], np.float64)
        M = R @ M
    return M


def project(cam, X, Y, Z):
    """World point (X, Y in frame px at depth 1 units * Z ... see module doc) to screen; returns (x, y, scale)."""
    den = np.maximum(Z - cam.z, 1e-3)
    sx = W / 2 + cam.f * (X - cam.x) / den
    sy = H / 2 + cam.f * (Y - cam.y) / den
    if cam.roll:
        c, s = math.cos(math.radians(cam.roll)), math.sin(math.radians(cam.roll))
        dx, dy = sx - W / 2, sy - H / 2
        sx, sy = W / 2 + c * dx - s * dy, H / 2 + s * dx + c * dy
    return sx, sy, cam.f / den


def layer_point(L, cam, t, u, v):
    """Screen position of a layer pixel."""
    M = layer_matrix(L, cam, t)
    p = M @ np.array([u, v, 1.0])
    return p[0], p[1], math.sqrt(abs(np.linalg.det(M[:2, :2])))


def blur_fast(img, sigma):
    if sigma < 0.5:
        return img
    if sigma < 6:
        return cv2.GaussianBlur(img, (0, 0), sigma)
    k = 2 if sigma < 14 else 4
    h, w = img.shape[:2]
    sm = cv2.resize(img, (w // k, h // k), interpolation=cv2.INTER_AREA)
    sm = cv2.GaussianBlur(sm, (0, 0), sigma / k)
    return cv2.resize(sm, (w, h), interpolation=cv2.INTER_LINEAR)


def compose(layers, cam, t, out=None, coc_max=40.0):
    if out is None:
        out = np.zeros((H, W, 3), np.float32)
    for L in sorted(layers, key=lambda l: -l.Z):
        op = 1.0 if L.visible is None else float(L.visible(t))
        if op <= 0.001:
            continue
        rgb, a = L.frame(t)
        M = layer_matrix(L, cam, t)[:2]
        if a is None:
            src = rgb
        else:
            src = np.dstack([rgb * a[..., None], a])
        wr = cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        coc = min(abs(cam.ap * (1.0 / max(cam.focus, 1e-3) - 1.0 / L.Z) * cam.f), coc_max) if cam.ap else 0.0
        if coc > 0.6:
            wr = blur_fast(wr, coc * 0.5)
        if a is None:
            if L.add:
                out += wr * op
            else:
                out = out * (1 - op) + wr * op if op < 1 else wr.copy()
        else:
            if L.add:
                out += wr[..., :3] * op
            else:
                aa = wr[..., 3:] * op
                out = out * (1 - aa) + wr[..., :3] * op
    return out


# ------------------------------------------------------------------ live elements
_FL = {}


def flame_sprite(t, seed=0, h=150, lean=0.0, gutter=0.0, size=1.0):
    """A candle flame (RGB, premultiplied, additive) on a small canvas; the base of the flame is at (cx, h*0.86)."""
    r = np.random.default_rng(seed)
    w = int(h * 0.62)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    cx, base = w / 2.0, h * 0.86
    fl = 1 + 0.07 * noise1(t, seed, 2.1) + 0.04 * noise1(t, seed + 1, 7.3)
    fl *= (1 - 0.45 * gutter * (0.5 + 0.5 * noise1(t, seed + 5, 5.0)))
    L = h * 0.62 * fl * size
    sway = (0.06 * noise1(t, seed + 2, 0.9) + 0.03 * noise1(t, seed + 3, 3.1)) * L + lean * L
    u = np.clip((base - yy) / max(L, 1), -0.3, 1.4)
    xc = cx + sway * np.clip(u, 0, 1) ** 1.6
    rad = (h * 0.105 * size) * np.where(u < 0.35, np.sqrt(np.clip(u / 0.35, 0, 1)) * 0.75 + 0.25 * np.clip(u / 0.35, 0, 1) + 0.0,
                                        np.clip(1 - (u - 0.35) / 0.65, 0, 1) ** 0.85)
    d = np.abs(xx - xc) / np.maximum(rad, 1e-3)
    inside = np.clip(1 - d, 0, 1) * (u > -0.08) * (u < 1.0)
    core = np.clip(1 - np.abs(xx - xc) / np.maximum(rad * 0.45, 1e-3), 0, 1) * np.clip((u - 0.02) / 0.2, 0, 1) * np.clip(1 - (u - 0.15) / 0.5, 0, 1)
    blue = np.clip(1 - d, 0, 1) * np.exp(-((u + 0.02) / 0.12) ** 2)
    col = (inside[..., None] ** 1.2 * np.array([1.0, 0.52, 0.16], np.float32) * 1.4
           + core[..., None] * np.array([1.0, 0.92, 0.7], np.float32) * 2.2
           + blue[..., None] * np.array([0.15, 0.25, 0.9], np.float32) * 0.6)
    col = cv2.GaussianBlur(col, (0, 0), 1.1)
    return col.astype(np.float32), (cx, base), fl


def add_flame(img, x, y, scale, t, seed=0, lean=0.0, gutter=0.0, glow=1.0, size=1.0):
    """Add a flame whose base sits at screen (x, y); scale = screen px per sprite px."""
    hpx = int(max(24, 150 * scale))
    spr, (bx, by), fl = flame_sprite(t, seed, hpx, lean, gutter, size)
    sh, sw = spr.shape[:2]
    x0, y0 = int(round(x - bx)), int(round(y - by))
    xa, ya = max(x0, 0), max(y0, 0)
    xb, yb = min(x0 + sw, W), min(y0 + sh, H)
    if xb > xa and yb > ya:
        img[ya:yb, xa:xb] += spr[ya - y0:yb - y0, xa - x0:xb - x0]
    if glow > 0:
        gx, gy = x, y - hpx * 0.35
        rr = hpx * 1.6
        ys, xs = int(max(gy - rr * 3, 0)), int(max(gx - rr * 3, 0))
        ye, xe = int(min(gy + rr * 3, H)), int(min(gx + rr * 3, W))
        if ye > ys and xe > xs:
            yy, xx = np.mgrid[ys:ye, xs:xe].astype(np.float32)
            d2 = ((xx - gx) ** 2 + (yy - gy) ** 2) / (rr * rr)
            g = (0.55 * np.exp(-d2 * 2.5) + 0.22 * np.exp(-d2 * 0.45)) * glow * fl
            img[ys:ye, xs:xe] += g[..., None] * np.array([1.0, 0.55, 0.22], np.float32) * 0.5
    return fl


class Particles:
    """Points in the world volume (X, Y in frame px units at depth 1, Z depth) drifting with a velocity field."""
    def __init__(self, n, box, seed=0, vel=(0, 0, 0), jitter=6.0, size=(1.0, 2.6), col=(1.0, 0.9, 0.75), kind='dust',
                 bright=1.0, life=None):
        r = np.random.default_rng(seed)
        (x0, x1), (y0, y1), (z0, z1) = box
        self.p0 = np.stack([r.uniform(x0, x1, n), r.uniform(y0, y1, n), r.uniform(z0, z1, n)], 1).astype(np.float32)
        self.box = box
        self.ph = r.uniform(0, 100, (n, 3)).astype(np.float32)
        self.fr = r.uniform(0.05, 0.25, (n, 3)).astype(np.float32)
        self.sz = r.uniform(size[0], size[1], n).astype(np.float32)
        self.br = r.uniform(0.3, 1.0, n).astype(np.float32) * bright
        self.vel = np.array(vel, np.float32)
        self.jit = jitter
        self.col = np.array(col, np.float32)
        self.kind = kind

    def pos(self, t):
        (x0, x1), (y0, y1), (z0, z1) = self.box
        p = self.p0 + self.vel * t + self.jit * np.sin(2 * math.pi * self.fr * t + self.ph) * np.array([1, 1, 0.002], np.float32)
        p[:, 0] = x0 + np.mod(p[:, 0] - x0, x1 - x0)
        p[:, 1] = y0 + np.mod(p[:, 1] - y0, y1 - y0)
        return p

    def draw(self, img, cam, t, light=None, gain=1.0):
        p = self.pos(t)
        Z = p[:, 2]
        X, Y = p[:, 0] * Z, p[:, 1] * Z
        sx, sy, sc = project(cam, X, Y, Z)
        buf = np.zeros((H // 2, W // 2), np.float32)
        tw = 0.6 + 0.4 * np.sin(2 * math.pi * self.fr[:, 2] * 3 * t + self.ph[:, 2])
        for i in range(len(p)):
            x, y = sx[i] / 2, sy[i] / 2
            if 0 <= x < W / 2 and 0 <= y < H / 2:
                b = self.br[i] * tw[i] * gain
                if light is not None:
                    b *= light[int(min(sy[i], H - 1)), int(min(sx[i], W - 1))]
                if b > 0.01:
                    rad = max(0.6, self.sz[i] * sc[i] * 0.5)
                    cv2.circle(buf, (int(x * 16), int(y * 16)), int(rad * 16), float(b), -1, cv2.LINE_AA, 4)
        buf = cv2.GaussianBlur(buf, (0, 0), 0.8)
        buf = cv2.resize(buf, (W, H), interpolation=cv2.INTER_LINEAR)
        img += buf[..., None] * self.col
        return img


def rain(img, t, mask=None, seed=0, n=900, angle=8.0, speed=2600.0, length=(40, 110), alpha=0.22, col=(0.75, 0.8, 0.9),
         light=None, depth=(0.3, 1.0), region=None):
    """Screen-space rain streaks (depth-layered: far ones thin and dim, near ones long and soft)."""
    r = np.random.default_rng(seed)
    x0, y0, x1, y1 = region if region else (0, 0, W, H)
    xs = r.uniform(x0 - 200, x1 + 200, n)
    ph = r.uniform(0, 1, n)
    dz = r.uniform(depth[0], depth[1], n)
    span = (y1 - y0) + 300
    y = y0 - 150 + np.mod(ph * span + t * speed * dz, span)
    a = math.radians(angle)
    L = (length[0] + (length[1] - length[0]) * dz)
    buf = np.zeros((H, W), np.float32)
    for i in range(n):
        xx = xs[i] + (y[i] - y0) * math.tan(a)
        xa, ya = xx, y[i]
        xb, yb = xx - L[i] * math.sin(a), y[i] - L[i] * math.cos(a)
        th = 1 if dz[i] < 0.75 else 2
        cv2.line(buf, (int(xa * 16), int(ya * 16)), (int(xb * 16), int(yb * 16)), float(alpha * (0.35 + 0.65 * dz[i])), th, cv2.LINE_AA, 4)
    buf = cv2.GaussianBlur(buf, (0, 0), 0.7)
    if mask is not None:
        buf *= mask
    if light is not None:
        buf *= light
    img += buf[..., None] * np.array(col, np.float32)
    return img


def smoke(t, h, w, seed=0, rise=60.0, scale=60.0, turb=1.0):
    """A field of rising smoke (0..1), w x h, for masking into plumes."""
    from shade import fbm
    key = (h, w, seed, scale)
    if key not in _FL:
        _FL[key] = (fbm(h * 2, w, scale, 5, seed), fbm(h * 2, w, scale * 0.5, 4, seed + 1))
    a, b = _FL[key]
    off = int(t * rise) % h
    n1 = a[off:off + h]
    off2 = int(t * rise * 1.6) % h
    n2 = b[off2:off2 + h]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = (n2 - 0.5) * 30 * turb
    m = cv2.remap(n1, xx + dx, yy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return np.clip((m - 0.42) * 2.4, 0, 1)


# ------------------------------------------------------------------ lens and film
def bloom(img, thr=0.9, strength=0.35, tint=(1.0, 0.85, 0.7)):
    lum = img.max(axis=2)
    src = img * np.clip((lum - thr) / max(1e-3, 1 - thr * 0.5), 0, None)[..., None]
    sm = cv2.resize(src, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    acc = np.zeros_like(sm)
    for s, wgt in ((2, 0.4), (6, 0.3), (16, 0.2), (40, 0.1)):
        acc += cv2.GaussianBlur(sm, (0, 0), s) * wgt
    up = cv2.resize(acc, (W, H), interpolation=cv2.INTER_LINEAR)
    return img + up * strength * np.array(tint, np.float32)


def streak(img, thr=1.2, strength=0.12, tint=(1.0, 0.7, 0.45)):
    lum = img.max(axis=2)
    src = img * np.clip(lum - thr, 0, None)[..., None]
    sm = cv2.resize(src, (W // 4, H // 8), interpolation=cv2.INTER_AREA)
    k = np.exp(-np.abs(np.arange(-120, 121)) / 40.0).astype(np.float32)
    k /= k.sum()
    sm = cv2.filter2D(sm, -1, k[None, :])
    up = cv2.resize(sm, (W, H), interpolation=cv2.INTER_LINEAR)
    return img + up * strength * 6 * np.array(tint, np.float32)


def aberration(img, amt=0.0015):
    if amt <= 0:
        return img
    out = img.copy()
    for c, s in ((0, 1 + amt), (2, 1 - amt)):
        M = np.array([[s, 0, W / 2 * (1 - s)], [0, s, H / 2 * (1 - s)]], np.float32)
        out[..., c] = cv2.warpAffine(img[..., c], M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
    return out


_VIG = {}


def vignette(img, strength=0.45, power=2.0):
    k = (strength, power)
    if k not in _VIG:
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H / 2) / (H * 0.6)) ** 2)
        _VIG[k] = (1 - strength * np.clip(d, 0, 1.5) ** power)[..., None].astype(np.float32)
    return img * _VIG[k]


_GR = {}


def grain(img, frame, amt=0.035):
    if 'g' not in _GR:
        r = np.random.default_rng(7)
        _GR['g'] = [cv2.GaussianBlur(r.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.7) for _ in range(8)]
    g = _GR['g'][frame % 8]
    sh = (frame * 37) % 97, (frame * 53) % 89
    g = np.roll(np.roll(g, sh[0], 0), sh[1], 1)
    lum = img.mean(axis=2, keepdims=True)
    return img + g[..., None] * amt * (0.35 + 0.65 * np.sqrt(np.clip(lum, 0, 1)))


def tonemap(img, exposure=1.0, lift=(0.0, 0.0, 0.0), gamma=(1.0, 1.0, 1.0), gain=(1.0, 1.0, 1.0), sat=1.0, knee=0.8):
    x = img * exposure
    # soft shoulder above the knee
    over = np.clip(x - knee, 0, None)
    x = np.where(x > knee, knee + over / (1 + over / (1.0 - knee + 1e-3) * 0.9 + 1e-6) * (1 - knee) / (1 - knee + 1e-3), x)
    x = np.clip(x, 0, None)
    if sat != 1.0:
        l = x.mean(axis=2, keepdims=True)
        x = l + (x - l) * sat
    x = x * np.array(gain, np.float32) + np.array(lift, np.float32) * (1 - x)
    x = np.clip(x, 0, 1) ** (1.0 / np.array(gamma, np.float32))
    return np.clip(x, 0, 1)


def weave(img, frame, amt=0.6):
    dx = amt * noise1(frame / FPS, 3, 0.7)
    dy = amt * noise1(frame / FPS, 4, 0.6)
    M = np.array([[1, 0, dx], [0, 1, dy]], np.float32)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


# ------------------------------------------------------------------ text
FONTS = ROOT + '/fonts/'
_FONT = {}


def font(name, size):
    from PIL import ImageFont
    k = (name, size)
    if k not in _FONT:
        _FONT[k] = ImageFont.truetype(FONTS + name, size)
    return _FONT[k]


def text_image(lines, fname, size, col=(1, 1, 1), spacing=1.25, align='center', tracking=0, width=None, var=None):
    """Render lines of text to a float RGBA image (straight alpha)."""
    from PIL import Image, ImageDraw
    f = font(fname, size)
    if var is not None:
        try:
            f.set_variation_by_axes(var)
        except Exception:
            pass
    ws = []
    for ln in lines:
        if tracking:
            w = sum(f.getlength(c) for c in ln) + tracking * max(len(ln) - 1, 0)
        else:
            w = f.getlength(ln)
        ws.append(w)
    tw = int(max(ws) + size) if width is None else width
    lh = int(size * spacing)
    th = lh * len(lines) + size // 2
    im = Image.new('L', (tw, th), 0)
    d = ImageDraw.Draw(im)
    for i, ln in enumerate(lines):
        x = (tw - ws[i]) / 2 if align == 'center' else size / 2
        y = i * lh + size * 0.1
        if tracking:
            for c in ln:
                d.text((x, y), c, font=f, fill=255)
                x += f.getlength(c) + tracking
        else:
            d.text((x, y), ln, font=f, fill=255)
    a = np.asarray(im, np.float32) / 255.0
    rgb = np.ones(a.shape + (3,), np.float32) * np.array(col, np.float32)
    return rgb, a


def put(img, rgb, a, x, y, opacity=1.0, shadow=0.0, glow=0.0, glow_col=(1.0, 0.8, 0.5), anchor='center'):
    h, w = a.shape
    if anchor == 'center':
        x0, y0 = int(round(x - w / 2)), int(round(y - h / 2))
    else:
        x0, y0 = int(round(x)), int(round(y))
    xa, ya, xb, yb = max(x0, 0), max(y0, 0), min(x0 + w, W), min(y0 + h, H)
    if xb <= xa or yb <= ya:
        return img
    sa = a[ya - y0:yb - y0, xa - x0:xb - x0] * opacity
    sr = rgb[ya - y0:yb - y0, xa - x0:xb - x0]
    reg = img[ya:yb, xa:xb]
    if shadow > 0:
        sh = cv2.GaussianBlur(sa, (0, 0), 6) * shadow
        reg *= (1 - sh[..., None] * 0.85)
    if glow > 0:
        gl = cv2.GaussianBlur(sa, (0, 0), 14) * glow
        reg += gl[..., None] * np.array(glow_col, np.float32)
    img[ya:yb, xa:xb] = reg * (1 - sa[..., None]) + sr * sa[..., None]
    return img
