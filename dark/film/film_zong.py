"""Dark Corners, episode 2: The Ship Called Care (the Zong, 1781). Plain telling (direct_zong.py), voice 4, the Bamberg v3
cutting grammar through film_kit. Scenes: the look-test sea (storm), its dusk, night and Jamaica variants with detail
plates, the empty sea, four documents written by candlelight, black on the hardest line.
    python film_zong.py info | still T out.jpg | frames A B out.mp4"""
from darkroot import ROOT
import sys, os, math
sys.path.insert(0, ROOT + '/film')
sys.path.insert(0, ROOT + '/look')
import numpy as np
import film_kit as K
from film_kit import Shot, Look, Cell, Black, S0, E0, Wd, CUT, FLASH, ob, CINZEL, ITAL, ROMAN
import pages as PG
import scenes as LS
from core import Item, Light, P, rect, ellipse, ridge, catmull, rng

GROUPS = [('far', 0.0, 0.5), ('ship', 0.5, 0.8), ('fg', 0.8, 1.01)]
ZS = (2.6, 1.25, 1.05)
SHIPZ = (0.595, 0.66)


# ------------------------------------------------------------------ scene variants of the look-test sea
def _no_ship(sc):
    sc.items = [it for it in sc.items if not (SHIPZ[0] <= it.z < SHIPZ[1])]
    sc.lights = []
    return sc


def _calm(sc, sky, amb, key, haze, sheen=None):
    sc.items = [it for it in sc.items if it.name not in ('curtain', 'swell', 'swellfoam')]
    sc.rain = None
    sc.sky = sky
    sc.amb = np.array(amb, np.float32); sc.key_col = np.array(key, np.float32)
    sc.haze_col = np.array(haze, np.float32)
    for it in sc.items:
        if it.name == 'sheen' and sheen is not None:
            it.col = np.array(sheen, np.float32)
    return sc


DUSK_SKY = dict(stops=[(0, (0.16, 0.14, 0.2)), (0.3, (0.42, 0.3, 0.32)), (0.47, (0.85, 0.55, 0.36)), (0.535, (1.0, 0.72, 0.45)),
                       (0.545, (0.62, 0.48, 0.4)), (1, (0.22, 0.2, 0.24))],
                glow=[(330, 1000, 380, (1.0, 0.65, 0.35), 0.9), (330, 1010, 70, (1.0, 0.9, 0.7), 1.2)],
                clouds=[dict(y0=200, y1=900, cell=320, seed=61, cov=0.42, soft=0.2, col_top=(1.0, 0.7, 0.5),
                             col_bot=(0.35, 0.25, 0.3), dens=0.8, ystretch=0.2)])
NIGHT_SKY = dict(stops=[(0, (0.015, 0.02, 0.045)), (0.35, (0.03, 0.045, 0.08)), (0.53, (0.08, 0.1, 0.15)), (0.545, (0.05, 0.06, 0.09)),
                        (1, (0.02, 0.03, 0.045))],
                 glow=[(820, 420, 300, (0.5, 0.58, 0.8), 0.3)], moon=(820, 420, 34, (0.85, 0.88, 0.95)),
                 stars=(900, 1000),
                 clouds=[dict(y0=250, y1=800, cell=300, seed=62, cov=0.5, soft=0.25, col_top=(0.3, 0.33, 0.42),
                              col_bot=(0.05, 0.06, 0.09), dens=0.8, ystretch=0.3)])


def storm():
    return LS.zong()


def dusk():
    return _calm(LS.zong(), DUSK_SKY, (0.3, 0.24, 0.26), (0.7, 0.48, 0.32), (0.55, 0.42, 0.38), sheen=(1.0, 0.7, 0.45))


def island(sc, x0, x1, base, amp, z, col, seed=71):
    sc.add(Item(polys=[ridge(x0, x1, base, amp, seed, octaves=6, gain=0.5, cells=2, ybottom=base + 30)], z=z, col=col,
                mat='mountain', key=0.5, recv=0, name='jamaica', hatch=-15))
    return sc


def jamaica():
    return island(dusk(), 640, 1180, 1050, 120, 0.25, (0.28, 0.24, 0.3))


def black_river():
    sc = island(dusk(), 380, 1180, 1050, 230, 0.27, (0.24, 0.24, 0.24), seed=72)
    sc.add(Item(polys=[rect(380, 1036, 1180, 1052)], z=0.28, col=(0.14, 0.17, 0.13), mat='foliage', key=0.6, recv=0, name='shore'))
    return sc


def night(rope=False):
    sc = _calm(LS.zong(), NIGHT_SKY, (0.05, 0.06, 0.1), (0.25, 0.3, 0.45), (0.06, 0.07, 0.11), sheen=(0.55, 0.62, 0.8))
    for it in sc.items:
        if it.name in ('sea', 'swell', 'troughs'):
            it.col = it.col * 0.55
        if it.name in ('crests', 'swellfoam', 'bowfoam'):
            it.col = it.col * 0.6
    if rope:   # one rope hanging from the rail into the sea
        x, y, L = 770, 1150, 560
        u = L / 65.0
        top = (x - 22 * u, y - 7.0 * u)
        line = catmull([top, (x - 21 * u, y - 3.5 * u), (x - 22.5 * u, y + 0.4 * u)], 8)
        sc.add(Item(lines=[(line, 2.0)], z=0.64, col=(0.5, 0.45, 0.38), mat='rope', key=0.8, recv=1.0, name='rope', outline=False, detail=True))
    return sc


def empty_dusk():
    return _no_ship(dusk())


def empty_night():
    return _no_ship(night())


def bob(amp=1.0, seed=3):
    """The ship's roll and heave on the swell."""
    def m(t):
        rot = amp * (0.7 * math.sin(t * 0.9 + seed) + 0.3 * math.sin(t * 2.1 + 1.3 * seed))
        dv = amp * 6 * math.sin(t * 0.9 + seed + 0.6)
        return (0.0, dv, rot, 1.0, 1155.0, 1725.0)
    return m


def swell_motion(amp=1.0):
    return lambda t: (6 * amp * math.sin(t * 0.5), 10 * amp * math.sin(t * 0.8 + 1.0), 0.0, 1.0, 810.0, 2700.0)


RAIN = [dict(seed=7, n=900, angle=16, speed=2400, length=(30, 95), alpha=0.17, col=(0.62, 0.66, 0.72)),
        dict(seed=8, n=160, angle=16, speed=3300, length=(110, 220), alpha=0.07, col=(0.7, 0.74, 0.8), depth=(0.9, 1.0))]


def mk(key, make, zoom=1.0, center=(540, 960), rain=False, roll=1.0):
    def f():
        lk = Look(key, make, GROUPS, ZS, zoom=zoom, center=center, rain=RAIN if rain else None)
        for L in lk.layers:
            if L.name == 'ship':
                L.motion = bob(roll * (1.6 if rain else 0.8))
                if zoom != 1.0:
                    m0 = L.motion
                    pu, pv = 810 + zoom * (1155 - center[0] * 1.5), 1440 + zoom * (1725 - center[1] * 1.5)
                    L.motion = lambda t, m0=m0, pu=pu, pv=pv: (lambda r: (r[0], r[1] * zoom, r[2], 1.0, pu, pv))(m0(t))
            if L.name == 'fg':
                L.motion = swell_motion(2.0 if rain else 1.0)
        return lk
    return f


# ------------------------------------------------------------------ the documents (quill hands, English)
LEDGER = "Luke Collingwood master, from the Coast of Africa for Jamaica."
LEDGER_2 = "442 Slaves on board, valued at 30l. per Head. Insured for 8,000l."
COURT_HEAD = "Guildhall, 6th March 1783. Gregson and others against Gilbert."
COURT_V = "The Jury found a Verdict before Lord Mansfield for the Plaintiffs."
COURT_LEE = "it is the case of throwing over goods"
SHARP_PRE = "To the Lords Commissioners of the Admiralty."
SHARP = "that the blood of the murdered may not rest on the whole kingdom"
KB_HEAD = "Gregson v. Gilbert. Thursday, 22d May, 1783."
KB = "after the rain (if the fact be so), for which, upon the evidence, there appears to have been no necessity."


def pages():
    V = K.V
    P = {}
    P['ledger'] = PG.build_page('z_ledger', [(LEDGER, -1, -1), (LEDGER_2, Wd('x4', 'insured') - 0.2, E0('x4') + 0.2)], style=K.DOC,
                                seed=61, x0=96, y0=K.DOC_Y, width=945)
    P['court'] = PG.build_page('z_court', [(COURT_HEAD, -1, -1), (COURT_V, S0('c2') + 0.2, E0('c2') + 0.3),
                                           (COURT_LEE, Wd('c3', 'case') - 0.2, E0('c3') + 0.3)], style=K.DOC, seed=62, x0=96, y0=K.DOC_Y, width=945)
    P['sharp'] = PG.build_page('z_sharp', [(SHARP_PRE, -1, -1), (SHARP, S0('e2') - 0.3, E0('e2') + 1.2)], style=PG.JUNIUS, seed=63, y0=K.DOC_Y)
    P['kb'] = PG.build_page('z_kb', [(KB_HEAD, -1, -1), (KB, S0('j1') + 0.4, E0('j1') + 0.6)], style=K.DOC, seed=64, x0=96, y0=K.DOC_Y, width=945)
    return P


# ------------------------------------------------------------------ the shot list
def build():
    sh = []
    FLASH.clear()
    sea = 'sea'
    storm_w = mk('z_storm', storm, rain=True)
    storm_deck = mk('z_storm', storm, 2.2, (640, 1070), rain=True)
    dusk_w = mk('z_dusk', dusk)
    dusk_deck = mk('z_dusk', dusk, 2.1, (620, 1060))
    dusk_stern = mk('z_dusk', dusk, 2.5, (790, 1080))
    dusk_bow = mk('z_dusk', dusk, 2.1, (360, 1050))
    jam = mk('z_jamaica', jamaica)
    river = mk('z_river', black_river)
    night_w = mk('z_night', night)
    night_stern = mk('z_nightr', lambda: night(True), 2.6, (775, 1085))
    night_rope = mk('z_nightr', lambda: night(True), 3.0, (585, 1110))
    e_dusk = mk('z_edusk', empty_dusk)
    e_night = mk('z_enight', empty_night)
    cellk = lambda page: (lambda: Cell(page))
    doc = lambda f, py=700: (lambda s: (lambda c: (*c.page_plate(470, py), f))(ob(s)))

    def pen(page, t, dx=0, dy=0, f=3.3):
        return lambda s: (lambda c: (lambda q: (q[0] + dx, q[1] + dy, f))(c.page_plate(470, PG.pen_at(c.base.page, t)[0][1])))(ob(s))

    def pkeys(*ks):
        """camera keys where a key may be a function of the shot (pen positions)"""
        return lambda s: [(t, (v(s) if callable(v) else v)) for t, v in ks]

    # 1. OPEN: the storm, the ship in the rain; lightning
    c1 = S0('o2') - 0.12
    sh.append(Shot('open', 0.0, c1, storm_w, [(0.0, (760, 1350, 1.05)), (c1, (900, 1560, 1.45))], xin=1.0, xout=0.0, key='storm_w', hand=0.9))
    FLASH.extend([(0.35, 1.2, (0.75, 0.82, 1.0)), (0.6, 0.5, (0.75, 0.82, 1.0))])
    # 2. HARD CUT: the court record ("a London court, as an insurance claim")
    c2 = S0('o3') - 0.1
    sh.append(Shot('court_open', c1, c2, cellk('court'), pkeys((c1, doc(3.23)), (c2, doc(3.48, 720))), key='cell_court', ap=9.0, **CUT))
    # 3. the empty sea at dusk under the promise and the title
    c3 = S0('x1') - 0.5
    sh.append(Shot('title_sea', c2, c3, e_dusk, [(c2, (700, 1500, 1.25)), (c3, (640, 1450, 1.12))], key='e_dusk', xin=0.0, xout=0.8, hand=0.5))
    # 4. THE ZONG: the ship at dusk; in on "care"
    care = Wd('x1', 'care') - 0.25
    tk = Wd('x1', 'taken') - 0.2
    sh.append(Shot('dusk_ship', c3 - 0.8, tk, dusk_w, [(c3 - 0.8, (820, 1500, 1.1)), (tk, (790, 1560, 1.25))], key='dusk_w', xin=0.8, xout=0.0, hand=0.6))
    sh.append(Shot('bow', tk, care, dusk_bow, [(tk, (520, 1560, 2.3)), (care, (560, 1580, 2.45))], key='dusk_bow', hand=0.6, **CUT))
    c4 = S0('x2') - 0.05
    sh.append(Shot('stern_care', care, c4, dusk_stern, [(care, (1150, 1600, 2.9)), (c4, (1165, 1610, 3.25))], key='dusk_stern', hand=0.6, **CUT))
    # 5. on board: crew and captives (the deck, close)
    tw = Wd('x2', 'twice') - 0.1
    sh.append(Shot('deck', c4, tw, dusk_deck, [(c4, (900, 1590, 2.35)), (tw, (960, 1580, 2.5))], key='dusk_deck', hand=0.8, **CUT))
    c5 = S0('x4') - 0.1
    sh.append(Shot('deck_wide', tw, c5, dusk_w, [(tw, (760, 1560, 1.5)), (c5, (780, 1600, 1.62))], key='dusk_w', hand=0.6, **CUT))
    # 6. INSURED: the ledger is written
    c6 = S0('m1') - 0.4
    led = lambda s: ob(s)
    sh.append(Shot('ledger', c5, c6, cellk('ledger'),
                   pkeys((c5, doc(2.89)), (Wd('x4', 'thirty'), pen('ledger', Wd('x4', 'thirty'), 20, 0, 2.89)), (c6, pen('ledger', E0('x4'), 40, 30, 3.06))),
                   key='cell_ledger', ap=9.0, xin=0.0, xout=0.5))
    # 7. JAMAICA, mistaken; sailed past it
    past = Wd('m1', 'sailed') - 0.2
    sh.append(Shot('jamaica', c6 - 0.5, past, jam, [(c6 - 0.5, (1350, 1540, 1.7)), (past, (1180, 1560, 1.5))], key='jam', xin=0.5, xout=0.0, hand=0.6))
    c7 = S0('m2') - 0.1
    sh.append(Shot('jamaica_past', past, c7, jam, [(past, (760, 1620, 1.18)), (c7, (700, 1600, 1.08))], key='jam', hand=0.5, **CUT))
    # 8. downwind, night falls; the water runs low
    c8 = S0('m3') - 0.15
    sh.append(Shot('night_falls', c7, c8, night_w, [(c7, (800, 1560, 1.2)), (c8, (860, 1620, 1.4))], key='night_w', xin=0.0, xout=0.0, hand=0.6))
    # 9. THE RULE: the ledger again, the price
    c9 = S0('d1') - 0.4
    m3b, m3c = Wd('m3', 'captives') - 0.15, Wd('m3', 'thrown') - 0.35
    sh.append(Shot('rule', c8, m3b, cellk('ledger'), pkeys((c8, doc(2.72)), (m3b, doc(3.15, 750))), key='cell_ledger', ap=9.0, xin=0.0, xout=0.0))
    sh.append(Shot('rule_sick', m3b, m3c, night_stern, [(m3b, (1120, 1640, 2.7)), (m3c, (1140, 1620, 2.85))], key='night_stern', hand=0.5, **CUT))
    sh.append(Shot('rule_paid', m3c, c9, cellk('ledger'), pkeys((m3c, pen('ledger', E0('x4') - 1.8, 20, 0, 2.55)), (c9, pen('ledger', E0('x4') - 1.8, 0, 0, 2.98))),
                   key='cell_ledger', ap=9.0, xin=0.0, xout=0.4))
    # 10. THE NIGHT OF 29 NOVEMBER: the lit stern, very close
    c10 = S0('d2') - 0.25
    sh.append(Shot('decided', c9 - 0.3, c10, night_stern, [(c9 - 0.3, (1170, 1620, 2.95)), (c10, (1160, 1630, 3.4))],
                   key='night_stern', xin=0.4, xout=0.0, hand=0.5, grade=dict(expo=1.1)))
    # 11. BLACK: the women and children (sound only)
    c11 = S0('d3') - 0.25
    sh.append(Shot('black_54', c10, c11, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, **CUT))
    # 12. two days later: the ship small in the night
    c12 = S0('r1') - 0.1
    sh.append(Shot('night_far', c11, c12, night_w, [(c11, (780, 1480, 1.0)), (c12, (790, 1500, 1.06))], key='night_w', hand=0.4, **CUT))
    # 13. THE RAIN: lightning on "rained"; the deck in the rain
    rained = Wd('r1', 'rained')
    FLASH.append((rained - 0.05, 1.3, (0.75, 0.82, 1.0)))
    cask = Wd('r1', 'filled') - 0.15
    sh.append(Shot('rain', c12, cask, storm_w, [(c12, (800, 1450, 1.2)), (cask, (840, 1500, 1.32))], key='storm_w', hand=1.0, **CUT))
    c13 = S0('r2') - 0.1
    sh.append(Shot('rain_deck', cask, c13, storm_deck, [(cask, (930, 1600, 2.45)), (c13, (960, 1620, 2.6))], key='storm_deck', hand=1.0, **CUT))
    # 14. "And they kept going." the storm, slowly
    c14 = S0('r3') - 0.1
    sh.append(Shot('kept_going', c13, c14, storm_w, [(c13, (900, 1600, 1.55)), (c14, (920, 1640, 1.7))], key='storm_w', hand=0.7, **CUT))
    # 15. chained; ten jumped (Dutch angle, a hit); the sea they chose
    jumped = Wd('r3', 'jumped')
    chose = Wd('r3', 'chose') - 0.25
    sh.append(Shot('chained', c14, chose, storm_deck, [(c14, (1000, 1640, 2.7)), (jumped, (940, 1600, 2.55)), (chose, (900, 1600, 2.5))],
                   key='storm_deck', hand=1.2, roll=-4.0, shake=[(Wd('r3', 'thrown'), 14.0), (jumped, 18.0)], **CUT))
    FLASH.append((jumped, 0.9, (1.0, 0.95, 0.9)))
    c15 = S0('p1') - 0.2
    sh.append(Shot('the_sea', chose, c15, storm_w, [(chose, (500, 2350, 1.6)), (c15, (520, 2380, 1.75))], key='storm_w', hand=0.8, xin=0.0, xout=0.5))
    # 16. the rope
    c16 = S0('a1') - 0.4
    sh.append(Shot('rope', c15 - 0.4, c16, night_rope, [(c15 - 0.4, (880, 1720, 3.4)), (Wd('p1', 'climbed'), (880, 1640, 3.55)), (c16, (885, 1600, 3.6))],
                   key='night_rope', xin=0.5, xout=0.6, hand=0.4, grade=dict(expo=1.15)))
    # 17. BLACK RIVER, JAMAICA: three weeks later
    c17 = S0('c1') - 0.4
    sh.append(Shot('black_river', c16 - 0.5, c17, river, [(c16 - 0.5, (780, 1520, 1.15)), (c17, (850, 1560, 1.35))], key='river', xin=0.7, xout=0.0, hand=0.5))
    # 18. THE CLAIM: the court record (verdict, the lawyer's words)
    c18 = S0('e1') - 0.4
    c2a = S0('c2') - 0.2
    sh.append(Shot('claim', c17, c2a, cellk('ledger'), pkeys((c17, doc(2.72)), (c2a, pen('ledger', E0('x4') - 1.8, 40, 0, 2.55))),
                   key='cell_ledger', ap=9.0, **CUT))
    sh.append(Shot('verdict', c2a, Wd('c3', 'case') - 0.3, cellk('court'),
                   pkeys((c2a, doc(2.89)), (S0('c2') + 0.3, pen('court', S0('c2') + 0.3, 20, 40, 2.72)), (E0('c2'), pen('court', E0('c2') - 0.2, 0, 30, 2.8))),
                   key='cell_court', ap=9.0, **CUT))
    sh.append(Shot('goods', Wd('c3', 'case') - 0.3, c18, cellk('court'),
                   pkeys((Wd('c3', 'case') - 0.3, pen('court', Wd('c3', 'case'), 20, 0, 3.23)), (c18, pen('court', E0('c3'), -20, 10, 3.48))),
                   key='cell_court', ap=9.0, xin=0.0, xout=0.5))
    # 19. EQUIANO AND SHARP: Sharp's letter to the Admiralty
    c19 = S0('j1') - 0.4
    tk2 = Wd('e1', 'took') - 0.3
    sh.append(Shot('equiano', c18 - 0.3, tk2, e_night, [(c18 - 0.3, (760, 1500, 1.15)), (tk2, (720, 1420, 1.3))], key='e_night', xin=0.5, xout=0.0, hand=0.4))
    sh.append(Shot('sharp', tk2, c19, cellk('sharp'),
                   pkeys((tk2, doc(2.63)), (S0('e2'), pen('sharp', S0('e2'), 20, -60, 2.55)), (c19, pen('sharp', E0('e2') + 1.0, 30, 10, 2.89))),
                   key='cell_sharp', ap=9.0, xin=0.0, xout=0.0))
    # 20. THE JUDGMENT: "after the rain"
    c20 = S0('f1') - 0.4
    j2a = S0('j2') - 0.2
    sh.append(Shot('judgment', c19, j2a, cellk('kb'),
                   pkeys((c19, doc(2.8)), (Wd('j1', 'rain'), pen('kb', S0('j1') + 2.0, 20, 0, 2.8)), (j2a, pen('kb', E0('j1'), 20, 30, 3.06))),
                   key='cell_kb', ap=9.0, xin=0.0, xout=0.0))
    sh.append(Shot('never', j2a, c20, e_night, [(j2a, (820, 1520, 1.3)), (c20, (800, 1420, 1.12))], key='e_night', hand=0.4, xin=0.0, xout=0.5))
    # 21. only their price
    c21 = S0('f2') - 0.4
    sh.append(Shot('price', c20 - 0.2, c21, cellk('ledger'), pkeys((c20 - 0.2, pen('ledger', E0('x4') - 1.5, 20, 0, 2.55)), (c21, pen('ledger', E0('x4') - 1.5, 30, 0, 3.31))),
                   key='cell_ledger', ap=9.0, xin=0.4, xout=0.6, grade=dict(expo=0.9)))
    # 22. 1807; the empty sea at dusk; the end
    c22 = S0('f3') - 0.3
    sh.append(Shot('campaign', c21 - 0.4, c22, dusk_w, [(c21 - 0.4, (760, 1560, 1.2)), (c22, (720, 1520, 1.1))], key='dusk_w', xin=0.6, xout=0.0, hand=0.5))
    endt = E0('f3') + 1.6
    sh.append(Shot('care_end', c22, endt, e_dusk, [(c22, (700, 1500, 1.15)), (endt, (640, 1300, 1.02))], key='e_dusk', xin=0.0, xout=0.9, hand=0.4))
    sh.append(Shot('endcard', E0('f3') + 1.0, K.TOTAL, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, xin=0.5, xout=0.0))
    return sh


def labels():
    V = K.V
    L = [
        (0.5, V['o1'][1] + 0.3, ['THE CARIBBEAN', '1781'], 330, 40, CINZEL),
        (V['x1'][0] - 0.1, V['x1'][1] + 0.3, ['THE ZONG', 'once the Dutch ship Zorg'], 330, 40, CINZEL),
        (V['x4'][0] - 0.2, V['x4'][1] + 0.4, ['THE INSURANCE', '£30 a head'], 330, 38, CINZEL),
        (V['m1'][0] - 0.2, V['m1'][1] + 0.3, ['JAMAICA', '27 November 1781'], 330, 38, CINZEL),
        (V['d1'][0] - 0.3, V['d1'][1] + 0.5, ['29 NOVEMBER 1781'], 330, 38, CINZEL),
        (V['d3'][0] - 0.2, V['d3'][1] + 0.3, ['1 DECEMBER 1781'], 330, 38, CINZEL),
        (V['a1'][0] - 0.2, V['a1'][1] + 0.3, ['BLACK RIVER, JAMAICA', '22 December 1781'], 330, 36, CINZEL),
        (V['c2'][0] - 0.2, V['c2'][1] + 0.4, ['LONDON', '6 March 1783'], 330, 38, CINZEL),
        (V['c3'][0] - 0.1, V['c3'][1] + 0.4, ["THE OWNERS' LAWYER", 'in court, 1783'], 330, 36, CINZEL),
        (V['e1'][0] - 0.2, V['e1'][1] + 0.3, ['OLAUDAH EQUIANO', 'and Granville Sharp, 19 March 1783'], 330, 34, CINZEL),
        (V['j1'][0] - 0.2, V['j1'][1] + 0.4, ["COURT OF KING'S BENCH", '22 May 1783'], 330, 34, CINZEL),
        (V['f2'][0] - 0.2, V['f2'][1] + 0.5, ['1807'], 330, 40, CINZEL),
    ]
    return L


END = [(['The Zong, 1781'], ITAL, 54, (0.92, 0.89, 0.82), 960),
       (['About 130 people were killed.', 'No one was ever tried for it.'], ITAL, 40, (0.86, 0.83, 0.76), 1110),
       (["Sources: Granville Sharp's papers (1783),", 'Gregson v Gilbert (1783), Walvin, The Zong (2011).'], ROMAN, 30, (0.72, 0.69, 0.64), 1300)]

GAP = dict(o1=0.6, o2=0.5, o3=0.5, x1=3.0, x2=0.6, x4=0.7, m1=1.0, m2=0.5, m3=0.7, d1=1.2, d2=0.7, d3=0.9, r1=1.0, r2=0.7,
           r3=0.8, p1=1.1, a1=1.2, c1=0.9, c2=0.6, c3=0.5, e1=1.1, e2=0.5, j1=0.9, j2=0.5, f1=1.2, f2=0.8, f3=0.7)

K.configure('zong', 'direct_zong', os.environ.get('VO_DIR', ROOT + '/film/vo_zong'), gap=GAP, title=('DARK CORNERS', ['The Ship', 'Called Care']),
            end=END, labels=labels, build=build, pages=pages)
TOTAL, NF, V = K.TOTAL, K.NF, K.V

if __name__ == '__main__':
    K.main(sys.argv)
