"""The sound of the Zong film: narration (voice 4), the sea (synthesised; the CC0 library has no surf), rain and wind,
timber, chain and rope (BigSoundBank CC0), the quill on the documents, and a sampled string score in D minor.
    python mix_zong.py out.wav"""
from darkroot import ROOT
import sys
sys.path.insert(0, ROOT + '/film')
import numpy as np
import pedalboard as pb
import film_zong as F
import film_kit as K
from mix_kit import *
import mix_kit as MK


def main(out):
    N = MK.setup(K.TOTAL)
    V, S = K.V, K.S
    shots = K.shots()
    sh = {s.name: s for s in shots}
    fxb = np.zeros(N, np.float32); ambL = np.zeros(N, np.float32); ambR = np.zeros(N, np.float32)
    mus = np.zeros(N, np.float32); vo = np.zeros(N, np.float32)
    dur = N / SR
    W_ = K.Wd

    def amb(x, env, g, off=7):
        nonlocal ambL, ambR
        ambL += x * env * db(g); ambR += np.roll(x, off * SR) * env * db(g)

    # ---------------------------------------------------------------- beds
    calm = MK.env_of(shots, {'title_sea', 'dusk_ship', 'bow', 'stern_care', 'deck', 'deck_wide', 'jamaica', 'jamaica_past', 'night_falls',
                             'rule_sick', 'decided', 'night_far', 'rope', 'black_river', 'equiano', 'never', 'campaign', 'care_end'})
    stormy = MK.env_of(shots, {'open', 'rain', 'rain_deck', 'kept_going', 'chained', 'the_sea'})
    black = MK.env_of(shots, {'black_54'})
    docs = MK.env_of(shots, {'court_open', 'ledger', 'rule', 'rule_paid', 'claim', 'verdict', 'goods', 'sharp', 'judgment', 'price'})
    s1 = sea(dur, 1, swell=0.09, rough=0.6)
    amb(s1, calm, -19)
    amb(lp(s1, 400), black, -21)
    s2 = sea(dur, 2, swell=0.16, rough=1.6)
    amb(s2, stormy, -14, off=5)
    rain = loop(fx('rain_thunder_1'), dur)
    amb(hp(rain, 100), stormy, -17, off=11)
    wind = loop(fx('strong_wind_1'), dur)
    amb(lp(wind, 3500), stormy, -23, off=9)
    amb(lp(loop(fx('wind_whistle_1'), dur), 2500), np.maximum(calm * 0.6, black), -31, off=4)
    room = lp(loop(fx('wind_inside_2'), dur), 800)
    amb(room, docs, -30)
    amb(lp(hp(loop(fx('rain_concrete'), dur), 150), 1200), docs, -34, off=13)
    fxb += hp(loop(fx('candle_sparkle_1'), dur), 250) * docs * db(-30)
    # timber creaks on the ship shots
    deckenv = MK.env_of(shots, {'deck', 'deck_wide', 'stern_care', 'bow', 'decided', 'rule_sick', 'rain_deck', 'chained', 'rope'})
    cr = np.zeros(N, np.float32)
    names = ['creaking_door_1', 'creaking_door_2', 'creaking_door_4', 'long_creak_door', 'wood_vibr']
    t = 8.0; k = 0
    while t < dur - 3:
        place(cr, lp(onset(fx(names[k % len(names)])), 1500), t, -8 - 3 * (k % 3), fi=0.2, fo=0.8, length=2.2)
        t += 3.1 + 1.7 * ((k * 7) % 5) / 5; k += 1
    fxb += cr * deckenv * db(-12)
    # ---------------------------------------------------------------- the quill on the documents
    P = K.pages_for_film()
    scr = MK.scratch()
    e = np.zeros(N, np.float32)
    for page, names_ in (('ledger', ('ledger',)), ('court', ('verdict', 'goods')), ('sharp', ('sharp',)), ('kb', ('judgment',))):
        for nm in names_:
            e += MK.pen_env(P[page], sh[nm].t0, sh[nm].t1)
    fxb += scr * e * db(-14)
    # ---------------------------------------------------------------- events
    th = lp(fx('thunder_4'), 1400)
    place(ambL, th, 0.3, -10, fo=3.0, length=8.0); place(ambR, th, 0.34, -11, fo=3.0, length=8.0)
    place(fxb, onset(fx('whoosh_6')), sh['court_open'].t0 - 0.25, -22, length=0.6, fo=0.2)
    place(fxb, fx('page_turned'), sh['ledger'].t0 + 0.05, -24, length=1.6)
    place(fxb, fx('page_turned'), sh['claim'].t0 + 0.05, -25, length=1.6)
    place(fxb, onset(fx('heartbeat_4')), sh['black_54'].t0 + 0.4, -21, fi=0.3, fo=1.2, length=max(sh['black_54'].t1 - sh['black_54'].t0, 1.0))
    place(fxb, lp(onset(fx('heavy_chain')), 2500), sh['black_54'].t0 + 0.2, -22, fo=1.0, length=2.5)
    rained = W_('r1', 'rained')
    t8 = lp(fx('thunder_8'), 1600)
    place(ambL, t8, rained - 0.02, -10, fo=3.0, length=7.0); place(ambR, t8, rained, -11, fo=3.0, length=7.0)
    place(ambL, hp(loop(fx('rain_thunder_2'), 6.0), 200), rained, -15, fi=0.4, fo=2.0, length=6.0)
    place(fxb, lp(onset(fx('chain_med_1')), 4000), W_('r3', 'chained') - 0.1, -15, length=1.6, fo=0.4)
    place(fxb, lp(onset(fx('handcuffs_4')), 3500), W_('r3', 'chained') + 0.5, -20, length=1.2, fo=0.4)
    place(fxb, lp(splash(3, 0.8), 1800), W_('r3', 'jumped') + 0.25, -20, length=1.4, fo=0.6)
    place(fxb, lp(onset(fx('rope_big')), 3500), W_('p1', 'rope') - 0.1, -17, fi=0.1, length=2.0, fo=0.5)
    place(fxb, lp(onset(fx('rope_slide_1')), 4000), W_('p1', 'climbed'), -19, length=1.6, fo=0.5)
    place(fxb, onset(fx('book_closed_2')), sh['price'].t1 - 0.6, -17, length=1.5, fo=0.5)
    place(fxb, onset(fx('door_knock')), sh['equiano'].t1 - 0.5, -22, length=1.6, fo=0.4)
    place(ambL, lp(onset(fx('church_bell_1')), 2200), V['f3'][1] + 1.1, -24, fo=2.0, length=max(K.TOTAL - V['f3'][1] - 1.1, 1.0))
    fxb = pb.Pedalboard([pb.Reverb(room_size=0.3, damping=0.6, wet_level=0.16, dry_level=0.9, width=0.6)])(fxb, SR)

    # ---------------------------------------------------------------- score (D minor)
    def hold(kind, n, t0, t1, g, fi=3.0, fo=2.5):
        place(mus, held(note(kind, n), max(t1 - t0, 1.5)), t0, g, fi=fi, fo=fo)
    hold('cb', 'D1', 0.2, V['o3'][1] + 3.0, -14, fi=2.0)
    hold('cello', 'D2', V['o2'][0] - 0.5, V['x1'][0] + 1.0, -15)
    hold('vla', 'D3', V['o3'][1] + 0.2, V['x1'][0] + 1.5, -19, fi=1.0)
    hold('vln', 'A3', V['o3'][1] + 0.4, V['x1'][0] + 1.2, -22, fi=1.0)
    hold('cello', 'F2', V['x1'][0] - 0.5, V['x4'][1] + 1.0, -19)
    hold('cb', 'D1', V['m1'][0], V['m3'][1] + 1.0, -17)
    hold('cello', 'A2', V['m2'][0], V['m3'][1] + 1.5, -19)
    hold('vln', 'D5', V['m3'][0], V['m3'][1] + 1.0, -30, fi=2.0, fo=1.0)
    hold('cb', 'A#0', V['d1'][0] - 1.0, V['d3'][1] + 1.0, -13, fi=2.5, fo=1.5)
    hold('cello', 'A2', V['d1'][0], V['d3'][1] + 1.0, -21, fi=3.0, fo=1.5)
    place(mus, held(note('trem', 'D'), max(V['r3'][1] - V['r1'][0] + 1.0, 1.5)), V['r1'][0] - 0.5, -24, fi=1.5, fo=1.0)
    hold('cb', 'D1', V['r2'][0] - 0.5, V['r3'][1] + 1.5, -14)
    hold('vla', 'D3', V['p1'][0] - 0.8, V['a1'][1] + 1.5, -21)
    hold('cello', 'D2', V['a1'][0] - 0.5, V['c3'][1] + 1.0, -18)
    hold('cb', 'D1', V['c2'][0] - 0.5, V['c3'][1] + 1.0, -16)
    hold('cello', 'F2', V['e1'][0] - 1.0, V['e2'][1] + 2.0, -17)
    hold('vla', 'A3', V['e2'][0], V['j1'][1] + 1.0, -21)
    hold('cello', 'D2', V['j1'][0] - 1.0, V['j2'][1] + 2.0, -16)
    hold('vln', 'A3', V['j2'][0] - 0.3, V['f1'][1] + 2.0, -20)
    hold('cb', 'D1', V['f1'][0] - 1.5, K.TOTAL, -15, fo=2.0)
    hold('cello', 'D2', V['f2'][0], K.TOTAL, -17, fo=2.0)
    hold('vla', 'A3', V['f3'][0], K.TOTAL, -20, fo=2.0)
    hold('vln', 'D5', V['f3'][0] + 1.0, K.TOTAL, -24, fo=2.0)
    # ---------------------------------------------------------------- narration
    for lid in K.ORDER:
        x = load(K.C['vo'] + lid + '.wav')
        kind = 'letter' if K.QUOTE[lid] else 'narr'
        place(vo, voice_chain(kind, x), S[lid], 0.0)
    master(out, vo, fxb, ambL, ambR, mus)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT + '/out/zong.wav')
