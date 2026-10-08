"""Chatterbox job list for the keeper's directed reading (direct_bamberg.py). Recording units: phrases, except that a
phrase under four words is recorded joined to its neighbour (the voice garbles very short phrases on their own); the
unit is cut back into its phrases at the silences afterwards (voice2_build.py), with the directed pauses.
    python perf_bamberg.py ../../voice2/jobs.json [line ids] [release]"""
import sys, os, json, importlib
_D = importlib.import_module(os.environ.get('DIRECT', 'direct_bamberg'))
DIRECTED, DELIVERY, SAY = _D.DIRECTED, _D.DELIVERY, _D.SAY
LINES = getattr(_D, 'LINES', None) or importlib.import_module('script_bamberg').LINES

VOICE, REF = 'N', 'ref_m_deep.wav'          # keeper voice 4 (Sam, 8 Oct 2026)
SEEDS = (3, 11, 29, 47, 61)
HOLD_SCALE = float(os.environ.get('HOLD_SCALE', '0.75'))                           # the marked pauses, scaled to fit the film under three minutes


def nwords(t):
    return len(t.replace('-', ' ').split())


def units(lid):
    ph = [dict(text=t, style=d, hold=h * HOLD_SCALE, lands=l) for t, d, h, l in DIRECTED[lid]]
    U = [[p] for p in ph]
    changed = True
    while changed and len(U) > 1:
        changed = False
        for i, u in enumerate(U):
            if sum(nwords(p['text']) for p in u) < 4:
                j = i + 1 if i + 1 < len(U) else i - 1
                a, b = min(i, j), max(i, j)
                U[a:b + 1] = [U[a] + U[b]]
                changed = True
                break
    return U


def plan():
    P = []
    quote = {l[0]: l[4] for l in LINES}
    for lid, *_ in LINES:
        for k, u in enumerate(units(lid)):
            text = ' '.join(p['text'] for p in u)
            say = ' '.join(SAY.get(p['text'], p['text']) for p in u)
            P.append(dict(line=lid, k=k, text=say, check=text, style=u[0]['style'], phrases=u, hold=u[-1]['hold'],
                          lands=u[-1]['lands'], quote=quote[lid]))
    return P


if __name__ == '__main__':
    P = plan()
    if len(sys.argv) > 2 and sys.argv[2]:
        sub = set(sys.argv[2].split(','))
        P = [p for p in P if p['line'] in sub]
    takes = []
    for p in P:
        ex, cfg, temp = DELIVERY[p['style']]
        for sd in SEEDS:
            takes.append(dict(out=f"{VOICE}_{p['line']}_{p['k']}_{sd}", text=p['text'], check=p['check'], ref=REF, ex=ex, cfg=cfg,
                              temp=temp, seed=sd))
    rel = sys.argv[3] if len(sys.argv) > 3 else 'voice2-keeper-bamberg2'
    json.dump(dict(release=rel, takes=takes), open(sys.argv[1], 'w'), indent=0)
    print(len(P), 'units', len(takes), 'takes', sum(len(p['phrases']) for p in P), 'phrases')
