"""Phone-level pronunciation audit. Every sentence the narrator speaks is run through a universal phone recogniser
(Allosaurus) and aligned, phone by phone, with the pronunciation it should have (espeak-ng's dictionary, or our own IPA
for names). Words whose consonants go missing or change (a dropped /j/ in 'universities', 'Tepe' said 'teep') are
flagged, so a wrong sound is caught before anyone hears it."""
import os, re, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import voices as VO

FUNC = set("a an the and of in on at to by for with from as is are was were be been it its his her their our your this that these those or but so if then than into onto who what which when where how".split())
VOW = set("aeiouæɑɒɔəɚɛɜɝɪʊʌyøœɯɤɐɨʉ")
_M = [None]


def rec():
    if _M[0] is None:
        from allosaurus.app import read_recognizer
        _M[0] = read_recognizer()
    return _M[0]


def norm_ipa(s):
    s = s.replace("ˈ", "").replace("ˌ", "").replace("ː", "").replace("ɹ", "r").replace("ɾ", "t").replace("ʔ", "")
    s = s.replace("ɚ", "ər").replace("ɝ", "ɜr").replace("ᵻ", "ɪ").replace("ɐ", "ə").replace("ɡ", "g").replace("ɫ", "l")
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c in "ʰʲʷ̃ ̩͡":
            i += 1; continue
        if c == "d" and s[i + 1:i + 2] == "ʒ":
            out.append("dʒ"); i += 2; continue
        if c == "t" and s[i + 1:i + 2] == "ʃ":
            out.append("tʃ"); i += 2; continue
        if c.strip():
            out.append(c)
        i += 1
    return out


def expected(word, k):
    import heteronyms as HN
    if HN.split(word.replace("*", "")):
        return norm_ipa(HN.ipa(word.replace("*", "")))
    key = VO._key(word)
    if key in VO.LEX:
        return norm_ipa(VO.LEX[key])
    w = re.sub(r"[^\w'’\-]", "", VO._plain(word))
    if not w:
        return []
    return norm_ipa(k.tokenizer.phonemize(w, "en-us"))


def heard(a, sr=48000):
    import soundfile as sf
    from scipy.signal import resample_poly
    p = "/tmp/_phonecheck.wav"
    sf.write(p, resample_poly(a, 1, 3).astype(np.float32), 16000)
    return norm_ipa("".join(rec().recognize(p, "eng").split()))


def cost(a, b):
    if a == b:
        return 0
    va, vb = a[0] in VOW, b[0] in VOW
    if va and vb:
        return .35
    return 1.2 if va != vb else 1.0


def align(E, Hh):
    """E: [(phone, word index)], Hh: [phone]. Returns per-word (cost, n, first-consonant-kept)."""
    n, m = len(E), len(Hh)
    D = np.zeros((n + 1, m + 1)); B = np.zeros((n + 1, m + 1), int)
    for i in range(1, n + 1):
        D[i, 0] = D[i - 1, 0] + (.5 if E[i - 1][0] in VOW else 1); B[i, 0] = 1
    for j in range(1, m + 1):
        D[0, j] = D[0, j - 1] + (.5 if Hh[j - 1] in VOW else .9); B[0, j] = 2
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            e = E[i - 1][0]
            c = [D[i - 1, j - 1] + cost(e, Hh[j - 1]), D[i - 1, j] + (.5 if e in VOW else 1), D[i, j - 1] + (.5 if Hh[j - 1] in VOW else .9)]
            k = int(np.argmin(c)); D[i, j] = c[k]; B[i, j] = k
    i, j, per = n, m, {}
    got = {}
    while i > 0 or j > 0:
        k = B[i, j] if i > 0 and j > 0 else (1 if i > 0 else 2)
        if k == 0:
            w = E[i - 1][1]; per[w] = per.get(w, 0) + cost(E[i - 1][0], Hh[j - 1]); got.setdefault(w, []).insert(0, Hh[j - 1]); i -= 1; j -= 1
        elif k == 1:
            w = E[i - 1][1]; per[w] = per.get(w, 0) + (.5 if E[i - 1][0] in VOW else 1); got.setdefault(w, []).insert(0, "·"); i -= 1
        else:
            j -= 1
    return per, got


def audit(words, audio):
    k = VO.Kokoro("af_heart", "/tmp/_kc").k
    E, exp = [], {}
    for wi, w in enumerate(words):
        ph = expected(w, k); exp[wi] = ph
        E += [(p, wi) for p in ph]
    Hh = heard(audio)
    per, got = align(E, Hh)
    bad = []
    for wi, w in enumerate(words):
        ph = exp[wi]
        if len(ph) < 2:
            continue
        c = per.get(wi, 0) / len(ph)
        g = got.get(wi, [])
        first = next((p for p in ph if p not in VOW), None)
        lost_first = first is not None and ph.index(first) == 0 and (not g or g[0] != first)
        fw = VO._plain(w).lower().strip(".,;:?!…'\"")
        if (lost_first and first in ("j", "h", "w") and fw not in FUNC) or (c > .7 and len(ph) >= 4 and fw not in FUNC):
            bad.append({"word": VO._plain(w), "expected": " ".join(ph), "heard": " ".join(g), "score": round(c, 2)})
        hs = hetero_check(w, g)
        if hs:
            bad.append(hs)
    return bad


def seq_cost(a, b):
    n, m = len(a), len(b); D = np.zeros((n + 1, m + 1))
    for i in range(1, n + 1): D[i, 0] = i
    for j in range(1, m + 1): D[0, j] = j
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            D[i, j] = min(D[i - 1, j - 1] + cost(a[i - 1], b[j - 1]), D[i - 1, j] + 1, D[i, j - 1] + 1)
    return D[n, m] / max(1, n)


def hetero_check(w, got):
    """A heteronym is wrong when what was heard sits closer to another sense than to the one the script asked for."""
    import heteronyms as HN
    tok = w.replace("*", "")
    s = HN.split(tok)
    if not s:
        return None
    g = [p for p in got if p != "·"]
    sc = {k: seq_cost(norm_ipa(v), g) for k, v in HN.senses_ipa(tok).items()}
    want = s[1]
    best = min(sc, key=sc.get)
    if best != want and sc[best] + .05 < sc[want]:
        return {"word": s[0], "heteronym": True, "wanted": want, "heard_as": best, "heard": " ".join(got), "scores": {k: round(v, 2) for k, v in sc.items()}}
    return None


NAMES = {"göbekli", "tepe", "khafre", "khafre's", "giza", "upuaut", "gantenbrink", "djedi", "kalambo", "zambia", "tanzania", "sulawesi",
         "genevieve", "petzinger", "homo", "erectus", "java", "mesopotamia", "apophis", "andromeda", "mkultra", "olson", "clovis",
         "dryas", "stonehenge", "enclosure", "vulture", "lsd", "cia", "bce", "universities", "luminescence", "denisovans", "sahara",
         "khufu", "khufu's", "muons", "merer", "ankhhaf", "tura", "wadi", "jarf", "heit", "ghurab", "menkaure", "saqqara", "serapeum", "apis", "psamtik",
         "amasis", "cambyses", "osiris", "herodotus", "abydos", "petrie", "mariette", "hawass", "lehner", "schoch", "cayce", "bauval", "alnitak",
         "seked", "rhind", "eratosthenes", "djoser", "mohs", "sphinx", "orion", "nagoya", "dobecki", "rosetau", "memphis", "aswan"}


def names_report(words, audio):
    k = VO.Kokoro("af_heart", "/tmp/_kc").k
    E, exp = [], {}
    for wi, w in enumerate(words):
        ph = expected(w, k); exp[wi] = ph; E += [(p, wi) for p in ph]
    per, got = align(E, heard(audio))
    out = []
    for wi, w in enumerate(words):
        key = re.sub(r"[^a-zöüışçğ']", "", VO._plain(w).lower().replace("’", "'"))
        if key in NAMES or key.rstrip("'s") in NAMES:
            out.append((VO._plain(w), " ".join(exp[wi]), " ".join(got.get(wi, [])), round(per.get(wi, 0) / max(1, len(exp[wi])), 2)))
    return out
