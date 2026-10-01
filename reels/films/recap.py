"""The ledger recap: a File's ledger told like a science show, one case at a time, in its cabinet (see cabinet.py).

The narration comes from rewrite/ledgers/<id>.json (hook, one entry per case: where, the mystery, how we know, the verdict; the close).
Every case has its own moment: the camera settles on its niche, a location note appears, the claim is drawn (a question mark, a dotted
claimed layer, or a claim written dim), the evidence note arrives, then the verdict frame and chip (and a red strike for a ruled-out claim).
The close reads the cabinet together: what held, what waits, and the people behind it all.
"""
import copy, json, os
from cabinet import Cabinet, VCOL

HERE = os.path.dirname(os.path.abspath(__file__))
ROLES = ("world", "collision", "cost", "reversal")


def _cells_of(ledger_fn):
    """The cabinet cells the File's current ledger() builds (recorded, then rebuilt fresh)."""
    rec = {}
    orig = Cabinet.__init__

    def spy(self, cells, **kw):
        rec.setdefault("cells", copy.deepcopy(cells)); rec.setdefault("kw", dict(kw))
        orig(self, cells, **kw)
    Cabinet.__init__ = spy
    try:
        old = ledger_fn()
    finally:
        Cabinet.__init__ = orig
    return old, rec["cells"], rec["kw"]


def split(n):
    """How many cases each of the four middle beats carries."""
    base, extra = divmod(n, 4)
    return [base + (1 if k < extra else 0) for k in range(4)]


def recap(ledger_fn, lid, extras=None, B=None):
    """ledger_fn: the File's current ledger() (for its cabinet and metadata). lid: the ledger id. extras: optional
    {"hook": [elements drawn with the question marks], "close": {0..3: elements added on that close sentence}, "cells": {i: {...}}}."""
    extras = extras or {}
    data = json.load(open(os.path.join(HERE, "rewrite", "ledgers", lid + ".json"), encoding="utf-8"))
    old, cells, kw = _cells_of(ledger_fn)
    C = Cabinet(cells, **kw)
    C.build()
    C.note_min_rows = 2
    if callable(extras):
        extras = extras(C, data) or {}
    n = C.n
    BLUE, AMB, BONE_ = "#9fd0ff", "#f2c98e", "#e9dccb"
    s_all = C.step(C.cam_all(k=.95), [e for i in range(n) for e in C.question(i, dx=C.w * .3, dy=-C.h * .55, at=.2 + .06 * i, size=46, c="#c9c1ee", id="q%d" % i)]
                   + list(extras.get("hook", [])))
    K, verdicts = {}, {}
    first = True
    for case in data["cases"]:
        i = case["cell"]; v = case["verdict"]; verdicts[i] = v
        a = C.step(C.cam_cell(i), C.note(i, case["where"], at=.5, c=BONE_), drop=["q%d" % k for k in range(n)] if first else ())
        first = False
        if v == "ruled" and case.get("claim_text"):
            claim = C.claim(i, case["claim_text"], at=.4, rows=1)
        elif v in ("awaiting", "open", "mixed", "plausible"):
            claim = C.question(i, dx=C.w * .3, dy=-C.h * .5, at=.3, size=64, c=VCOL.get(v, BLUE))
        else:
            claim = C.question(i, dx=C.w * .3, dy=-C.h * .5, at=.3, size=64, c="#c9c1ee")
        b = C.step(C.cam_cell(i), claim + list(extras.get("cells", {}).get(i, {}).get("claim", [])), keep_notes=True)
        ev = C.note(i, case["evidence_note"], at=1.0, c=AMB, stack=True) if case.get("evidence_note") else []
        if v in ("established", "strong"):
            ev += C.people(i, 3, at=1.6)
        c = C.step(C.cam_cell(i), ev + list(extras.get("cells", {}).get(i, {}).get("evidence", [])), keep_notes=True)
        chip = case.get("chip") or None
        vd = C.verdict(i, v, chip if v != "ruled" or chip else None, .2)
        if v == "ruled" and case.get("claim_text"):
            vd += C.strike_claim(i, .5)
        d = C.step(C.cam_cell(i), vd + list(extras.get("cells", {}).get(i, {}).get("verdict", [])), keep_notes=True)
        K[i] = (a, b, c, d)
    # the close: the whole cabinet, what held, what still waits, and the people behind it
    held = [i for i, v in verdicts.items() if v in ("established", "strong")]
    waits = [i for i, v in verdicts.items() if v in ("awaiting", "open", "plausible", "mixed")]
    trench = lambda i, at: C.local(i, [{"k": "rect", "x": -C.w * .40, "y": -C.h * .58, "w": C.w * .80, "h": C.h * .62, "r": 10, "fill": "rgba(159,208,255,.04)", "c": BLUE, "sw": 2.4,
                                       "style": "inferred", "fx": "draw", "dur": 1.0, "in": at}])
    ce = extras.get("close", {})
    e1 = C.step(C.cam_all(), list(ce.get(0, [])))
    e2 = C.step(C.cam_all(), [x for k, i in enumerate(held) for x in C.wash(i, VCOL["strong"], at=.2 + .12 * k, op=.13)] + list(ce.get(1, [])))
    e3 = C.step(C.cam_all(), [x for k, i in enumerate(waits) for x in trench(i, .2 + .12 * k)] + list(ce.get(2, [])))
    e4 = C.step(C.cam_all(), [x for i in range(n) for x in C.people(i, 2, at=.2 + .08 * i)] + list(ce.get(3, [])))
    e5 = C.step(C.cam_all(k=.86, sy=720))
    g = lambda st, d=".6": "[go:%d|%s]" % (st, d)
    P = "[p:0.93]"

    def L(case):
        a, b, c, d = K[case["cell"]]
        return "[gap:0.4]" + g(a, "1.5") + P + case["t1"] + " " + g(b) + case["t2"] + " " + g(c) + case["t3"] + " " + g(d) + case["t4"]
    hook = data["hook"]
    cut = hook.find("[act:", hook.find("[act:") + 5)                 # the question marks rise on the hook's second sentence
    hook_line = "[d:intrigue][sfx:boom][p:0.94]" + (hook[:cut] + g(s_all, "1.3") + hook[cut:] if cut > 0 else hook + g(s_all, "1.3"))
    beats = [{"role": "hook", "visual": {"from": 0}, "lines": [hook_line]}]
    cases = list(data["cases"]); last = s_all
    moods = {"world": "[d:calm]", "collision": "[d:build]", "cost": "[d:build]", "reversal": "[d:build]"}
    for role, k in zip(ROLES, split(len(cases))):
        chunk, cases = cases[:k], cases[k:]
        if not chunk:
            continue
        lines = [L(cs) for cs in chunk]
        lines[0] = moods[role] + lines[0]
        beats.append({"role": role, "visual": {"from": last}, "lines": lines})
        last = K[chunk[-1]["cell"]][3]
    cl = data["close"]
    marks = [g(e1, "2"), g(e2, ".8"), g(e3, ".8"), g(e4, ".8")]
    close = "[d:verdict][gap:0.5]" + " ".join(marks[k] + (P if k == 0 else "") + s for k, s in enumerate(cl[:4])) + (" " + " ".join(cl[4:]) if len(cl) > 4 else "")
    tag = [close]
    if data.get("motto"):
        tag.append("[d:tension][p:0.93]" + g(e5, "4") + "[act:the motto, quiet and sure][tune:fall]^Coherence is the measure. [gap:0.45][act:gentle, the closing note][tune:fall]Not ^final demonstration.")
    else:
        tag[0] = tag[0] + " " + g(e5, "3")                          # no motto: the cabinet still pulls back at the end
    beats.append({"role": "tag", "visual": {"from": last}, "lines": tag})
    old = copy.deepcopy(old)
    old.update(beats=beats, shots=C.shots)
    if data.get("hook_text"):
        old["hook_text"] = data["hook_text"]
    return old
