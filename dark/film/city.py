"""Bamberg by night in rain, 1628: the Domberg and the cathedral (east towers lower than the west in 1628), the town
roofs, the old wall, and the Drudenhaus (built June to August 1627) with its portal: Justitia in a niche and the Virgil
line DISCITE JUSTITIAM MONITI ET NON TEMNERE DIVOS. The look-test scene (approved 'Candlelit Oil'), split into depth
layers for parallax, with an optional zoom for detail plates."""
from darkroot import ROOT
import sys
import copy
import math
import numpy as np
import cv2
sys.path.insert(0, ROOT + '/look')
from core import base_render, filmic, P, rect, ellipse, Item, Light
import scenes as LS
import plates as PL

PW, PH = 1620, 2880
GROUPS = [('far', 0.0, 0.42), ('wall', 0.42, 0.58), ('house', 0.58, 0.75), ('figures', 0.75, 1.01)]


def scene():
    sc = LS.bamberg()
    # move Justitia's niche up a little so the inscription band fits between the arch and the niche
    for it in sc.items:
        if it.name in ('niche', 'justitia', 'scales', 'pans'):
            it.polys = [p + np.array([0, -26], np.float32) for p in it.polys]
            it.lines = [(p + np.array([0, -26], np.float32), w) for p, w in it.lines]
    band = rect(492, 1196, 628, 1220)
    sc.add(Item(polys=[band], z=0.6025, col=(0.66, 0.63, 0.56), mat='stone', key=1.0, name='inscription_band'))
    return sc


def zoom_scene(sc, zoom, center):
    """Scale the whole design around `center` (design px) so it renders as a detail plate."""
    if zoom == 1.0:
        return sc
    s2 = copy.deepcopy(sc)
    c = np.array(center, np.float32)
    m = np.array([540.0, 960.0], np.float32)
    f = lambda p: (p - c) * zoom + m
    for it in s2.items:
        it.polys = [f(p) for p in it.polys]
        it.lines = [(f(p), w * zoom) for p, w in it.lines]
        if it.wline is not None:
            it.wline = (it.wline - c[1]) * zoom + m[1]
    for L in s2.lights:
        L.x, L.y = (L.x - c[0]) * zoom + m[0], (L.y - c[1]) * zoom + m[1]
        L.r *= zoom
    sk = s2.sky
    if 'glow' in sk:
        sk['glow'] = [((gx - c[0]) * zoom + m[0], (gy - c[1]) * zoom + m[1], r * zoom, col, a) for gx, gy, r, col, a in sk['glow']]
    if 'moon' in sk:
        mx, my, mr, mc = sk['moon']
        sk['moon'] = ((mx - c[0]) * zoom + m[0], (my - c[1]) * zoom + m[1], mr * zoom, mc)
    if s2.sun is not None:
        s2.sun = ((s2.sun[0] - c[0]) * zoom + m[0], (s2.sun[1] - c[1]) * zoom + m[1])
    return s2


def inscription(img, zoom, center, S):
    """Carve the Virgil line into the band over the portal (relief lit by the lantern on the right)."""
    from PIL import Image, ImageDraw, ImageFont
    x0, y0, x1, y1 = 492, 1196, 628, 1220
    c = np.array(center, np.float32)
    m = np.array([540.0, 960.0], np.float32)
    X0, Y0 = ((np.array([x0, y0]) - c) * zoom + m) * S
    X1, Y1 = ((np.array([x1, y1]) - c) * zoom + m) * S
    w, h = int(X1 - X0), int(Y1 - Y0)
    if w < 40 or h < 8:
        return img
    ss = 4
    im = Image.new('L', (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    txt1, txt2 = 'DISCITE IVSTITIAM MONITI', 'ET NON TEMNERE DIVOS'
    f = ImageFont.truetype(ROOT + '/fonts/Cinzel[wght].ttf', int(h * ss * 0.36))
    for k, t in enumerate((txt1, txt2)):
        tw = f.getlength(t)
        d.text(((w * ss - tw) / 2, h * ss * (0.08 + 0.46 * k)), t, font=f, fill=255)
    a = cv2.resize(np.asarray(im, np.float32) / 255.0, (w, h), interpolation=cv2.INTER_AREA)
    hgt = cv2.GaussianBlur(-a, (0, 0), max(0.6, h * 0.02))
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3)
    shade = np.clip(1 + (gx * 1.0 - gy * 0.6) * 4, 0.3, 1.6)
    ys, xs = int(Y0), int(X0)
    reg = img[ys:ys + h, xs:xs + w]
    reg *= (1 - 0.55 * a)[..., None]
    reg *= shade[..., None] ** 0.7
    return img


def render_layers(zoom=1.0, center=(560, 1200)):
    sc = zoom_scene(scene(), zoom, center)
    out = {}
    for name, z0, z1 in GROUPS:
        s2 = copy.copy(sc)
        s2.items = [it for it in sc.items if z0 <= it.z < z1]
        if name != 'far':
            s2.fog = []
        buf = base_render(s2, PW, PH)
        img = buf['img']
        if name == 'house':
            img = inscription(img, zoom, center, buf['S'])
        img = filmic(img, exposure=1.3, contrast=1.1, sat=1.25)
        a = None if name == 'far' else np.clip(buf['cover'], 0, 1)
        out[name] = (img.astype(np.float32), a)
    # positions of live lights (torch, lantern) in plate px
    lights = []
    for L in sc.lights:
        lights.append((L.x * PW / 1080, L.y * PW / 1080, L.r * PW / 1080, L.I))
    out['lights'] = lights
    return out


def prepare(zoom=1.0, center=(560, 1200), force=False):
    name = 'city' + ('' if zoom == 1.0 else f'_z{zoom:g}_{int(center[0])}_{int(center[1])}')
    z = None if force else PL.load(name)
    if z is not None:
        return z
    L = render_layers(zoom, center)
    sc_ = 1.5 * zoom / (1.0 if zoom == 1.0 else 1.6)
    arrs = {}
    for k, v in L.items():
        if k == 'lights':
            continue
        img, a = v
        pr, pa = PL.paint_layer(img, a, sc_, seed=31 + len(arrs), display=True, detail=1.2 if k == 'house' else 1.0)
        arrs[k] = pr
        if pa is not None:
            arrs[k + '_a'] = pa
    arrs['lights'] = np.array(L['lights'], np.float32)
    PL.save(name, **arrs)
    return PL.load(name)
