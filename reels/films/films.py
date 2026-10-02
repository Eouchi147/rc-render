"""Film compiler: an episode spec (script beats + shots) becomes
   1. a stage page films/out/<id>.html (the kit engine and this film's shots), and
   2. an episode entry for reel.py (episodes/files.json), with the File code shown in the top bar.
   Specs live in films/f<NN>.py as functions returning dicts; helpers here do maps, timelines and repetition."""
import json, os, re, math, copy, html, importlib, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REELS = os.path.dirname(HERE)
BUILD = os.path.join(REELS, "..", "build", "src")
OUT = os.environ.get("RC_FILMS_OUT") or os.path.join(HERE, "out")        # a sandbox can compile elsewhere
EPS = os.environ.get("RC_FILMS_EPS") or os.path.join(REELS, "episodes", "files.json")

# ---------------------------------------------------------------- geography (Natural Earth via world-atlas)
_TOPO = None
def _topo():
    global _TOPO
    if _TOPO is None:
        p = os.path.join(HERE, "geo", "land-50m.json")
        t = json.load(open(p))
        sc, tr = t["transform"]["scale"], t["transform"]["translate"]
        arcs = []
        for a in t["arcs"]:
            x = y = 0; pts = []
            for dx, dy in a:
                x += dx; y += dy; pts.append((x * sc[0] + tr[0], y * sc[1] + tr[1]))
            arcs.append(pts)
        def ring(ix):
            out = []
            for i in ix:
                seg = arcs[i] if i >= 0 else arcs[~i][::-1]
                out.extend(seg if not out else seg[1:])
            return out
        polys = []
        for g in t["objects"]["land"]["geometries"]:
            if g["type"] == "Polygon":
                polys.append([ring(r) for r in g["arcs"]])
            elif g["type"] == "MultiPolygon":
                for p_ in g["arcs"]:
                    polys.append([ring(r) for r in p_])
        _TOPO = polys
    return _TOPO


class View:
    """Equirectangular view of a lon/lat box, scaled by cos(latitude), fitted into a frame rectangle."""
    def __init__(self, lon0, lon1, lat0, lat1, rect=(40, 300, 920, 1000)):
        self.b = (lon0, lon1, lat0, lat1)
        k = math.cos(math.radians((lat0 + lat1) / 2))
        w, h = (lon1 - lon0) * k, (lat1 - lat0)
        s = min(rect[2] / w, rect[3] / h)
        self.s, self.k = s, k
        self.ox = rect[0] + (rect[2] - w * s) / 2
        self.oy = rect[1] + (rect[3] - h * s) / 2

    def p(self, lon, lat):
        lon0, lon1, lat0, lat1 = self.b
        return (round(self.ox + (lon - lon0) * self.k * self.s, 1), round(self.oy + (lat1 - lat) * self.s, 1))

    def km(self, km):   # pixels per km at the view's centre
        return km / 111.32 * self.s

    def land(self, pad=6.0, tol=1.2):
        lon0, lon1, lat0, lat1 = self.b
        out = []
        for poly in _topo():
            for r in poly[:1]:
                xs = [q[0] for q in r]; ys = [q[1] for q in r]
                if max(xs) < lon0 - pad or min(xs) > lon1 + pad or max(ys) < lat0 - pad or min(ys) > lat1 + pad:
                    continue
                subs, pts, last, plo = [], [], None, None
                for lo, la in r:
                    if plo is not None and abs(lo - plo) > 180:      # the ring crosses the antimeridian (Fiji, Chukotka): break the path, no line across the world
                        subs.append(pts); pts, last = [], None
                    plo = lo
                    q = self.p(lo, la)
                    if last and abs(q[0] - last[0]) < tol and abs(q[1] - last[1]) < tol:
                        continue
                    pts.append(q); last = q
                subs.append(pts)
                d = "".join("M" + "L".join(f"{x} {y}" for x, y in sp) + "Z" for sp in subs if len(sp) > 3)
                if d:
                    out.append(d)
        return out

    def line(self, lonlats):
        pts = [self.p(*q) for q in lonlats]
        return "M" + "L".join(f"{x} {y}" for x, y in pts)


# ---------------------------------------------------------------- time axes
class Axis:
    def __init__(self, a, b, x0=150, x1=850, log=False):
        self.a, self.b, self.x0, self.x1, self.log = a, b, x0, x1, log

    def x(self, v):
        if self.log:
            t = (math.log10(v) - math.log10(self.a)) / (math.log10(self.b) - math.log10(self.a))
        else:
            t = (v - self.a) / (self.b - self.a)
        return round(self.x0 + (self.x1 - self.x0) * t, 1)


def yr(v):
    return f"{abs(v):,} BCE" if v < 0 else f"{v} CE"


# ---------------------------------------------------------------- shots
def like(prev, add=None, cam=None, drop=None, **kw):
    """A shot that repeats the last one (its elements already built) plus additions."""
    s = copy.deepcopy(prev)
    els = []
    for e in s.get("els", []):
        if drop and e.get("id") in drop:
            continue
        e = dict(e); e["in"] = -1; els.append(e)
    s["els"] = els + (add or [])
    if cam:
        s["cam"] = cam
    s.update(kw)
    return s


ASPECTS = {"16:9": (1778, 1000)}           # landscape frame (long form); no aspect = the 9:16 frame of the Shorts, 1000 x 1778
L16 = re.compile(r"^//<16:9\n.*?^//16:9>\n", re.S | re.M)


def kit_source(aspect=None):
    """kit.js as a page embeds it: a landscape page gets it whole, a 9:16 page without its //<16:9 ... //16:9> blocks,
    which leaves exactly the 9:16 kit (every Short's page stays byte for byte what it was)."""
    src = open(os.path.join(HERE, "kit.js"), encoding="utf-8").read()
    return src if aspect in ASPECTS else L16.sub("", src)


def page(ep):
    sid = ep["id"]
    shots = ep["shots"]
    states = [{"sc": i} for i in range(len(shots))]
    payload = {"shots": shots}
    if ep.get("aspect") in ASPECTS:                     # kit.js reads the frame size from the data (aspect first: preview.py looks for it)
        vw, vh = ASPECTS[ep["aspect"]]
        payload = {"aspect": ep["aspect"], "vw": vw, "vh": vh, "shots": shots}
        if ep.get("wall"):                              # a long film as one wall (mural.py): every panel's frame, built once
            payload = {"aspect": ep["aspect"], "vw": vw, "vh": vh, "wall": ep["wall"], "shots": shots}
    data = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    js = lambda f: open(f, encoding="utf-8").read()
    steps = "".join(f'<div class="sy-st" data-i="{i}"></div>' for i in range(len(shots)))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(ep['title'])}</title>
<style>html,body{{margin:0;background:#0d0b09}}.page{{display:block}}.sy{{position:relative;height:{len(shots) + 1}00vh}}
.sy-stage{{position:fixed;inset:0;overflow:hidden}}.sy-svg{{width:100%;height:100%;display:block}}.sy-st{{height:100vh}}.sy-hud,.sy-intro{{display:none}}</style>
</head><body><div class="page" id="page-films">
<section class="sy" id="sy-{sid}" data-sy="{sid}" data-states='{json.dumps(states)}'>
<script type="application/json" class="sy-data">{data}</script>
<div class="sy-in"><div class="sy-stage"><svg class="sy-svg" xmlns="http://www.w3.org/2000/svg"></svg></div><div class="sy-steps">{steps}</div></div></section></div>
<script>window.RC={{view:function(){{return 'films';}}}};</script>
<script>{js(os.path.join(BUILD, 'mo.js'))}</script>
<script>{js(os.path.join(BUILD, 'scrolly.js'))}</script>
<script>{kit_source(ep.get('aspect'))}</script>
<script>SY.add({json.dumps(sid)},RCKIT);</script>
</body></html>"""


KEEP = ("id", "series", "code", "title", "case", "verdict", "claim", "mood", "hook_text", "beats", "post", "hashtags", "sources", "voice", "loop", "cap_bottom")
LONG_KEEP = ("aspect", "yt_title", "description", "intro_title", "end_line")    # kept for landscape (long-form) films only


# films voiced by the directed IPA narrator (voices.CAST['narrator']); the rest still carry the first voice until re-voiced
NARRATOR_VOICE = "narrator"        # every film: the directed IPA narrator (voices.CAST['narrator'])


def _hold_under_hook16(ep, hold=3.3, top=300):
    """Landscape: the hook title sits top left for its first ~3 s (frame y < ~280 of 1000). Labels of the opening panel that would
    land up there wait until it clears. Panel children are placed at the panel's offset (and scale and crop, for a 9:16 scene shown
    in a window of a 16:9 panel); the camera centres its point."""
    fr = ep["beats"][0]["visual"]["from"]; sh = ep["shots"][fr]
    vw, vh = ASPECTS[ep["aspect"]]
    z, cx, cy = (sh.get("cam") or [1, vw / 2, vh / 2])[:3]
    def walk(els, oy, k):
        for e in els:
            if e.get("k") == "panel" and e.get("els"):
                s, c = e.get("s") or 1, e.get("crop") or [0, 0]
                walk(e["els"], oy + k * ((e.get("oy") or 0) - (c[1] * s if (e.get("s") or e.get("crop")) else 0)), k * s); continue
            kk, y = e.get("k"), e.get("y")
            if kk not in ("cap", "label", "pin") or not isinstance(y, (int, float)) or e.get("in", 0) == -1: continue
            if vh / 2 + (oy + k * y - cy) * z < top:
                e["in"] = max(e.get("in", 0) or 0, hold)
    walk(sh.get("els", []), 0, 1)


def _hold_under_hook(ep, hold=3.3):
    """The hook title card covers the top of the frame for its first ~3 s: text in the opening shot that sits up there waits until it clears.
    Limits are in the shot's own units, mapped through its camera zoom; a caption pill reaches further up than a label's baseline."""
    if ep.get("aspect") in ASPECTS:
        return _hold_under_hook16(ep, hold)
    fr = ep["beats"][0]["visual"]["from"]; sh = ep["shots"][fr]
    z, _, cy = (sh.get("cam") or [1, 500, 860])[:3]
    for e in sh.get("els", []):
        k, y = e.get("k"), e.get("y")
        if k not in ("cap", "label") or not isinstance(y, (int, float)) or e.get("in", 0) == -1: continue
        top = 550 if k == "cap" else 500
        if cy + (y - cy) * z < top:
            e["in"] = max(e.get("in", 0), hold)


def check_long(ep):
    """A landscape film: chapter titles short and plain (they go on screen and into the YouTube chapters), no dashes on screen."""
    dash = re.compile("[\u2013\u2014]")
    seen = [b["chapter"] for b in ep["beats"] if b.get("chapter")]
    for t in seen:
        assert isinstance(t, str) and 0 < len(t) <= 40 and not dash.search(t), (ep["id"], "chapter title", t)
    def texts(els):
        for e in els:
            if e.get("els"):
                yield from texts(e["els"])
            for k in ("t", "t2", "text"):
                if isinstance(e.get(k), str):
                    yield e[k]
    panels = (ep.get("wall") or {}).get("panels", [])               # the wall's frames: their bases' own words (strata names...)
    words = [t for sh in ep["shots"] for t in texts(sh.get("els", []))] + [t for p in panels for t in texts([p] + p.get("els", []))]
    words += [l.get("t") for p in panels for q in [p] + p.get("els", []) for l in (q.get("bs") or {}).get("layers", []) if isinstance(l.get("t"), str)]
    bad = sorted({t for t in words if dash.search(t)})
    assert not bad, (ep["id"], "em or en dash in on-screen text", bad[:5])


def compile_file(mod_name):
    mod = importlib.import_module(mod_name)
    os.makedirs(OUT, exist_ok=True)
    eps = json.load(open(EPS)) if os.path.exists(EPS) else []
    by = {e["id"]: e for e in eps}
    import director
    bd = os.environ.get("RC_FILMS_BOARDS") or os.path.join(REELS, "episodes", "boards"); os.makedirs(bd, exist_ok=True)   # a sandbox can keep its boards too
    for ep in mod.EPISODES():
        _hold_under_hook(ep)
        board = director.direct(ep)
        json.dump(board, open(os.path.join(bd, ep["id"] + ".json"), "w"), indent=1)
        open(os.path.join(OUT, ep["id"] + ".html"), "w", encoding="utf-8").write(page(ep))
        e = {k: ep[k] for k in KEEP if k in ep}
        e.update({"view": "films", "story": ep["id"], "site": os.path.join("films", "out", ep["id"] + ".html"),
                  "voice": ep.get("voice") or NARRATOR_VOICE})
        if ep.get("aspect") in ASPECTS:                   # long form: its extra fields, and its chapters checked
            e.update({k: ep[k] for k in LONG_KEEP if k in ep})
            check_long(ep)
        n = len(ep["shots"])
        for b in e["beats"]:
            for k in ("from", "to"):
                if k in b.get("visual", {}):
                    assert 0 <= b["visual"][k] <= n - 1, (ep["id"], b)
        for b in e["beats"]:
            for ln in b["lines"]:
                for m in re.finditer(r"\[go:([\d.]+)", ln):
                    assert float(m.group(1)) <= n - 1, (ep["id"], ln, n)
        sys.path.insert(0, os.path.join(REELS, "free")); import heteronyms as HN
        probs = [p for b in e["beats"] for ln in b["lines"] for p in HN.lint(ln)]
        assert not probs, (ep["id"], probs)                   # every heteronym must say which sense it is
        by[e["id"]] = e
        print(f"  {ep['code']} {ep['id']}: {n} shots, {sum(len(b['lines']) for b in e['beats'])} lines")
    json.dump(list(by.values()), open(EPS, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    for m in sys.argv[1:]:
        compile_file(m)
