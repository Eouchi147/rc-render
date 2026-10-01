"""The director: plans every shot's camera move and lens before a frame is drawn.

Each shot gets a `dir` block that kit.js plays back:
  move   one or more of push, pull, truck, crane, vertigo (dolly zoom), snap, rack (focus pull), orbit, rise
  amt    strength (1 = house style)      side   +1 / -1 for truck and crane direction
  ts     tilt-shift strength 0..1 (blurred top and bottom bands: the miniature look for maps, plans and models)
  dof    shallow depth of field (px of blur on the far layers)     from   rack-focus start blur
  dutch  degrees of roll (used sparingly, for unease)             dur    seconds the move takes

The grammar, in one breath: open on a dolly zoom or a snap to hook; maps and plans are shot as miniatures
(tilt-shift, slow truck); cross-sections descend like a crane going underground; 3-D models orbit and rise;
quotes and numbers get a slow push with the stars racked out of focus; the twist lands on a snap or a vertigo;
the verdict pulls back and lifts, to let the audience breathe. Consecutive moves alternate direction so the
cut always feels like a new angle. An author can override any shot by writing its own `dir`.
"""


def _is_iso(sh):
    return any(e.get("k") == "iso" for e in sh.get("els", []))


def _kind(sh):
    b = sh.get("base", "dark")
    ks = {e.get("k") for e in sh.get("els", [])}
    if _is_iso(sh):
        return "iso"
    if b in ("map", "plan"):
        return b
    if b == "section":
        return "section"
    if b == "sky":
        return "land"
    if b == "paper":
        return "paper"
    if ks & {"axis", "band"}:
        return "timeline"
    if ks & {"num", "title", "para"}:
        return "card"
    return "object"


def roles(ep):
    """Which story role first shows each shot (hook, world, collision, cost, reversal, tag)."""
    out = {}
    for b in ep.get("beats", []):
        v = b.get("visual", {})
        for k in ("from", "to"):
            if k in v:
                out.setdefault(int(v[k]), b.get("role", ""))
        for ln in b.get("lines", []):
            import re
            for m in re.finditer(r"\[go:([\d.]+)", ln):
                out.setdefault(int(float(m.group(1))), b.get("role", ""))
    return out


def plan(sh, role, i, n, prev_side):
    kind = _kind(sh)
    side = -prev_side or 1
    d = {"side": side}
    if role == "hook" or i == 0:
        d.update(move={"iso": "push+rise", "land": "vertigo", "section": "vertigo", "object": "vertigo"}.get(kind, "snap+push"), amt=1.1 if kind != "card" else .6, dur=6)
        if kind in ("map", "plan"):
            d["ts"] = .85
    elif role == "reversal":
        d.update(move="snap+push", amt=1.2 if kind not in ("card", "timeline") else .6, dur=5)
        if kind == "land":
            d.update(move="vertigo", amt=1.3)
        elif kind == "iso":
            d.update(move="snap+rise", amt=1.2)
    elif role == "tag" or i == n - 1:
        d.update(move="pull+crane", amt=1.1 if kind not in ("card", "timeline") else .5, side=1, dur=7)
        if kind == "iso":
            d.update(move="pull+rise", amt=1.0)
    elif kind in ("map", "plan"):
        d.update(move="truck+push", amt=.9, ts=.9 if kind == "plan" else .75, dur=8)
    elif kind == "section":
        d.update(move="crane+push", amt=.9, side=-1, dur=8)
    elif kind == "iso":
        d.update(move="orbit+push", amt=.8, dur=8)
    elif kind == "land":
        d.update(move="truck", amt=1.0, dof=1.6, dur=8)
    elif kind == "paper":
        d.update(move="push+rack", amt=.7, dof=0, dur=7, dutch=-1.2 * side)
    elif kind == "timeline":
        d.update(move="truck", amt=.4, dur=8)
    elif kind == "card":
        d.update(move="push+rack", amt=.45, from_=5, dur=7)
    else:
        d.update(move="push+rack", amt=.8, dur=7)
    if "from_" in d:
        d["from"] = d.pop("from_")
    return d


def direct(ep):
    """Give every shot of an episode its planned move (keeping any the author wrote), and return the storyboard."""
    rs = roles(ep)
    n = len(ep["shots"])
    side, board, prev = 1, [], None
    ALT = {"section": dict(move="truck+rack", amt=.9, dof=0, from_=4, dur=8), "iso": dict(move="orbit+pull", amt=.8, dur=8),
           "map": dict(move="crane+push", amt=.8, ts=.75, dur=8), "plan": dict(move="crane+pull", amt=.8, ts=.9, dur=8),
           "land": dict(move="crane+push", amt=.9, dof=1.6, dur=8), "card": dict(move="pull+rack", amt=.45, from_=5, dur=7),
           "object": dict(move="truck+push", amt=.8, dof=1.2, dur=7)}
    for i, sh in enumerate(ep["shots"]):
        if "dir" not in sh:
            d = plan(sh, rs.get(i, ""), i, n, side)
            k = _kind(sh)
            if prev and prev[0] == k and prev[1] == d.get("move") and k in ALT:   # never the same move twice in a row
                a = dict(ALT[k]); d = {"side": d["side"], **a}
                if "from_" in d:
                    d["from"] = d.pop("from_")
            sh["dir"] = d
        prev = (_kind(sh), sh["dir"].get("move"))
        side = sh["dir"].get("side", side)
        board.append({"shot": i, "role": rs.get(i, ""), "kind": _kind(sh), **sh["dir"]})
    return board


NAMES = {"push": "push in", "pull": "pull back", "truck": "truck", "crane": "crane", "vertigo": "dolly zoom",
         "snap": "snap zoom", "rack": "rack focus", "orbit": "orbit", "rise": "crane up over the model"}


def describe(d):
    ms = [NAMES.get(m, m) for m in d.get("move", "hold").split("+")]
    extra = []
    if d.get("ts"):
        extra.append("tilt-shift")
    if d.get("dof"):
        extra.append("shallow focus")
    if d.get("dutch"):
        extra.append("dutch angle")
    return " + ".join(ms) + (" · " + ", ".join(extra) if extra else "")
