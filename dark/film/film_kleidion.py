"""Dark Corners, episode 4: As They Say (Kleidion, 1014). Plain telling (direct_kleidion.py), voice 4, the Bamberg v3
grammar through film_kit. Scenes: the look-test column of the blinded at Prilep with detail plates, Prilep without the
column, the walled pass in summer (the flank march, the rout), the gorge, the fortress at night, the two chroniclers'
pages, black. The blinding is always the chronicler's claim.
    python film_kleidion.py info | still T out.jpg | frames A B out.mp4"""
from darkroot import ROOT
import sys, os, math
sys.path.insert(0, ROOT + '/film')
sys.path.insert(0, ROOT + '/look')
import numpy as np
import film_kit as K
from film_kit import Shot, Look, Cell, Black, S0, E0, Wd, CUT, FLASH, ob, CINZEL, ITAL, ROMAN
import pages as PG
import scenes as LS
from core import Item, Light, Scene, P, rect, ellipse, ridge, catmull, rng
from parts import figure, rocks, grass

GROUPS = [('far', 0.0, 0.445), ('mid', 0.445, 0.75), ('fg', 0.75, 1.01)]
ZS = (2.8, 1.35, 1.05)
COLUMN = ('blind',)
CLUTTER = ('crow', 'branch', 'shield', 'boss', 'spear')


def _drop(sc, prefixes):
    sc.items = [it for it in sc.items if not any(it.name.startswith(p) for p in prefixes)]
    return sc


def column():
    return LS.kleidion()


def prilep():
    return _drop(LS.kleidion(), COLUMN)


SUMMER = dict(stops=[(0, (0.32, 0.42, 0.62)), (0.3, (0.5, 0.58, 0.72)), (0.5, (0.85, 0.8, 0.7)), (0.6, (0.95, 0.85, 0.66)),
                     (1, (0.6, 0.5, 0.38))],
              glow=[(820, 420, 420, (1.0, 0.92, 0.75), 0.6)],
              clouds=[dict(y0=200, y1=700, cell=320, seed=141, cov=0.38, soft=0.2, col_top=(1.0, 0.97, 0.92),
                           col_bot=(0.65, 0.66, 0.72), dens=0.7, ystretch=0.2)])


def pass_day(extra=None):
    sc = _drop(LS.kleidion(), COLUMN + CLUTTER + ('prilep', 'boulders', 'fort', 'road'))
    sc.sky = SUMMER; sc.mood = 'day'
    sc.amb = np.array([0.42, 0.42, 0.44], np.float32); sc.key_col = np.array([0.9, 0.8, 0.62], np.float32)
    sc.key_dir = (0.2, -0.9); sc.haze_col = np.array([0.72, 0.72, 0.74], np.float32); sc.haze, sc.haze_pow = 0.75, 1.3
    sc.sun = (820, 420); sc.rim = 0.4
    for it in sc.items:
        if it.name.startswith('ridge'):
            it.col = np.array([0.36, 0.42, 0.46], np.float32) * (0.85 + 0.15 * float(it.name[-1]))
        if it.name == 'tree':
            it.col = np.array([0.24, 0.32, 0.14], np.float32)
        if it.name == 'fields':
            it.col = np.array([0.55, 0.47, 0.28], np.float32)
        if it.name == 'grass':
            it.col = np.array([0.62, 0.52, 0.28], np.float32)
    # Samuel's wall across the narrows: an earth bank, a palisade, towers, guards
    xs = np.linspace(-40, 1120, 60)
    top = 1392 + 10 * np.sin(xs / 140)
    bank = np.vstack([np.stack([xs, top], 1), np.stack([xs[::-1], top[::-1] + 46], 1)])
    sc.add(Item(polys=[bank], z=0.452, col=(0.44, 0.34, 0.22), mat='ground', key=1.0, recv=0.3, name='bank', hatch=0))
    pal = [rect(x, 1392 + 10 * math.sin(x / 140) - 34, x + 6, 1392 + 10 * math.sin(x / 140) + 2) for x in np.arange(-40, 1120, 9)]
    sc.add(Item(polys=pal, z=0.453, col=(0.3, 0.22, 0.14), mat='wood', key=1.0, recv=0.3, name='palisade', hatch=90))
    tw = []
    for x in (150, 500, 850):
        y = 1392 + 10 * math.sin(x / 140)
        tw += [rect(x, y - 120, x + 56, y + 4), P([(x - 8, y - 118), (x + 64, y - 118), (x + 28, y - 160)])]
    sc.add(Item(polys=tw, z=0.454, col=(0.32, 0.23, 0.15), mat='wood', key=1.0, recv=0.3, name='towers', hatch=90))
    r = rng(150)
    for k in range(16):
        x = r.uniform(0, 1080)
        y = 1392 + 10 * math.sin(x / 140) - 34
        g, _ = figure(x, y, 26, face=1 if k % 2 else -1, z=0.455, col=(0.12, 0.09, 0.07), robe=0.2, halberd=k % 3 == 0, seed=500 + k,
                      name='guard%d' % k)
        sc.add(*g)
    if extra:
        extra(sc)
    return sc


def flank(sc):
    """Xiphias's men coming down the mountain behind the wall."""
    r = rng(160)
    for k in range(34):
        u = k / 33
        x = 640 + 420 * u + r.uniform(-20, 20)
        y = 1230 + 70 * u + r.uniform(-14, 14)
        g, _ = figure(x, y, 20, face=-1, z=0.315, col=(0.14, 0.12, 0.13), robe=0.2, step=0.5, halberd=True, seed=600 + k, name='flank%d' % k)
        sc.add(*g)


def rout(sc):
    """The defenders break: smoke along the wall, men running."""
    for k, x in enumerate((120, 380, 640, 900)):
        sm = catmull(P([(x - 20, 1380), (x - 60, 1250), (x - 10, 1100), (x - 70, 940), (x + 10, 900), (x + 50, 980), (x + 30, 1120),
                        (x + 40, 1260), (x + 25, 1380)]), 6, closed=True)
        sc.add(Item(polys=[sm], z=0.46, col=(0.5, 0.46, 0.44), alpha=0.42, mat='smoke', key=0.6, recv=0.3, outline=False, name='smoke%d' % k))
    r = rng(170)
    for k in range(22):
        x = r.uniform(-20, 1080); y = r.uniform(1470, 1640)
        g, _ = figure(x, y, 50 + (y - 1470) * 0.4, face=1 if r.random() < 0.6 else -1, z=0.5 + (y - 1470) / 1200, col=(0.12, 0.09, 0.07),
                      robe=0.2, step=0.9, bow=10, arm='fwd', seed=700 + k, name='flee%d' % k)
        sc.add(*g)


def gorge():
    sc = Scene('gorge')
    sc.mood = 'dusk'
    sc.sky = dict(stops=[(0, (0.3, 0.24, 0.3)), (0.4, (0.7, 0.5, 0.4)), (0.55, (0.9, 0.66, 0.45)), (1, (0.4, 0.3, 0.28))],
                  glow=[(560, 700, 300, (1.0, 0.7, 0.45), 0.6)])
    sc.amb = np.array([0.22, 0.17, 0.18], np.float32); sc.key_col = np.array([0.6, 0.42, 0.3], np.float32)
    sc.key_dir = (0.4, -0.8); sc.haze_col = np.array([0.6, 0.42, 0.36], np.float32); sc.haze, sc.haze_pow = 0.7, 1.3
    sc.sun = (560, 700); sc.rim = 0.7; sc.focus = 0.6
    L = catmull(P([(-40, 260), (180, 420), (300, 760), (380, 1100), (430, 1420), (470, 1700), (430, 1960), (-40, 1960)]), 8, closed=True)
    R = catmull(P([(1120, 200), (900, 460), (790, 800), (720, 1150), (660, 1450), (640, 1720), (700, 1960), (1120, 1960)]), 8, closed=True)
    sc.add(Item(polys=[ridge(250, 850, 1050, 240, 181, octaves=6)], z=0.15, col=(0.42, 0.3, 0.32), mat='mountain', key=0.6, recv=0, name='back'))
    sc.add(Item(polys=[rect(300, 1300, 800, 1960)], z=0.2, col=(0.3, 0.22, 0.2), mat='ground', key=0.8, recv=0.2, name='floor'))
    g = []
    for k in range(14):
        u = k / 13
        x = 520 + 30 * math.sin(k) ; y = 1330 + 360 * u
        it, _ = figure(x + (k % 3 - 1) * 26, y, 22 + 90 * u ** 1.5, face=1, z=0.22 + 0.2 * u, col=(0.12, 0.08, 0.07), robe=0.2, step=0.5,
                       halberd=k % 2 == 0, seed=800 + k, name='men%d' % k)
        g += it
    sc.add(*g)
    sc.add(Item(polys=[L], z=0.6, col=(0.17, 0.12, 0.12), mat='stone', key=0.8, recv=0, name='wallL', hatch=60))
    sc.add(Item(polys=[R], z=0.62, col=(0.15, 0.11, 0.11), mat='stone', key=0.8, recv=0, name='wallR', hatch=-60))
    sc.add(rocks(260, 470, 1250, 0.605, 182, col=(0.2, 0.15, 0.14), n=24, smin=14, smax=40, top=lambda x: 700 + (x - 260) * 0.8))
    falling = [ellipse(480 + 50 * k, 500 + 160 * k, 14 + 4 * (k % 3), 11, 9) for k in range(5)]
    sc.add(Item(polys=falling, z=0.5, col=(0.22, 0.17, 0.15), mat='stone', key=0.8, recv=0, name='stones'))
    return sc


NIGHT = dict(stops=[(0, (0.02, 0.025, 0.05)), (0.35, (0.05, 0.05, 0.09)), (0.5, (0.12, 0.09, 0.12)), (0.6, (0.07, 0.06, 0.08)),
                    (1, (0.04, 0.035, 0.04))],
             glow=[(240, 420, 280, (0.6, 0.62, 0.8), 0.25)], moon=(240, 420, 34, (0.9, 0.9, 0.95)), stars=(1400, 1000))


def fort_night():
    sc = _drop(LS.kleidion(), COLUMN + ('crow', 'branch'))
    sc.sky = NIGHT; sc.mood = 'night'
    sc.amb = np.array([0.06, 0.06, 0.09], np.float32); sc.key_col = np.array([0.22, 0.24, 0.34], np.float32)
    sc.key_dir = (-0.5, -0.8); sc.haze_col = np.array([0.06, 0.06, 0.09], np.float32); sc.haze = 0.55
    sc.sun = None; sc.rim = 0.3; sc.dust = None
    for it in sc.items:
        if it.name in ('fields', 'road', 'grass') or it.name.startswith(('tree', 'ridge', 'prilep', 'boulders', 'fort')):
            it.col = it.col * 0.45
    wins = [rect(818, 1040, 830, 1056), rect(842, 1045, 850, 1058), rect(946, 1052, 956, 1066), rect(876, 1062, 886, 1074)]
    sc.add(Item(polys=wins, z=0.395, col=(1.0, 0.65, 0.3), mat='window', emit=2.0, key=0, recv=0, name='wins', outline=False))
    sc.lights.append(Light(860, 1060, (1.0, 0.6, 0.28), I=1.0, r=120, z=0.39, air=0.2, flare=0.3))
    return sc


def mk(key, make, zoom=1.0, center=(540, 960), dust=False):
    def f():
        return Look(key, make, GROUPS, ZS, zoom=zoom, center=center)
    return f


# ------------------------------------------------------------------ the pages (English renderings)
SKY_HEAD = "John Skylitzes, Synopsis of Histories (written decades after 1014):"
SKY = "The emperor blinded the captives, about fifteen thousand, as they say, and sent them to Samuel."
KEK_HEAD = "Kekaumenos, Advice and Stories (1070s):"
KEK = "the emperor Basil captured fourteen thousand Bulgarians at the barrier."


def pages():
    return {'sky': PG.build_page('k_sky', [(SKY_HEAD, -1, -1), (SKY, S0('b2') - 0.2, E0('b2') + 0.6)], style=K.DOC, seed=81, x0=96, y0=K.DOC_Y, width=945),
            'kek': PG.build_page('k_kek', [(KEK_HEAD, -1, -1), (KEK, Wd('q1', 'another') - 0.1, Wd('q1', 'nothing') - 0.6)], style=K.DOC,
                                 seed=82, x0=96, y0=K.DOC_Y, width=945)}


# ------------------------------------------------------------------ shots
def build():
    sh = []
    FLASH.clear()
    col_w = mk('k_column', column)
    lead = mk('k_column', column, 2.0, (560, 1720))
    col_mid = mk('k_column', column, 1.8, (340, 1520))
    fortz = mk('k_column', column, 2.6, (880, 1080))
    pril = mk('k_prilep', prilep)
    field = mk('k_prilep', prilep, 2.0, (230, 1790))
    pas = mk('k_pass', pass_day)
    wall = mk('k_pass', pass_day, 2.2, (520, 1340))
    fl = mk('k_flank', lambda: pass_day(flank))
    fl_z = mk('k_flank', lambda: pass_day(flank), 2.2, (840, 1250))
    ro = mk('k_rout', lambda: pass_day(rout))
    ro_z = mk('k_rout', lambda: pass_day(rout), 1.8, (520, 1450))
    gor = mk('k_gorge', gorge)
    fn = mk('k_fortn', fort_night)
    fn_z = mk('k_fortn', fort_night, 2.8, (880, 1060))
    cellk = lambda page: (lambda: Cell(page))
    doc = lambda f, py=700: (lambda s: (lambda c: (*c.page_plate(560, py), f))(ob(s)))
    pen = lambda page, t, dx=0, dy=0, f=3.3: (lambda s: (lambda c: (c.pen_plate(t)[0] + dx, c.pen_plate(t)[1] + dy, f))(ob(s)))
    pkeys = lambda *ks: (lambda s: [(t, (v(s) if callable(v) else v)) for t, v in ks])

    # 1. OPEN: the column on the road at dusk
    c1 = S0('o2') - 0.12
    sh.append(Shot('open', 0.0, c1, col_w, [(0.0, (900, 1500, 1.1)), (c1, (720, 2150, 1.4))], xin=1.0, xout=0.0, key='col_w', hand=0.6))
    # 2. "he sent them home": the leader, close; black on "Blind."
    bl = Wd('o2', 'blind') - 0.08
    sh.append(Shot('leader_open', c1, bl, lead, [(c1, (900, 2600, 2.1)), (bl, (880, 2560, 2.3))], key='lead', hand=0.5, **CUT))
    c2 = S0('o3') - 0.1
    sh.append(Shot('black_blind', bl, c2, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, **CUT))
    # 3. the promise and the title over Prilep at dusk
    c3 = S0('x1') - 0.5
    sh.append(Shot('title', c2, c3, pril, [(c2, (1250, 1650, 1.6)), (c3, (1260, 1600, 1.75))], key='pril', xin=0.0, xout=0.8, hand=0.4))
    # 4. Basil; Samuel; forty years
    c4 = S0('x2') - 0.15
    sh.append(Shot('basil', c3 - 0.6, c4, pas, [(c3 - 0.6, (820, 1700, 1.15)), (c4, (780, 1800, 1.28))], key='pas', xin=0.6, xout=0.0, hand=0.5))
    c5 = S0('x3') - 0.15
    sh.append(Shot('samuel', c4, c5, pril, [(c4, (1260, 1650, 1.7)), (c5, (1300, 1620, 1.95))], key='pril', hand=0.5, **CUT))
    sv = Wd('x3', 'samuel') - 0.2
    sh.append(Shot('ambush', c5, sv, gor, [(c5, (800, 1900, 1.2)), (sv, (820, 2000, 1.35))], key='gor', hand=0.8, **CUT))
    c6 = S0('w1') - 0.4
    sh.append(Shot('among_dead', sv, c6, field, [(sv, (360, 2700, 2.05)), (c6, (340, 2680, 2.3))], key='field', hand=0.4, xin=0.0, xout=0.6))
    # 5. THE WALL, summer 1014; "the key"
    kp = Wd('w1', 'key') - 0.3
    pc = Wd('w1', 'called') - 0.6
    sh.append(Shot('summer', c6 - 0.4, pc, pas, [(c6 - 0.4, (800, 1600, 1.1)), (pc, (790, 1900, 1.25))], key='pas', xin=0.6, xout=0.0, hand=0.5))
    sh.append(Shot('the_wall', pc, kp, wall, [(pc, (700, 2010, 2.25)), (kp, (760, 2000, 2.4))], key='wall', hand=0.5, **CUT))
    c7 = S0('w2') - 0.1
    sh.append(Shot('the_key', kp, c7, wall, [(kp, (780, 1980, 2.9)), (c7, (785, 1975, 3.1))], key='wall', hand=0.3, **CUT))
    # 6. attacks fail (impacts, a tilt)
    hd = Wd('w2', 'held') - 0.4
    a1, a2 = Wd('w2', 'attacked'), Wd('w2', 'again')
    sh.append(Shot('attack', c7, hd, wall, [(c7, (700, 2030, 2.3)), (hd, (840, 2010, 2.5))], key='wall', hand=1.2, roll=-3.5,
                   shake=[(a1, 16.0), (a2, 14.0), (a2 + 0.6, 12.0)], **CUT))
    FLASH.extend([(a1 + 0.02, 0.8, (1.0, 0.95, 0.88)), (a2 + 0.02, 0.7, (1.0, 0.95, 0.88))])
    c8 = S0('t1') - 0.15
    sh.append(Shot('held', hd, c8, pas, [(hd, (800, 1980, 1.35)), (c8, (805, 1990, 1.42))], key='pas', hand=0.3, **CUT))
    # 7. over the mountain; behind the wall
    bh = Wd('t1', 'came') - 0.3
    sh.append(Shot('flank', c8, bh, fl_z, [(c8, (1180, 1840, 2.3)), (bh, (1300, 1900, 2.45))], key='fl_z', hand=0.6, **CUT))
    c9 = S0('t2') - 0.15
    sh.append(Shot('behind', bh, c9, fl, [(bh, (900, 1760, 1.2)), (c9, (880, 1820, 1.3))], key='fl', hand=0.6, **CUT))
    # 8. the rout
    kl = Wd('t2', 'killed') - 0.25
    sh.append(Shot('panic', c9, kl, ro_z, [(c9, (760, 2160, 1.9)), (kl, (800, 2180, 2.0))], key='ro_z', hand=1.2, roll=3.0,
                   shake=[(Wd('t2', 'panicked'), 14.0)], **CUT))
    FLASH.append((Wd('t2', 'panicked'), 0.7, (1.0, 0.95, 0.88)))
    c10 = S0('s1') - 0.15
    sh.append(Shot('captured', kl, c10, ro, [(kl, (800, 1900, 1.25)), (c10, (820, 1960, 1.35))], key='ro', hand=0.6, **CUT))
    # 9. Samuel escapes: the road to Prilep
    c11 = S0('r1') - 0.3
    gw = Wd('s1', 'got') - 0.3
    sh.append(Shot('nearly', c10, gw, ro, [(c10, (700, 2200, 1.5)), (gw, (650, 2260, 1.6))], key='ro', hand=0.8, **CUT))
    sh.append(Shot('away', gw, c11, pril, [(gw, (900, 2100, 1.2)), (c11, (1050, 1800, 1.3))], key='pril', hand=0.5, xin=0.0, xout=0.5))
    # 10. the gorge
    c12 = S0('b1') - 0.2
    tr = Wd('r1', 'trapped')
    sh.append(Shot('gorge', c11 - 0.3, c12, gor, [(c11 - 0.3, (820, 1500, 1.2)), (tr, (810, 2050, 1.45)), (c12, (800, 2150, 1.55))], key='gor',
                   xin=0.4, xout=0.0, hand=0.8, shake=[(tr + 0.3, 18.0)]))
    FLASH.append((tr + 0.3, 0.7, (1.0, 0.95, 0.88)))
    # 11. BLACK: the order
    c13 = S0('b2') - 0.2
    sh.append(Shot('black_order', c12, c13, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, **CUT))
    # 12. the chronicle is written
    c14 = S0('b3') - 0.3
    sh.append(Shot('skylitzes', c13, c14, cellk('sky'),
                   pkeys((c13, doc(3.3)), (Wd('b2', 'fifteen'), pen('sky', Wd('b2', 'fifteen'), 100, 0, 3.1)), (c14, pen('sky', E0('b2') + 0.3, 30, 20, 3.5))),
                   key='cell_sky', ap=9.0, xin=0.0, xout=0.0))
    # 13. hundreds, each led by a one-eyed man; home to their tsar
    ld = Wd('b3', 'each') - 0.2
    hm = Wd('b3', 'and') - 0.2
    sh.append(Shot('hundreds', c14, ld, col_mid, [(c14, (500, 2250, 1.9)), (ld, (540, 2290, 2.0))], key='col_mid', hand=0.6, **CUT))
    sh.append(Shot('one_eye', ld, hm, lead, [(ld, (880, 2560, 2.2)), (hm, (870, 2520, 2.45))], key='lead', hand=0.4, **CUT))
    c15 = S0('d1') - 0.2
    sh.append(Shot('home', hm, c15, col_w, [(hm, (760, 1900, 1.25)), (c15, (840, 1700, 1.15))], key='col_w', hand=0.5, **CUT))
    # 14. Samuel sees them; collapses; water; dies
    co = Wd('d1', 'collapsed') - 0.25
    sh.append(Shot('sees', c15, co, fortz, [(c15, (1300, 1640, 2.65)), (co, (1310, 1630, 2.75))], key='fortz', hand=0.5, **CUT))
    c16 = S0('d2') - 0.2
    sh.append(Shot('collapse', co, c16, fortz, [(co, (1320, 1610, 3.3)), (c16, (1325, 1615, 3.45))], key='fortz', hand=0.3, roll=-2.0,
                   shake=[(co + 0.25, 8.0)], **CUT))
    c17 = S0('d3') - 0.25
    sh.append(Shot('water', c16, c17, fn_z, [(c16, (1300, 1590, 2.9)), (c17, (1305, 1595, 3.2))], key='fn_z', hand=0.3, xin=0.0, xout=0.0))
    c18 = S0('q1') - 0.3
    sh.append(Shot('dead', c17, c18, fn, [(c17, (1100, 1700, 1.5)), (c18, (1000, 1650, 1.25))], key='fn', hand=0.3, xin=0.0, xout=0.5))
    # 15. was it true? the other writer
    an = Wd('q1', 'another') - 0.3
    sh.append(Shot('true', c18, an, cellk('sky'), pkeys((c18, pen('sky', E0('b2') - 1.0, 60, 0, 3.2)), (an, pen('sky', E0('b2') - 1.0, 40, 0, 3.6))),
                   key='cell_sky', ap=9.0, xin=0.3, xout=0.0, grade=dict(expo=0.92)))
    c19 = S0('q2') - 0.3
    sh.append(Shot('kekaumenos', an, c19, cellk('kek'),
                   pkeys((an, doc(3.3)), (Wd('q1', 'fourteen'), pen('kek', Wd('q1', 'fourteen'), 100, 0, 3.1)), (c19, pen('kek', Wd('q1', 'nothing') - 0.7, 20, 20, 3.5))),
                   key='cell_kek', ap=9.0, xin=0.0, xout=0.0))
    c20 = S0('f1') - 0.3
    sh.append(Shot('historians', c19, c20, col_w, [(c19, (820, 1650, 1.12)), (c20, (800, 1500, 1.04))], key='col_w', hand=0.4, xin=0.0, xout=0.5,
                   grade=dict(sat=0.7)))
    # 16. four more years; the nickname, later
    nk = Wd('f1', 'nickname') - 0.3
    sh.append(Shot('fought_on', c20 - 0.3, nk, pas, [(c20 - 0.3, (820, 1650, 1.15)), (nk, (800, 1800, 1.25))], key='pas', xin=0.5, xout=0.0, hand=0.5))
    c21 = S0('f2') - 0.3
    sh.append(Shot('nickname', nk, c21, pril, [(nk, (1250, 1650, 1.55)), (c21, (1150, 1700, 1.3))], key='pril', hand=0.4, xin=0.0, xout=0.5))
    # 17. "About fifteen thousand... as they say." the column walks on; the end
    endt = E0('f2') + 1.6
    sh.append(Shot('as_they_say', c21 - 0.3, endt, col_w, [(c21 - 0.3, (700, 2200, 1.45)), (endt, (820, 1500, 1.05))], key='col_w', hand=0.4,
                   xin=0.5, xout=0.9))
    sh.append(Shot('endcard', E0('f2') + 1.0, K.TOTAL, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, xin=0.5, xout=0.0))
    return sh


def labels():
    V = K.V
    return [
        (0.5, V['o1'][1] + 0.3, ['THE BALKANS', '1014'], 330, 40, CINZEL),
        (V['x1'][0] - 0.1, V['x1'][1] + 0.3, ['BASIL II', 'Eastern Roman emperor'], 330, 40, CINZEL),
        (V['x2'][0] - 0.1, V['x2'][1] + 0.3, ['SAMUEL', 'tsar of the Bulgarians'], 330, 40, CINZEL),
        (V['w1'][0] - 0.2, V['w1'][1] + 0.3, ['THE PASS OF KLEIDION', 'summer 1014'], 330, 36, CINZEL),
        (V['t1'][0] - 0.1, V['t1'][1] + 0.3, ['NIKEPHOROS XIPHIAS', 'Byzantine general'], 330, 36, CINZEL),
        (V['b2'][0] - 0.1, V['b2'][1] + 0.4, ['JOHN SKYLITZES', 'chronicler, writing decades later'], 330, 34, CINZEL),
        (V['d1'][0] - 0.2, V['d1'][1] + 0.3, ['OCTOBER 1014'], 330, 38, CINZEL),
        (V['q1'][0] + 1.2, V['q1'][1] + 0.4, ['KEKAUMENOS', 'writing in the 1070s'], 330, 36, CINZEL),
        (V['f1'][0] - 0.2, find_or(V['f1']), ['1018'], 330, 40, CINZEL),
    ]


def find_or(span):
    return span[0] + 2.6


END = [(['Kleidion, 1014'], ITAL, 54, (0.92, 0.89, 0.82), 960),
       (['How many were blinded is still debated.', 'Only one chronicle tells the story.'], ITAL, 38, (0.86, 0.83, 0.76), 1110),
       (['Sources: John Skylitzes; Kekaumenos;', 'Stephenson (2003); Holmes (2005).'], ROMAN, 30, (0.72, 0.69, 0.64), 1290)]

GAP = dict(o1=0.6, o2=0.5, o3=0.6, x1=3.0, x2=0.6, x3=0.6, w1=1.0, w2=0.6, t1=0.8, t2=0.5, s1=0.7, r1=0.9, b1=1.0, b2=0.8,
           b3=0.7, d1=1.0, d2=0.6, d3=0.7, q1=1.2, q2=0.6, f1=1.1, f2=1.0)

K.configure('kleidion', 'direct_kleidion', os.environ.get('VO_DIR', ROOT + '/film/vo_kleidion'), gap=GAP,
            title=('DARK CORNERS', ['As They Say']), end=END, labels=labels, build=build, pages=pages)
TOTAL, NF, V = K.TOTAL, K.NF, K.V

if __name__ == '__main__':
    K.main(sys.argv)
