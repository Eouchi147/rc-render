"""The cabinet of curiosities: the keeper's shelves, where each Dark Corners episode begins and ends.
Frontal plate 1620 x 2880: dark panelled wood, four shelves of objects drawn as lit solids (glass, brass, wood, paper),
a candle on the hero shelf. Hero object of episode 1: Junius's letter under a glass dome, with a brass tag.
Teaser of episode 2 (the Zong): a rolled document with a wax seal and the tag N° 2 · 1781."""
from darkroot import ROOT
import math
import numpy as np
import cv2
import engine as E
import shade as S
import tex as TX
import plates as PL

PW, PH = 1620, 2880
DENS = 1.5
SHELVES = [760, 1380, 2000, 2620]          # top surface of each shelf (plate px)
CANDLE = (1300.0, 1380.0)                  # base of the candle on the hero shelf
FLAME = (1300.0, 1105.0)
DOME = (790.0, 1380.0)                      # base centre of the glass dome
TAG1 = (790.0, 1440.0)
TAG2 = (560.0, 2060.0)
SCROLL = (560.0, 2000.0)
L = np.array([0.55, -0.45, 0.70])           # key light direction (from the candle side, above)
L = L / np.linalg.norm(L)


def lathe(img, alpha, cx, y_bot, profile, col, spec=0.4, glass=0.0, rough=0.0, seed=0, light=L, rim=0.0):
    """A solid of revolution seen from the front. profile: [(height above base, radius)], bottom to top."""
    hs = np.array([p[0] for p in profile], np.float32)
    rs = np.array([p[1] for p in profile], np.float32)
    top = int(y_bot - hs.max()) - 2
    x0, x1 = int(cx - rs.max() - 2), int(cx + rs.max() + 3)
    ys = np.arange(max(top, 0), int(y_bot) + 1)
    xs = np.arange(max(x0, 0), min(x1, img.shape[1]))
    Y, X = np.meshgrid(ys, xs, indexing='ij')
    h = (y_bot - Y).astype(np.float32)
    r = np.interp(h, hs, rs).astype(np.float32)
    dr = np.gradient(np.interp(np.arange(0, hs.max() + 1), hs, rs))
    slope = np.interp(h, np.arange(0, hs.max() + 1), dr).astype(np.float32)
    u = (X - cx) / np.maximum(r, 1e-3)
    inside = (np.abs(u) <= 1) & (h >= 0) & (h <= hs.max()) & (r > 0.5)
    uu = np.clip(u, -1, 1)
    nz = np.sqrt(1 - uu ** 2)
    nx, ny = uu, -slope * nz * 0.6
    n = np.stack([nx, ny, nz], -1)
    n /= np.linalg.norm(n, axis=-1, keepdims=True) + 1e-6
    lam = np.clip((n * light).sum(-1), 0, 1)
    hv = light + np.array([0, 0, 1.0]); hv /= np.linalg.norm(hv)
    sp = np.clip((n * hv).sum(-1), 0, 1) ** 40 * spec
    c = np.array(col, np.float32)
    if rough:
        c = c * (0.85 + 0.3 * S.fbm(len(ys), len(xs), 10, 3, seed))[..., None]
    shade_ = 0.12 + 0.95 * lam
    rgb = c * shade_[..., None] + sp[..., None] * np.array([1.0, 0.85, 0.65], np.float32)
    if rim:
        rgb += (np.abs(uu) ** 6 * rim)[..., None] * np.array([1.0, 0.7, 0.4], np.float32)
    a = inside.astype(np.float32)
    a = cv2.GaussianBlur(a, (0, 0), 0.7)
    reg = img[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
    if glass > 0:
        # glass: mostly see-through, tinted, bright rims and a long highlight
        edge = np.abs(uu) ** 5
        streak = np.exp(-((uu - 0.45) / 0.07) ** 2) * 0.9 + np.exp(-((uu + 0.6) / 0.05) ** 2) * 0.35
        trans = (1 - glass * (0.25 + 0.6 * edge))
        g = reg * trans[..., None] * np.array([0.95, 0.98, 0.96], np.float32) + \
            (edge * 0.35 + streak * spec)[..., None] * np.array([1.0, 0.9, 0.75], np.float32)
        reg[:] = reg * (1 - a[..., None]) + g * a[..., None]
    else:
        reg[:] = reg * (1 - a[..., None]) + rgb * a[..., None]
    if alpha is not None:
        ar = alpha[ys[0]:ys[-1] + 1, xs[0]:xs[-1] + 1]
        np.maximum(ar, a, out=ar)
    return a


def box(img, x0, y0, x1, y1, col, seed=0, bands=(), lit=1.0):
    m = np.zeros(img.shape[:2], np.float32)
    cv2.rectangle(m, (int(x0), int(y0)), (int(x1), int(y1)), 1.0, -1)
    w = x1 - x0
    xx = np.arange(img.shape[1], dtype=np.float32)
    u = np.clip((xx - x0) / max(w, 1), 0, 1)
    sh = (0.35 + 0.75 * np.clip(np.sin(u * math.pi), 0, None) ** 0.6 * (0.6 + 0.4 * u)) * lit
    c = np.array(col, np.float32)[None, None] * sh[None, :, None]
    c = c * (0.88 + 0.24 * S.fbm(img.shape[0], img.shape[1], 30, 2, seed))[..., None]
    for yb in bands:
        cv2.rectangle(m, (0, 0), (0, 0), 0, 1)
        bm = np.zeros(img.shape[:2], np.float32)
        cv2.rectangle(bm, (int(x0), int(yb)), (int(x1), int(yb + 6)), 1.0, -1)
        c = c * (1 - bm[..., None]) + np.array([0.75, 0.55, 0.22], np.float32) * sh[None, :, None] * bm[..., None]
    img[:] = img * (1 - m[..., None]) + c * m[..., None]


def engraved_tag(img, cx, cy, lines, w=270, h=86):
    """A small brass plate with engraved capitals."""
    from PIL import Image, ImageDraw, ImageFont
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    reg = img[y0:y0 + h, x0:x0 + w]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    brass = np.array([0.62, 0.45, 0.2], np.float32) * (0.75 + 0.35 * (1 - yy / h))[..., None]
    brass *= (0.9 + 0.2 * S.fbm(h, w, 6, 2, 4))[..., None]
    edge = ((xx < 3) | (xx > w - 4) | (yy < 3) | (yy > h - 4)).astype(np.float32)
    brass = brass * (1 - 0.4 * edge[..., None])
    im = Image.new('L', (w * 3, h * 3), 0)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(ROOT + '/fonts/Cinzel[wght].ttf', int(h * 3 * 0.3))
    for k, t in enumerate(lines):
        tw = f.getlength(t)
        d.text(((w * 3 - tw) / 2, h * 3 * (0.12 + 0.42 * k)), t, font=f, fill=255)
    a = cv2.resize(np.asarray(im, np.float32) / 255.0, (w, h), interpolation=cv2.INTER_AREA)
    brass = brass * (1 - 0.7 * a[..., None])
    reg[:] = brass
    # its shadow on the shelf edge
    img[y0 + h:y0 + h + 8, x0 + 4:x0 + w + 4] *= 0.6


def build():
    img = np.zeros((PH, PW, 3), np.float32)
    wall, _, _ = TX.surface('dark_paneled_wood', PH, PW, scale=0.9, tint=(0.55, 0.38, 0.25))
    img[:] = wall * 0.55
    yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
    # the shelves: plank top, lit front edge, shadow under
    plank, _, _ = TX.surface('old_planks_02', PH, PW, scale=0.7, tint=(0.62, 0.45, 0.3))
    for sy in SHELVES:
        img[sy - 26:sy + 40] = plank[sy - 26:sy + 40] * np.linspace(0.55, 1.05, 66)[:, None, None]
        img[sy + 40:sy + 130] *= np.linspace(0.35, 1.0, 90)[:, None, None]
        img[sy - 140:sy - 26] *= np.linspace(1.0, 0.8, 114)[:, None, None]
    # side posts
    for x in (40, PW - 40):
        img[:, x - 40:x + 40] = plank[:, x - 40:x + 40] * 0.6
    # ---- shelf 1: books, an hourglass, a brass globe
    s1 = SHELVES[0] - 26
    bx = 120
    r = np.random.default_rng(3)
    for k in range(9):
        w_ = r.uniform(42, 70); h_ = r.uniform(230, 330)
        col = [(0.32, 0.12, 0.08), (0.12, 0.18, 0.12), (0.35, 0.28, 0.16), (0.16, 0.12, 0.2)][k % 4]
        box(img, bx, s1 - h_, bx + w_, s1, col, seed=k, bands=(s1 - h_ + 30, s1 - 50))
        bx += w_ + 3
    lathe(img, None, 930, s1, [(0, 60), (14, 60), (16, 40), (90, 12), (100, 10), (110, 12), (190, 40), (196, 60), (210, 60)],
          (0.5, 0.36, 0.18), spec=0.6)
    lathe(img, None, 930, s1 - 16, [(0, 42), (60, 28), (85, 8), (95, 0)], (0.85, 0.75, 0.55), spec=0.2)      # sand
    lathe(img, None, 930, s1 - 14, [(0, 44), (80, 14), (96, 9), (112, 14), (180, 44), (182, 0)], (1, 1, 1), spec=0.8, glass=0.5)
    lathe(img, None, 1270, s1, [(0, 70), (12, 70), (14, 20), (60, 14), (62, 0)], (0.5, 0.36, 0.16), spec=0.6)
    lathe(img, None, 1270, s1 - 60, [(0, 0)] + [(110 + 110 * math.sin(a), 110 * math.cos(a)) for a in np.linspace(-math.pi / 2, math.pi / 2, 24)][1:],
          (0.42, 0.34, 0.2), spec=0.5, rough=1.0, seed=8)
    cv2.ellipse(img, (1270, int(s1 - 170)), (128, 128), -20, 200, 340, (0.55, 0.42, 0.2), 6, cv2.LINE_AA)
    # ---- shelf 2 (hero): specimen jar, the dome with the letter, the candle
    s2 = SHELVES[1] - 26
    lathe(img, None, 360, s2 - 8, [(0, 92), (200, 92), (201, 0)], (0.55, 0.32, 0.08), spec=0.3, rough=1.0, seed=12)       # amber liquid
    lathe(img, None, 360, s2 - 60, [(0, 25), (40, 38), (80, 30), (120, 18), (140, 0)], (0.18, 0.1, 0.05), spec=0.2)      # a pod in it
    lathe(img, None, 360, s2, [(0, 95), (10, 100), (250, 100), (262, 80), (275, 80), (290, 92), (300, 92)], (1, 1, 1), spec=0.9, glass=0.6)
    lathe(img, None, 360, s2 - 300, [(0, 94), (24, 94), (25, 0)], (0.3, 0.22, 0.14), spec=0.2)                          # lid
    # the dome's wooden base, the letter (folded, upright on a little easel) and the glass
    lathe(img, None, DOME[0], s2, [(0, 190), (30, 190), (32, 175), (44, 175), (46, 0)], (0.36, 0.22, 0.13), spec=0.4, rough=1.0, seed=20)
    lx0, ly1 = int(DOME[0] - 110), int(s2 - 50)
    paper, _, pa = S.paper(300, 220, seed=31, col=(0.86, 0.79, 0.64), age=0.7, folds=((0.33, 'h'), (0.66, 'h')))
    try:
        import pages as PG
        cov = PG.pages_for_film()['p1_full']['cov']
        cov = cv2.resize(cov, (220, 300), interpolation=cv2.INTER_AREA)
        paper = paper * (1 - 0.8 * cov[..., None]) + np.array([0.22, 0.13, 0.07], np.float32) * 0.8 * cov[..., None]
    except Exception:
        pass
    sh = np.linspace(1.05, 0.7, 220)[None, :, None]
    img[ly1 - 300:ly1, lx0:lx0 + 220] = img[ly1 - 300:ly1, lx0:lx0 + 220] * (1 - pa[..., None]) + paper * sh * 0.55 * pa[..., None]
    lathe(img, None, DOME[0], s2 - 44, [(0, 165)] + [(330 + 140 * math.sin(a), 165 * math.cos(a) ** 0.8) for a in np.linspace(0, math.pi / 2, 30)][1:],
          (1, 1, 1), spec=1.0, glass=0.45)
    engraved_tag(img, TAG1[0], TAG1[1] - 18, ['N° 1', 'BAMBERG · 1628'])
    # candle in a pewter holder (the flame itself is live)
    lathe(img, None, CANDLE[0], s2, [(0, 80), (10, 80), (14, 30), (40, 22), (60, 34), (66, 34), (68, 0)], (0.45, 0.45, 0.47), spec=0.8)
    lathe(img, None, CANDLE[0], s2 - 66, [(0, 26), (190, 26), (200, 22), (205, 0)], (0.9, 0.82, 0.62), spec=0.2, rim=0.4)
    # ---- shelf 3: apothecary bottles, the rolled document (next episode), crystals
    s3 = SHELVES[2] - 26
    for k, (x, hgt, rr, col) in enumerate([(160, 260, 50, (0.15, 0.25, 0.2)), (270, 320, 40, (0.3, 0.12, 0.08)), (370, 220, 46, (0.12, 0.14, 0.25))]):
        lathe(img, None, x, s3, [(0, rr), (hgt * 0.65, rr), (hgt * 0.78, rr * 0.35), (hgt, rr * 0.3)], col, spec=0.9, rough=1.0, seed=40 + k)
    # the rolled document, tied, with a red wax seal
    roll = np.zeros((PH, PW), np.float32)
    cv2.rectangle(roll, (440, int(s3 - 90)), (760, int(s3)), 1.0, -1)
    v = np.clip((yy - (s3 - 90)) / 90, 0, 1)
    pcol = np.array([0.82, 0.74, 0.58], np.float32) * (0.45 + 0.75 * np.clip(np.sin(v * math.pi), 0, None) ** 0.5)[..., None]
    img[:] = img * (1 - roll[..., None]) + pcol * roll[..., None]
    for x in (520, 680):
        cv2.line(img, (x, int(s3 - 92)), (x - 6, int(s3 + 2)), (0.25, 0.1, 0.06), 6, cv2.LINE_AA)
    cv2.circle(img, (600, int(s3 - 45)), 26, (0.45, 0.06, 0.04), -1, cv2.LINE_AA)
    cv2.circle(img, (600, int(s3 - 45)), 15, (0.32, 0.04, 0.03), 3, cv2.LINE_AA)
    engraved_tag(img, TAG2[0], TAG2[1] - 18, ['N° 2', '1781'], w=200)
    # a ship in a bottle (the next story is at sea)
    bx_, by_ = 1180, s3
    lathe(img, None, bx_, by_, [(0, 110), (8, 118), (300, 118), (330, 90), (360, 40), (420, 34), (432, 38), (440, 0)], (0.2, 0.3, 0.25), spec=0.3)
    hull = np.array([(bx_ - 80, by_ - 70), (bx_ + 85, by_ - 70), (bx_ + 60, by_ - 40), (bx_ - 60, by_ - 40)], np.float32)
    mh = S.poly_mask(PH, PW, hull)
    img[:] = img * (1 - mh[..., None]) + np.array([0.22, 0.13, 0.07], np.float32) * mh[..., None]
    for k, (mx, mh_) in enumerate([(-35, 190), (25, 220)]):
        cv2.line(img, (bx_ + mx, int(by_ - 70)), (bx_ + mx, int(by_ - 70 - mh_)), (0.18, 0.12, 0.08), 4, cv2.LINE_AA)
        for j in range(3):
            y0_ = by_ - 90 - mh_ * (0.28 * j + 0.1)
            sail = np.array([(bx_ + mx - 32 + 6 * j, y0_), (bx_ + mx + 32 - 6 * j, y0_), (bx_ + mx + 28 - 6 * j, y0_ + mh_ * 0.22), (bx_ + mx - 28 + 6 * j, y0_ + mh_ * 0.22)], np.float32)
            ms = S.poly_mask(PH, PW, sail)
            img[:] = img * (1 - ms[..., None]) + np.array([0.78, 0.72, 0.6], np.float32) * ms[..., None]
    lathe(img, None, bx_, by_, [(0, 110), (8, 118), (300, 118), (330, 90), (360, 40), (420, 34), (432, 38), (440, 0)], (1, 1, 1), spec=1.0, glass=0.55)
    lathe(img, None, bx_, by_ - 425, [(0, 30), (40, 26), (42, 0)], (0.45, 0.3, 0.18), spec=0.2, rough=1.0, seed=70)      # cork
    # ---- shelf 4: a spiral shell (ammonite) and more books lying flat
    s4 = SHELVES[3] - 26
    cx, cy, R = 480, s4 - 170, 160
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    th = np.arctan2(yy - cy, xx - cx)
    m = np.clip((R - d) / 2, 0, 1)
    rib = 0.5 + 0.5 * np.cos(th * 9 + np.log(d + 1) * 9)
    spiral = np.mod(np.log(d + 1) / 0.42 - th / (2 * math.pi), 1.0)
    ring = np.exp(-((spiral - 0.03) / 0.03) ** 2)
    shell = np.array([0.62, 0.52, 0.4], np.float32) * (0.55 + 0.35 * rib - 0.4 * ring)[..., None] * (1.1 - 0.5 * d / R)[..., None]
    img[:] = img * (1 - m[..., None]) + shell * m[..., None]
    for k in range(4):
        box(img, 900, s4 - 55 * (k + 1) - 2 * k, 1350 - 25 * k, s4 - 55 * k - 2 * k, [(0.3, 0.12, 0.08), (0.12, 0.2, 0.14), (0.4, 0.32, 0.18), (0.2, 0.15, 0.25)][k], seed=60 + k)
    # ---- light: the candle (warm, close), a cool ambient from the left
    dd = np.sqrt((xx - FLAME[0]) ** 2 + ((yy - FLAME[1]) * 0.9) ** 2)
    warm = 2.4 / (1 + (dd / 620) ** 2.0)
    cool = 0.10 + 0.08 * np.clip(1 - xx / PW, 0, 1)
    lit = warm[..., None] * np.array([1.0, 0.66, 0.36], np.float32) + cool[..., None] * np.array([0.5, 0.6, 0.85], np.float32)
    img = img * lit
    return img.astype(np.float32)


def prepare(force=False):
    z = None if force else PL.load('cabinet')
    if z is not None:
        return z
    img = build()
    pr, _ = PL.paint_layer(img, None, 1.5, seed=81, grade='warm', expo=1.6, detail=1.2)
    # the brass tags stay crisp (engraving survives the brush), lit like their shelf
    for (cx, cy), lines, w in ((TAG1, ['N° 1', 'BAMBERG · 1628'], 270), (TAG2, ['N° 2', '1781'], 200)):
        tag = np.zeros_like(pr)
        engraved_tag(tag, cx, cy - 18, lines, w=w)
        x0, y0 = int(cx - w / 2), int(cy - 18 - 43)
        k = float(np.clip(pr[y0:y0 + 86, x0:x0 + w].mean() / max(tag[y0:y0 + 86, x0:x0 + w].mean(), 1e-3), 0.3, 2.0))
        pr[y0:y0 + 86, x0:x0 + w] = tag[y0:y0 + 86, x0:x0 + w] * k
    PL.save('cabinet', img=pr)
    return PL.load('cabinet')


class CabinetShot:
    def __init__(self):
        z = prepare()
        self.layer = E.Layer(z['img'], None, Z=1.0, d=DENS, anchor=(PW / 2.0, PH / 2.0), name='cabinet')
        yy, xx = np.mgrid[0:PH, 0:PW].astype(np.float32)
        self.fmask = np.exp(-((xx - FLAME[0]) ** 2 + (yy - FLAME[1]) ** 2) / (2 * 520.0 ** 2)).astype(np.float32)
        self.layer.lights = [(self.fmask, lambda t: 1 + 0.08 * E.noise1(t, 2, 2.1) + 0.04 * E.noise1(t, 3, 7.3), None)]
        self.dust = E.Particles(240, ((-600, 600), (-1000, 900), (0.85, 1.2)), seed=6, vel=(3, -4, 0), jitter=12,
                                size=(1.0, 3.0), col=(1.0, 0.82, 0.58), bright=0.45)

    def render(self, t, cam, frame):
        img = E.compose([self.layer], cam, t)
        fx, fy, sc = E.layer_point(self.layer, cam, t, *FLAME)
        E.add_flame(img, fx, fy + 40 * sc, sc * 1.05, t, seed=4, glow=1.1, size=1.0)
        yy, xx = np.mgrid[0:E.H:4, 0:E.W:4].astype(np.float32)
        g = cv2.resize(np.exp(-(((xx - fx) ** 2 + (yy - fy) ** 2) / (2 * (420 * sc) ** 2))).astype(np.float32), (E.W, E.H))
        self.dust.draw(img, cam, t, light=g, gain=0.9)
        return img
