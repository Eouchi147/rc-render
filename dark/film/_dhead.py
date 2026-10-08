"""Shared delivery set for Dark Corners plain-telling scripts (same as Bamberg v3, approved 8 Oct 2026)."""
DELIVERY = {
    'calm':   (0.40, 0.20, 0.68),
    'grave':  (0.45, 0.17, 0.68),
    'firm':   (0.52, 0.24, 0.68),
    'letter': (0.55, 0.17, 0.72),   # quoted words, slower, closer
    'record': (0.32, 0.30, 0.65),   # a document read flat
}


def finish(SCRIPT, PRON):
    DIRECTED = {lid: ph for lid, q, ph in SCRIPT}
    QUOTE = {lid: q for lid, q, ph in SCRIPT}
    LINES = [(lid, ' '.join(p[0] for p in ph), '', 1.0, q) for lid, q, ph in SCRIPT]
    SAY = {}
    for _, _, ph in SCRIPT:
        for p in ph:
            s = p[0]
            for a, b in PRON.items():
                s = s.replace(a, b)
            if s != p[0]:
                SAY[p[0]] = s
    return DIRECTED, QUOTE, LINES, SAY
