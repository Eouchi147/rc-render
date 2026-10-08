"""The cell, July 1628: a plank desk against a rubble wall, the letter, an inkpot, a tallow candle, the barred window
with rain outside. Laid out in 3D (centimetres) and projected; surfaces lit in their own flat space, then warped.

World: x 0..120 (left to right), y 0..70 (near edge to the wall), z up from the desk top. The wall is the plane y = 70."""
import math
import numpy as np
import cv2
import shade as S
import tex as TX
from cam3d import Cam3

PW, PH = 1620, 2880
DENS = 1.5
CAM = Cam3(pos=(58, -16, 46), target=(56, 44, 13), fpx=1450, W=PW, H=PH)
PXCM = 12                                   # flat texture pixels per cm
DESK = (-20, 140, -40, 70)                  # x0, x1, y0, y1 (cm): the board is wider than the frame
WALLZ = (-90, 130)
CANDLE = dict(x=84.0, y=47.0, r=2.6, h=19.0, stub=5.5)
INK = dict(x=22.0, y=46.0, r=4.0, h=6.5)
WINDOW = (6, 38, 46, 86)                   # x0, x1, z0, z1 on the wall (cm)
PAPER = dict(x=52.0, y=22.0, w=21.0, h=32.0, rot=-5.0)     # centre (cm), size (cm), rotation (deg)
PAPER_PX = 54                               # paper texture pixels per cm (sharp ink)
MOON = np.array([0.42, -0.62, -0.66])       # direction the moonlight travels


def flame_pos(stub=False, height=None):
    hc = (CANDLE['stub'] if stub else CANDLE['h']) if height is None else height
    return np.array([CANDLE['x'], CANDLE['y'], hc + 3.2])


def warm(I=1.0):
    return np.array([1.0, 0.73, 0.46], np.float32) * I


# ------------------------------------------------------------------ lighting in flat space
def point_light_flat(N, P, Lpos, I, col, r=40.0, spec=0.0, shin=16.0):
    """N: HxWx3 normals in world orientation; P: HxWx3 world positions (cm). Returns diffuse+spec colour."""
    L = Lpos[None, None, :] - P
    d = np.linalg.norm(L, axis=-1) + 1e-6
    Ln = L / d[..., None]
    ndl = np.clip((N * Ln).sum(-1), 0, 1)
    fall = I / (1 + (d / r) ** 2)
    out = (ndl * fall)[..., None] * col
    if spec > 0:
        V = CAM.pos[None, None, :] - P
        V = V / (np.linalg.norm(V, axis=-1, keepdims=True) + 1e-6)
        Hh = Ln + V
        Hh /= (np.linalg.norm(Hh, axis=-1, keepdims=True) + 1e-6)
        out += ((np.clip((N * Hh).sum(-1), 0, 1) ** shin) * fall * spec)[..., None] * col
    return out.astype(np.float32)


def desk_flat(stub=False, seed=2, height=None):
    x0, x1, y0, y1 = DESK
    w, h = int((x1 - x0) * PXCM), int((y1 - y0) * PXCM)
    alb, N, Hg = TX.surface('old_planks_02', h, w, scale=0.85, rot=math.pi / 2, sat=0.7, tint=(1.0, 0.84, 0.66), gain=0.75)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    X = x0 + xx / PXCM
    Y = y1 - yy / PXCM
    P = np.stack([X, Y, np.zeros_like(X)], -1)
    Nw = np.stack([N[..., 0], -N[..., 1], N[..., 2]], -1)
    Nw = TX.flatten_normals(Nw, 0.8)
    stains = S.fbm(h, w, 180, 4, seed + 3)
    alb *= (0.8 + 0.3 * stains)[..., None]
    rng = np.random.default_rng(seed)
    for k in range(7):
        cx, cy, rr = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(6, 26)
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        if k < 4:
            alb = alb * (1 - 0.6 * np.exp(-(d / rr) ** 4))[..., None]
        else:
            alb = alb + 0.25 * np.exp(-(d / rr) ** 4)[..., None] * np.array([0.8, 0.7, 0.5], np.float32)
    F = flame_pos(stub, height)
    lit = point_light_flat(Nw, P, F, 2.6, warm(), r=26, spec=0.25, shin=10)
    lit += np.array([0.02, 0.024, 0.035], np.float32)
    rgb = alb * lit
    return rgb.astype(np.float32), (x0, x1, y0, y1), (w, h), P


def moon_patch_flat(P, soft=8.0):
    """Moonlight landing on the desk through the window bars (in desk-flat space)."""
    wx0, wx1, wz0, wz1 = WINDOW
    t = (70.0 - P[..., 1]) / (-MOON[1])
    X = P[..., 0] - MOON[0] * t
    Z = P[..., 2] - MOON[2] * t
    inside = (X > wx0) & (X < wx1) & (Z > wz0) & (Z < wz1)
    bars = np.zeros_like(X, dtype=bool)
    for k in range(1, 5):
        bx = wx0 + k * (wx1 - wx0) / 5
        bars |= np.abs(X - bx) < 0.9
    bars |= np.abs(Z - (wz0 + 0.45 * (wz1 - wz0))) < 0.8
    m = (inside & ~bars).astype(np.float32)
    return cv2.GaussianBlur(m, (0, 0), soft)


def wall_flat(stub=False, seed=1, height=None):
    x0, x1, y0, y1 = DESK
    z0, z1 = WALLZ
    w, h = int((x1 - x0) * PXCM), int((z1 - z0) * PXCM)
    alb, N, Hg = TX.surface('rough_block_wall', h, w, scale=1.15, sat=0.75, tint=(1.0, 0.9, 0.78), gain=0.85)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    X = x0 + xx / PXCM
    Z = z1 - yy / PXCM
    P = np.stack([X, np.full_like(X, 70.0), Z], -1)
    # tangent space (x right, y down, z out of the wall) -> world (x, -z, -y)
    Nw = np.stack([N[..., 0], -N[..., 2], -N[..., 1]], -1)
    damp = S.fbm(h, w, 220, 4, seed + 11)
    alb *= (0.7 + 0.4 * damp)[..., None]
    F = flame_pos(stub, height)
    lit = point_light_flat(Nw, P, F, 2.3, warm(), r=24)
    lit += np.array([0.016, 0.018, 0.028], np.float32)
    rgb = alb * lit
    wx0, wx1, wz0, wz1 = WINDOW

    def to_px(x, z):
        return ((x - x0) * PXCM, (z1 - z) * PXCM)
    rec = [to_px(wx0 - 5, wz1 + 6), to_px(wx1 + 5, wz1 + 6), to_px(wx1 + 5, wz0 - 4), to_px(wx0 - 5, wz0 - 4)]
    opn = [to_px(wx0, wz1), to_px(wx1, wz1), to_px(wx1, wz0), to_px(wx0, wz0)]
    m_rec = S.poly_mask(h, w, rec)
    m_open = S.poly_mask(h, w, opn)
    reveal = m_rec * (1 - m_open)
    side = alb * 0.35 * (lit * 0.6 + 0.02)
    rgb = rgb * (1 - reveal[..., None]) + side * reveal[..., None]
    ox, oy = opn[0]
    ow, oh = opn[1][0] - ox, opn[2][1] - oy
    sky = np.zeros((h, w, 3), np.float32) + np.array([0.012, 0.016, 0.03], np.float32)
    gx, gy = ox + ow * 0.7, oy + oh * 0.25
    g = np.exp(-(((xx - gx) / (ow * 0.8)) ** 2 + ((yy - gy) / (oh * 0.7)) ** 2))
    sky += g[..., None] * np.array([0.07, 0.09, 0.14], np.float32)
    cl = S.fbm(h, w, 60, 4, seed + 30)
    sky *= (0.6 + 0.8 * cl)[..., None]
    roofs = np.zeros((h, w), np.float32)
    rr = np.random.default_rng(seed + 40)
    bx = ox - 20
    while bx < ox + ow + 20:
        bw = rr.uniform(70, 140); bh = rr.uniform(60, 150)
        top = oy + oh - bh * 0.55 - rr.uniform(0, 60)
        roofs = np.maximum(roofs, S.poly_mask(h, w, [(bx, oy + oh + 5), (bx, top + bh * 0.4), (bx + bw / 2, top), (bx + bw, top + bh * 0.4), (bx + bw, oy + oh + 5)]))
        if rr.random() < 0.4:
            wxp, wyp = bx + bw * rr.uniform(0.3, 0.6), top + bh * 0.62
            roofs_w = S.poly_mask(h, w, [(wxp, wyp), (wxp + 10, wyp), (wxp + 10, wyp + 14), (wxp, wyp + 14)])
            sky = sky + roofs_w[..., None] * np.array([0.5, 0.32, 0.12], np.float32)
        bx += bw * rr.uniform(0.7, 1.0)
    sky = sky * (1 - roofs[..., None] * 0.8)
    rgb = rgb * (1 - m_open[..., None]) + sky * m_open[..., None]
    bars = np.zeros((h, w), np.float32)
    for k in range(1, 5):
        bxw = wx0 + k * (wx1 - wx0) / 5
        p0, p1 = to_px(bxw - 0.9, wz1 + 3), to_px(bxw + 0.9, wz0 - 3)
        bars = np.maximum(bars, S.poly_mask(h, w, [p0, (p1[0], p0[1]), p1, (p0[0], p1[1])]))
    zc = wz0 + 0.45 * (wz1 - wz0)
    p0, p1 = to_px(wx0 - 3, zc + 0.8), to_px(wx1 + 3, zc - 0.8)
    bars = np.maximum(bars, S.poly_mask(h, w, [p0, (p1[0], p0[1]), p1, (p0[0], p1[1])]))
    iron = np.array([0.05, 0.04, 0.035], np.float32) + lit * 0.05
    rgb = rgb * (1 - bars[..., None]) + iron * bars[..., None]
    return rgb.astype(np.float32), m_open, (w, h)


def paper_flat(seed=5, age=0.3):
    w, h = int(PAPER['w'] * PAPER_PX), int(PAPER['h'] * PAPER_PX)
    alb, hgt, a = S.paper(h, w, seed=seed, col=(0.86, 0.80, 0.67), age=age, folds=((0.5, 'h'), (0.5, 'v')), deckle=6)
    return alb, hgt, a


def paper_world(u, v):
    """Paper texture pixel -> world (cm) on the desk."""
    c, s = math.cos(math.radians(PAPER['rot'])), math.sin(math.radians(PAPER['rot']))
    lx = u / PAPER_PX - PAPER['w'] / 2
    ly = PAPER['h'] / 2 - v / PAPER_PX
    return PAPER['x'] + lx * c - ly * s, PAPER['y'] + lx * s + ly * c


def paper_H():
    w, h = int(PAPER['w'] * PAPER_PX), int(PAPER['h'] * PAPER_PX)
    flat = [(0, 0), (w, 0), (w, h), (0, h)]
    world = [(*paper_world(u, v), 0.02) for u, v in flat]
    return CAM.plane_H(world, flat)


def desk_H():
    x0, x1, y0, y1 = DESK
    w, h = int((x1 - x0) * PXCM), int((y1 - y0) * PXCM)
    return CAM.plane_H([(x0, y1, 0), (x1, y1, 0), (x1, y0, 0), (x0, y0, 0)], [(0, 0), (w, 0), (w, h), (0, h)])


def wall_H():
    x0, x1, _, _ = DESK
    z0, z1 = WALLZ
    w, h = int((x1 - x0) * PXCM), int((z1 - z0) * PXCM)
    return CAM.plane_H([(x0, 70, z1), (x1, 70, z1), (x1, 70, z0), (x0, 70, z0)], [(0, 0), (w, 0), (w, h), (0, h)])


def lit_paper(stub=False, seed=5, height=None):
    alb, hgt, a = paper_flat(seed)
    h, w = a.shape
    vv, uu = np.mgrid[0:h, 0:w].astype(np.float32)
    X, Y = paper_world(uu, vv)
    P = np.stack([X, Y, np.zeros_like(X)], -1)
    n = S.normals(cv2.GaussianBlur(hgt, (0, 0), 1.5), strength=4.0)
    c, s = math.cos(math.radians(PAPER['rot'])), math.sin(math.radians(PAPER['rot']))
    Nw = np.stack([n[..., 0] * c + n[..., 1] * s, n[..., 0] * s - n[..., 1] * c, n[..., 2]], -1)
    F = flame_pos(stub, height)
    lit = point_light_flat(Nw, P, F, 2.1, np.array([1.0, 0.84, 0.66], np.float32), r=28)
    lit += np.array([0.03, 0.033, 0.045], np.float32)
    moon = moon_patch_flat(P, soft=6) * 0.0
    rgb = alb * (lit + moon[..., None] * np.array([0.55, 0.68, 1.0], np.float32))
    return rgb.astype(np.float32), a


# ------------------------------------------------------------------ objects (drawn in plate space)
def cylinder(img, base_c, r, hgt, col, light, translucent=0.0, top_col=None, spec=0.3, alpha=None):
    """A vertical cylinder standing on the desk: projected body, shaded around and along, with a lit top ellipse."""
    H_, W_ = img.shape[:2]
    bx, by = base_c
    ang = np.linspace(0, 2 * math.pi, 96)
    ring_b = np.stack([bx + r * np.cos(ang), by + r * np.sin(ang), np.zeros_like(ang)], 1)
    ring_t = ring_b + np.array([0, 0, hgt])
    pb, _ = CAM.project(ring_b)
    pt, _ = CAM.project(ring_t)
    hull = cv2.convexHull(np.vstack([pb, pt]).astype(np.float32)).reshape(-1, 2)
    m = S.poly_mask(H_, W_, hull)
    xs = hull[:, 0]
    xl, xr = xs.min(), xs.max()
    yy, xx = np.mgrid[0:H_, 0:W_].astype(np.float32)
    u = np.clip((xx - xl) / max(xr - xl, 1), 0, 1)
    F = light
    ax_top, _ = CAM.project([(bx, by, hgt)])
    ax_bot, _ = CAM.project([(bx, by, 0)])
    lpx, _ = CAM.project([F])
    side = 0.5 + 0.5 * np.clip((lpx[0][0] - (xl + xr) / 2) / max(xr - xl, 1) * 1.5, -1, 1)
    cyl = np.clip(np.sin(u * math.pi), 0, 1) ** 0.7
    lam = np.clip(cyl * (0.4 + 1.2 * (side * u + (1 - side) * (1 - u))), 0, 1.4)
    vtop, vbot = ax_top[0][1], ax_bot[0][1]
    along = np.clip((yy - vtop) / max(vbot - vtop, 1), 0, 1)
    dist = np.linalg.norm(np.array(F) - np.array([bx, by, hgt * 0.5]))
    fall = 2.2 / (1 + (dist / 22) ** 2)
    shade_ = lam * fall * (1.0 - 0.45 * along)
    rgb = np.array(col, np.float32) * shade_[..., None] * warm()
    if translucent > 0:
        glow = np.exp(-along * 4.5) * translucent
        rgb += glow[..., None] * np.array([1.0, 0.5, 0.18], np.float32) * (0.25 + 0.75 * cyl)[..., None]
    rgb += (np.clip(cyl, 0, 1) ** 12 * spec * fall)[..., None] * warm()
    if translucent > 0:
        grain = S.fbm(H_, W_, 18, 3, 77)
        streaks = cv2.resize(cv2.resize(S.fbm(H_, W_, 6, 2, 78), (W_, max(2, H_ // 40))), (W_, H_))
        rgb *= (0.86 + 0.2 * grain + 0.1 * streaks)[..., None]
    out = img * (1 - m[..., None]) + rgb * m[..., None]
    mt = None
    if top_col is not None:
        mt = S.poly_mask(H_, W_, pt)
        out = out * (1 - mt[..., None]) + np.array(top_col, np.float32) * mt[..., None]
    if alpha is not None:
        np.maximum(alpha, m, out=alpha)
        if mt is not None:
            np.maximum(alpha, mt, out=alpha)
    return out.astype(np.float32), m, pt


def contact_shadow(img, c, r, k=0.6, spread=2.2, F=None):
    """Soft shadow on the desk around an object's base, pushed away from the flame."""
    H_, W_ = img.shape[:2]
    bx, by = c
    off = np.array([0.0, 0.0])
    if F is not None:
        d = np.array([bx - F[0], by - F[1]])
        off = d / (np.linalg.norm(d) + 1e-6) * r * 1.2
    ang = np.linspace(0, 2 * math.pi, 64)
    ring = np.stack([bx + off[0] + r * spread * np.cos(ang), by + off[1] + r * spread * np.sin(ang), np.zeros_like(ang)], 1)
    p, _ = CAM.project(ring)
    m = S.poly_mask(H_, W_, p)
    m = cv2.GaussianBlur(m, (0, 0), r * 5)
    return img * (1 - k * m[..., None])


def objects(img, alpha, stub=False, height=None):
    F = flame_pos(stub, height)
    H_, W_ = img.shape[:2]
    ang = np.linspace(0, 2 * math.pi, 64)
    yy, xx = np.mgrid[0:H_, 0:W_].astype(np.float32)
    # inkpot: glazed brown clay
    img = contact_shadow(img, (INK['x'], INK['y']), INK['r'], 0.65, 1.8, F)
    img, _, top = cylinder(img, (INK['x'], INK['y']), INK['r'], INK['h'], (0.16, 0.11, 0.07), F, spec=1.4, alpha=alpha)
    mouth = np.stack([INK['x'] + INK['r'] * 0.55 * np.cos(ang), INK['y'] + INK['r'] * 0.55 * np.sin(ang), np.full_like(ang, INK['h'] + 0.05)], 1)
    rim = np.stack([INK['x'] + INK['r'] * 0.85 * np.cos(ang), INK['y'] + INK['r'] * 0.85 * np.sin(ang), np.full_like(ang, INK['h'] + 0.05)], 1)
    pr, _ = CAM.project(rim)
    pm, _ = CAM.project(mouth)
    m_top = S.poly_mask(H_, W_, top)
    img = img * (1 - m_top[..., None]) + np.array([0.24, 0.15, 0.09], np.float32) * 0.9 * m_top[..., None]
    m_r = np.clip(S.poly_mask(H_, W_, pr) - S.poly_mask(H_, W_, pm), 0, 1)
    img = img * (1 - m_r[..., None]) + np.array([0.42, 0.27, 0.16], np.float32) * m_r[..., None]
    m_m = S.poly_mask(H_, W_, pm)
    img = img * (1 - m_m[..., None]) + np.array([0.008, 0.007, 0.012], np.float32) * m_m[..., None]
    gl, _ = CAM.project([(INK['x'] + 0.9, INK['y'] - 0.4, INK['h'] + 0.06)])
    gx, gy = gl[0]
    img += (np.exp(-(((xx - gx) / 9) ** 2 + ((yy - gy) / 4) ** 2)) * 1.6)[..., None] * warm()
    # the candle in an iron dish
    img = contact_shadow(img, (CANDLE['x'], CANDLE['y']), 6.0, 0.55, 1.4, None)
    dish = np.stack([CANDLE['x'] + 6.5 * np.cos(ang), CANDLE['y'] + 6.5 * np.sin(ang), np.full_like(ang, 0.9)], 1)
    pd, _ = CAM.project(dish)
    dish_b = np.stack([CANDLE['x'] + 5.8 * np.cos(ang), CANDLE['y'] + 5.8 * np.sin(ang), np.zeros_like(ang)], 1)
    pdb, _ = CAM.project(dish_b)
    m_d = S.poly_mask(H_, W_, cv2.convexHull(np.vstack([pd, pdb]).astype(np.float32)).reshape(-1, 2))
    img = img * (1 - m_d[..., None]) + np.array([0.06, 0.05, 0.045], np.float32) * m_d[..., None]
    np.maximum(alpha, m_d, out=alpha)
    pin, _ = CAM.project(np.stack([CANDLE['x'] + 5.6 * np.cos(ang), CANDLE['y'] + 5.6 * np.sin(ang), np.full_like(ang, 0.9)], 1))
    m_di = S.poly_mask(H_, W_, pin)
    img = img * (1 - m_di[..., None] * 0.6) + (np.array([0.16, 0.1, 0.06], np.float32) * 1.4) * m_di[..., None] * 0.6
    return img.astype(np.float32)


def candle_sprite(stub=False, height=None):
    F = flame_pos(stub) if height is None else np.array([CANDLE['x'], CANDLE['y'], height + 3.2])
    img = np.zeros((PH, PW, 3), np.float32)
    alpha = np.zeros((PH, PW), np.float32)
    H_, W_ = img.shape[:2]
    hc = (CANDLE['stub'] if stub else CANDLE['h']) if height is None else height
    img, m_c, top = cylinder(img, (CANDLE['x'], CANDLE['y']), CANDLE['r'], hc, (0.6, 0.48, 0.32), F, translucent=0.85,
                             top_col=(0.95, 0.66, 0.36), spec=0.08, alpha=alpha)
    # the molten cup at the top: darker rim, a bright pool
    ang = np.linspace(0, 2 * math.pi, 64)
    pool, _ = CAM.project(np.stack([CANDLE['x'] + CANDLE['r'] * 0.62 * np.cos(ang), CANDLE['y'] + CANDLE['r'] * 0.62 * np.sin(ang), np.full_like(ang, hc - 0.15)], 1))
    mp_ = S.poly_mask(H_, W_, pool)
    img = img * (1 - mp_[..., None]) + np.array([1.25, 0.82, 0.42], np.float32) * mp_[..., None]
    rr = np.random.default_rng(4)
    for k in range(6):
        a = rr.uniform(-1.2, 0.9)
        L = rr.uniform(1.5, hc * 0.8)
        cx_ = CANDLE['x'] + CANDLE['r'] * math.cos(a + math.pi / 2)
        cy_ = CANDLE['y'] - CANDLE['r'] * abs(math.sin(a + math.pi / 2))
        p0, _ = CAM.project([(cx_, cy_, hc)])
        p1, _ = CAM.project([(cx_, cy_, hc - L)])
        x0_, y0_ = p0[0]; x1_, y1_ = p1[0]
        wd = rr.uniform(3, 6)
        md = S.poly_mask(H_, W_, np.vstack([[[x0_ - wd, y0_], [x0_ + wd, y0_]], S.ellipse_pts(x1_, y1_, wd * 1.1, wd * 1.3, a0=0, a1=math.pi)[::-1]]))
        img = img * (1 - md[..., None] * 0.85) + (np.array([1.0, 0.85, 0.6], np.float32) * (0.9 + 1.2 * math.exp(-L / 6))) * md[..., None] * 0.85
    wt, _ = CAM.project([(CANDLE['x'], CANDLE['y'], hc + 1.6)])
    wb, _ = CAM.project([(CANDLE['x'], CANDLE['y'], hc)])
    mw = S.poly_mask(H_, W_, [(wb[0][0] - 3, wb[0][1]), (wb[0][0] + 3, wb[0][1]), (wt[0][0] + 4, wt[0][1]), (wt[0][0] - 1, wt[0][1] - 2)])
    img = img * (1 - mw[..., None]) + np.array([0.04, 0.025, 0.02], np.float32) * mw[..., None]
    np.maximum(alpha, mw, out=alpha)
    return img.astype(np.float32), np.clip(alpha, 0, 1)


BASE_CAM = CAM


def build(height=19.0, zoom=1.0, center=None):
    """Painted-plate layers in plate space: 'wall' (opaque), 'desk' (paper, inkpot, dish; alpha), 'candle' (sprite).
    zoom/center: the same view through a longer lens (a detail plate, painted with proportionally finer strokes)."""
    global CAM
    CAM = BASE_CAM if zoom == 1.0 else BASE_CAM.zoomed(zoom, center)
    try:
        return _build(height)
    finally:
        CAM = BASE_CAM


def _build(height):
    stub = False
    wall_rgb, m_open, (ww, wh) = wall_flat(stub, height=height)
    Hw = wall_H()
    wall = cv2.warpPerspective(wall_rgb, Hw, (PW, PH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    win = cv2.warpPerspective(m_open, Hw, (PW, PH), flags=cv2.INTER_LINEAR)
    d_rgb, _, (dw, dh), P = desk_flat(stub, height=height)
    Hd = desk_H()
    desk = cv2.warpPerspective(d_rgb, Hd, (PW, PH), flags=cv2.INTER_LINEAR)
    dmask = cv2.warpPerspective(np.ones((dh, dw), np.float32), Hd, (PW, PH), flags=cv2.INTER_LINEAR)
    mp = moon_patch_flat(P)
    mp = cv2.warpPerspective(mp, Hd, (PW, PH), flags=cv2.INTER_LINEAR)
    desk = desk + (mp * 0.035)[..., None] * np.array([0.5, 0.65, 1.0], np.float32) * (desk.mean(-1, keepdims=True) * 4 + 0.4)
    p_rgb, p_a = lit_paper(stub, height=height)
    Hp = paper_H()
    pw_ = cv2.warpPerspective(p_rgb, Hp, (PW, PH), flags=cv2.INTER_LINEAR)
    pa_ = cv2.warpPerspective(p_a, Hp, (PW, PH), flags=cv2.INTER_LINEAR)
    sh = cv2.GaussianBlur(np.roll(np.roll(pa_, 10, 0), -14, 1), (0, 0), 8)
    desk = desk * (1 - 0.5 * sh)[..., None]
    desk = desk * (1 - pa_[..., None]) + pw_ * pa_[..., None]
    alpha = dmask.copy()
    desk = objects(desk, alpha, stub, height=height)
    c_rgb, c_a = candle_sprite(height=height)
    return dict(wall=wall, window=win, desk=desk, desk_a=np.clip(alpha, 0, 1), paper_H=Hp, paper_a=pa_, candle=c_rgb, candle_a=c_a)
