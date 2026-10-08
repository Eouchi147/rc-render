"""Dark Corners, episode 3: I Am Buying Her Life (Arabia, about 600). Plain telling (direct_arabia.py), voice 4, the
Bamberg v3 grammar through film_kit. Scenes: the look-test camp under the stars with detail plates, the open desert,
the camp from afar, dawn (he walks home), a valley at Mecca, two pages (the old records, the grandson's verse), black.
No revered figure is shown or voiced; numbers are shown as the sources give them, in disagreement.
    python film_arabia.py info | still T out.jpg | frames A B out.mp4"""
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
from parts import figure, camel, shrub

GROUPS = [('far', 0.0, 0.5), ('camp', 0.5, 0.69), ('riders', 0.69, 0.85), ('fg', 0.85, 1.01)]
ZS = (3.0, 1.5, 1.15, 1.04)
CAMP = ('tent1', 'tent2', 'hearth', 'flame', 'smoke', 'woman')
SHE = ('she1', 'she2', 'leads')
RIDER = ('mount', 'sasaa')


def _drop(sc, prefixes):
    sc.items = [it for it in sc.items if not any(it.name.startswith(p) for p in prefixes)]
    return sc


def _moon(sc):
    sc.amb = sc.amb * 1.7
    sc.key_col = sc.key_col * 1.8
    return sc


def camp():
    return _moon(LS.arabia())


def search():
    sc = _moon(_drop(LS.arabia(), CAMP + SHE))
    sc.lights = []; sc.embers = None
    sc.sky = dict(sc.sky); sc.sky['glow'] = []
    return sc


def camp_far():
    sc = _moon(_drop(LS.arabia(), SHE + RIDER))
    return sc


DAWN_SKY = dict(stops=[(0, (0.1, 0.13, 0.25)), (0.35, (0.3, 0.33, 0.46)), (0.6, (0.75, 0.6, 0.55)), (0.68, (1.0, 0.78, 0.55)),
                       (0.7, (0.6, 0.45, 0.38)), (1, (0.3, 0.22, 0.2))],
                glow=[(760, 1330, 420, (1.0, 0.7, 0.45), 0.8)], stars=(300, 600))


def dawn():
    sc = _drop(LS.arabia(), CAMP + SHE + RIDER)
    sc.lights = []; sc.embers = None
    sc.sky = DAWN_SKY
    sc.amb = np.array([0.32, 0.28, 0.3], np.float32); sc.key_col = np.array([0.8, 0.6, 0.42], np.float32)
    sc.key_dir = (0.5, -0.4); sc.haze_col = np.array([0.6, 0.48, 0.45], np.float32); sc.haze = 0.6
    for it in sc.items:
        if it.name.startswith(('dune', 'plain', 'fgdune')):
            it.col = it.col * 2.2
    w, _ = figure(470, 1700, 330, face=-1, z=0.75, col=(0.07, 0.055, 0.05), robe=0.34, step=0.55, headcloth=True, arm='hang',
                  arm2='hang', seed=301, name='walker')
    sc.add(*w)
    steps = [ellipse(470 + 70 * k, 1712 + 6 * k, 9, 3.5, 10) for k in range(1, 9)]
    sc.add(Item(polys=steps, z=0.74, col=(0.12, 0.09, 0.08), mat='sand', key=0.6, recv=0.2, outline=False, name='prints', alpha=0.7))
    return sc


def mecca():
    """A valley of dark rock at night; small flat-roofed houses; a man holding a newborn, a father turned to him."""
    from core import Scene
    sc = Scene('mecca')
    sc.mood = 'night'
    sc.sky = dict(stops=[(0, (0.012, 0.016, 0.04)), (0.35, (0.03, 0.04, 0.08)), (0.5, (0.07, 0.07, 0.11)), (1, (0.04, 0.035, 0.04))],
                  stars=(1600, 900), glow=[(780, 300, 260, (0.6, 0.65, 0.85), 0.2)], moon=(780, 300, 30, (0.9, 0.9, 0.95)))
    sc.amb = np.array([0.07, 0.075, 0.11], np.float32); sc.key_col = np.array([0.22, 0.25, 0.38], np.float32)
    sc.key_dir = (0.3, -0.9); sc.haze_col = np.array([0.07, 0.07, 0.11], np.float32); sc.haze, sc.haze_pow = 0.5, 1.4
    sc.focus = 0.75
    for k, (base, amp, z, col, seed) in enumerate([(1080, 330, 0.12, (0.1, 0.09, 0.11), 401), (1200, 300, 0.22, (0.12, 0.1, 0.11), 402),
                                                    (1330, 200, 0.33, (0.14, 0.12, 0.12), 403)]):
        sc.add(Item(polys=[ridge(-40, 1120, base, amp, seed, octaves=7, gain=0.55)], z=z, col=col, mat='mountain', key=0.7, recv=0.2,
                    name='rock%d' % k, hatch=-25))
    r = rng(404)
    houses, wins = [], []
    for i in range(14):
        x = 40 + i * 74 + r.uniform(-20, 20); w = r.uniform(60, 110); h = r.uniform(60, 120); y = 1420 + r.uniform(-30, 30)
        houses.append(rect(x, y - h, x + w, y))
        if r.random() < 0.35:
            wins.append(rect(x + w * 0.4, y - h * 0.55, x + w * 0.4 + 10, y - h * 0.55 + 14))
    sc.add(Item(polys=houses, z=0.42, col=(0.2, 0.16, 0.13), mat='stone', key=0.8, recv=1.0, name='houses', hatch=0))
    sc.add(Item(polys=wins, z=0.421, col=(1.0, 0.65, 0.3), mat='window', emit=1.6, key=0, recv=0, name='wins', outline=False))
    sc.add(Item(polys=[rect(-20, 1415, 1100, 1940)], z=0.45, col=(0.16, 0.12, 0.1), mat='ground', key=0.8, recv=1.0, name='ground',
                shade=(0.8, 1.1), hatch=-5))
    # a doorway lit from inside, the two men in front of it
    sc.add(Item(polys=[rect(600, 1330, 760, 1660)], z=0.55, col=(0.22, 0.17, 0.13), mat='stone', key=0.8, recv=1.0, name='house_near'))
    sc.add(Item(polys=[rect(640, 1450, 700, 1660)], z=0.551, col=(1.0, 0.62, 0.3), mat='window', emit=1.4, key=0, recv=0, name='door', outline=False))
    sc.lights.append(Light(670, 1560, (1.0, 0.6, 0.3), I=1.4, r=260, z=0.56, air=0.18, flare=0.3))
    z_, _ = figure(470, 1760, 430, face=1, z=0.7, col=(0.05, 0.04, 0.035), robe=0.4, headcloth=True, arm='chest', baby=True,
                   seed=410, name='zayd')
    sc.add(*z_)
    f_, _ = figure(840, 1770, 420, face=-1, z=0.71, col=(0.05, 0.04, 0.035), robe=0.36, headcloth=True, bow=14, arm='hang',
                   seed=411, name='father')
    sc.add(*f_)
    xs = np.linspace(-40, 1120, 50)
    ys = 1860 - 30 * np.sin(np.linspace(0, 3.0, 50))
    sc.add(Item(polys=[np.vstack([np.stack([xs, ys], 1), [(1120, 1960), (-40, 1960)]])], z=0.9, col=(0.08, 0.06, 0.05), mat='ground',
                key=0.9, recv=0.3, name='fg', shade=(1.2, 0.7)))
    sc.add(shrub(140, 1870, 150, 0.92, 412))
    return sc


MECCA_G = [('far', 0.0, 0.5), ('near', 0.5, 0.8), ('fg', 0.8, 1.01)]
FIRE = (735, 1474)


def mk(key, make, zoom=1.0, center=(540, 960), fire=True, groups=GROUPS, zs=ZS, expo=2.0):
    def f():
        fl = [(FIRE[0], FIRE[1], 0.35, 63)] if fire else ()
        em = dict(x=FIRE[0], y=FIRE[1] - 20, n=70, spread=24, rise=320, seed=94) if fire else None
        return Look(key, make, groups, zs, zoom=zoom, center=center, flames=fl, embers=em, expo=expo)
    return f


# ------------------------------------------------------------------ the pages
REC_HEAD = "How many girls did he save? What the old books say:"
REC = ["Ibn Durayd: 30", "The Book of Songs: 96", "al-Tabarani: 360", "The Book of Songs: 400"]
POEM_HEAD = "al-Farazdaq, of his grandfather:"
POEM = "he is the one who held back those who would bury, and gave life to the buried girl, so that she was not buried."


def pages():
    V = K.V
    words = ['thirty', 'ninety', 'three', 'four']
    parts = [(REC_HEAD, -1, -1)]
    for i, w in enumerate(words):
        a = Wd('v2', w) - 0.15 if w != 'ninety' else Wd('v2', 'ninety-six') - 0.15
        parts.append((REC[i], a, a + 0.9))
    P = {'records': PG.build_page('a_records', parts, style=K.DOC, seed=71, x0=96, y0=K.DOC_Y, width=945),
         'poem': PG.build_page('a_poem', [(POEM_HEAD, -1, -1), (POEM, S0('g2') - 0.3, E0('g2') + 0.8)], style=K.DOC, seed=72,
                               x0=96, y0=K.DOC_Y, width=945)}
    return P


# ------------------------------------------------------------------ shots
def build():
    sh = []
    FLASH.clear()
    camp_w = mk('a_camp', camp)
    rider = mk('a_camp', camp, 1.9, (250, 1520))
    she = mk('a_camp', camp, 2.0, (60, 1520))
    fire = mk('a_camp', camp, 2.4, (720, 1430))
    tents = mk('a_camp', camp, 1.9, (640, 1400))
    sky = mk('a_camp', camp, 1.6, (700, 500))
    srch = mk('a_search', search, fire=False)
    srch_r = mk('a_search', search, 1.9, (250, 1520), fire=False)
    far = mk('a_campfar', camp_far)
    dawn_w = mk('a_dawn', dawn, fire=False, expo=1.3)
    dawn_c = mk('a_dawn', dawn, 1.9, (470, 1560), fire=False, expo=1.3)
    mec = mk('a_mecca', mecca, fire=False, groups=MECCA_G, zs=(2.6, 1.2, 1.04))
    mec_z = mk('a_mecca', mecca, 1.8, (480, 1540), fire=False, groups=MECCA_G, zs=(2.6, 1.2, 1.04))
    mec_f = mk('a_mecca', mecca, 1.8, (820, 1540), fire=False, groups=MECCA_G, zs=(2.6, 1.2, 1.04))
    cellk = lambda page: (lambda: Cell(page))
    doc = lambda f, py=700: (lambda s: (lambda c: (*c.page_plate(470, py), f))(ob(s)))
    pen = lambda page, t, dx=0, dy=0, f=3.3: (lambda s: (lambda c: (lambda q: (q[0] + dx, q[1] + dy, f))(c.page_plate(470, PG.pen_at(c.base.page, t)[0][1])))(ob(s)))
    pkeys = lambda *ks: (lambda s: [(t, (v(s) if callable(v) else v)) for t, v in ks])

    # 1. OPEN: the stars, then down to the rider and his camels
    c1 = S0('o2') - 0.12
    sh.append(Shot('open', 0.0, c1, camp_w, [(0.0, (880, 900, 1.2)), (S0('o1') + 1.5, (700, 1700, 1.15)), (c1, (500, 2250, 1.35))],
                   xin=1.0, xout=0.0, key='camp_w', hand=0.6))
    # 2. HARD CUT: the rider, close
    c2 = S0('o3') - 0.1
    sh.append(Shot('rider_open', c1, c2, rider, [(c1, (390, 2240, 2.2)), (c2, (380, 2200, 2.4))], key='rider', hand=0.6, **CUT))
    # 3. the sky over the promise and the title (the stars the Arabs called the daughters of the bier)
    c3 = S0('x1') - 0.5
    sh.append(Shot('title_sky', c2, c3, sky, [(c2, (1100, 760, 1.8)), (c3, (1080, 700, 1.95))], key='sky', xin=0.0, xout=0.8, hand=0.3))
    # 4. SA'SA'A
    c4 = S0('x2') - 0.2
    sh.append(Shot('sasaa', c3 - 0.6, c4, rider, [(c3 - 0.6, (360, 2230, 2.25)), (c4, (370, 2160, 2.5))], key='rider', xin=0.6, xout=0.0, hand=0.5))
    # 5. hard years: the open desert; black on the burial
    bur = Wd('x2', 'buried') - 0.55
    sh.append(Shot('hard', c4, bur, srch, [(c4, (820, 1900, 1.15)), (bur, (800, 1980, 1.3))], key='srch', hand=0.5, **CUT))
    c5 = S0('x3') - 0.2
    sh.append(Shot('black_bury', bur, c5, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, **CUT))
    # 6. not every family: the camp from afar
    c6 = S0('s1') - 0.4
    sh.append(Shot('not_every', c5, c6, far, [(c5, (1050, 2160, 1.7)), (c6, (1080, 2180, 1.85))], key='far', xin=0.0, xout=0.6, hand=0.4))
    # 7. the search; two tents
    tents_t = Wd('s1', 'late') - 0.2
    sh.append(Shot('search', c6 - 0.5, tents_t, srch_r, [(c6 - 0.5, (330, 2280, 2.15)), (tents_t, (420, 2260, 2.3))], key='srch_r', xin=0.6, xout=0.0, hand=0.6))
    c7 = S0('s2') - 0.15
    sh.append(Shot('two_tents', tents_t, c7, far, [(tents_t, (900, 2050, 1.25)), (c7, (980, 2120, 1.55))], key='far', hand=0.4, **CUT))
    # 8. the old man; your camels
    cm = Wd('s2', 'their') - 0.2
    sh.append(Shot('old_tent', c7, cm, tents, [(c7, (930, 2100, 2.0)), (cm, (950, 2090, 2.2))], key='tents', hand=0.5, **CUT))
    c8 = S0('s3') - 0.15
    sh.append(Shot('milk', cm, c8, she, [(cm, (130, 2290, 2.3)), (c8, (150, 2260, 2.45))], key='she', hand=0.5, **CUT))
    # 9. the birth: the fire and the women
    c9 = S0('s4') - 0.15
    sh.append(Shot('birth', c8, c9, fire, [(c8, (1090, 2160, 2.65)), (c9, (1100, 2130, 2.9))], key='fire', hand=0.4, **CUT))
    # 10. boy or girl: the tent, close and tilted
    c10 = S0('s5') - 0.2
    sh.append(Shot('boy_girl', c9, c10, tents, [(c9, (1050, 2120, 2.35)), (c10, (1080, 2140, 2.6))], key='tents', hand=0.6, roll=-3.0, **CUT))
    # 11. "It was a girl." the fire, very close, still
    c11 = S0('b1') - 0.25
    sh.append(Shot('girl', c10, c11, fire, [(c10, (1100, 2170, 3.0)), (c11, (1102, 2180, 3.2))], key='fire', hand=0.2, **CUT))
    # 12. he asks to buy her; the old man; the answer
    ins = Wd('b1', 'insulted') - 0.3
    sh.append(Shot('ask', c11, ins, rider, [(c11, (380, 2200, 2.3)), (ins, (390, 2180, 2.45))], key='rider', hand=0.5, **CUT))
    c12 = S0('b2') - 0.15
    sh.append(Shot('insulted', ins, c12, tents, [(ins, (870, 2110, 2.4)), (c12, (880, 2100, 2.55))], key='tents', hand=0.5, **CUT))
    life = Wd('b2', 'life') - 0.35
    sh.append(Shot('answer', c12, life, rider, [(c12, (380, 2230, 2.35)), (life, (375, 2190, 2.75))], key='rider', hand=0.4, **CUT))
    c13 = S0('b3') - 0.2
    sh.append(Shot('her_life', life, c13, fire, [(life, (1095, 2150, 2.8)), (c13, (1100, 2140, 3.05))], key='fire', hand=0.3, xin=0.0, xout=0.0))
    # 13. the price
    ride = Wd('b3', 'riding') - 0.6
    sh.append(Shot('price', c13, ride, she, [(c13, (110, 2300, 2.3)), (ride, (160, 2270, 2.45))], key='she', hand=0.5, **CUT))
    c14 = S0('v1') - 0.4
    sh.append(Shot('mount', ride, c14, rider, [(ride, (390, 2260, 2.2)), (c14, (380, 2300, 2.3))], key='rider', hand=0.5, xin=0.0, xout=0.6))
    # 14. he walks home at dawn; the promise
    pr = Wd('v1', 'promise') - 0.3
    sh.append(Shot('dawn', c14 - 0.4, pr, dawn_w, [(c14 - 0.4, (820, 2100, 1.1)), (pr, (780, 2160, 1.22))], key='dawn_w', xin=0.7, xout=0.0, hand=0.4))
    c15 = S0('v2') - 0.3
    sh.append(Shot('vow', pr, c15, dawn_c, [(pr, (700, 2330, 2.05)), (c15, (690, 2300, 2.25))], key='dawn_c', hand=0.5, xin=0.0, xout=0.5))
    # 15. the old records disagree; every number was a girl (the daughters of the bier)
    ev = S0('v2') + (E0('v2') - S0('v2')) * 0.82
    evn = Wd('v2', 'every') - 0.3
    sh.append(Shot('records', c15, evn, cellk('records'),
                   pkeys((c15, doc(2.8)), (Wd('v2', 'ninety-six'), pen('records', Wd('v2', 'ninety-six') + 0.4, 20, 0, 2.55)),
                         (evn, pen('records', Wd('v2', 'four') + 0.6, 20, 20, 2.63))), key='cell_rec', ap=9.0, xin=0.0, xout=0.0))
    c16 = S0('z1') - 0.4
    sh.append(Shot('daughters', evn, c16, sky, [(evn, (1060, 720, 1.85)), (c16, (1050, 640, 2.0))], key='sky', hand=0.3, xin=0.0, xout=0.6))
    # 16. Zayd, in Mecca
    c17 = S0('z2') - 0.2
    sh.append(Shot('mecca', c16 - 0.4, c17, mec, [(c16 - 0.4, (820, 1900, 1.1)), (c17, (840, 2050, 1.3))], key='mec', xin=0.6, xout=0.0, hand=0.5))
    dk = Wd('z2', 'do') - 0.25
    sh.append(Shot('father', c17, dk, mec_f, [(c17, (1240, 2280, 2.0)), (dk, (1235, 2250, 2.15))], key='mec_f', hand=0.5, **CUT))
    c18 = S0('z3') - 0.15
    sh.append(Shot('zayd', dk, c18, mec_z, [(dk, (725, 2200, 2.0)), (c18, (720, 2150, 2.3))], key='mec_z', hand=0.4, **CUT))
    c19 = S0('g1') - 0.4
    sh.append(Shot('grown', c18, c19, mec, [(c18, (840, 2100, 1.4)), (c19, (820, 2000, 1.2))], key='mec', hand=0.4, xin=0.0, xout=0.6))
    # 17. the grandson's verse
    c20 = S0('f1') - 0.4
    ol = Wd('g1', 'one') - 0.3
    sh.append(Shot('years', c19 - 0.4, ol, dawn_w, [(c19 - 0.4, (760, 1900, 1.15)), (ol, (800, 1700, 1.05))], key='dawn_w', xin=0.6, xout=0.0, hand=0.4))
    sh.append(Shot('poem', ol, c20, cellk('poem'),
                   pkeys((ol, doc(2.72)), (S0('g2'), pen('poem', S0('g2') + 0.3, 20, 10, 2.55)), (c20, pen('poem', E0('g2'), 20, 20, 2.89))),
                   key='cell_poem', ap=9.0, xin=0.0, xout=0.0))
    # 18. somewhere in that desert a girl grew up; the camp under the stars; the end
    gr = Wd('f1', 'because') - 0.3
    sh.append(Shot('grew_up', c20, gr, fire, [(c20, (1080, 2140, 2.7)), (gr, (1095, 2160, 2.9))], key='fire', hand=0.3, **CUT))
    endt = E0('f1') + 1.6
    sh.append(Shot('camels_end', gr, endt, camp_w, [(gr, (500, 2200, 1.35)), (endt, (820, 1300, 1.08))], key='camp_w', hand=0.4, xin=0.0, xout=0.9))
    sh.append(Shot('endcard', E0('f1') + 1.0, K.TOTAL, lambda: Black(), [(0, (810, 1440, 1.0))], key='black', hand=0.0, xin=0.5, xout=0.0))
    return sh


def labels():
    V = K.V
    return [
        (0.5, V['o1'][1] + 0.3, ['ARABIA', 'about 600'], 330, 40, CINZEL),
        (V['x1'][0] - 0.1, V['x1'][1] + 0.4, ["SA'SA'A IBN NAJIYA", 'of the Tamim tribe'], 330, 38, CINZEL),
        (V['b2'][0] - 0.1, V['b2'][1] + 0.3, ['WHAT HE SAID', 'as the old records tell it'], 330, 36, CINZEL),
        (V['v2'][0] - 0.2, V['v2'][1] + 0.3, ['THE OLD RECORDS', 'written down centuries later'], 330, 36, CINZEL),
        (V['z1'][0] - 0.1, V['z1'][1] + 0.5, ['ZAYD IBN AMR', 'Mecca'], 330, 40, CINZEL),
        (V['g1'][0] - 0.2, V['g2'][1] + 0.4, ['AL-FARAZDAQ', 'his grandson, a poet'], 330, 38, CINZEL),
    ]


END = [(["Sa'sa'a ibn Najiya", 'Arabia, about 600'], ITAL, 50, (0.92, 0.89, 0.82), 980),
       (['These accounts were written down', 'generations later. Their numbers differ.'], ITAL, 38, (0.86, 0.83, 0.76), 1140),
       (['Sources: al-Tabarani; The Book of Songs;', 'Paraskeva (2021); Lindstedt (2023).'], ROMAN, 30, (0.72, 0.69, 0.64), 1320)]

GAP = dict(o1=0.6, o2=0.5, o3=0.5, x1=3.0, x2=0.6, x3=0.8, s1=1.1, s2=0.6, s3=0.6, s4=0.6, s5=0.6, b1=1.0, b2=0.5, b3=0.7,
           v1=0.9, v2=0.8, z1=1.2, z2=0.6, z3=0.6, g1=1.1, g2=0.5, f1=1.2)

K.configure('arabia', 'direct_arabia', os.environ.get('VO_DIR', ROOT + '/film/vo_arabia'), gap=GAP,
            title=('DARK CORNERS', ['I Am Buying', 'Her Life']), end=END, labels=labels, build=build, pages=pages)
TOTAL, NF, V = K.TOTAL, K.NF, K.V

if __name__ == '__main__':
    K.main(sys.argv)
