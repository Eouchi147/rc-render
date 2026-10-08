"""The two records, side by side today in the Staatsbibliothek Bamberg (RB.Msc.148/299 and /300): the court's
protocol (a sewn file in a clerk's hand) and Junius's letter (one sheet, folded, a note written crosswise in the
margin). A dark table, one warm light from above. World in cm; camera looking down at the table."""
import math
import numpy as np
import cv2
import shade as S
import tex as TX
from cam3d import Cam3
import cell as C

PW, PH = 1620, 2880
DENS = 1.5
CAM = Cam3(pos=(60, -16, 64), target=(60, 38, 0), fpx=1650, W=PW, H=PH)
PXCM = 12
TABLE = (-40, 160, -50, 95)
LIGHT = np.array([70.0, 36.0, 62.0])          # a warm lamp above, off frame
PAPER_PX = 54
LETTER = dict(x=58.0, y=14.0, w=21.0, h=32.0, rot=-4.0)
RECORD_L = dict(x=48.0, y=52.0, w=21.0, h=32.0, rot=2.0)    # the open file: left page
RECORD_R = dict(x=69.2, y=52.7, w=21.0, h=32.0, rot=2.0)    # right page
BASE_CAM = CAM


def warm():
    return np.array([1.0, 0.86, 0.7], np.float32)


def table_flat():
    x0, x1, y0, y1 = TABLE
    w, h = int((x1 - x0) * PXCM), int((y1 - y0) * PXCM)
    alb, N, _ = TX.surface('dark_wooden_planks', h, w, scale=0.9, rot=math.pi / 2, sat=0.6, tint=(1.0, 0.8, 0.62), gain=0.55)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    X = x0 + xx / PXCM
    Y = y1 - yy / PXCM
    P = np.stack([X, Y, np.zeros_like(X)], -1)
    Nw = TX.flatten_normals(np.stack([N[..., 0], -N[..., 1], N[..., 2]], -1), 0.6)
    lit = C.point_light_flat(Nw, P, LIGHT, 4.2, warm(), r=34, spec=0.5, shin=30)
    lit += np.array([0.012, 0.012, 0.016], np.float32)
    # far edge of the table falls into darkness; shelves of files beyond
    rgb = alb * lit
    return rgb.astype(np.float32), (w, h)


def table_H():
    x0, x1, y0, y1 = TABLE
    w, h = int((x1 - x0) * PXCM), int((y1 - y0) * PXCM)
    return CAM.plane_H([(x0, y1, 0), (x1, y1, 0), (x1, y0, 0), (x0, y0, 0)], [(0, 0), (w, 0), (w, h), (0, h)])


def sheet_world(spec, u, v):
    c, s = math.cos(math.radians(spec['rot'])), math.sin(math.radians(spec['rot']))
    lx = u / PAPER_PX - spec['w'] / 2
    ly = spec['h'] / 2 - v / PAPER_PX
    return spec['x'] + lx * c - ly * s, spec['y'] + lx * s + ly * c


def sheet_H(spec, z=0.05):
    w, h = int(spec['w'] * PAPER_PX), int(spec['h'] * PAPER_PX)
    flat = [(0, 0), (w, 0), (w, h), (0, h)]
    world = [(*sheet_world(spec, u, v), z) for u, v in flat]
    return CAM.plane_H(world, flat)


def lit_sheet(spec, seed, folds, age, col, gutter=None, z=0.05):
    w, h = int(spec['w'] * PAPER_PX), int(spec['h'] * PAPER_PX)
    alb, hgt, a = S.paper(h, w, seed=seed, col=col, age=age, folds=folds, deckle=5)
    vv, uu = np.mgrid[0:h, 0:w].astype(np.float32)
    X, Y = sheet_world(spec, uu, vv)
    P = np.stack([X, Y, np.full_like(X, z)], -1)
    n = S.normals(cv2.GaussianBlur(hgt, (0, 0), 1.5), strength=5.0)
    c, s = math.cos(math.radians(spec['rot'])), math.sin(math.radians(spec['rot']))
    Nw = np.stack([n[..., 0] * c + n[..., 1] * s, n[..., 0] * s - n[..., 1] * c, n[..., 2]], -1)
    lit = C.point_light_flat(Nw, P, LIGHT, 3.6, warm(), r=40)
    lit += np.array([0.02, 0.02, 0.026], np.float32)
    rgb = alb * lit
    if gutter == 'right':          # the left page of the open file curves down into the spine on its right edge
        g = np.clip((uu - w * 0.82) / (w * 0.18), 0, 1)
        rgb *= (1 - 0.65 * g ** 1.6)[..., None]
    elif gutter == 'left':
        g = np.clip((w * 0.18 - uu) / (w * 0.18), 0, 1)
        rgb *= (1 - 0.65 * g ** 1.6)[..., None]
    return rgb.astype(np.float32), a


def shelves(h, w, seed=3):
    """Beyond the table: tall shelves of bound files, barely touched by the light."""
    r = np.random.default_rng(seed)
    img = np.zeros((h, w, 3), np.float32) + np.array([0.008, 0.007, 0.007], np.float32)
    for row, (y0, y1) in enumerate([(0, 300), (330, 640), (670, 980)]):
        x = -20
        while x < w:
            bw = r.uniform(28, 70)
            top = y0 + r.uniform(10, 70)
            col = np.array([r.uniform(0.05, 0.11), r.uniform(0.035, 0.07), r.uniform(0.025, 0.05)], np.float32)
            m = S.poly_mask(h, w, [(x, y1), (x, top), (x + bw - 3, top + r.uniform(-4, 4)), (x + bw - 3, y1)])
            shade_ = 0.6 + 0.4 * np.clip(1 - np.abs(np.arange(w) - (x + bw / 2)) / bw, 0, 1)
            img = img * (1 - m[..., None]) + (col * 0.5)[None, None] * m[..., None]
            x += bw
        img[y1:y1 + 30] *= 0.4
    return img


BASE_CAM = CAM


def build(zoom=1.0, center=None):
    global CAM
    CAM = BASE_CAM if zoom == 1.0 else BASE_CAM.zoomed(zoom, center)
    try:
        return _build()
    finally:
        CAM = BASE_CAM


def _build():
    trgb, (tw, th) = table_flat()
    Ht = table_H()
    img = cv2.warpPerspective(trgb, Ht, (PW, PH), flags=cv2.INTER_LINEAR)
    tm = cv2.warpPerspective(np.ones((th, tw), np.float32), Ht, (PW, PH), flags=cv2.INTER_LINEAR)
    sh = shelves(PH, PW)
    img = img * tm[..., None] + sh * 0.6 * (1 - tm[..., None])
    out = {}
    for key, spec, seed, folds, age, col, gut in (
            ('letter', LETTER, 7, ((0.5, 'h'), (0.5, 'v')), 0.9, (0.8, 0.72, 0.58), None),
            ('rec_l', RECORD_L, 8, (), 0.75, (0.82, 0.75, 0.6), 'right'),
            ('rec_r', RECORD_R, 9, (), 0.75, (0.82, 0.75, 0.6), 'left')):
        rgb, a = lit_sheet(spec, seed, folds, age, col, gut)
        Hs = sheet_H(spec)
        wr = cv2.warpPerspective(rgb, Hs, (PW, PH), flags=cv2.INTER_LINEAR)
        wa = cv2.warpPerspective(a, Hs, (PW, PH), flags=cv2.INTER_LINEAR)
        shd = cv2.GaussianBlur(np.roll(np.roll(wa, 12, 0), 10, 1), (0, 0), 10)
        img = img * (1 - 0.6 * shd)[..., None]
        img = img * (1 - wa[..., None]) + wr * wa[..., None]
        out[key + '_H'] = Hs
    # the file's leather cover peeking out under the two pages, and the sewn spine
    out['img'] = img.astype(np.float32)
    return out
