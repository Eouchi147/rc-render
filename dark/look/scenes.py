"""The four story moments, as 2.5D scenes shared by every style."""
import math
import numpy as np
from core import Scene, Item, Light, P, rect, ellipse, catmull, ridge, T, rng, fbm1d, DW, DH
from parts import (figure, flame, camel, house_gable, roofline, tower, tent, ship, rocks, grass, tree_blob, shrub,
                   limb, _xf)


# ================================================================== BAMBERG, June 1628: they bring the mayor
def bamberg():
    sc = Scene('bamberg')
    sc.title = 'Bamberg, 1628'
    sc.mood = 'night'
    sc.sky = dict(stops=[(0, (0.04, 0.05, 0.08)), (0.22, (0.08, 0.09, 0.13)), (0.42, (0.14, 0.15, 0.2)),
                         (0.56, (0.17, 0.17, 0.21)), (1, (0.08, 0.08, 0.1))],
                  glow=[(250, 300, 420, (0.55, 0.62, 0.8), 0.32)],
                  moon=(250, 300, 46, (0.86, 0.88, 0.95)),
                  clouds=[dict(y0=0, y1=760, cell=320, seed=4, cov=0.42, soft=0.22, col_top=(0.36, 0.38, 0.45),
                               col_bot=(0.1, 0.11, 0.14), dens=0.92, ystretch=0.4)])
    sc.amb = np.array([0.1, 0.11, 0.15], np.float32)
    sc.key_col = np.array([0.3, 0.36, 0.5], np.float32)
    sc.key_dir = (-0.6, -0.8)
    sc.haze_col = np.array([0.17, 0.19, 0.25], np.float32)
    sc.haze, sc.haze_pow = 0.7, 1.5
    sc.sun = (250, 300)
    sc.rim = 0.25
    sc.focus = 0.84
    # Domberg hill and the cathedral (east towers lower than the west towers in 1628)
    hill = P([(430, 990), (520, 930), (640, 895), (800, 880), (960, 890), (1100, 905), (1100, 1100), (430, 1100)])
    sc.add(Item(polys=[catmull(hill, 6, closed=True)], z=0.17, col=(0.12, 0.13, 0.17), mat='ground', key=0.7, recv=0, name='domberg'))
    cath = [rect(700, 830, 960, 905), P([(690, 840), (970, 840), (948, 790), (712, 790)])]
    sc.add(Item(polys=cath, z=0.2, col=(0.14, 0.15, 0.19), mat='stone', key=0.8, recv=0, name='cathedral', hatch=90))
    for it in tower(718, 905, 30, 175, 40, 0.205, col=(0.15, 0.16, 0.2), roof=(0.13, 0.13, 0.17), kind='pyramid', recv=0, name='eastT1', windows=1):
        sc.add(it)
    for it in tower(752, 905, 30, 165, 40, 0.205, col=(0.15, 0.16, 0.2), roof=(0.13, 0.13, 0.17), kind='pyramid', recv=0, name='eastT2', windows=1):
        sc.add(it)
    for it in tower(912, 905, 34, 250, 95, 0.205, col=(0.15, 0.16, 0.2), roof=(0.13, 0.13, 0.17), kind='spire', recv=0, name='westT1'):
        sc.add(it)
    for it in tower(948, 905, 34, 258, 100, 0.205, col=(0.15, 0.16, 0.2), roof=(0.13, 0.13, 0.17), kind='spire', recv=0, name='westT2'):
        sc.add(it)
    its, _ = roofline(500, 700, 905, 0.215, 21, col=(0.13, 0.13, 0.17), hmin=50, hmax=90, wmin=40, wmax=80, lit=0.3)
    sc.add(*its)
    # town roofs
    its, _ = roofline(-30, 1110, 1075, 0.36, 3, col=(0.1, 0.1, 0.13), hmin=70, hmax=170, wmin=60, wmax=125, lit=0.2)
    sc.add(*its)
    # old city wall with a round tower
    wall = [rect(-20, 1010, 1100, 1160)]
    for x in range(-20, 1100, 38):
        wall.append(rect(x, 995, x + 20, 1012))
    sc.add(Item(polys=wall, z=0.48, col=(0.24, 0.23, 0.24), mat='stone', key=0.9, recv=0.6, name='citywall', hatch=0))
    for it in tower(60, 1160, 90, 240, 70, 0.49, col=(0.25, 0.24, 0.25), roof=(0.14, 0.12, 0.13), kind='cone', name='walltower', windows=2):
        sc.add(it)
    # torture house (half-timbered, against the wall) linked by a covered passage
    its, lts = house_gable(-60, 1440, 180, 2, 125, 120, 0.56, wall=(0.5, 0.46, 0.42), seed=7, lit=0.5, chimney=True, jetty=6)
    sc.add(*its)
    sc.lights.extend(lts)
    sc.add(Item(polys=[rect(118, 1185, 175, 1235), P([(112, 1188), (182, 1188), (147, 1162)])], z=0.575, col=(0.3, 0.26, 0.24),
                mat='wood', name='passage'))
    # ---- the Drudenhaus (witch house), 1627: long two-storey block, portal with Justitia, chapel with apse
    dz = 0.6
    wallc = (0.44, 0.42, 0.39)
    gable = P([(150, 1455), (220, 1425), (220, 1128), (186, 905), (150, 1150)])
    sc.add(Item(polys=[gable], z=dz - 0.004, col=tuple(c * 1.12 for c in wallc), mat='plaster', key=1.25, name='dh_gable', hatch=0))
    fac = rect(220, 1128, 900, 1425)
    sc.add(Item(polys=[fac], z=dz, col=wallc, mat='plaster', key=0.85, name='drudenhaus', hatch=0))
    roof = P([(206, 1132), (912, 1132), (898, 905), (186, 905)])
    sc.add(Item(polys=[roof], z=dz + 0.001, col=(0.2, 0.15, 0.14), mat='roof', key=0.9, name='dh_roof', hatch=60))
    tiles = []
    for yy in np.arange(925, 1130, 14):
        tiles.append((P([(196 + (yy - 905) * 0.09, yy), (906 - (yy - 905) * 0.04, yy)]), 1.4))
    sc.add(Item(lines=tiles, z=dz + 0.0015, col=(0.12, 0.09, 0.08), mat='roof', name='dh_tiles', outline=False, detail=True))
    # dormers
    for dx in (300, 470, 650, 820):
        dp = [rect(dx - 22, 975, dx + 22, 1030), P([(dx - 30, 978), (dx + 30, 978), (dx, 948)])]
        sc.add(Item(polys=dp, z=dz + 0.002, col=(0.42, 0.4, 0.37), mat='plaster', name='dormer'))
        sc.add(Item(polys=[rect(dx - 9, 990, dx + 9, 1022)], z=dz + 0.003, col=(0.05, 0.05, 0.06), mat='window', key=0, name='dormer_w', outline=False))
    # windows: two rows, cells with bars
    bars = []
    r = rng(17)
    for row, cy in ((0, 1215), (1, 1335)):
        for i, cx in enumerate(np.linspace(262, 858, 12)):
            if abs(cx - 560) < 60:
                continue
            lit = (row, i) in ((0, 2), (1, 9))
            wc = (1.0, 0.68, 0.32) if lit else (0.05, 0.05, 0.06)
            sc.add(Item(polys=[rect(cx - 14, cy - 20, cx + 14, cy + 20)], z=dz + 0.003, col=wc, mat='window',
                        emit=1.7 if lit else 0, key=0, recv=0.3, name='cell'))
            if lit:
                sc.lights.append(Light(cx, cy, (1.0, 0.62, 0.3), I=0.3, r=45, z=dz, air=0.06))
            for bx in (-6, 0, 6):
                bars.append((P([(cx + bx, cy - 20), (cx + bx, cy + 20)]), 2.2))
            bars.append((P([(cx - 16, cy - 22), (cx + 16, cy - 22)]), 3))
            bars.append((P([(cx - 16, cy + 22), (cx + 16, cy + 22)]), 3))
    sc.add(Item(lines=bars, z=dz + 0.004, col=(0.12, 0.11, 0.11), mat='metal', name='bars', outline=False, detail=True))
    # portal and Justitia niche
    portal = [rect(505, 1265, 615, 1425), ellipse(560, 1265, 55, 40, 24, math.pi, 2 * math.pi)]
    sc.add(Item(polys=portal, z=dz + 0.002, col=(0.7, 0.67, 0.6), mat='stone', key=1.0, name='portal_frame'))
    door = [rect(522, 1280, 598, 1425), ellipse(560, 1280, 38, 28, 24, math.pi, 2 * math.pi)]
    sc.add(Item(polys=door, z=dz + 0.003, col=(0.07, 0.05, 0.045), mat='wood', key=0.4, name='door'))
    sc.add(Item(polys=[rect(530, 1150, 590, 1245), ellipse(560, 1150, 30, 22, 20, math.pi, 2 * math.pi)], z=dz + 0.002,
                col=(0.32, 0.3, 0.28), mat='stone', name='niche'))
    jus, _ = figure(560, 1240, 82, face=1, z=dz + 0.004, col=(0.78, 0.75, 0.68), robe=0.46, female=True, arm='up',
                    arm2='hang', name='justitia', outline=True)
    sc.add(*jus)
    sc.add(Item(lines=[(P([(536, 1172), (586, 1172)]), 2.5), (P([(538, 1172), (538, 1186)]), 1.5), (P([(584, 1172), (584, 1186)]), 1.5),
                       (P([(560, 1162), (560, 1172)]), 2)], z=dz + 0.005, col=(0.78, 0.75, 0.68), mat='stone', name='scales', detail=True))
    sc.add(Item(polys=[ellipse(538, 1188, 9, 3.5, 12), ellipse(584, 1188, 9, 3.5, 12)], z=dz + 0.005, col=(0.78, 0.75, 0.68), mat='stone', name='pans'))
    for cx in (440, 680):
        sc.add(Item(polys=[ellipse(cx, 1210, 50, 30, 30)], z=dz + 0.002, col=(0.68, 0.65, 0.58), mat='stone', name='cartouche'))
        sc.add(Item(lines=[(P([(cx - 30, 1200 + k * 9), (cx + 30, 1200 + k * 9)]), 1.6) for k in range(3)], z=dz + 0.003,
                    col=(0.3, 0.27, 0.25), mat='stone', name='cart_text', outline=False, detail=True))
    # lantern by the portal
    sc.add(Item(polys=[rect(627, 1300, 645, 1330)], z=dz + 0.004, col=(1.0, 0.75, 0.4), mat='window', emit=2.2, key=0, recv=0, name='lantern', outline=False))
    sc.lights.append(Light(636, 1315, (1.0, 0.62, 0.3), I=0.7, r=90, z=dz, air=0.12, flare=0.4))
    # chapel with apse and a ridge turret
    chap = [rect(900, 1090, 1010, 1425), ellipse(1010, 1257, 40, 167, 30, -math.pi / 2, math.pi / 2)]
    sc.add(Item(polys=chap, z=dz - 0.002, col=(0.52, 0.5, 0.47), mat='plaster', key=0.8, name='chapel', hatch=0))
    sc.add(Item(polys=[P([(890, 1095), (1045, 1095), (1020, 940), (915, 940)])], z=dz - 0.001, col=(0.2, 0.15, 0.14), mat='roof', name='chapel_roof', hatch=60))
    sc.add(Item(polys=[ellipse(955, 1250, 16, 46, 20)], z=dz, col=(0.05, 0.05, 0.06), mat='window', key=0, name='chapel_win'))
    for it in tower(965, 945, 22, 45, 70, dz + 0.001, col=(0.45, 0.42, 0.4), roof=(0.18, 0.14, 0.13), kind='spire', name='turret', windows=1):
        sc.add(it)
    # wet street (reflective)
    sc.add(Item(polys=[rect(-20, 1420, 1100, 1940)], z=0.66, col=(0.16, 0.16, 0.19), mat='water', key=0.6, recv=1.0,
                name='street', wline=1428, shade=(0.8, 1.1)))
    sc.items[-1].refl, sc.items[-1].rblur = 0.42, 9
    cob = []
    rr = rng(5)
    for yy in np.arange(1440, 1920, 18):
        for xx in np.arange(-20, 1100, 30):
            if rr.random() < 0.35:
                cob.append((P([(xx + rr.uniform(0, 10), yy + rr.uniform(-3, 3)), (xx + rr.uniform(18, 26), yy + rr.uniform(-3, 3))]), 1.4))
    sc.add(Item(lines=cob, z=0.67, col=(0.1, 0.1, 0.12), mat='stone', name='cobbles', outline=False, detail=True, alpha=0.6))
    # the procession: guard with torch, the mayor (hands bound), guard with halberd; a clerk at the door
    clerk, _ = figure(575, 1428, 150, face=1, z=0.62, col=(0.07, 0.065, 0.06), robe=0.42, hat='brim', collar='band', name='clerk')
    sc.add(*clerk)
    g1, l1 = figure(640, 1700, 300, face=-1, z=0.84, col=(0.075, 0.065, 0.06), robe=0.2, step=0.55, arm='up', arm2='hang',
                    hat='morion', torch=True, cloak=True, name='guard1', seed=3, light_I=1.3)
    sc.add(*g1)
    sc.lights.extend(l1)
    jun, _ = figure(770, 1735, 318, face=-1, z=0.86, col=(0.06, 0.055, 0.05), robe=0.22, step=0.45, bow=7, arm='bound',
                    arm2='bound', collar='ruff', name='junius', seed=4)
    sc.add(*jun)
    g2, _ = figure(905, 1775, 335, face=-1, z=0.88, col=(0.07, 0.06, 0.055), robe=0.2, step=0.6, arm='staff', arm2='hang',
                   hat='morion', halberd=True, cloak=True, name='guard2', seed=5)
    sc.add(*g2)
    # foreground frame: a dark timber corner with a hanging sign, left edge
    sc.add(Item(polys=[rect(-40, -20, 52, 1960)], z=0.97, col=(0.04, 0.035, 0.03), mat='wood', key=0.2, recv=0.3, name='fg_post'))
    sc.add(Item(lines=[(P([(52, 1045), (205, 1045)]), 10), (P([(70, 1045), (52, 1100)]), 7)], z=0.97, col=(0.04, 0.035, 0.03),
                mat='wood', key=0.2, recv=0.3, name='fg_bracket'))
    sc.add(Item(lines=[(P([(150, 1045), (150, 1072)]), 2), (P([(190, 1045), (190, 1072)]), 2)], z=0.97, col=(0.04, 0.035, 0.03), mat='metal', name='fg_chain', detail=True))
    sc.add(Item(polys=[P([(132, 1072), (208, 1072), (208, 1150), (170, 1168), (132, 1150)])], z=0.97, col=(0.05, 0.04, 0.035),
                mat='wood', key=0.2, recv=0.4, name='fg_sign'))
    sc.fog = [dict(y0=980, y1=1210, z=0.55, col=(0.26, 0.28, 0.34), dens=0.42, cov=0.3, seed=8, cell=260),
              dict(y0=1380, y1=1520, z=0.7, col=(0.22, 0.23, 0.28), dens=0.3, cov=0.35, seed=9, cell=220, front=0.15)]
    sc.rain = dict(n=1600, angle=10, len=(26, 64), alpha=0.2, seed=21)
    return sc


# ================================================================== THE ZONG, 1 December 1781: the rain
def zong():
    sc = Scene('zong')
    sc.title = 'The Zong, 1781'
    sc.mood = 'storm'
    hz = 1045
    sc.sky = dict(stops=[(0, (0.11, 0.12, 0.15)), (0.28, (0.2, 0.21, 0.24)), (0.45, (0.4, 0.38, 0.35)),
                         (0.53, (0.75, 0.62, 0.45)), (0.545, (0.62, 0.56, 0.48)), (1, (0.3, 0.32, 0.34))],
                  glow=[(250, 650, 330, (1.0, 0.78, 0.5), 0.95), (250, 650, 90, (1.0, 0.9, 0.7), 0.9)],
                  clouds=[dict(y0=-40, y1=940, cell=360, seed=31, cov=0.36, soft=0.22, col_top=(0.5, 0.48, 0.46),
                               col_bot=(0.09, 0.1, 0.12), dens=1.0, ystretch=0.42),
                          dict(y0=820, y1=1030, cell=260, seed=32, cov=0.5, soft=0.2, col_top=(0.42, 0.4, 0.4),
                               col_bot=(0.2, 0.2, 0.22), dens=0.7, ystretch=0.25)])
    sc.amb = np.array([0.2, 0.22, 0.25], np.float32)
    sc.key_col = np.array([0.55, 0.48, 0.42], np.float32)
    sc.key_dir = (-0.75, -0.6)
    sc.haze_col = np.array([0.36, 0.38, 0.4], np.float32)
    sc.haze, sc.haze_pow = 0.6, 1.4
    sc.sun = (250, 650)
    sc.rim = 0.35
    sc.focus = 0.6
    # rain curtain under the cloud (left)
    curtain = P([(-40, 760), (520, 780), (600, 1050), (-40, 1050)])
    sc.add(Item(polys=[curtain], z=0.22, col=(0.3, 0.31, 0.33), mat='rain', alpha=0.45, key=0.4, recv=0, outline=False, name='curtain', shade=(0.9, 1.1)))
    # sea
    sc.add(Item(polys=[rect(-20, hz, 1100, 1940)], z=0.3, col=(0.16, 0.22, 0.26), mat='water', key=0.5, recv=0.6,
                name='sea', wline=hz, shade=(1.25, 0.6)))
    sc.add(Item(polys=[ellipse(300, hz + 60, 300, 26, 40)], z=0.31, col=(1.0, 0.85, 0.62), emit=0.55, alpha=0.55,
                mat='glint', key=0, recv=0, outline=False, name='sheen'))
    # wave crests: perspective rows
    r = rng(33)
    lines_l, lines_d = [], []
    for k in range(80):
        t = (k / 80) ** 1.7
        y = hz + 8 + t * (1900 - hz)
        amp = 2 + t * 26
        L = 60 + t * 600
        x = r.uniform(-100, 1100)
        xs = np.linspace(x, x + L, 30)
        ys = y + np.sin(np.linspace(0, math.pi * r.uniform(1, 3), 30)) * amp * 0.25 - np.sin(np.linspace(0, math.pi, 30)) * amp
        lines_l.append((np.stack([xs, ys], 1), 1 + t * 5))
        lines_d.append((np.stack([xs, ys + amp * 0.7 + 3 + t * 8], 1), 1 + t * 7))
    sc.add(Item(lines=lines_d, z=0.4, col=(0.07, 0.1, 0.13), mat='water', key=0.4, recv=0.3, name='troughs', outline=False, detail=True, alpha=0.8))
    sc.add(Item(lines=lines_l, z=0.41, col=(0.55, 0.6, 0.62), mat='foam', key=0.6, recv=0.4, name='crests', outline=False, detail=True, alpha=0.7))
    # the ship, bow to the left, stern windows lit
    its, lts = ship(770, 1150, 560, z=0.6, face=-1, seed=41, people=24)
    sc.add(*its)
    sc.lights.extend(lts)
    # spray at the bow and wake
    wake = [ellipse(230 + k * 30, 1160 + (k % 2) * 6, 40 - k, 6, 16) for k in range(8)]
    sc.add(Item(polys=wake, z=0.61, col=(0.75, 0.78, 0.78), mat='foam', alpha=0.7, key=0.6, recv=0.3, outline=False, name='bowfoam'))
    # foreground swell with a foam crest
    xs = np.linspace(-40, 1120, 80)
    tt = np.linspace(0, 1, 80)
    ys = 1880 - 330 * np.exp(-((tt - 0.18) / 0.28) ** 2) - 60 * tt + 18 * np.sin(np.linspace(0, 13, 80))
    swell = np.vstack([np.stack([xs, ys], 1), [(1120, 1960), (-40, 1960)]])
    sc.add(Item(polys=[swell], z=0.93, col=(0.06, 0.09, 0.11), mat='water', key=0.7, recv=0.2, name='swell', shade=(1.3, 0.5)))
    foam = [(np.stack([xs, ys + 4], 1), 7), (np.stack([xs[10:60], ys[10:60] + 16], 1), 3)]
    sc.add(Item(lines=foam, z=0.935, col=(0.82, 0.85, 0.85), mat='foam', key=0.8, recv=0.2, alpha=0.85, outline=False, name='swellfoam', detail=True))
    sc.rain = dict(n=2400, angle=16, len=(30, 80), alpha=0.2, seed=34, curtains=[(-40, 560, 760, 1060, 1400)])
    sc.fog = [dict(y0=hz - 60, y1=hz + 90, z=0.35, col=(0.4, 0.4, 0.42), dens=0.45, cov=0.3, seed=35, cell=300)]
    return sc


# ================================================================== ARABIA, about 600: a fire in the dark
def arabia():
    sc = Scene('arabia')
    sc.title = 'Arabia, about 600'
    sc.mood = 'night'
    hz = 1335
    # Banat Na'sh (the Big Dipper): bier (4) and the daughters (3)
    dip = [(0, 0), (0.05, 0.62), (0.82, 0.8), (0.9, 0.3), (1.5, 0.18), (2.05, 0.05), (2.62, 0.32)]
    bright = [(520 + 175 * a, 300 + 175 * b, 3.2 if i in (0, 1, 5) else 2.4) for i, (a, b) in enumerate(dip)]
    sc.sky = dict(stops=[(0, (0.008, 0.012, 0.035)), (0.3, (0.02, 0.03, 0.07)), (0.55, (0.05, 0.06, 0.12)),
                         (0.645, (0.12, 0.1, 0.13)), (0.66, (0.08, 0.07, 0.08)), (1, (0.04, 0.035, 0.04))],
                  milky=(-60, -40, 1040, 1250, 150, 0.32), stars=(2600, 1320), bright=bright,
                  glow=[(545, hz + 60, 200, (1.0, 0.55, 0.25), 0.16)])
    sc.amb = np.array([0.06, 0.07, 0.11], np.float32)
    sc.key_col = np.array([0.1, 0.12, 0.2], np.float32)
    sc.key_dir = (0.0, -1.0)
    sc.haze_col = np.array([0.06, 0.065, 0.1], np.float32)
    sc.haze, sc.haze_pow = 0.55, 1.4
    sc.focus = 0.74
    sc.sun = (470, hz + 70)
    # distant dunes
    for k, (base, amp, z, col, seed) in enumerate([(hz + 10, 55, 0.12, (0.07, 0.07, 0.1), 51), (hz + 40, 70, 0.22, (0.08, 0.075, 0.1), 52),
                                                    (hz + 80, 60, 0.32, (0.1, 0.085, 0.1), 53)]):
        sc.add(Item(polys=[ridge(-40, 1120, base, amp, seed, octaves=3, gain=0.4, cells=2)], z=z, col=col, mat='sand',
                    key=0.8, recv=0.2, name='dune%d' % k, hatch=-8))
    # the plain
    sc.add(Item(polys=[rect(-20, hz + 70, 1100, 1940)], z=0.45, col=(0.2, 0.15, 0.12), mat='sand', key=0.8, recv=1.0,
                name='plain', shade=(0.7, 1.1), hatch=-5))
    ripples = []
    r = rng(54)
    for k in range(70):
        y = hz + 110 + (k / 70) ** 1.5 * 560
        x = r.uniform(-50, 1050)
        L = 40 + (y - hz) * 0.5
        ripples.append((catmull([(x, y), (x + L * 0.5, y - 4 - (y - hz) * 0.01), (x + L, y)], 5), 1 + (y - hz) / 300))
    sc.add(Item(lines=ripples, z=0.5, col=(0.12, 0.09, 0.08), mat='sand', name='ripples', outline=False, detail=True, alpha=0.6))
    # the poor camp: two tents, a birth fire with women around it
    for it in tent(560, 1420, 210, 84, 0.46, seed=61, glow=None, open_side=False, name='tent2'):
        sc.add(it)
    for it in tent(770, 1462, 300, 112, 0.55, seed=62, glow=(1.0, 0.6, 0.3), name='tent1'):
        sc.add(it)
    fx, fy = 735, 1470
    for k, (sx, sy) in enumerate([(-20, 4), (0, 8), (20, 4)]):
        sc.add(Item(polys=[ellipse(fx + sx, fy + sy, 10, 6, 12)], z=0.565, col=(0.08, 0.06, 0.05), mat='stone', key=0.3, name='hearth'))
    sc.add(*flame(fx, fy, 42, 0.57, seed=63))
    sc.lights.append(Light(fx, fy - 20, (1.0, 0.55, 0.22), I=1.6, r=150, z=0.56, air=0.16, flare=0.7))
    smoke = catmull(P([(fx - 10, fy - 50), (fx - 30, fy - 160), (fx + 10, fy - 300), (fx - 40, fy - 480), (fx + 20, fy - 520),
                       (fx + 40, fy - 460), (fx + 25, fy - 300), (fx + 20, fy - 160), (fx + 12, fy - 50)]), 6, closed=True)
    sc.add(Item(polys=[smoke], z=0.555, col=(0.35, 0.3, 0.3), alpha=0.25, mat='smoke', key=0.2, recv=0.6, outline=False, name='smoke'))
    for k, (dx, face, sit) in enumerate([(-62, 1, True), (52, -1, False), (88, -1, True)]):
        w, _ = figure(fx + dx, fy + 6, 112, face=face, z=0.56, col=(0.06, 0.045, 0.04), robe=0.48, female=True, sit=sit,
                      arm='chest' if k == 1 else 'hang', seed=70 + k, name='woman%d' % k)
        sc.add(*w)
    # Sa'sa'a on his male camel, leading two she-camels heavy with young
    cx, cy, ch = 250, 1700, 340
    its = camel(cx, cy, ch, face=1, z=0.75, col=(0.05, 0.04, 0.035), gait=0.6, head=-4, seed=81, saddle=True, name='mount')
    sc.add(*its)
    u = ch / 2.25
    rh = 1.75 * u
    rider, _ = figure(cx - 0.08 * u, cy - 2.3 * u + 0.5 * rh, rh, face=1, z=0.752, col=(0.05, 0.04, 0.035), robe=0.32,
                      headcloth=True, sit=True, arm='lead', arm2='hang', seed=82, name='sasaa')
    sc.add(*rider)
    c2 = camel(-40, 1650, 300, face=1, z=0.72, col=(0.055, 0.045, 0.04), gait=-0.3, pregnant=True, head=4, seed=83, name='she1')
    sc.add(*c2)
    c3 = camel(-260, 1610, 270, face=1, z=0.7, col=(0.06, 0.05, 0.045), gait=0.4, pregnant=True, head=-2, seed=84, name='she2')
    sc.add(*c3)
    u2 = 300 / 2.25
    hand = (cx - 0.08 * u + 0.2 * rh, cy - 2.3 * u + 0.5 * rh - 0.6 * rh)
    rope = catmull([hand, (cx - 0.6 * u, cy - 1.1 * u), (-40 + 2.15 * u2, 1650 - 2.0 * u2)], 6)
    sc.add(Item(lines=[(rope, 2.2)], z=0.73, col=(0.12, 0.09, 0.07), mat='rope', outline=False, name='leads', detail=True))
    # foreground shrubs (ghada) and a ridge of sand
    xs = np.linspace(-40, 1120, 60)
    ys = 1840 - 40 * np.sin(np.linspace(0, 3.2, 60)) - 10 * np.sin(np.linspace(0, 13, 60))
    sc.add(Item(polys=[np.vstack([np.stack([xs, ys], 1), [(1120, 1960), (-40, 1960)]])], z=0.9, col=(0.13, 0.1, 0.085),
                mat='sand', key=0.9, recv=0.3, name='fgdune', shade=(1.2, 0.7), hatch=-5))
    sc.add(shrub(905, 1835, 190, 0.92, 91), shrub(560, 1880, 120, 0.93, 92), shrub(1010, 1880, 90, 0.92, 93))
    sc.embers = dict(x=fx, y=fy - 30, n=110, spread=30, rise=420, seed=94)
    return sc


# ================================================================== KLEIDION, October 1014: the blinded army comes home
def kleidion():
    sc = Scene('kleidion')
    sc.title = 'Kleidion, 1014'
    sc.mood = 'dusk'
    hz = 1180
    sc.sky = dict(stops=[(0, (0.2, 0.17, 0.27)), (0.28, (0.45, 0.32, 0.36)), (0.47, (0.9, 0.6, 0.4)), (0.56, (1.0, 0.8, 0.52)),
                         (0.62, (0.88, 0.62, 0.44)), (1, (0.45, 0.32, 0.3))],
                  glow=[(840, 985, 470, (1.0, 0.7, 0.4), 1.0), (840, 985, 120, (1.0, 0.92, 0.7), 1.4)],
                  moon=(840, 985, 50, (1.4, 1.25, 0.95)),
                  clouds=[dict(y0=230, y1=760, cell=300, seed=41, cov=0.56, soft=0.16, col_top=(1.0, 0.76, 0.55),
                               col_bot=(0.45, 0.3, 0.32), dens=0.85, ystretch=0.16, envp=0.6)])
    sc.amb = np.array([0.26, 0.2, 0.24], np.float32)
    sc.key_col = np.array([0.55, 0.38, 0.26], np.float32)
    sc.key_dir = (0.45, -0.7)
    sc.haze_col = np.array([0.82, 0.58, 0.45], np.float32)
    sc.haze, sc.haze_pow = 0.82, 1.25
    sc.sun = (840, 985)
    sc.rim = 0.9
    sc.focus = 0.86
    for k, (base, amp, z, col, seed) in enumerate([(1060, 300, 0.06, (0.5, 0.38, 0.42), 101), (1130, 250, 0.13, (0.42, 0.32, 0.36), 102),
                                                    (1215, 190, 0.22, (0.34, 0.26, 0.3), 103), (1300, 140, 0.31, (0.27, 0.21, 0.24), 104)]):
        env = (lambda t: (0.6 + 0.4 * np.sin(t * math.pi * 1.3 + 1.0)) * (1 - 0.8 * np.exp(-((t - 0.775) / 0.1) ** 2)))
        sc.add(Item(polys=[ridge(-40, 1120, base, amp, seed, octaves=7, gain=0.55, env=env)], z=z, col=col, mat='mountain',
                    key=0.6, recv=0, name='ridge%d' % k, hatch=-20))
    # the granite hill of Prilep with a simple timber-and-stone stronghold (not the later towers)
    hill = catmull(P([(560, 1420), (640, 1250), (720, 1170), (800, 1120), (900, 1112), (980, 1150), (1060, 1205), (1120, 1260),
                      (1120, 1440)]), 6, closed=True)
    sc.add(Item(polys=[hill], z=0.38, col=(0.3, 0.25, 0.25), mat='stone', key=0.9, recv=0, name='prilep', hatch=35))
    sc.add(rocks(600, 1110, 1400, 0.385, 105, col=(0.33, 0.28, 0.27), n=55, smin=18, smax=55,
                 top=lambda x: 1120 + 0.0009 * (x - 880) ** 2, name='boulders'))
    sc.items[-1].outline = False
    pal = []
    for x in np.arange(760, 1000, 9):
        pal.append(rect(x, 1068 - 6 * math.sin(x / 30), x + 6, 1120))
    pal.append(rect(800, 1010, 860, 1120))
    pal.append(P([(792, 1012), (868, 1012), (830, 975)]))
    pal.append(rect(930, 1030, 975, 1120))
    pal.append(P([(924, 1032), (981, 1032), (952, 1000)]))
    pal.append(rect(860, 1040, 905, 1120))
    sc.add(Item(polys=pal, z=0.39, col=(0.22, 0.17, 0.17), mat='wood', key=0.9, recv=0, name='fort', hatch=90))
    # fields and the road
    sc.add(Item(polys=[rect(-20, 1300, 1100, 1940)], z=0.42, col=(0.36, 0.28, 0.16), mat='ground', key=0.9, recv=0.2,
                name='fields', shade=(0.9, 0.75), hatch=-3))
    road_c = catmull(P([(120, 1330), (300, 1400), (430, 1470), (380, 1560), (300, 1660), (430, 1780), (640, 1960)]), 12)
    n = len(road_c)
    wids = np.linspace(14, 360, n) ** 1.0
    d = np.gradient(road_c, axis=0)
    d /= np.linalg.norm(d, axis=1, keepdims=True) + 1e-9
    nrm = np.stack([-d[:, 1], d[:, 0]], 1)
    road = np.vstack([road_c + nrm * wids[:, None] / 2, (road_c - nrm * wids[:, None] / 2)[::-1]])
    sc.add(Item(polys=[road], z=0.43, col=(0.82, 0.68, 0.5), mat='road', key=1.2, recv=0.2, name='road', hatch=-3))
    # autumn chestnuts
    for k, (x, y, h, z) in enumerate([(60, 1480, 260, 0.5), (210, 1420, 170, 0.47), (980, 1520, 300, 0.52), (860, 1460, 160, 0.48)]):
        sc.add(*tree_blob(x, y, h, z, 110 + k, col=(0.58, 0.32, 0.12)))
    # the procession along the road, far to near; every hundred led by a one-eyed man
    idx = np.linspace(0.12, 0.99, 24) ** 1.7
    for k, t in enumerate(idx):
        i = min(int(t * (n - 1)), n - 1)
        px, py = road_c[i]
        hgt = 26 + 400 * t ** 1.6
        zz = 0.44 + 0.5 * t
        lead = (k == len(idx) - 1)
        fx = px + (np.random.default_rng(k).random() - 0.5) * wids[i] * 0.3
        it, _ = figure(fx, py + 4, hgt, face=1, z=zz, col=(0.12, 0.08, 0.07), robe=0.28, step=0.25 + 0.5 * ((k * 7) % 3) / 2,
                       bow=10 + (k % 4) * 3, arm='staff' if lead else 'fwd', arm2='hang', bandage=True, one_eye=lead, staff=lead,
                       cloak=(k % 3 == 0), hat='hood' if k % 4 == 1 else None, seed=200 + k, name='blind%d' % k,
                       band_col=(0.92, 0.88, 0.8))
        sc.add(*it)
    # foreground: a broken spear and a shield in the dry grass, crows on a dead branch
    sc.add(grass(-40, 1120, 1720, 1960, 0.94, 120, n=520, col=(0.5, 0.38, 0.2), hmin=30, hmax=110, lean=0.15, w=2.6))
    sc.add(Item(polys=[ellipse(150, 1840, 92, 40, 40)], z=0.95, col=(0.35, 0.24, 0.16), mat='wood', key=1.0, recv=0.2, name='shield'))
    sc.add(Item(polys=[ellipse(150, 1840, 22, 10, 20)], z=0.951, col=(0.5, 0.45, 0.4), mat='metal', key=1.0, name='boss'))
    sc.add(Item(lines=[(P([(40, 1905), (330, 1770)]), 7), (P([(340, 1765), (420, 1730)]), 6)], z=0.952, col=(0.2, 0.14, 0.1),
                mat='wood', name='spear', outline=True))
    sc.add(Item(polys=[P([(420, 1730), (470, 1704), (440, 1730), (424, 1740)])], z=0.952, col=(0.45, 0.42, 0.4), mat='metal', name='spearhead'))
    branch = [(P([(1100, 1080), (980, 1150), (900, 1190)]), 14), (P([(980, 1150), (940, 1110)]), 6), (P([(930, 1180), (880, 1170)]), 4)]
    sc.add(Item(lines=branch, z=0.97, col=(0.08, 0.06, 0.05), mat='wood', key=0.4, recv=0, name='branch', outline=False))
    for (bx, by, s) in ((955, 1128, 30), (905, 1166, 26)):
        crow = [ellipse(bx, by, s * 0.75, s * 0.42, 20), ellipse(bx + s * 0.6, by - s * 0.35, s * 0.24, s * 0.22, 14),
                P([(bx + s * 0.8, by - s * 0.38), (bx + s * 1.15, by - s * 0.3), (bx + s * 0.8, by - s * 0.26)]),
                P([(bx - s * 0.6, by - s * 0.05), (bx - s * 1.25, by + s * 0.2), (bx - s * 0.6, by + s * 0.2)])]
        sc.add(Item(polys=crow, z=0.971, col=(0.04, 0.035, 0.035), mat='animal', key=0.3, recv=0, name='crow'))
    sc.dust = dict(box=(300, 900, 1080, 1700), n=420, seed=130)
    return sc


SCENES = dict(bamberg=bamberg, zong=zong, arabia=arabia, kleidion=kleidion)
