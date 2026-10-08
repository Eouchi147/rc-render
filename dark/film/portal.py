"""The portal of the Drudenhaus, close: sandstone, a moulded arch, the carved Virgil line over the door, Justitia in her
niche (scales raised, sword lowered), a lantern on an iron bracket; rain on stone. Frontal view, plate 1620 x 2880."""
from darkroot import ROOT
import math
import numpy as np
import cv2
import shade as S
import tex as TX

PW, PH = 1620, 2880
LANTERN = (1185.0, 1880.0)


def lantern_light(n, I=3.2, r=520.0, z=160.0, col=(1.0, 0.68, 0.38)):
    return S.PLight(LANTERN[0], LANTERN[1], z, col, I=I, r=r)


def statue_mask(h, w, cx, base, H):
    """Justitia: robed figure, blindfolded head, right arm raised with scales, left arm down with a sword."""
    s = H / 10.0
    parts = {}
    body = S.catmull([(cx - 1.2 * s, base), (cx - 1.5 * s, base - 2.5 * s), (cx - 1.25 * s, base - 5.0 * s),
                      (cx - 1.05 * s, base - 6.6 * s), (cx - 0.75 * s, base - 7.6 * s), (cx - 0.35 * s, base - 8.1 * s),
                      (cx + 0.35 * s, base - 8.1 * s), (cx + 0.8 * s, base - 7.6 * s), (cx + 1.05 * s, base - 6.6 * s),
                      (cx + 1.2 * s, base - 5.0 * s), (cx + 1.55 * s, base - 2.5 * s), (cx + 1.3 * s, base)], 10)
    parts['body'] = S.poly_mask(h, w, body)
    head = S.ellipse_pts(cx, base - 8.85 * s, 0.52 * s, 0.68 * s)
    parts['head'] = S.poly_mask(h, w, head)
    neck = [(cx - 0.22 * s, base - 8.3 * s), (cx + 0.22 * s, base - 8.3 * s), (cx + 0.25 * s, base - 7.9 * s), (cx - 0.25 * s, base - 7.9 * s)]
    parts['neck'] = S.poly_mask(h, w, neck)
    # raised right arm (viewer's left): shoulder -> elbow -> hand above the head
    arm_r = S.catmull([(cx - 0.75 * s, base - 7.5 * s), (cx - 1.35 * s, base - 8.1 * s), (cx - 1.6 * s, base - 9.4 * s),
                       (cx - 1.45 * s, base - 10.3 * s), (cx - 1.2 * s, base - 10.25 * s), (cx - 1.25 * s, base - 9.4 * s),
                       (cx - 1.0 * s, base - 8.3 * s), (cx - 0.55 * s, base - 7.8 * s)], 8)
    parts['arm_r'] = S.poly_mask(h, w, arm_r)
    # lowered left arm (viewer's right) holding the sword
    arm_l = S.catmull([(cx + 0.8 * s, base - 7.5 * s), (cx + 1.3 * s, base - 6.6 * s), (cx + 1.45 * s, base - 5.3 * s),
                       (cx + 1.6 * s, base - 4.6 * s), (cx + 1.25 * s, base - 4.5 * s), (cx + 1.05 * s, base - 5.4 * s),
                       (cx + 0.85 * s, base - 6.6 * s)], 8)
    parts['arm_l'] = S.poly_mask(h, w, arm_l)
    sword = [(cx + 1.42 * s, base - 4.7 * s), (cx + 1.52 * s, base - 4.7 * s), (cx + 1.55 * s, base - 0.5 * s), (cx + 1.47 * s, base - 0.2 * s),
             (cx + 1.39 * s, base - 0.5 * s)]
    guard = [(cx + 1.1 * s, base - 4.62 * s), (cx + 1.85 * s, base - 4.62 * s), (cx + 1.85 * s, base - 4.5 * s), (cx + 1.1 * s, base - 4.5 * s)]
    hilt = [(cx + 1.43 * s, base - 5.2 * s), (cx + 1.51 * s, base - 5.2 * s), (cx + 1.51 * s, base - 4.62 * s), (cx + 1.43 * s, base - 4.62 * s)]
    parts['sword'] = np.maximum(np.maximum(S.poly_mask(h, w, sword), S.poly_mask(h, w, guard)), S.poly_mask(h, w, hilt))
    # scales: beam, chains, two pans
    bx, by = cx - 1.33 * s, base - 10.35 * s
    beam = [(bx - 1.1 * s, by - 0.05 * s), (bx + 1.1 * s, by - 0.05 * s), (bx + 1.1 * s, by + 0.05 * s), (bx - 1.1 * s, by + 0.05 * s)]
    m = S.poly_mask(h, w, beam)
    for sx_ in (-1, 1):
        px = bx + sx_ * 1.05 * s
        for k in (-1, 1):
            ch = [(px - 0.02 * s, by), (px + 0.02 * s, by), (px + k * 0.3 * s + 0.02 * s, by + 1.2 * s), (px + k * 0.3 * s - 0.02 * s, by + 1.2 * s)]
            m = np.maximum(m, S.poly_mask(h, w, ch))
        pan = S.ellipse_pts(px, by + 1.25 * s, 0.38 * s, 0.11 * s, a0=0, a1=math.pi)
        m = np.maximum(m, S.poly_mask(h, w, np.vstack([[[px - 0.38 * s, by + 1.2 * s], [px + 0.38 * s, by + 1.2 * s]], pan[::-1]])))
    parts['scales'] = m
    return parts


def build():
    h, w = PH, PW
    alb, N, Hg = TX.surface('large_sandstone_blocks_01', h, w, scale=1.05, sat=0.8, tint=(1.0, 0.92, 0.82), gain=0.95)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    nw = np.stack([N[..., 0], N[..., 1], N[..., 2]], -1)
    hmap = np.zeros((h, w), np.float32)
    # --- architecture (height map, plate px): door opening, moulded arch, inscription band, niche, plinth
    cx = w / 2.0
    door_top, door_bot, door_hw = 1720.0, 2880.0, 300.0
    arch = np.vstack([[[cx - door_hw, door_bot], [cx - door_hw, door_top]], S.ellipse_pts(cx, door_top, door_hw, 220, 64, math.pi, 2 * math.pi), [[cx + door_hw, door_bot]]])
    m_door = S.poly_mask(h, w, arch)
    outer = np.vstack([[[cx - door_hw - 110, door_bot], [cx - door_hw - 110, door_top]], S.ellipse_pts(cx, door_top, door_hw + 110, 330, 64, math.pi, 2 * math.pi), [[cx + door_hw + 110, door_bot]]])
    m_frame = S.poly_mask(h, w, outer) - m_door
    band_y0, band_y1 = 1300.0, 1450.0
    m_band = S.poly_mask(h, w, [(cx - 560, band_y0), (cx + 560, band_y0), (cx + 560, band_y1), (cx - 560, band_y1)])
    cornice = S.poly_mask(h, w, [(cx - 600, band_y0 - 40), (cx + 600, band_y0 - 40), (cx + 580, band_y0), (cx - 580, band_y0)])
    sill = S.poly_mask(h, w, [(cx - 580, band_y1), (cx + 580, band_y1), (cx + 600, band_y1 + 36), (cx - 600, band_y1 + 36)])
    niche_y0, niche_y1, niche_hw = 260.0, 1250.0, 270.0
    niche = np.vstack([[[cx - niche_hw, niche_y1], [cx - niche_hw, niche_y0 + niche_hw]], S.ellipse_pts(cx, niche_y0 + niche_hw, niche_hw, niche_hw, 64, math.pi, 2 * math.pi), [[cx + niche_hw, niche_y1]]])
    m_niche = S.poly_mask(h, w, niche)
    plinth = S.poly_mask(h, w, [(cx - 230, 1160), (cx + 230, 1160), (cx + 250, 1250), (cx - 250, 1250)])
    hmap += m_frame * (0.6 + 0.4 * np.clip(1 - np.abs(cv2.distanceTransform((m_frame > 0.5).astype(np.uint8), cv2.DIST_L2, 5) - 40) / 40, 0, 1))
    hmap += m_band * 0.35 + cornice * 0.8 + sill * 0.7 - m_door * 2.0 - m_niche * 0.9 + plinth * 0.6
    # the niche interior: a half-dome shading (deep shadow at the top)
    # --- Justitia
    parts = statue_mask(h, w, cx, 1165.0, 900.0)
    stat = np.zeros((h, w), np.float32)
    hstat = np.zeros((h, w), np.float32)
    for k, m in parts.items():
        r_ = {'body': 160, 'head': 40, 'neck': 20, 'arm_r': 30, 'arm_l': 30, 'sword': 6, 'scales': 5}[k]
        hstat = np.maximum(hstat, S.inflate(m, r_, 0.55) * (1.2 if k in ('arm_r', 'scales') else 1.0) + (0.6 if k in ('arm_r', 'sword', 'scales') else 0) * m)
        stat = np.maximum(stat, m)
    folds = S.fbm(h, w, 14, 3, 5)
    drape = np.sin((xx - cx) * 0.09 + folds * 4) * 0.05 * parts['body']
    hstat += drape
    # blindfold
    blind = S.poly_mask(h, w, [(cx - 70, 1165 - 9.05 * 90), (cx + 70, 1165 - 9.05 * 90), (cx + 72, 1165 - 8.85 * 90), (cx - 72, 1165 - 8.85 * 90)]) * parts['head']
    # --- lighting: the lantern (warm, low, right) and the cold night
    n = S.normals(cv2.GaussianBlur(hmap, (0, 0), 2.0), strength=40.0)
    n = n * 0.6 + nw * 0.4
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    L = lantern_light(n)
    lit, sp = S.light(n, [L], amb=(0.03, 0.035, 0.05), key=(-0.3, -0.6, 0.5), key_col=(0.06, 0.08, 0.13), spec=0.25, shininess=10)
    rgb = alb * lit + sp * 0.5
    # the niche: in shadow, darker towards its hood
    nd = np.clip((yy - niche_y0) / (niche_y1 - niche_y0), 0, 1)
    rgb = rgb * (1 - m_niche[..., None] * (0.75 - 0.35 * nd)[..., None])
    # the door: dark oak with iron studs, barely lit
    dalb, dN, _ = TX.surface('rough_pine_door', h, w, scale=1.3, sat=0.6, tint=(0.8, 0.62, 0.45), gain=0.6)
    dl, ds = S.light(dN, [L], amb=(0.01, 0.01, 0.015), spec=0.3, shininess=8)
    door = dalb * dl + ds * 0.3
    for sy in np.arange(door_top + 60, door_bot, 140):
        for sxx in np.arange(cx - door_hw + 60, cx + door_hw - 30, 120):
            st = np.exp(-(((xx - sxx) / 9) ** 2 + ((yy - sy) / 9) ** 2))
            door = door + st[..., None] * np.array([0.25, 0.2, 0.15], np.float32) * (dl.mean(-1, keepdims=True) * 2)
    rgb = rgb * (1 - m_door[..., None]) + door * m_door[..., None]
    # statue: weathered pale sandstone, lit from below right
    sn = S.normals(cv2.GaussianBlur(hstat, (0, 0), 1.5), strength=55.0)
    slit, ssp = S.light(sn, [S.PLight(LANTERN[0], LANTERN[1], 260, (1.0, 0.68, 0.38), I=3.6, r=900)], amb=(0.04, 0.045, 0.06),
                        key=(-0.3, -0.7, 0.4), key_col=(0.07, 0.09, 0.14), spec=0.2, shininess=8)
    salb = np.array([0.7, 0.64, 0.54], np.float32) * (0.85 + 0.3 * S.fbm(h, w, 30, 4, 9))[..., None]
    srgb = salb * slit + ssp * 0.3
    srgb = srgb * (1 - blind[..., None] * 0.35)
    rgb = rgb * (1 - stat[..., None]) + srgb * stat[..., None]
    # --- the carved inscription (two lines, Roman capitals)
    from PIL import Image, ImageDraw, ImageFont
    bw, bh = 1080, 150
    ss = 3
    im = Image.new('L', (bw * ss, bh * ss), 0)
    d = ImageDraw.Draw(im)
    f = ImageFont.truetype(ROOT + '/fonts/Cinzel[wght].ttf', int(52 * ss))
    for k, t in enumerate(('DISCITE IVSTITIAM MONITI', 'ET NON TEMNERE DIVOS')):
        tw = f.getlength(t)
        d.text(((bw * ss - tw) / 2, (10 + 70 * k) * ss), t, font=f, fill=255)
    a = cv2.resize(np.asarray(im, np.float32) / 255.0, (bw, bh), interpolation=cv2.INTER_AREA)
    y0, x0 = int(band_y0), int(cx - bw / 2)
    carve = np.zeros((h, w), np.float32)
    carve[y0:y0 + bh, x0:x0 + bw] = a
    hc = cv2.GaussianBlur(-carve, (0, 0), 1.4)
    gx = cv2.Sobel(hc, cv2.CV_32F, 1, 0, ksize=3)
    gy = cv2.Sobel(hc, cv2.CV_32F, 0, 1, ksize=3)
    lx, ly = (LANTERN[0] - xx), (LANTERN[1] - yy)
    ln = np.sqrt(lx * lx + ly * ly) + 1e-6
    shade_ = np.clip(1 + (gx * lx / ln + gy * ly / ln) * 6, 0.25, 1.8)
    rgb = rgb * (1 - 0.6 * carve)[..., None] * shade_[..., None] ** 0.8
    # wet stone: darker lower down, streaks
    wet = np.clip((yy - 1500) / 1400, 0, 1) * (0.7 + 0.3 * S.fbm(h, w, 40, 3, 12))
    rgb = rgb * (1 - 0.25 * wet)[..., None]
    # the lantern: iron bracket from the wall, a glazed box with a flame
    br = S.poly_mask(h, w, [(1420, 1700), (1440, 1700), (1440, 1720), (1215, 1760), (1215, 1748), (1420, 1712)])
    rgb = rgb * (1 - br[..., None]) + np.array([0.04, 0.035, 0.03], np.float32) * br[..., None]
    box = S.poly_mask(h, w, [(1140, 1790), (1230, 1790), (1222, 1960), (1148, 1960)])
    cap = S.poly_mask(h, w, [(1128, 1790), (1185, 1745), (1242, 1790)])
    glass = np.exp(-(((xx - LANTERN[0]) / 34) ** 2 + ((yy - LANTERN[1]) / 60) ** 2))
    lan = np.array([0.9, 0.6, 0.3], np.float32)[None, None] * (0.6 + 1.6 * glass)[..., None]
    rgb = rgb * (1 - box[..., None]) + lan * box[..., None]
    rgb = rgb * (1 - cap[..., None]) + np.array([0.05, 0.04, 0.035], np.float32) * cap[..., None]
    for xb in (1140, 1185, 1230):
        mb = S.poly_mask(h, w, [(xb - 4, 1790), (xb + 4, 1790), (xb + 3, 1960), (xb - 3, 1960)])
        rgb = rgb * (1 - mb[..., None]) + np.array([0.04, 0.035, 0.03], np.float32) * mb[..., None]
    return rgb.astype(np.float32)


def prepare(force=False):
    import plates as PL
    z = None if force else PL.load('portal')
    if z is not None:
        return z
    img = build()
    pr, _ = PL.paint_layer(img, None, 1.5, seed=41, expo=1.8, detail=1.3)
    PL.save('portal', img=pr)
    return PL.load('portal')
