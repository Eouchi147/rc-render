"""The sound of the Arabia film: narration (voice 4), the desert night (wind, insects, a far owl), the birth fire, the
quill on the two pages, Mecca at night, and a sampled string score.
    python mix_arabia.py out.wav"""
from darkroot import ROOT
import sys
sys.path.insert(0, ROOT + '/film')
import numpy as np
import pedalboard as pb
import film_arabia as F
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
    desert = MK.env_of(shots, {'open', 'rider_open', 'title_sky', 'sasaa', 'hard', 'not_every', 'search', 'two_tents', 'old_tent', 'milk',
                               'birth', 'boy_girl', 'girl', 'ask', 'insulted', 'answer', 'her_life', 'price', 'mount', 'daughters',
                               'grew_up', 'camels_end'})
    firec = MK.env_of(shots, {'birth', 'boy_girl', 'girl', 'her_life', 'grew_up', 'old_tent', 'insulted'})
    dawnc = MK.env_of(shots, {'dawn', 'vow', 'years'})
    mecca = MK.env_of(shots, {'mecca', 'father', 'zayd', 'grown'})
    docs = MK.env_of(shots, {'records', 'poem'})
    black = MK.env_of(shots, {'black_bury'})
    wind = lp(loop(fx('wind_plain'), dur), 2200)
    amb(wind, np.maximum(desert, dawnc), -24)
    amb(lp(wind, 500), black, -26)
    night = hp(loop(fx('campaign_night_1'), dur), 1500)
    amb(night, np.maximum(desert, mecca), -30, off=11)
    fire = loop(fx('fire_branching_1'), dur)
    amb(fire, firec, -21, off=3)
    amb(lp(loop(fx('strong_wind_1'), dur), 1500), dawnc, -27, off=5)
    amb(lp(loop(fx('night_after_rain'), dur), 3000), mecca, -28, off=9)
    room = lp(loop(fx('wind_inside_2'), dur), 800)
    amb(room, docs, -30)
    fxb += hp(loop(fx('candle_sparkle_1'), dur), 250) * docs * db(-30)
    P = K.pages_for_film()
    scr = MK.scratch()
    e = MK.pen_env(P['records'], sh['records'].t0, sh['records'].t1) + MK.pen_env(P['poem'], sh['poem'].t0, sh['poem'].t1)
    fxb += scr * e * db(-14)
    # events
    place(ambL, lp(onset(fx('owl_long_eared')), 3000), 2.5, -27, fo=2.0, length=4.0)
    place(fxb, onset(fx('whoosh_6')), sh['rider_open'].t0 - 0.25, -23, length=0.6, fo=0.2)
    place(fxb, lp(onset(fx('heartbeat_5')), 2000), sh['black_bury'].t0 + 0.1, -22, fo=0.6, length=max(sh['black_bury'].t1 - sh['black_bury'].t0, 1.0))
    place(ambR, lp(onset(fx('owl_tawny')), 2600), sh['two_tents'].t0 + 0.4, -28, fo=1.5, length=3.0)
    place(fxb, onset(fx('fire_foley')), sh['birth'].t0 + 0.1, -24, length=2.0, fo=0.8)
    place(fxb, onset(fx('cloth')), sh['boy_girl'].t0 + 0.3, -24, length=1.2, fo=0.4)
    place(fxb, onset(fx('page_turned')), sh['records'].t0 + 0.05, -24, length=1.6)
    place(ambL, lp(onset(fx('old_dog_bark_3')), 2500), sh['mecca'].t0 + 1.2, -30, length=2.0, fo=0.8)
    place(fxb, onset(fx('door_plain')), sh['father'].t0 + 0.2, -26, length=1.5, fo=0.5)
    place(fxb, onset(fx('sigh_nose')), V['g2'][1] + 0.3, -32, length=1.4, fo=0.5)
    fxb = pb.Pedalboard([pb.Reverb(room_size=0.3, damping=0.6, wet_level=0.14, dry_level=0.9, width=0.6)])(fxb, SR)

    def hold(kind, n, t0, t1, g, fi=3.0, fo=2.5):
        place(mus, held(note(kind, n), max(t1 - t0, 1.5)), t0, g, fi=fi, fo=fo)
    hold('cb', 'D1', 0.2, V['o3'][1] + 3.0, -15, fi=2.0)
    hold('cello', 'D2', V['o2'][0] - 0.5, V['x1'][0] + 1.0, -16)
    hold('vla', 'A3', V['o3'][1] + 0.2, V['x1'][0] + 1.5, -20, fi=1.0)
    hold('vln', 'D5', V['o3'][1] + 0.4, V['x1'][0] + 1.2, -26, fi=1.0)
    hold('cello', 'F2', V['x1'][0] - 0.5, V['x3'][1] + 1.0, -19)
    hold('cb', 'A#0', V['x2'][0], V['x3'][1] + 1.0, -16)
    hold('vla', 'D3', V['s1'][0] - 0.5, V['s3'][1] + 1.0, -21)
    hold('cb', 'D1', V['s3'][0], V['s5'][1] + 1.0, -15)
    place(mus, held(note('trem', 'D'), max(V['s5'][1] - V['s4'][0] + 0.5, 1.5)), V['s4'][0] - 0.5, -25, fi=1.5, fo=1.0)
    hold('cello', 'A2', V['s4'][0], V['s5'][1] + 1.0, -20)
    hold('cello', 'D2', V['b1'][0] - 0.5, V['b3'][1] + 1.0, -17)
    hold('vln', 'A3', V['b2'][0], V['b2'][1] + 1.5, -20, fi=1.0)
    hold('vla', 'F3' if False else 'D3', V['v1'][0] - 0.5, V['v2'][1] + 1.0, -21)
    hold('cello', 'F2', V['v2'][0], V['v2'][1] + 1.5, -18)
    hold('cb', 'D1', V['z1'][0] - 0.5, V['z3'][1] + 1.0, -16)
    hold('vla', 'A3', V['z2'][0], V['z3'][1] + 1.0, -21)
    hold('cello', 'D2', V['g1'][0] - 1.0, K.TOTAL, -16, fo=2.0)
    hold('cb', 'D1', V['g2'][0] - 1.0, K.TOTAL, -16, fo=2.0)
    hold('vln', 'A3', V['g2'][0], K.TOTAL, -21, fo=2.0)
    hold('vln', 'D5', V['f1'][0] + 1.0, K.TOTAL, -25, fo=2.0)
    for lid in K.ORDER:
        x = load(K.C['vo'] + lid + '.wav')
        place(vo, voice_chain('letter' if K.QUOTE[lid] else 'narr', x), S[lid], 0.0)
    master(out, vo, fxb, ambL, ambR, mus)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT + '/out/arabia.wav')
