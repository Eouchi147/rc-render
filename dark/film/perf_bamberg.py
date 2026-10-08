"""The narrator's performance of the Bamberg script: each sentence with its emotion (Chatterbox exaggeration), pace
(cfg weight: lower is slower and more deliberate) and the pause after it. Writes the Chatterbox job list.
    python perf_bamberg.py ../../voice2/jobs.json"""
import sys, re, json
from script_bamberg import LINES

# direction: (exaggeration, cfg weight, temperature)
STYLE = {      # the keeper: fascinated, a touch wry, bold. Lower cfg = slower, more deliberate
    's_hook': (0.58, 0.30, 0.72), 's_wry': (0.50, 0.33, 0.72),
    's_hush': (0.45, 0.25, 0.70), 's_calm': (0.40, 0.30, 0.70), 's_grief': (0.55, 0.22, 0.72),
    's_dread': (0.50, 0.22, 0.70), 's_cold': (0.30, 0.35, 0.65), 's_pain': (0.62, 0.20, 0.75),
    's_break': (0.70, 0.18, 0.75), 's_turn': (0.50, 0.25, 0.70), 's_build': (0.45, 0.30, 0.70), 's_verdict': (0.45, 0.20, 0.68),
}
DIR = {
    'h1': 's_hook', 'h2': 's_hook', 'h3': 's_hook', 'h4': 's_calm', 'c4': 's_hook', 'q1': 's_grief', 'q2': 's_pain',
    'w1': 's_calm', 'w2': 's_calm', 'w3': 's_build', 'w4': 's_grief', 'w5': 's_dread',
    'j1': 's_calm', 'j2': 's_turn',
    't1': 's_dread', 't2': 's_cold', 't3': 's_pain', 't4': 's_cold', 't5': 's_pain', 't6': 's_break',
    'p1': 's_wry', 'p2': 's_pain',
    'l1': 's_turn', 'l2': 's_turn', 'l3': 's_cold', 'l4': 's_dread', 'l5': 's_build', 'l6': 's_build', 'l7': 's_verdict',
    'e1': 's_calm', 'e2': 's_grief', 'e3': 's_break',
    'c1': 's_verdict', 'c2': 's_wry', 'c3': 's_verdict',
}
# pauses after a sentence (seconds), where the story holds its breath; default 0.35
HOLD = {('h1', 0): 0.45, ('h3', 0): 0.3, ('j2', 2): 0.35, ('c4', 0): 0.45, ('c4', 1): 0.4, ('h4', 0): 0.55, ('q2', 0): 0.45, ('q2', 1): 0.5, ('w1', 0): 0.4, ('w1', 1): 0.3, ('w4', 0): 0.6,
        ('j2', 0): 0.7, ('t1', 0): 0.6, ('t5', 0): 0.75, ('p2', 0): 0.5, ('l2', 0): 0.45, ('l2', 1): 0.6,
        ('l3', 0): 0.45, ('l6', 0): 0.55, ('l7', 0): 0.5, ('e1', 0): 0.35, ('e3', 0): 0.8, ('c2', 0): 0.5}
# per-sentence overrides of the style (a sentence inside a line that needs a different colour)
OVR = {('t2', 0): 's_turn', ('t5', 1): 's_break', ('j2', 3): 's_wry', ('c3', 0): 's_calm', ('c2', 0): 's_hook'}
SAY = {'Fifty-five.': 'Fifty five.'}     # what the voice is given, where the written form reads badly
VOICES = {'F': 'ref_brit.wav', 'G': 'ref_brit_slow.wav', 'M': 'ref_m_brit.wav', 'N': 'ref_m_deep.wav'}
SEEDS = (3, 11, 29)


def sentences(text):
    out, cur = [], []
    for w in text.split():
        cur.append(w)
        if re.search(r"[.?!:]['\"’”)]*$", w):
            out.append(' '.join(cur)); cur = []
    if cur:
        out.append(' '.join(cur))
    # a colon that introduces a quotation stays with what follows when the lead-in is short
    merged = []
    for s in out:
        if merged and merged[-1].endswith(':') and len(merged[-1].split()) <= 3:
            merged[-1] += ' ' + s
        else:
            merged.append(s)
    return merged


def plan():
    P = []
    for lid, text, d, sp, q in LINES:
        for k, s in enumerate(sentences(text)):
            st = OVR.get((lid, k), DIR[lid])
            P.append(dict(line=lid, k=k, text=SAY.get(s, s), check=s, style=st, hold=HOLD.get((lid, k), 0.35), quote=q))
    return P


if __name__ == '__main__':
    P = plan()
    sub = set(sys.argv[2].split(',')) if len(sys.argv) > 2 else None
    if sub:
        P = [p for p in P if p['line'] in sub]
    takes = []
    for v, ref in VOICES.items():
        for p in P:
            ex, cfg, temp = STYLE[p['style']]
            for sd in SEEDS:
                takes.append(dict(out=f"{v}_{p['line']}_{p['k']}_{sd}", text=p['text'], check=p['check'], ref=ref, ex=ex, cfg=cfg, temp=temp, seed=sd))
    json.dump(dict(release=sys.argv[3] if len(sys.argv) > 3 else 'voice2-bamberg-r3', takes=takes), open(sys.argv[1], 'w'), indent=0)
    json.dump(P, open(sys.argv[1].replace('jobs.json', 'perf_bamberg.json'), 'w'), indent=1)
    print(len(P), 'sentences', len(takes), 'takes')
