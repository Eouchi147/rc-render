"""Voice D for the Dark Corners series (Sam's pick, 8 Oct 2026): Kokoro af_nicole, soft and close, directed line by line
with a somber, empathetic set of directions. Writes vo/<id>.wav (48 kHz mono, dry) and vo/timing.json."""
from darkroot import ROOT
import sys, os, re, json
sys.path.insert(0, ROOT + '/voice')
import numpy as np, soundfile as sf
import voices as VO
from script_bamberg import LINES, LEX_ADD
VO.LEX.update(LEX_ADD)
SR = VO.SR
VOICE = 'af_nicole'

# The narrator's emotional range for this series: never bright, never theatrical. Register is low, the melody narrow,
# and the pace slows where the story hurts. reg: semitones, rng: melody width, tempo: rate, final: how a line lands.
VO.DIRECTION.update({
    "s_hush":    {"reg": -0.9, "rng": 1.22, "tempo": 0.93, "final": "fall", "gain": -0.5, "decl": 0.9},     # the cold open: a secret
    "s_calm":    {"reg": -0.8, "rng": 1.12, "tempo": 0.95, "final": "fall", "gain": 0.0, "decl": 0.8},      # plain telling, sober
    "s_grief":   {"reg": -0.7, "rng": 1.28, "tempo": 0.88, "final": "fall", "gain": -0.8, "decl": 1.0},     # his words, tender
    "s_dread":   {"reg": -1.2, "rng": 1.08, "tempo": 0.92, "final": "suspend", "gain": -1.0, "decl": 0.4},  # something is coming
    "s_cold":    {"reg": -1.0, "rng": 0.92, "tempo": 0.97, "final": "fall", "gain": 0.0, "decl": 0.3},      # the court record: flat
    "s_pain":    {"reg": -0.6, "rng": 1.32, "tempo": 0.88, "final": "fall", "gain": 0.3, "decl": 1.0},      # his letter on the torture
    "s_break":   {"reg": -1.0, "rng": 1.2, "tempo": 0.84, "final": "fall", "gain": -1.2, "decl": 1.2},      # the voice nearly gives way
    "s_turn":    {"reg": -0.6, "rng": 1.3, "tempo": 0.93, "final": "fall", "gain": 0.4, "decl": 1.0},       # the turn of the story
    "s_build":   {"reg": -0.5, "rng": 1.2, "tempo": 0.97, "final": "fall", "gain": 0.2, "decl": 0.6},       # the chain, the streets
    "s_verdict": {"reg": -1.3, "rng": 1.05, "tempo": 0.9, "final": "fall", "gain": 0.0, "decl": 1.1},      # the end of a movement
})
DIR = {
    'h1': 's_hush', 'h2': 's_hush', 'h3': 's_hush', 'h4': 's_calm', 'q1': 's_grief', 'q2': 's_pain',
    'w1': 's_calm', 'w2': 's_calm', 'w3': 's_build', 'w4': 's_grief', 'w5': 's_dread',
    'j1': 's_calm', 'j2': 's_turn',
    't1': 's_dread', 't2': 's_cold', 't3': 's_pain', 't4': 's_cold', 't5': 's_pain', 't6': 's_break',
    'p1': 's_calm', 'p2': 's_pain',
    'l1': 's_turn', 'l2': 's_turn', 'l3': 's_cold', 'l4': 's_dread', 'l5': 's_build', 'l6': 's_build', 'l7': 's_verdict',
    'e1': 's_calm', 'e2': 's_grief', 'e3': 's_break',
    'c1': 's_verdict', 'c2': 's_turn', 'c3': 's_verdict',
}
PACE = 1.05          # af_nicole is slow by nature: a touch quicker keeps the film under 3:00

if __name__ == '__main__':
    os.makedirs(ROOT + '/film/vo', exist_ok=True)
    k = VO.Kokoro(VOICE, ROOT + '/film/vo/cache_d', intone='directed')
    only = set(sys.argv[1:])
    tp = ROOT + '/film/vo/timing.json'
    out = json.load(open(tp)) if (only and os.path.exists(tp)) else {}
    for lid, text, d, sp, q in LINES:
        if only and lid not in only:
            continue
        words = text.split()
        sents, cur = [], []
        for w in words:
            cur.append(w)
            if re.search(r"[.?!:]['\"’”)]*$", w):
                sents.append(cur); cur = []
        if cur:
            sents.append(cur)
        plan = [(s, sp * PACE, DIR.get(lid, 's_calm'), {}) for s in sents]
        takes = k.say_line(plan)
        parts, spans, t = [], [], 0.0
        for (seg, loc, extra), s in zip(takes, sents):
            parts.append(seg)
            for (a, b), w in zip(loc, s):
                spans.append([w, round(t + a, 3), round(t + b, 3)])
            t += len(seg) / SR
            if extra > 0:
                parts.append(np.zeros(int(extra * SR), np.float32)); t += extra
        a = np.concatenate(parts).astype(np.float32)
        sf.write(f'{ROOT}/film/vo/{lid}.wav', a, SR)
        out[lid] = {"dur": round(len(a) / SR, 3), "words": spans, "q": q}
        print(lid, round(len(a) / SR, 2), flush=True)
    json.dump(out, open(tp, 'w'), indent=1)
    print('total speech', round(sum(v['dur'] for v in out.values()), 1))
