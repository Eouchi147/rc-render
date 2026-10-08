"""Chatterbox job list for the keeper's directed reading (direct_bamberg.py): every phrase, five takes, plus alternate
spellings for phrases the voice tends to garble. The best take per phrase is chosen afterwards (voice2_build.py).
    python perf_bamberg.py ../../voice2/jobs.json [line ids] [release]"""
import sys, json
from direct_bamberg import DIRECTED, DELIVERY, SAY, ALT
from script_bamberg import LINES

VOICE, REF = 'N', 'ref_m_deep.wav'          # keeper voice 4 (Sam, 8 Oct 2026)
SEEDS = (3, 11, 29, 47, 61)
VOICES = {VOICE: REF}


def plan():
    P = []
    quote = {l[0]: l[4] for l in LINES}
    for lid, _, *_ in LINES:
        for k, (text, dlv, hold, lands) in enumerate(DIRECTED[lid]):
            P.append(dict(line=lid, k=k, text=SAY.get(text, text), check=text, style=dlv, hold=hold, lands=lands, quote=quote[lid],
                          alts=ALT.get(text, [SAY.get(text, text)])))
    return P


if __name__ == '__main__':
    P = plan()
    if len(sys.argv) > 2 and sys.argv[2]:
        sub = set(sys.argv[2].split(','))
        P = [p for p in P if p['line'] in sub]
    takes = []
    for p in P:
        ex, cfg, temp = DELIVERY[p['style']]
        for a, txt in enumerate(p['alts']):
            for sd in SEEDS:
                takes.append(dict(out=f"{VOICE}_{p['line']}_{p['k']}_{sd}" + (f"_a{a}" if a else ''), text=txt, check=p['check'],
                                  ref=REF, ex=ex, cfg=cfg, temp=temp, seed=sd))
    rel = sys.argv[3] if len(sys.argv) > 3 else 'voice2-keeper-bamberg'
    json.dump(dict(release=rel, takes=takes), open(sys.argv[1], 'w'), indent=0)
    print(len(P), 'phrases', len(takes), 'takes')
