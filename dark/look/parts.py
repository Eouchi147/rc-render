"""Builders: figures, camels, ship, houses, tents, towers, flames. All in design space (1080 x 1920)."""
import math
import numpy as np
from core import Item, Light, P, rect, ellipse, catmull, stroke_poly, T, rng, fbm1d

DARK = (0.06, 0.055, 0.05)


def _xf(pts, x, y, h, face):
    Q = P(pts)
    return np.stack([x + Q[:, 0] * h * face, y - Q[:, 1] * h], 1)


def _rot(pts, ang, ox, oy):
    Q = P(pts).copy()
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    X, Y = Q[:, 0] - ox, Q[:, 1] - oy
    return np.stack([ox + X * c - Y * s, oy + X * s + Y * c], 1)


def limb(a, b, c, w0, w1, w2):
    """two-segment tapered limb polygon in unit space: a->b->c."""
    pts = catmull([a, b, c], 6)
    n = len(pts)
    ws = np.interp(np.linspace(0, 1, n), [0, 0.5, 1], [w0, w1, w2])
    d = np.gradient(pts, axis=0)
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    return np.vstack([pts + nrm * ws[:, None] / 2, (pts - nrm * ws[:, None] / 2)[::-1]])


def figure(x, y, h, face=1, z=0.8, col=DARK, robe=0.25, step=0.0, bow=0.0, arm='hang', arm2='hang',
           hat=None, collar=None, bandage=False, one_eye=False, cloak=False, headcloth=False, female=False,
           baby=False, torch=False, staff=False, halberd=False, rope_to=None, key=1.0, recv=1.0, name='fig',
           collar_col=(0.88, 0.86, 0.8), band_col=(0.86, 0.84, 0.78), seed=0, light_I=1.6, sit=False,
           bulk=1.0, outline=True, hair=False):
    """A standing/walking person. (x, y) = feet on ground. Returns (items, lights)."""
    r = rng(seed)
    items, lights = [], []
    body = []
    hip = (0.0, 0.5)
    lean = bow
    # legs
    if sit:
        body.append(limb((0.0, 0.5), (0.16, 0.47), (0.17, 0.25), 0.075 * bulk, 0.06, 0.05))
        body.append(limb((0.0, 0.5), (0.13, 0.45), (0.1, 0.24), 0.075 * bulk, 0.06, 0.05))
    else:
        s = step
        fA = (0.17 * s, 0.0)
        fB = (-0.17 * s, 0.0)
        kA = (0.09 * s + 0.02, 0.26)
        kB = (-0.06 * s - 0.01, 0.25)
        body.append(limb(hip, kA, (fA[0], 0.03), 0.085 * bulk, 0.06, 0.05))
        body.append(limb(hip, kB, (fB[0], 0.03), 0.085 * bulk, 0.06, 0.05))
        for f in (fA, fB):
            body.append(P([(f[0] - 0.03, 0.0), (f[0] + 0.07, 0.0), (f[0] + 0.065, 0.03), (f[0] - 0.03, 0.045)]))
    # torso (unit space, before lean)
    tw = 0.075 * bulk
    torso = P([(-tw, 0.8), (tw + 0.01, 0.8), (tw * 0.85, 0.62), (tw * 0.95, 0.5), (-tw * 0.95, 0.5), (-tw * 0.9, 0.62)])
    up = [torso]
    # head
    hx, hy = 0.015, 0.915
    head = ellipse(hx, hy, 0.058, 0.07, 28)
    nose = P([(hx + 0.05, hy + 0.01), (hx + 0.075, hy - 0.015), (hx + 0.045, hy - 0.025)])
    neck = P([(-0.03, 0.78), (0.035, 0.78), (0.03, 0.86), (-0.025, 0.86)])
    up += [head, nose, neck]
    if hair or female:
        up.append(P([(hx - 0.06, hy + 0.04), (hx + 0.03, hy + 0.08), (hx - 0.075, hy - 0.08), (hx - 0.05, hy - 0.12)]))
    if headcloth or female:
        up.append(P([(hx - 0.075, hy + 0.06), (hx + 0.02, hy + 0.09), (hx + 0.07, hy + 0.03), (hx + 0.04, hy - 0.03),
                     (hx - 0.02, hy - 0.06), (-0.09, 0.72), (-0.11, 0.68), (-0.1, 0.8)]))
    if hat == 'brim':
        up.append(ellipse(hx, hy + 0.055, 0.12, 0.018, 24))
        up.append(P([(hx - 0.055, hy + 0.06), (hx - 0.045, hy + 0.13), (hx + 0.05, hy + 0.13), (hx + 0.055, hy + 0.06)]))
    elif hat == 'tricorn':
        up.append(P([(hx - 0.1, hy + 0.05), (hx + 0.1, hy + 0.05), (hx + 0.07, hy + 0.1), (hx, hy + 0.12), (hx - 0.07, hy + 0.1)]))
    elif hat == 'cap':
        up.append(P([(hx - 0.062, hy + 0.03), (hx + 0.06, hy + 0.035), (hx + 0.03, hy + 0.1), (hx - 0.05, hy + 0.11), (hx - 0.09, hy + 0.06)]))
    elif hat == 'cone':
        up.append(P([(hx - 0.07, hy + 0.035), (hx + 0.07, hy + 0.035), (hx + 0.005, hy + 0.15)]))
    elif hat == 'morion':
        up.append(P([(hx - 0.13, hy + 0.04), (hx - 0.06, hy + 0.07), (hx - 0.03, hy + 0.13), (hx + 0.03, hy + 0.13),
                     (hx + 0.06, hy + 0.07), (hx + 0.13, hy + 0.05), (hx + 0.07, hy + 0.035), (hx - 0.07, hy + 0.035)]))
    elif hat == 'hood':
        up.append(P([(hx - 0.085, hy - 0.06), (hx - 0.085, hy + 0.05), (hx - 0.02, hy + 0.11), (hx + 0.06, hy + 0.07),
                     (hx + 0.07, hy + 0.02), (hx + 0.03, hy + 0.05), (hx - 0.04, hy - 0.08)]))
    # robe / coat skirt
    hem = max(0.5 - robe, 0.03)
    if robe > 0.02:
        fl = 0.05 + robe * 0.25
        sk = P([(-tw * 0.95, 0.52), (tw * 0.95 + 0.01, 0.52), (tw + fl + 0.02 * step, hem), (-tw - fl + 0.02 * step, hem - 0.01)])
        up.append(sk)
    if cloak:
        up.append(P([(-0.06, 0.82), (0.02, 0.84), (-0.07, 0.6), (-0.16 - 0.03 * step, max(hem, 0.2) - 0.03),
                     (-0.02, max(hem, 0.2)), (-0.09, 0.62)]))
    # arms (unit space, attached at shoulder)
    sh = (0.0, 0.78)

    def arm_pts(kind):
        if kind == 'hang':
            return sh, (0.03, 0.63), (0.04, 0.5)
        if kind == 'fwd':          # hand on the shoulder of the man ahead
            return sh, (0.13, 0.74), (0.27, 0.77)
        if kind == 'up':           # torch raised
            return sh, (0.1, 0.84), (0.13, 1.0)
        if kind == 'lead':         # holding a rope, forward-down
            return sh, (0.08, 0.66), (0.2, 0.6)
        if kind == 'staff':
            return sh, (0.07, 0.66), (0.15, 0.62)
        if kind == 'chest':        # holding a baby
            return sh, (0.08, 0.65), (0.04, 0.7)
        if kind == 'back':
            return sh, (-0.05, 0.63), (-0.08, 0.5)
        if kind == 'bound':        # hands tied behind
            return sh, (-0.06, 0.66), (-0.02, 0.55)
        if kind == 'reach':        # both arms up (rain)
            return sh, (0.06, 0.92), (0.1, 1.06)
        return sh, (0.03, 0.63), (0.04, 0.5)
    hands = []
    for kind in (arm, arm2):
        a, b, c = arm_pts(kind)
        up.append(limb(a, b, c, 0.06 * bulk, 0.05, 0.04))
        up.append(ellipse(c[0], c[1], 0.022, 0.022, 10))
        hands.append(c)
    if baby:
        up.append(ellipse(0.07, 0.7, 0.06, 0.035, 18))
    # lean upper body around the hip
    ups = [_rot(p, -lean, 0.0, 0.5) for p in up]
    hands = [tuple(_rot([hnd], -lean, 0.0, 0.5)[0]) for hnd in hands]
    allb = body + ups
    polys = [_xf(p, x, y, h, face) for p in allb]
    items.append(Item(polys=polys, z=z, col=col, mat='figure', key=key, recv=recv, outline=outline, name=name))
    headc = _rot([(hx, hy)], -lean, 0.0, 0.5)[0]
    if collar:
        cpts = ellipse(0.005, 0.795, 0.075 if collar == 'ruff' else 0.06, 0.022 if collar == 'ruff' else 0.03, 20)
        if collar == 'band':
            cpts = P([(-0.05, 0.81), (0.06, 0.81), (0.07, 0.75), (0.0, 0.73), (-0.05, 0.76)])
        cpts = _rot(cpts, -lean, 0.0, 0.5)
        items.append(Item(polys=[_xf(cpts, x, y, h, face)], z=z + 0.001, col=collar_col, mat='cloth', key=key,
                          recv=recv, outline=False, name=name + '_collar'))
    if bandage:
        bw = 0.024
        bpts = P([(hx - 0.062, hy + 0.012 + bw), (hx + 0.066, hy + 0.016 + bw), (hx + 0.066, hy + 0.012 - bw * 0.6),
                  (hx - 0.062, hy + 0.0 - bw * 0.6)])
        if one_eye:
            bpts = P([(hx - 0.06, hy + 0.045), (hx + 0.03, hy + 0.035), (hx + 0.066, hy + 0.0), (hx + 0.066, hy - 0.02),
                      (hx + 0.02, hy + 0.005), (hx - 0.062, hy + 0.0)])
        bpts = _rot(bpts, -lean, 0.0, 0.5)
        items.append(Item(polys=[_xf(bpts, x, y, h, face)], z=z + 0.001, col=band_col, mat='cloth', key=key,
                          recv=recv, outline=False, name=name + '_band'))
    if torch:
        hx_, hy_ = hands[0]
        top = (hx_ + 0.02, hy_ + 0.16)
        stick = _xf([(hx_ - 0.01, hy_ - 0.06), top], x, y, h, face)
        items.append(Item(lines=[(stick, max(0.018 * h, 2))], z=z + 0.002, col=(0.18, 0.12, 0.08), mat='wood',
                          key=key, recv=recv, name=name + '_torch'))
        fx, fy = _xf([top], x, y, h, face)[0]
        items.extend(flame(fx, fy, 0.11 * h, z + 0.003, seed=seed + 7))
        lights.append(Light(fx, fy - 0.04 * h, (1.0, 0.55, 0.22), I=light_I, r=0.95 * h, z=z, flare=0.5, air=0.12))
    if staff or halberd:
        hx_, hy_ = hands[0]
        bot = _xf([(hx_ + 0.02, 0.0)], x, y, h, face)[0]
        topp = _xf([(hx_ + 0.03, 1.05 if staff else 1.25)], x, y, h, face)[0]
        items.append(Item(lines=[(P([bot, topp]), max(0.016 * h, 2))], z=z + 0.002, col=(0.16, 0.12, 0.09), mat='wood',
                          key=key, recv=recv, name=name + '_staff'))
        if halberd:
            tx, ty = topp
            blade = P([(tx, ty + 0.02 * h), (tx + 0.09 * h * face, ty + 0.05 * h), (tx + 0.1 * h * face, ty + 0.12 * h),
                       (tx + 0.01 * h * face, ty + 0.14 * h), (tx, ty - 0.08 * h), (tx - 0.04 * h * face, ty + 0.06 * h)])
            items.append(Item(polys=[blade], z=z + 0.002, col=(0.35, 0.36, 0.38), mat='metal', key=key, recv=recv,
                              name=name + '_blade'))
    if rope_to is not None:
        hx_, hy_ = hands[1] if arm2 == 'lead' else hands[0]
        a = _xf([(hx_, hy_)], x, y, h, face)[0]
        b = P(rope_to)
        mid = (a + b) / 2 + (0, 0.06 * h)
        items.append(Item(lines=[(catmull([a, mid, b], 6), max(0.008 * h, 1.5))], z=z - 0.002, col=(0.2, 0.15, 0.1),
                          mat='rope', key=key, recv=recv, outline=False, name=name + '_rope'))
    return items, lights


def flame(x, y, s, z, seed=0, col=(1.0, 0.62, 0.22), core=(1.0, 0.92, 0.6)):
    r = rng(seed)
    pts = []
    n = 14
    for i in range(n + 1):
        t = i / n
        ang = math.pi * t
        w = math.sin(ang) ** 0.8 * (1 - t * 0.35)
        pts.append((x - s * 0.35 * w * math.cos(0) + 0, 0))
    outer = []
    for i in range(24):
        t = i / 23
        side = -1 if i < 12 else 1
        u = t * 2 if t < 0.5 else (1 - t) * 2
        hh = (1 - u) * s * 1.3
        ww = math.sin(u * math.pi * 0.95) * s * 0.33 * (1 + 0.25 * (r.random() - 0.5))
        outer.append((x + side * ww + (r.random() - 0.5) * s * 0.08, y - hh))
    outer = P(outer)
    inner = T(outer, s=0.55, ox=x, oy=y - s * 0.1)
    return [Item(polys=[outer], z=z, col=col, mat='fire', emit=2.2, key=0, recv=0, outline=False, name='flame', glow=1.0),
            Item(polys=[inner], z=z + 0.001, col=core, mat='fire', emit=3.0, key=0, recv=0, outline=False, name='flame_core')]


# ------------------------------------------------------------------ camels
CAMEL = [(-1.2, 1.62), (-1.08, 1.78), (-0.8, 1.9), (-0.55, 2.06), (-0.25, 2.28), (0.0, 2.25), (0.25, 2.06),
         (0.45, 1.88), (0.65, 1.8), (0.95, 1.72), (1.25, 1.62), (1.48, 1.72), (1.62, 1.95), (1.7, 2.15), (1.72, 2.25),
         (1.7, 2.34), (1.78, 2.27), (1.9, 2.24), (2.1, 2.15), (2.22, 2.08), (2.28, 2.0), (2.25, 1.94), (2.12, 1.92),
         (2.0, 1.95), (1.85, 1.98), (1.72, 1.95), (1.62, 1.85), (1.55, 1.68), (1.45, 1.45), (1.3, 1.28), (1.1, 1.15),
         (0.92, 1.05), (0.8, 0.98), (0.5, 0.98), (0.0, 0.96), (-0.45, 1.0), (-0.75, 1.08), (-1.05, 1.25), (-1.18, 1.45)]
BELLY = (32, 33, 34, 35)


def camel(x, y, h, face=1, z=0.7, col=DARK, gait=0.0, pregnant=False, head=0.0, seed=0, key=1.0, recv=1.0,
          name='camel', saddle=False):
    """Dromedary in profile. (x, y) = ground under the body centre; h = height of the hump (~2.25 units)."""
    u = h / 2.25
    body = P(CAMEL).copy()
    if pregnant:
        for i in BELLY:
            body[i, 1] -= 0.14 if i in (33, 34) else 0.08
    if head:
        sel = slice(10, 28)
        body[sel] = _rot(body[sel], head, 1.1, 1.5)
    out = catmull(body, 5, closed=True)
    polys = [out]
    g = gait
    legs = [((0.72, 1.06), (0.74 + 0.12 * g, 0.6), (0.76 + 0.24 * g, 0.1)),
            ((0.6, 1.04), (0.6 - 0.1 * g, 0.6), (0.56 - 0.22 * g, 0.1)),
            ((-0.82, 1.15), (-1.0 - 0.06 * g, 0.62), (-0.86 - 0.2 * g, 0.1)),
            ((-0.66, 1.12), (-0.86 + 0.1 * g, 0.62), (-0.68 + 0.22 * g, 0.1))]
    for a, b, c in legs:
        polys.append(limb(a, b, c, 0.27, 0.13, 0.1))
        polys.append(P([(c[0] - 0.1, 0.0), (c[0] + 0.12, 0.0), (c[0] + 0.07, 0.11), (c[0] - 0.06, 0.12)]))
    polys.append(limb((-1.16, 1.58), (-1.24, 1.25), (-1.2, 0.98), 0.07, 0.045, 0.06))
    polys = [_xf(p, x, y, u, face) for p in polys]
    items = [Item(polys=polys, z=z, col=col, mat='animal', key=key, recv=recv, name=name)]
    if saddle:
        sp = _xf(P([(-0.5, 2.1), (-0.25, 2.36), (0.12, 2.36), (0.35, 2.12), (0.2, 1.95), (-0.35, 1.95)]), x, y, u, face)
        items.append(Item(polys=[sp], z=z + 0.001, col=(0.3, 0.16, 0.1), mat='cloth', key=key, recv=recv, name=name + '_saddle'))
    return items


# ------------------------------------------------------------------ architecture
def house_gable(x, y, w, floors, fh, roof_h, z, wall=(0.62, 0.56, 0.48), timber=(0.2, 0.14, 0.1), roof=(0.25, 0.16, 0.13),
                jetty=8, seed=0, lit=0.25, key=1.0, recv=1.0, win_col=(1.0, 0.7, 0.35), name='house', chimney=True,
                timber_w=5, braces=True):
    """Half-timbered front-gable house. (x, y) = bottom-left on the street."""
    r = rng(seed)
    items, lights = [], []
    polys = []
    tl = []
    cur_y = y
    x0, x1 = x, x + w
    floor_boxes = []
    for f in range(floors):
        top = cur_y - fh
        polys.append(rect(x0, top, x1, cur_y))
        floor_boxes.append((x0, top, x1, cur_y))
        cur_y = top
        x0 -= jetty
        x1 += jetty
    x0 += jetty
    x1 -= jetty
    apex = (x0 + x1) / 2
    gable = P([(x0, cur_y), (x1, cur_y), (apex, cur_y - roof_h)])
    polys.append(gable)
    items.append(Item(polys=polys, z=z, col=wall, mat='plaster', key=key, recv=recv, name=name, hatch=0))
    # roof edge (bargeboards) as thick strips
    over = 14
    rp = P([(x0 - over, cur_y + 6), (apex, cur_y - roof_h - 10), (x1 + over, cur_y + 6), (x1 + over - 16, cur_y + 6),
            (apex, cur_y - roof_h + 10), (x0 - over + 16, cur_y + 6)])
    items.append(Item(polys=[rp], z=z + 0.002, col=roof, mat='roof', key=key, recv=recv, name=name + '_roof', hatch=45))
    # timber framing
    for (bx0, by0, bx1, by1) in floor_boxes:
        tl.append((P([(bx0, by1), (bx1, by1)]), timber_w + 1))
        tl.append((P([(bx0, by0), (bx1, by0)]), timber_w + 1))
        nb = max(2, int((bx1 - bx0) / 46))
        xs = np.linspace(bx0 + 3, bx1 - 3, nb + 1)
        for xx in xs:
            tl.append((P([(xx, by0), (xx, by1)]), timber_w))
        if braces:
            for i in range(nb):
                if r.random() < 0.55:
                    a, b = xs[i], xs[i + 1]
                    if r.random() < 0.5:
                        tl.append((P([(a, by1), (b, by0)]), timber_w - 1))
                    else:
                        tl.append((P([(a, by0), (b, by1)]), timber_w - 1))
        # windows
        nwin = nb
        for i in range(nwin):
            a, b = xs[i], xs[i + 1]
            ww = (b - a) * 0.45
            wh = (by1 - by0) * 0.42
            cx = (a + b) / 2
            cy = by0 + (by1 - by0) * 0.45
            if r.random() < 0.8:
                on = r.random() < lit
                wp = rect(cx - ww / 2, cy - wh / 2, cx + ww / 2, cy + wh / 2)
                items.append(Item(polys=[wp], z=z + 0.003, col=win_col if on else (0.08, 0.07, 0.07), mat='window',
                                  emit=1.6 if on else 0.0, key=0.3, recv=recv * 0.5, outline=True, name=name + '_win'))
                if on:
                    lights.append(Light(cx, cy, win_col, I=0.35, r=60, z=z, air=0.08))
                tl.append((P([(cx, cy - wh / 2), (cx, cy + wh / 2)]), 2))
    # gable timbers
    tl.append((P([(x0 + 10, cur_y), (apex, cur_y - roof_h + 8)]), timber_w))
    tl.append((P([(x1 - 10, cur_y), (apex, cur_y - roof_h + 8)]), timber_w))
    tl.append((P([(apex, cur_y), (apex, cur_y - roof_h + 10)]), timber_w))
    items.append(Item(lines=tl, z=z + 0.002, col=timber, mat='wood', key=key, recv=recv, name=name + '_timber', detail=True))
    if chimney:
        cxp = apex + (r.random() - 0.5) * w * 0.3
        items.append(Item(polys=[rect(cxp - 9, cur_y - roof_h * 0.75, cxp + 9, cur_y - roof_h * 0.35)], z=z - 0.001,
                          col=roof, mat='stone', key=key, recv=recv, name=name + '_chim'))
    return items, lights


def roofline(x0, x1, base, z, seed, col=(0.12, 0.11, 0.12), hmin=60, hmax=150, wmin=60, wmax=130, lit=0.15,
             win_col=(1.0, 0.68, 0.32), key=0.6, recv=0.4, name='roofs', spires=()):
    """A row of distant gables and roofs as one silhouette + lit windows."""
    r = rng(seed)
    polys = []
    items, lights = [], []
    x = x0
    while x < x1:
        w = r.uniform(wmin, wmax)
        hgt = r.uniform(hmin, hmax)
        kind = r.random()
        wall_top = base - hgt * 0.55
        if kind < 0.55:   # front gable
            polys.append(P([(x, base + 10), (x, wall_top), (x + w / 2, base - hgt), (x + w, wall_top), (x + w, base + 10)]))
        else:             # eaves side with steep roof
            polys.append(P([(x, base + 10), (x, wall_top), (x + w * 0.15, base - hgt * 0.95), (x + w * 0.85, base - hgt * 0.95),
                            (x + w, wall_top), (x + w, base + 10)]))
        if r.random() < 0.5:
            cx = x + r.uniform(0.2, 0.8) * w
            polys.append(rect(cx - 5, base - hgt * 1.02, cx + 5, base - hgt * 0.7))
        for k in range(r.integers(0, 3)):
            if r.random() < lit:
                wx = x + r.uniform(0.2, 0.8) * w
                wy = base - r.uniform(0.15, 0.45) * hgt
                items.append(Item(polys=[rect(wx - 5, wy - 7, wx + 5, wy + 7)], z=z + 0.001, col=win_col, mat='window',
                                  emit=1.5, key=0, recv=0, outline=False, name=name + '_win'))
        x += w * r.uniform(0.8, 1.0)
    for sp in spires:
        polys.extend(sp)
    items.insert(0, Item(polys=polys, z=z, col=col, mat='roofs', key=key, recv=recv, name=name, hatch=0))
    return items, lights


def tower(x, y, w, h, roof_h, z, col=(0.5, 0.48, 0.45), roof=(0.2, 0.18, 0.2), kind='spire', key=1.0, recv=1.0,
          name='tower', windows=2):
    items = []
    polys = [rect(x - w / 2, y - h, x + w / 2, y)]
    items.append(Item(polys=polys, z=z, col=col, mat='stone', key=key, recv=recv, name=name, hatch=90))
    if kind == 'spire':
        rp = P([(x - w / 2 - 4, y - h), (x + w / 2 + 4, y - h), (x, y - h - roof_h)])
    elif kind == 'pyramid':
        rp = P([(x - w / 2 - 5, y - h), (x + w / 2 + 5, y - h), (x, y - h - roof_h * 0.45)])
    elif kind == 'cone':
        rp = P([(x - w / 2 - 6, y - h), (x + w / 2 + 6, y - h), (x, y - h - roof_h)])
    else:
        rp = None
    if rp is not None:
        items.append(Item(polys=[rp], z=z + 0.001, col=roof, mat='roof', key=key, recv=recv, name=name + '_roof', hatch=60))
    for k in range(windows):
        wy = y - h * (0.35 + 0.4 * k / max(windows, 1))
        items.append(Item(polys=[ellipse(x, wy - 8, w * 0.12, 6, 12, math.pi, 2 * math.pi), rect(x - w * 0.12, wy - 8, x + w * 0.12, wy + 12)],
                          z=z + 0.002, col=(0.05, 0.05, 0.06), mat='window', key=0, recv=0, name=name + '_slit', outline=False))
    return items


def tent(x, y, w, h, z, col=(0.09, 0.08, 0.075), open_side=True, seed=0, key=0.6, recv=1.0, name='tent', glow=None,
         poles=3):
    """Black goat-hair tent: long, low, sagging between pole tops. (x, y) = left ground point."""
    r = rng(seed)
    items = []
    tops = [(x + w * (i + 0.5) / poles, y - h * (0.95 + 0.08 * r.random())) for i in range(poles)]
    roof = [(x - w * 0.06, y - h * 0.32)]
    for i, tp in enumerate(tops):
        roof.append(tp)
        if i < poles - 1:
            nx = tops[i + 1]
            roof.append(((tp[0] + nx[0]) / 2, (tp[1] + nx[1]) / 2 + h * 0.16))
    roof.append((x + w * 1.06, y - h * 0.32))
    eave = [(x + w * 1.0, y - h * 0.22), (x + w * 0.5, y - h * 0.3), (x, y - h * 0.22)]
    poly = P(roof + eave)
    items.append(Item(polys=[catmull(poly, 4, closed=True)], z=z, col=col, mat='tent', key=key, recv=recv, name=name, hatch=-10))
    # walls (curtains) hanging to ground, with an open section lit from inside
    wall = P([(x, y - h * 0.22), (x + w, y - h * 0.22), (x + w, y), (x, y)])
    items.append(Item(polys=[wall], z=z - 0.002, col=tuple(c * 0.8 for c in col), mat='tent', key=key, recv=recv, name=name + '_wall', hatch=90))
    if open_side:
        ox0 = x + w * 0.38
        ox1 = x + w * 0.72
        op = P([(ox0, y - h * 0.22), (ox1, y - h * 0.22), (ox1 + 6, y), (ox0 - 6, y)])
        gcol = glow if glow is not None else (0.03, 0.025, 0.02)
        items.append(Item(polys=[op], z=z + 0.001, col=gcol, mat='window', emit=1.2 if glow else 0.0, key=0, recv=0.5,
                          name=name + '_open', outline=False))
    ropes = []
    for tp in tops:
        for sgn in (-1, 1):
            if r.random() < 0.8:
                ropes.append((P([tp, (tp[0] + sgn * w * 0.35, y + 4)]), 1.6))
    for p in (0, 1):
        ropes.append((P([(x + w * (0.03 + 0.94 * p), y - h * 0.25), (x + w * (-0.18 + 1.36 * p), y + 6)]), 1.6))
    items.append(Item(lines=ropes, z=z - 0.003, col=(0.16, 0.13, 0.1), mat='rope', key=key, recv=recv, name=name + '_ropes',
                      outline=False, detail=True))
    for tp in tops:
        items.append(Item(lines=[(P([tp, (tp[0], y)]), 3)], z=z - 0.004, col=(0.2, 0.15, 0.1), mat='wood', key=key, recv=recv,
                          name=name + '_pole', outline=False, detail=True))
    return items


# ------------------------------------------------------------------ ship
def ship(x, y, L, z=0.6, face=-1, hull=(0.12, 0.09, 0.07), sail=(0.62, 0.6, 0.55), spar=(0.1, 0.08, 0.07),
         seed=0, key=1.0, recv=1.0, people=20, lantern=True, nets=True):
    """Small three-masted merchant ship in near-profile, bow toward `face`. (x, y) = waterline at the stern end,
    L = hull length in px. Returns (items, lights)."""
    r = rng(seed)
    u = L / 65.0  # feet -> px

    def X(fx):
        return x + face * (65 - fx) * u * -1 if face == 1 else x - (65 - fx) * u

    def pt(fx, fy):
        # fx: 0 = bow, 65 = stern. bow toward face
        if face == -1:
            return (x - (65 - fx) * u, y - fy * u)
        return (x + (65 - fx) * u, y - fy * u)
    items, lights = [], []
    hullp = [pt(-1, 9.5), pt(3, 8.4), pt(18, 7.2), pt(32, 6.8), pt(46, 7.6), pt(48, 9.6), pt(64, 10.8), pt(65.5, 11.4),
             pt(65.5, 2), pt(64.5, -1.5), pt(55, -2.5), pt(20, -2.5), pt(6, -2.0), pt(1.5, 0.5), pt(-0.5, 5)]
    items.append(Item(polys=[P(hullp)], z=z, col=hull, mat='wood', key=key, recv=recv, name='hull', hatch=0))
    # wale / rail lines
    wl = [(P([pt(0.5, 6.0), pt(20, 4.6), pt(40, 4.5), pt(64.8, 6.8)]), 3.0 * u),
          (P([pt(1, 8.6), pt(18, 7.3), pt(32, 6.9), pt(46, 7.7)]), 1.2 * u)]
    items.append(Item(lines=wl, z=z + 0.002, col=(0.05, 0.04, 0.035), mat='wood', key=key, recv=recv, name='wales', detail=True, outline=False))
    # transom (3/4 stern) with windows
    tr = P([pt(65.5, 11.4), pt(68.5, 10.6) if face == -1 else pt(62.5, 10.6), (pt(68.5, 2.5) if face == -1 else pt(62.5, 2.5)), pt(65.5, 2)])
    if face == -1:
        tr = P([pt(65.5, 11.4), (x + 3.2 * u, y - 10.8 * u), (x + 3.2 * u, y - 2.8 * u), pt(65.5, 2)])
    items.append(Item(polys=[tr], z=z + 0.001, col=tuple(c * 1.25 for c in hull), mat='wood', key=key, recv=recv, name='transom'))
    if lantern:
        for k in range(3):
            wx0 = x + (0.3 + k * 0.95) * u
            wp = rect(wx0, y - 9.4 * u, wx0 + 0.75 * u, y - 7.6 * u)
            items.append(Item(polys=[wp], z=z + 0.003, col=(1.0, 0.72, 0.35), mat='window', emit=1.8, key=0, recv=0,
                              name='sternwin', outline=False))
        lights.append(Light(x + 1.8 * u, y - 8.5 * u, (1.0, 0.62, 0.3), I=0.7, r=10 * u, z=z, air=0.12, flare=0.3))
        lx, ly = x + 2.0 * u, y - 13.5 * u
        items.append(Item(polys=[rect(lx - 0.5 * u, ly - 0.9 * u, lx + 0.5 * u, ly + 0.9 * u)], z=z + 0.004,
                          col=(1.0, 0.8, 0.45), mat='window', emit=2.4, key=0, recv=0, name='lantern', outline=False))
        lights.append(Light(lx, ly, (1.0, 0.66, 0.32), I=0.9, r=9 * u, z=z, air=0.25, flare=0.6))
    # masts and yards
    masts = [(12, 58), (31, 66), (50, 46)]
    spars = []
    sails = []
    for i, (mx, mh) in enumerate(masts):
        spars.append((P([pt(mx, 7), pt(mx + 0.4, mh)]), 1.1 * u))
        levels = [0.42, 0.66, 0.86] if i < 2 else [0.5, 0.78]
        for j, lv in enumerate(levels):
            yy = 7 + (mh - 7) * lv
            half = (13 - j * 3.5) * (1 if i < 2 else 0.75)
            spars.append((P([pt(mx - half, yy), pt(mx + half, yy)]), 0.6 * u))
            if j == 0:
                # furled course: a thick bundle along the yard
                spars.append((P([pt(mx - half * 0.95, yy + 0.4), pt(mx + half * 0.95, yy + 0.4)]), 1.3 * u))
            elif j == 1 and i < 2:
                # set topsail: trapezoid with billow
                y2 = 7 + (mh - 7) * levels[j + 1] if j + 1 < len(levels) else yy + 8
                top_half = half * 0.78
                bot_half = half
                sp = [pt(mx - top_half, y2 - 0.3), pt(mx + top_half, y2 - 0.3), pt(mx + bot_half, yy + 0.6),
                      pt(mx, yy + 1.6), pt(mx - bot_half, yy + 0.6)]
                sails.append(catmull(P(sp), 5, closed=True))
    # bowsprit and jib
    spars.append((P([pt(1, 9.2), pt(-20, 17)]), 0.9 * u))
    jib = P([pt(-18, 17.2), pt(11.5, 50), pt(4, 12)])
    sails.append(jib)
    items.append(Item(lines=spars, z=z + 0.004, col=spar, mat='wood', key=key, recv=recv, name='spars', outline=False))
    items.append(Item(polys=sails, z=z + 0.003, col=sail, mat='sail', key=key, recv=recv, name='sails', hatch=80))
    # rigging
    rig = []
    for (mx, mh) in masts:
        top = pt(mx + 0.4, mh)
        rig.append((P([top, pt(mx - 9, 8.5)]), 0.25 * u))
        rig.append((P([top, pt(mx + 9, 8.0)]), 0.25 * u))
        rig.append((P([pt(mx + 0.3, mh * 0.62), pt(mx + 5, 7.8)]), 0.2 * u))
    rig.append((P([pt(12.4, 58), pt(-20, 17)]), 0.22 * u))
    rig.append((P([pt(31.4, 66), pt(12.4, 40)]), 0.22 * u))
    rig.append((P([pt(50.4, 46), pt(31.4, 44)]), 0.22 * u))
    rig.append((P([pt(50.4, 46), pt(64, 12)]), 0.22 * u))
    items.append(Item(lines=rig, z=z + 0.001, col=(0.12, 0.1, 0.09), mat='rope', key=key, recv=recv, name='rigging',
                      outline=False, detail=True))
    if nets:
        net = []
        for fx in np.arange(4, 46, 1.6):
            a = pt(fx, 8.0 - 0.025 * fx)
            b = pt(fx + 1.6, 11.6 - 0.025 * fx)
            net.append((P([a, b]), 0.12 * u))
            b2 = pt(fx - 1.6, 11.6 - 0.025 * fx)
            net.append((P([a, b2]), 0.12 * u))
        net.append((P([pt(4, 11.8), pt(46, 10.6)]), 0.2 * u))
        items.append(Item(lines=net, z=z + 0.002, col=(0.15, 0.13, 0.11), mat='rope', key=key, recv=recv, name='nets',
                          outline=False, detail=True, alpha=0.8))
    # people on deck: small figures along the rail
    for k in range(people):
        fx = r.uniform(6, 44)
        fy = 7.6 - 0.02 * fx
        fxp, fyp = pt(fx, fy)
        hh = r.uniform(4.6, 5.6) * u
        it, _ = figure(fxp, fyp, hh, face=face if r.random() < 0.6 else -face, z=z + 0.0025, col=(0.07, 0.06, 0.055),
                       robe=0.0, step=r.uniform(0, 0.5), arm=r.choice(['hang', 'reach', 'hang', 'back']), seed=seed + k,
                       key=key, recv=recv, outline=False, name='deckfig')
        items.extend(it)
    return items, lights


# ------------------------------------------------------------------ nature
def rocks(x0, x1, base, z, seed, col=(0.45, 0.42, 0.4), n=40, smin=20, smax=90, key=1.0, recv=1.0, name='rocks', top=None):
    """a heap of granite boulders; top(x) gives the upper envelope y."""
    r = rng(seed)
    polys = []
    for i in range(n):
        x = r.uniform(x0, x1)
        ytop = top(x) if top else base
        y = r.uniform(ytop, base)
        s = r.uniform(smin, smax) * (0.6 + 0.4 * (y - ytop) / max(base - ytop, 1))
        k = 9
        ang = np.linspace(0, 2 * math.pi, k, endpoint=False) + r.random()
        rad = s * (0.75 + 0.35 * r.random(k))
        pts = np.stack([x + rad * np.cos(ang) * 1.25, y + rad * np.sin(ang) * 0.8], 1)
        polys.append(catmull(pts, 4, closed=True))
    return Item(polys=polys, z=z, col=col, mat='stone', key=key, recv=recv, name=name, hatch=30)


def grass(x0, x1, y0, y1, z, seed, n=400, col=(0.45, 0.35, 0.18), hmin=20, hmax=70, lean=0.25, w=2.0, name='grass'):
    r = rng(seed)
    lines = []
    for i in range(n):
        x = r.uniform(x0, x1)
        y = r.uniform(y0, y1)
        hh = r.uniform(hmin, hmax) * (0.5 + 0.5 * (y - y0) / max(y1 - y0, 1))
        bend = r.normal(lean, 0.25)
        pts = [(x, y), (x + bend * hh * 0.35, y - hh * 0.55), (x + bend * hh, y - hh)]
        lines.append((catmull(pts, 4), w * r.uniform(0.6, 1.3)))
    return Item(lines=lines, z=z, col=col, mat='grass', key=1.0, recv=1.0, name=name, outline=False, detail=True)


def tree_blob(x, y, h, z, seed, col=(0.4, 0.25, 0.12), trunk=(0.16, 0.11, 0.08), name='tree', key=1.0, recv=1.0):
    r = rng(seed)
    polys = []
    for i in range(14):
        cx = x + r.normal(0, h * 0.18)
        cy = y - h * 0.62 + r.normal(0, h * 0.13)
        rr = h * r.uniform(0.12, 0.22)
        polys.append(ellipse(cx, cy, rr * 1.15, rr, 16))
    items = [Item(lines=[(P([(x, y), (x + h * 0.03, y - h * 0.5)]), h * 0.06)], z=z - 0.001, col=trunk, mat='wood',
                  key=key, recv=recv, name=name + '_trunk', outline=False),
             Item(polys=polys, z=z, col=col, mat='foliage', key=key, recv=recv, name=name, hatch=20)]
    return items


def shrub(x, y, s, z, seed, col=(0.18, 0.15, 0.1), name='shrub'):
    r = rng(seed)
    lines = []
    for i in range(18):
        a = math.radians(r.uniform(-150, -30))
        L = s * r.uniform(0.5, 1.0)
        mx = x + math.cos(a) * L * 0.5 + r.normal(0, s * 0.05)
        my = y + math.sin(a) * L * 0.5
        lines.append((catmull([(x, y), (mx, my), (x + math.cos(a) * L, y + math.sin(a) * L)], 4), r.uniform(1.0, 2.6)))
    return Item(lines=lines, z=z, col=col, mat='shrub', key=1.0, recv=1.0, name=name, outline=False, detail=True)
