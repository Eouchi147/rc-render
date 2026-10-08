"""The sound of the Kleidion film: narration (voice 4), the column on the road (shuffling steps, crows, wind), the pass
in summer (wind, impacts on the wall), the gorge, the fortress at night (fire, water, a heartbeat), the quill on the two
chronicles, and a sampled string score.
    python mix_kleidion.py out.wav"""
from darkroot import ROOT
import sys
sys.path.insert(0, ROOT + '/film')
import numpy as np
import pedalboard as pb
import film_kleidion as F
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
    road = MK.env_of(shots, {'open', 'leader_open', 'hundreds', 'one_eye', 'home', 'historians', 'as_they_say'})
    dusk = MK.env_of(shots, {'title', 'samuel', 'away', 'among_dead', 'nickname', 'sees', 'collapse'})
    summer = MK.env_of(shots, {'basil', 'summer', 'the_wall', 'the_key', 'attack', 'held', 'flank', 'behind', 'panic', 'captured', 'nearly', 'fought_on'})
    battle = MK.env_of(shots, {'attack', 'panic', 'captured', 'nearly'})
    gorge = MK.env_of(shots, {'gorge', 'ambush'})
    night = MK.env_of(shots, {'water', 'dead'})
    docs = MK.env_of(shots, {'skylitzes', 'true', 'kekaumenos'})
    wind = lp(loop(fx('strong_wind_village'), dur), 2600)
    amb(wind, np.maximum(road, dusk), -24)
    amb(lp(loop(fx('wind_plain'), dur), 3500), summer, -24, off=5)
    st = lp(loop(fx('steps_concrete'), dur), 1400)
    amb(st, road, -24, off=3)
    amb(np.roll(st, int(0.37 * SR)), road, -27, off=9)
    amb(loop(fx('crows_2'), dur), np.maximum(road, dusk) * 0.8, -31, off=13)
    amb(lp(loop(fx('cave_2'), dur), 1500), gorge, -24)
    amb(lp(loop(fx('wind_whistle_2'), dur), 2500), gorge, -28, off=4)
    amb(loop(fx('fireplace_1'), dur), night, -23, off=4)
    amb(lp(loop(fx('night_after_rain'), dur), 2500), night, -30, off=8)
    room = lp(loop(fx('wind_inside_2'), dur), 800)
    amb(room, docs, -30)
    fxb += hp(loop(fx('candle_sparkle_1'), dur), 250) * docs * db(-30)
    P = K.pages_for_film()
    scr = MK.scratch()
    e = MK.pen_env(P['sky'], sh['skylitzes'].t0, sh['skylitzes'].t1) + MK.pen_env(P['kek'], sh['kekaumenos'].t0, sh['kekaumenos'].t1)
    fxb += scr * e * db(-14)
    # battle: impacts on the wall, the rout
    for k, w in enumerate(('attacked', 'again')):
        t = W_('w2', w)
        place(fxb, lp(onset(fx('blow_1' if k == 0 else 'blow_2')), 2500), t, -12, length=1.0, fo=0.4)
        place(fxb, lp(onset(fx('anvil_1')), 3000), t + 0.12, -22, length=1.2, fo=0.5)
    place(fxb, lp(onset(fx('wood_vibr')), 2000), W_('w2', 'held'), -18, length=1.5, fo=0.5)
    tp = W_('t2', 'panicked')
    place(fxb, lp(onset(fx('blow_2')), 2200), tp, -12, length=1.0, fo=0.4)
    for k in range(5):
        place(fxb, lp(onset(fx('anvil_2' if k % 2 else 'anvil_1')), 2600 - 200 * k), tp + 0.5 + 0.55 * k, -21 - 2 * k, length=0.9, fo=0.3)
    amb(lp(loop(fx('strong_wind_1'), dur), 900), battle, -22, off=3)
    place(fxb, lp(onset(fx('body_fall_2')), 1600), W_('r1', 'trapped') + 0.3, -12, length=1.2, fo=0.4)
    place(fxb, lp(onset(fx('iron_bar_fall_2')), 1800), W_('r1', 'trapped') + 0.6, -19, length=1.5, fo=0.5)
    place(fxb, onset(fx('whoosh_6')), sh['leader_open'].t0 - 0.25, -23, length=0.6, fo=0.2)
    place(fxb, lp(onset(fx('heartbeat_5')), 1800), sh['black_blind'].t0, -20, length=max(sh['black_blind'].t1 - sh['black_blind'].t0 + 0.6, 1.0), fo=0.6)
    place(fxb, lp(onset(fx('heavy_chain')), 2400), sh['black_order'].t0 + 0.2, -22, length=2.2, fo=0.8)
    place(fxb, onset(fx('page_turned')), sh['skylitzes'].t0 + 0.05, -24, length=1.6)
    place(fxb, lp(onset(fx('body_fall_5')), 1500), W_('d1', 'collapsed') + 0.25, -15, length=1.2, fo=0.4)
    place(fxb, onset(fx('drops_1')), W_('d2', 'drank') - 0.1, -24, length=1.2, fo=0.4)
    place(fxb, lp(onset(fx('heartbeat_4')), 2200), W_('d2', 'heart') - 0.6, -19, length=3.2, fo=1.4)
    place(ambL, lp(onset(fx('church_bell_1')), 2200), V['d3'][0] + 0.2, -22, fo=3.0, length=6.0)
    place(ambR, lp(onset(fx('church_bell_1')), 2000), V['d3'][0] + 0.25, -23, fo=3.0, length=6.0)
    place(fxb, onset(fx('page_turned')), sh['kekaumenos'].t0 + 0.05, -24, length=1.6)
    place(ambL, lp(onset(fx('carrion_crow_4')), 3000), sh['as_they_say'].t0 + 0.8, -26, fo=1.0, length=3.0)
    fxb = pb.Pedalboard([pb.Reverb(room_size=0.32, damping=0.55, wet_level=0.16, dry_level=0.9, width=0.6)])(fxb, SR)

    def hold(kind, n, t0, t1, g, fi=3.0, fo=2.5):
        place(mus, held(note(kind, n), max(t1 - t0, 1.5)), t0, g, fi=fi, fo=fo)
    hold('cb', 'D1', 0.2, V['o3'][1] + 3.0, -14, fi=2.0)
    hold('cello', 'D2', V['o2'][0] - 0.5, V['x1'][0] + 1.0, -15)
    hold('vla', 'D3', V['o3'][1] + 0.2, V['x1'][0] + 1.5, -19, fi=1.0)
    hold('vln', 'A3', V['o3'][1] + 0.4, V['x1'][0] + 1.2, -22, fi=1.0)
    hold('cello', 'F2', V['x1'][0] - 0.5, V['x3'][1] + 1.0, -19)
    hold('cb', 'D1', V['w1'][0] - 0.5, V['w2'][1] + 1.0, -17)
    place(mus, held(note('trem', 'D'), max(V['t2'][1] - V['t1'][0] + 0.5, 1.5)), V['t1'][0] - 0.5, -23, fi=1.0, fo=1.0)
    hold('cb', 'A#0', V['t1'][0] - 0.5, V['s1'][1] + 1.0, -14)
    hold('cello', 'A2', V['s1'][0] - 0.3, V['r1'][1] + 1.0, -19)
    hold('cb', 'D1', V['b2'][0] - 0.3, V['b3'][1] + 1.5, -14)
    hold('cello', 'D2', V['b2'][0], V['b3'][1] + 1.5, -18)
    hold('vln', 'D5', V['b3'][0], V['b3'][1] + 1.0, -28, fi=2.0, fo=1.0)
    hold('cello', 'F2', V['d1'][0] - 0.5, V['d3'][1] + 2.0, -17)
    hold('vla', 'A3', V['d2'][0], V['d3'][1] + 2.0, -21)
    hold('cb', 'D1', V['q1'][0] - 0.5, V['q2'][1] + 1.0, -17)
    hold('cello', 'D2', V['f1'][0] - 1.0, K.TOTAL, -16, fo=2.0)
    hold('vla', 'A3', V['f2'][0] - 0.5, K.TOTAL, -20, fo=2.0)
    hold('vln', 'D5', V['f2'][0] + 0.5, K.TOTAL, -24, fo=2.0)
    for lid in K.ORDER:
        x = load(K.C['vo'] + lid + '.wav')
        place(vo, voice_chain('letter' if K.QUOTE[lid] else ('record' if lid == 'b2' else 'narr'), x), S[lid], 0.0)
    master(out, vo, fxb, ambL, ambR, mus)


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else ROOT + '/out/kleidion.wav')
