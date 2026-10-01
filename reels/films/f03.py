"""File 03 · The Sky Fell? Floods, fire and ice at the end of the last Ice Age.
03.01 (sky-fell) already exists; this file adds 03.02 to 03.06."""
import math
from films import like, View, Axis
from scenes import timeline, event, stat, quote, silhouette, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot, LAURENTIDE, CORDILLERAN
from iso3d import shot as iso, lab, aim, diorama

SERIES = "The Sky Fell?"
ICE = "#dfe9f2"


def B(role, frm, lines, cut=True):
    return {"role": role, "visual": {"from": frm, "cut": cut} if cut else {"from": frm}, "lines": lines}


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def L_(x, y, t, c=None, z=0, **k):
    return dict(lab(x, y, t, c, z=z), st="lab", **k)


# ---------------------------------------------------------------- 03.02 The Flood Geologists Laughed At
def scablands():
    # the region: Montana's ice-dammed lake, the scablands of Washington, the Columbia to the sea
    v = View(-124.5, -111, 44.2, 49.6, (40, 330, 920, 900))
    lake = [(-114.4, 46.4), (-113.6, 46.9), (-113.2, 47.5), (-114.1, 47.9), (-114.9, 47.6), (-115.3, 47.1), (-114.9, 46.6)]
    scab = [(-119.8, 47.9), (-118.2, 47.9), (-117.6, 47.2), (-118.4, 46.4), (-119.6, 46.2), (-119.9, 46.9)]
    ice = [(-125, 50.5), (-122.5, 48.4), (-120.5, 47.9), (-118.6, 48.2), (-117.2, 48.0), (-116.2, 48.4), (-115.2, 48.1), (-113.6, 48.6), (-111, 48.9), (-111, 50.5)]
    columbia = [(-117.6, 49.4), (-118.2, 48.6), (-119.0, 47.9), (-119.9, 47.4), (-119.4, 46.5), (-119.0, 46.2), (-121.2, 45.7), (-122.7, 45.6), (-123.5, 46.2), (-124.0, 46.3)]
    base = mapshot(v, extra=[{"k": "line", "p": [v.p(*q) for q in columbia], "c": "#5fa8c9", "w": 2, "op": .6, "curve": True, "id": "river"},
                             {"k": "poly", "p": [v.p(*q) for q in ice], "fill": "rgba(235,245,255,.5)", "c": "#ffffff", "w": 1.4, "curve": True, "id": "ice"},
                             {"k": "label", "x": v.p(-118, 49.3)[0], "y": v.p(-118, 49.3)[1], "t": "Cordilleran ice sheet", "st": "ital", "c": "#e6eef6"},
                             {"k": "label", "x": v.p(-122.6, 45.3)[0], "y": v.p(-122.6, 45.3)[1] + 30, "t": "Columbia", "st": "small", "c": "#9fd0ff"}])
    s0 = like(base, cam=[1.6, v.p(-116.5, 47)[0], v.p(-116.5, 47)[1]], add=[
        {"k": "poly", "p": [v.p(*q) for q in lake], "fill": "rgba(95,168,201,.55)", "c": SCAN, "w": 1.6, "curve": True, "in": .2, "id": "lake"},
        {"k": "label", "x": v.p(-113.9, 46.2)[0], "y": v.p(-113.9, 46.2)[1] + 30, "t": "glacial Lake Missoula", "c": "#cfe6ff", "in": .6},
        {"k": "q", "x": v.p(-116.2, 48.1)[0], "y": v.p(-116.2, 48.1)[1], "size": 60, "in": 1.0, "fx": "pop"}])
    s1 = like(base, add=[{"k": "poly", "p": [v.p(*q) for q in scab], "fill": "rgba(236,90,60,.3)", "c": OCHRE, "w": 1.6, "curve": True, "in": .3},
                         {"k": "label", "x": v.p(-118.9, 46.0)[0], "y": v.p(-118.9, 46.0)[1] + 34, "t": "the Channeled Scablands", "c": "#ffb09a", "in": .8},
                         {"k": "pin", "x": v.p(-119.35, 47.6)[0], "y": v.p(-119.35, 47.6)[1], "t": "Dry Falls", "c": GOLD, "a": "end", "lx": -18, "in": 1.2},
                         {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    # Dry Falls against Niagara: a 3-D diorama, the same scale
    falls = [{"t": "box", "x": -40, "z": 0, "y": 0, "w": 56, "d": 30, "h": 12.1, "c": "#8a6a4a", "edge": "rgba(0,0,0,.3)"},        # Dry Falls: 5.6 km wide, 121 m
             {"t": "box", "x": 30, "z": 4, "y": 0, "w": 8.2, "d": 20, "h": 5.1, "c": "#6d7a4a", "edge": "rgba(0,0,0,.3)"},         # Niagara Horseshoe: .82 km, 51 m
             {"t": "flat", "pts": [[-68, -15], [-12, -15], [-12, 15], [-68, 15]], "y": 12.15, "c": "#a8845c"},
             {"t": "flat", "pts": [[25.9, -6], [34.1, -6], [34.1, 14], [25.9, 14]], "y": 5.15, "c": "#3f86b0"},
             L_(-40, 15, "Dry Falls · 5.6 km wide · 121 m", GOLD), L_(30, 8, "Niagara · 0.8 km · 51 m", "#cfe6ff", dy=44)]
    s2 = iso(falls, cam=[1, 500, 900], s=8.5, x=500, y=1000, az=-28, spin=1.6, el=.4, table={"r": 78, "rz": 30, "grid": 10, "strata": [{"h": 2, "c": "#a8845c"}, {"h": 6, "c": "#7d6045"}]})
    s2["els"] += [{"k": "cap", "x": 500, "y": 400, "t": "one cataract, to scale", "in": .2},
                  {"k": "label", "x": 500, "y": 1360, "t": "dry today: the river that cut it is gone", "st": "small", "in": .9}]
    # the stacked flood beds
    beds = []
    for i in range(14):
        y = 1180 - i * 46
        beds.append({"k": "rect", "x": 220, "y": y - 46, "w": 560, "h": 40, "fill": "#a88860" if i % 2 else "#8c6f4c", "c": "#e9dccb", "sw": .8, "in": .1 + i * .06})
        beds.append({"k": "line", "p": [[220, y - 6], [780, y - 6]], "c": "#f2dcb4", "w": 1.4, "style": "claimed", "op": .7, "in": .15 + i * .06})
    s3 = {"base": "dark", "floor": 1182, "cam": [1.05, 500, 880], "els": beds + [
        {"k": "cap", "x": 500, "y": 460, "t": "Touchet Formation · about 40 flood beds", "in": .1},
        {"k": "label", "x": 500, "y": 1240, "t": "burrows and volcanic ash between them: years passed between floods", "st": "small", "in": 1.2}]}
    # the timeline of dates
    tl, ax = timeline(-20000, -11000, [(-20000, "20,000"), (-17000, "17,000"), (-14000, "14,000"), (-11000, "11,000")], "When the floods ran · years ago", y=820)
    tl["els"] += event(ax, -18200, "a major flood · 18,200 ± 1,500", row=0, c=SCAN, i=.3, sub="beryllium-10 on flood boulders") + \
                 event(ax, -14700, "the last floods · 14,700 ± 1,200", row=1, c=SCAN, i=.7) + \
                 event(ax, -12900, "Younger Dryas · 12,900", row=2, c=GOLD, i=1.1, sub="no flood bed dated here, yet")
    s4 = tl
    s5 = quote("Bretz was right and his critics were wrong. The lesson: catastrophe must be tested, not ruled out.", "after Randall Carlson · the challengers' case", y=720, size=42)
    s6 = like(s1, cam=[1.15, 500, 860], add=[{"k": "arrow", "p": [v.p(-114.3, 47.2), v.p(-117.8, 47.9), v.p(-119.4, 46.4), v.p(-121.5, 45.7), v.p(-123.8, 46.2)], "curve": True, "c": SCAN, "w": 3, "in": .2, "fx": "draw", "dur": 2.2},
                                             {"k": "label", "x": v.p(-122.4, 45.1)[0], "y": v.p(-122.4, 45.1)[1] + 40, "t": "to the Pacific, in days", "c": "#cfe6ff", "in": 1.6}])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:EASTERN WASHINGTON][sfx:boom][act:setting the scene, intrigued]In {1923|nineteen twenty-three}, a geologist said a ^*flood* carved this land in ^days.",
                      "[d:tension][cam:1.15|0|0][act:dry, a rueful smile][tune:fall]His colleagues ^laughed at him for ^forty years."], cut=False),
        B("world", 1, ["[d:calm][k:THE SCABLANDS][act:wonder, seeing it through his eyes]J Harlen Bretz saw dry ^waterfalls, giant ^ripples, and canyons with ^no river to cut them.",
                       "[d:build][go:2|0][act:relishing the numbers]Dry Falls: five and a half kilometres ^wide, a hundred and twenty-one metres ^high. [sfx:shimmer][act:delighted, building]^Niagara would fit inside it ^seven times over. [d:aside][act:quick, playful aside, lower][tune:fall]Which is a ^rude thing to say to Niagara."]),
        B("collision", 3, ["[d:build][k:THE SOURCE][act:explaining, building the picture]The water came from an Ice Age ^lake in Montana, dammed by a wall of ice ^six hundred metres tall.",
                           "[d:list][act:vivid, the scale sinking in]When the dam ^floated, two and a half ^thousand cubic kilometres of water emptied across the ^state. [act:leaning in][tune:fallrise]And not ^once. [act:the punch, slower][tune:fall]About ^*forty* times."]),
        B("cost", 4, ["[d:build][k:THE DATES][act:matter of fact, precise]Exposure dates on the flood boulders: roughly ^eighteen thousand to ^fourteen thousand seven hundred years ago."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:warm, a vindication story]In {1979|nineteen seventy-nine}, at ^ninety-six, Bretz got geology's highest ^medal. [act:quoting him, mischievous]His reply: [sfx:hit]all my enemies are ^dead, so I have no one to ^gloat over.",
                          "[d:calm][act:even, reporting a newer idea]Some now go ^further, and tie the biggest floods to a ^comet. [d:aside][act:a careful caveat, lower]That needs a flood bed dated to the ^Younger Dryas. [act:plain, open-minded][tune:fallrise]^None has been found, yet."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]The ^floods? [act:firm, certain][tune:highfall]^*Established*. [act:the next question, even][tune:rise]A ^comet behind them? [act:the verdict, level-headed][tune:fall]Still awaiting ^evidence.",
                     "[d:tension][p:0.93][act:grounded, fair][tune:fall]Catastrophes are ^real. [act:the last word, a knowing smile][tune:fall]The trick is proving ^*which* one."]),
    ]
    return EP("scablands", "03.02", "The Flood Geologists Laughed At", "channeled-scablands", "solid", "Did catastrophic floods carve the Scablands?", "A flood... carved this in *days*.", beats, shots,
              "Bretz 1923 · Waitt 1980, GSA Bulletin · Balbas et al. 2017, Geology · Bjornstad 2006, On the Trail of the Ice Age Floods",
              "The Channeled Scablands were cut by dozens of Ice Age floods from glacial Lake Missoula. How Bretz was vindicated, and what a comet link would still need.",
              ["#IceAge", "#Geology", "#Catastrophe", "#Washington", "#Science"])


def _take(ep_fn, shots, froms):
    """The film with its narration rewritten (films/rewrite/<id>.json) and its pictures re-ordered for one take: shots is the new
    list of scenes in the order the story meets them, froms the new first picture of each beat. Times in these scenes are seconds
    of the rewritten narration (no automatic stretch)."""
    from mural import rewritten
    ep = rewritten(ep_fn())
    ep["shots"] = shots
    for b, f in zip(ep["beats"], froms):
        b["visual"]["from"] = f
    return ep


def scablands_m():
    """The Scablands as one continuous take (see mural.py): the scarred land, seven Niagaras, the ice dam that floated, forty flood beds,
    a boulder's suntan and the comet's empty slot are drawn, then the flood runs to the sea on the map."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, BONE as BN, AU
    WATER, ROCK, ROCKD, ICE_ = "#3f86b0", "#5b4a3c", "#3b3028", "#e6eff6"
    # 0 · the hook: the scarred land in profile, a dry waterfall, a lone geologist; the flood he imagined; forty years of laughter
    land = [{"k": "poly", "p": [[-10, 650], [140, 640], [320, 656], [520, 644], [760, 660], [1010, 648], [1010, 1200], [-10, 1200]], "fill": "#76604c", "c": "#8a7460", "w": 1.5, "in": -1}] + \
           [line([[x, 652 + (x * 7) % 9], [x + 3, 735 + (x * 13) % 25]], -1, "#2e251e", 2, draw=False, op=.55) for x in range(0, 1000, 23)] + \
           [{"k": "poly", "p": [[-10, 800], [428, 800], [437, 818], [445, 905], [450, 1000], [456, 1085], [492, 1118], [540, 1128], [590, 1108], [615, 1085], [1010, 1085], [1010, 1778], [-10, 1778]],
             "fill": ROCKD, "c": "#c9ad85", "w": 2, "in": -1}] + \
           [line([[-10, y], [440 + (y - 800) * .05, y]], -1, "#6b5644", 2, draw=False, op=.7) for y in (870, 950, 1030)] + \
           [line([[-10, y], [1010, y]], -1, "#6b5644", 2, draw=False, op=.7) for y in (1170, 1260)] + \
           [line([[437, 818 + 34 * k], [447, 830 + 34 * k]], -1, "#c9ad85", 1.5, draw=False, op=.4) for k in range(7)]
    hook = {"base": "sky", "tod": "dusk", "ground": 1400, "sun": [850, 590, 24], "cam": [1.15, 500, 830], "els": land + [
                person(392, 800, 72, 1.6),
                line([[0, 548], [1000, 548]], 7.4, BLUE, 3, "claimed", 1.4)] +
            [arrow([[120 + 260 * k, 590], [270 + 260 * k, 590]], 7.9 + .25 * k, BLUE, 3, "claimed", .6, False) for k in range(3)] +
            [person(110 + 48 * k, 800, 66, 10.2 + .2 * k, "#cbbca8") for k in range(4)] +
            [line([[230, 420], [770, 420]], 11.9, AU, 4, dur=1.4), line([[230, 404], [230, 436]], 11.9, AU, 3, draw=False), line([[770, 404], [770, 436]], 13.2, AU, 3, draw=False),
             label(230, 390, "1923", 11.7, AU, 30), label(500, 470, "40 years", 12.8, AU, 32)]}
    ripples = [[620 + 4 * j, round(1085 - 16 * abs(math.sin(math.pi * j / 15)), 1)] for j in range(91)]
    seeing = [label(392, 700, "J Harlen Bretz", 1.2, BN, 30),
              {"k": "poly", "p": ellipse(446, 950, 64, 175, 40), "fill": "none", "c": AMB, "w": 3, "curve": True, "in": 3.3, "fx": "draw", "dur": .9},
              label(372, 990, "dry waterfall", 3.6, AMB, 30, "end"),
              {"k": "poly", "p": ripples + [[984, 1085], [620, 1085]], "fill": ROCKD, "c": "#e9d3ab", "w": 2.5, "in": 4.2, "fx": "draw", "dur": 1.2},
              label(800, 1150, "giant ripples", 4.6, "#e9d3ab", 30),
              line([[470, 1112], [540, 1122], [600, 1100], [980, 1060]], 8.6, BLUE, 3, "claimed", 1.0, True)] + question(760, 990, 9.4, 70) + \
             [label(860, 990, "no river", 9.6, LILAC, 30)]
    # 1 · Dry Falls face-on, to scale with Niagara (both heights stretched alike): seven Niagaras fit along its lip
    KM, M = 840 / 5.6, 330 / 121
    nw, nh = .8 * KM, 51 * M
    face = [[80, 1050], [80, 728], [170, 722], [270, 731], [380, 719], [500, 727], [620, 716], [740, 729], [850, 720], [920, 726], [920, 1050]]
    falls = {"base": "dark", "floor": 1050, "cam": [1.12, 500, 930], "els": [
                line([[40, 1050], [960, 1050]], .1, "#8c7152", 2, draw=False),
                {"k": "poly", "p": face, "fill": "#6e5a48", "c": "#e9d3ab", "w": 2, "in": .4, "fx": "fill", "dur": 1.2}] +
             [line([[x, 735], [x + 2, 1040]], .9, "#2e251e", 2, draw=False, op=.5) for x in range(96, 912, 19)] +
             [label(500, 640, "Dry Falls", .8, AU, 34, st="serif"),
              line([[80, 690], [920, 690]], 1.8, BN, 2.5, dur=1.0), line([[80, 676], [80, 704]], 1.8, BN, 2.5, draw=False), line([[920, 676], [920, 704]], 2.6, BN, 2.5, draw=False),
              label(500, 676, "5.6 km", 2.6, BN, 30),
              line([[890, 728], [890, 1050]], 4.8, BN, 2.5, dur=.9), line([[876, 728], [904, 728]], 4.8, BN, 2.5, draw=False), line([[876, 1050], [904, 1050]], 5.6, BN, 2.5, draw=False),
              label(870, 900, "121 m", 5.4, BN, 30, "end"),
              bx(80, 1050 - nh, nw, nh, WATER, "#cfe6ff", 2, 2, 6.6, fx="rise")] + \
            [line([[92 + 12 * k, 1050 - nh + 6], [92 + 12 * k, 1044]], 6.8, "#e6f4ff", 2, draw=False, op=.6) for k in range(9)] + \
            [label(80 + nw / 2, 1050 - nh - 18, "Niagara", 7.0, "#cfe6ff", 30)] + \
            [bx(80 + nw * k, 1050 - nh, nw, nh, "rgba(159,208,255,.18)", "#cfe6ff", 3, 2, 12.4 + .3 * k, style="inferred", fx="pop") for k in range(1, 7)] + \
            [label(80 + nw * (k + .5), 1100, str(k + 1), 12.2 + .3 * k, "#cfe6ff", 30) for k in range(7)]}
    # 2 · the map: where the water came from (the lake behind the ice dam) and, at the end, where it went
    v = View(-128.5, -110.5, 43, 50.5, (40, 330, 920, 1000))
    P = lambda q: [v.p(*p) for p in q]
    ice = [(-131, 58), (-131, 50.2), (-125, 50.4), (-122.5, 48.4), (-120.5, 47.9), (-118.6, 48.2), (-117.2, 48.0), (-116.2, 48.4), (-115.2, 48.1), (-113.6, 48.6), (-111, 48.9), (-107, 49.0), (-107, 58)]
    lake = [(-114.4, 46.4), (-113.6, 46.9), (-113.2, 47.5), (-114.1, 47.9), (-114.9, 47.75), (-115.6, 47.95), (-116.05, 48.18), (-116.2, 48.02), (-115.5, 47.72), (-115.3, 47.1), (-114.9, 46.6)]
    scab = [(-119.8, 47.9), (-118.2, 47.9), (-117.6, 47.2), (-118.4, 46.4), (-119.6, 46.2), (-119.9, 46.9)]
    columbia = [(-117.6, 49.4), (-118.2, 48.6), (-119.0, 47.9), (-119.9, 47.4), (-119.4, 46.5), (-119.0, 46.2), (-121.2, 45.7), (-122.7, 45.6), (-123.5, 46.2), (-124.0, 46.3)]
    dam = v.p(-116.2, 48.1)
    from f01 import mapshot as _ms
    mp = _ms(v, cam=[1.3, 470, 720], extra=[
        {"k": "line", "p": P(columbia), "c": "#5fa8c9", "w": 2.4, "op": .7, "curve": True, "in": -1},
        {"k": "poly", "p": P(ice), "fill": "rgba(235,245,255,.3)", "c": "#ffffff", "w": 1.4, "curve": True, "in": .2},
        label(*v.p(-121.0, 50.0), "ice sheet", .6, "#e6eef6", 36, st="ital"),
        label(*v.p(-126.0, 47.3), "Pacific", .6, "#9fd0ff", 34, st="ital"),
        {"k": "poly", "p": P(scab), "fill": "rgba(236,90,60,.32)", "c": "#ec5a3c", "w": 2, "curve": True, "in": .8, "fx": "draw", "dur": .9},
        label(*v.p(-118.8, 45.65), "the scarred land", 1.5, "#ffb09a", 30),
        {"k": "poly", "p": P(lake), "fill": "rgba(95,168,201,.7)", "c": "#9fd0ff", "w": 2, "curve": True, "in": 3.6, "fx": "fill", "dur": 1.4},
        label(*v.p(-114.1, 45.9), "Montana", 5.0, "#e9dccb", 34, st="ital"),
        glow(dam[0], dam[1], 70, 7.0, .9, "scan"), {"k": "line", "p": [[dam[0] - 16, dam[1] - 22], [dam[0] + 14, dam[1] + 20]], "c": ICE_, "w": 14, "in": 7.0, "fx": "pop"},
        label(dam[0] - 28, dam[1] - 14, "ice dam", 7.4, ICE_, 30, "end")])
    route = [arrow(P([(-114.6, 47.3), (-116.0, 47.95), (-117.8, 47.9), (-119.2, 46.9), (-119.4, 46.4), (-121.5, 45.7), (-123.8, 46.2), (-125.2, 46.25)]), 1.4, BLUE, 5, "known", 3.0)] + \
            [label(*v.p(-125.6, 45.4), "in days", 5.0, "#cfe6ff", 30)] + \
            [line([[820, 880], [730, 1000]], 6.8, LILAC, 3, "claimed", .8), glow(730, 1000, 50, 7.4, .8, "scan"), dot(730, 1000, 9, "#f5f0ff", 7.4)] + question(700, 1120, 8.6, 70)
    # 4 · the ice dam from the side: six hundred metres of ice, a building as tall; the lake lifts it like a cork, and out it goes, forty times
    gyL, gyR = 1270, 1300
    dsec = {"base": "sky", "tod": "night", "ground": 1500, "sun": False, "cam": [1.08, 500, 900], "els": [
                {"k": "poly", "p": [[-10, 1240], [300, 1255], [560, 1270], [740, 1275], [1010, 1320], [1010, 1778], [-10, 1778]], "fill": ROCKD, "c": "#c9ad85", "w": 2, "in": -1},
                {"k": "poly", "p": [[-10, 770], [566, 770], [566, 1268], [300, 1255], [-10, 1240]], "fill": "rgba(63,134,176,.85)", "c": "#9fd0ff", "w": 2, "in": -1},
                {"k": "poly", "p": [[566, 740], [724, 742], [732, 1274], [566, 1270]], "fill": ICE_, "c": "#ffffff", "w": 2, "in": -1},
                line([[600, 760], [640, 900], [620, 1040]], -1, "#a9c4d8", 2, draw=False), line([[690, 800], [670, 960]], -1, "#a9c4d8", 2, draw=False),
                label(280, 860, "the lake", .3, "#e6f4ff", 32), label(645, 680, "ice dam", .3, BN, 30),
                line([[760, 742], [760, 1274]], 1.0, AU, 2.5, dur=.9), line([[746, 742], [774, 742]], 1.0, AU, 2.5, draw=False), line([[746, 1274], [774, 1274]], 1.8, AU, 2.5, draw=False),
                label(780, 1010, "600 m", 1.8, AU, 32, "start"),
                {"k": "rect", "x": 878, "y": 742, "w": 60, "h": 560, "fill": "rgba(245,236,220,.1)", "c": "#e9dccb", "sw": 2, "in": 3.9, "fx": "rise"}] +
            [line([[884, 758 + 20 * k], [932, 758 + 20 * k]], 4.1, "#e9dccb", 1.2, draw=False, op=.45) for k in range(26)]}
    lift = [arrow([[600 + 40 * k, 1330], [600 + 40 * k, 1262]], .5 + .12 * k, "#cfe6ff", 4, dur=.5, curve=False) for k in range(4)] + \
           [{"k": "poly", "p": [[566, 706], [724, 708], [732, 1240], [566, 1236]], "fill": ICE_, "c": "#ffffff", "w": 2, "in": 3.4, "fx": "rise", "dur": 1.0},
            line([[600, 726], [640, 866], [620, 1006]], 3.4, "#a9c4d8", 2, draw=False), line([[690, 766], [670, 926]], 3.4, "#a9c4d8", 2, draw=False),
            {"k": "poly", "p": [[566, 1236], [732, 1240], [732, 1276], [566, 1271]], "fill": "#5fa8c9", "c": "#cfe6ff", "w": 2, "in": 4.2},
            bx(290, 755, 44, 26, "#b08850", "#e9d3ab", 1.5, 8, 5.2, fx="pop"),
            {"k": "poly", "p": [[732, 1240], [800, 1190], [900, 1150], [1010, 1130], [1010, 1330], [732, 1278]], "fill": "rgba(95,168,201,.8)", "c": "#9fd0ff", "w": 2, "in": 7.0, "fx": "fill", "dur": 1.6}] + \
           [arrow([[750, 1240 - 20 * k], [860, 1215 - 22 * k], [990, 1205 - 24 * k]], 7.6 + .3 * k, "#f2fbff", 5, dur=.9) for k in range(3)]
    tally = []
    for g in range(8):
        x0 = 130 + g * 96
        for j in range(5):
            k = 5 * g + j
            at = 12.3 if k == 0 else 13.0 + .035 * (k - 1)
            tally.append(line([[x0 + 13 * j, 360], [x0 + 13 * j, 430]] if j < 4 else [[x0 - 8, 420], [x0 + 50, 370]], at, BN if j < 4 else AU, 4, dur=.15))
    # 5 · forty flood beds, stacked like pages; burrows and ash between them: years between floods
    beds = []
    for k in range(40):
        y = 1300 - 20 * (k + 1)
        beds.append(bx(220, y, 560, 19, "#b39a76" if k % 2 else "#9c8462", r=0, at=3.0 + .06 * k))
        beds.append(line([[220, y], [780, y]], 3.0 + .06 * k, "#4a3a2c", 1.5, draw=False))
    burrows = [line([[x, y], [x + 9, y + 18], [x - 5, y + 36], [x + 6, y + 54]], 8.9 + .12 * k, "#2a1d12", 6, dur=.4, curve=True) for k, (x, y) in
               enumerate([(300, 520), (520, 640), (690, 780), (360, 900), (610, 1020), (450, 1160)])]
    ash = [line([[220, y], [780, y]], 10.1 + .2 * k, "#f0ede6", 4, dur=.6) for k, y in enumerate((700, 960, 1180))]
    bedsc = {"base": "dark", "floor": 1300, "cam": [1.05, 500, 920], "els": [line([[160, 1300], [840, 1300]], .1, "#8c7152", 2, draw=False)] + beds + burrows + ash + [
                line([[810, 1300], [810, 500]], 6.0, AU, 2.5, dur=.8), line([[798, 1300], [822, 1300]], 6.0, AU, 2.5, draw=False), line([[798, 500], [822, 500]], 6.7, AU, 2.5, draw=False),
                label(830, 910, "about 40", 6.3, AU, 30, "start"),
                label(200, 655, "burrows", 9.2, "#e9d3ab", 30, "end"), label(200, 965, "ash", 10.4, "#f0ede6", 30, "end"),
                bx(205, 1027, 590, 26, "none", AU, 3, 4, 11.2), label(200, 1052, "years", 11.5, AU, 30, "end")]}
    # 6 · when: a boulder in the open, rays from space building up a 'suntan' in its surface; the dates
    rock = [[330, 1150], [318, 1060], [350, 960], [430, 905], [540, 890], [630, 925], [676, 1010], [668, 1150]]
    clock = {"base": "dark", "stars": 120, "cam": [1.0, 500, 900], "els": [
                {"k": "poly", "p": [[-10, 1150], [1010, 1150], [1010, 1778], [-10, 1778]], "fill": "#2e251e", "c": "#8c7152", "w": 2, "in": -1},
                {"k": "poly", "p": rock, "fill": "#7d6a58", "c": "#e9d3ab", "w": 2, "curve": True, "in": 3.1, "fx": "rise"},
                {"k": "rays", "x0": 260, "x1": 740, "y0": 300, "y1": 930, "n": 46, "c": "#9fd0ff", "spread": .35, "in": 5.6, "dur": 1.2},
                {"k": "line", "p": rock[1:-1], "c": AU, "w": 7, "curve": True, "in": 9.0, "fx": "draw", "dur": 1.4},
                glow(500, 930, 200, 10.8, .55, "lamp")] +
             [dot(x, y, 4, AU, 7.6 + .1 * k) for k, (x, y) in enumerate([(372, 975), (420, 940), (470, 925), (520, 918), (570, 930), (615, 958), (640, 1000), (352, 1020), (450, 950), (590, 975)])] +
             [line([[150, 1300], [850, 1300]], 14.4, "#e9dccb", 2.5, dur=.8)] +
             [line([[x, 1288], [x, 1312]], 14.6, "#e9dccb", 2, draw=False) for x in (150, 500, 850)] +
             [line([[325, 1300], [614, 1300]], 18.2, AU, 16, dur=1.6), label(325, 1260, "18,000", 18.2, AU, 30), label(614, 1260, "14,700", 19.6, AU, 30),
              label(500, 1360, "years ago", 15.0, "#cbbca8", 28)]}
    # 7 · 1979: the old man and his medal; his enemies, gone
    medal = {"base": "dark", "floor": 1220, "cam": [1.05, 500, 920], "els": [
                label(500, 470, "1979", .3, AU, 52, st="serif"), label(500, 530, "age 96", 1.6, BN, 30),
                person(500, 1220, 320, .5, "#e8d6b8"), glow(500, 1000, 230, .6, .35, "lamp"),
                line([[478, 925], [500, 990], [522, 925]], 3.0, "#b0301e", 6, draw=False),
                {"k": "circle", "x": 500, "y": 1000, "r": 24, "fill": AU, "c": "#fff3d0", "w": 2, "in": 3.4, "fx": "pop"}, glow(500, 1000, 90, 3.4, .8, "lamp")] +
             [{"k": "lib", "k2": "person", "x": x, "y": 1220, "h": 250, "color": "#cbbca8", "op": .2, "keepop": True, "in": 6.0 + .25 * k} for k, x in enumerate((150, 270, 730, 850))]}
    # 8 · the comet idea: the dated floods, a sudden cold spell 12,900 years ago, and the flood bed nobody has found
    X = lambda ya: 120 + 760 * (20000 - ya) / 10000
    comet = {"base": "dark", "stars": 140, "cam": [1.0, 500, 900], "els": [
                line([[120, 1150], [880, 1150]], .2, "#e9dccb", 2.5, dur=.8)] +
             [line([[X(y), 1138], [X(y), 1162]], .3, "#e9dccb", 2, draw=False) for y in (20000, 15000, 10000)] +
             [label(X(y), 1200, t, .4, "#cbbca8", 28) for y, t in ((20000, "20,000"), (10000, "10,000"))] +
             [label(500, 1250, "years ago", .5, "#cbbca8", 28),
              line([[X(18000), 1110], [X(14700), 1110]], 2.8, BLUE, 16, dur=.9), label((X(18000) + X(14700)) / 2, 1070, "the floods", 3.2, BLUE, 30),
              {"k": "rect", "x": X(12900), "y": 760, "w": X(11700) - X(12900), "h": 380, "fill": "rgba(159,208,255,.2)", "c": "none", "sw": 0, "in": 6.6, "fx": "fill", "dur": 1.0},
              line([[X(12900), 760], [X(12900), 1150]], 6.6, "#cfe6ff", 2.5, dur=.8), label(X(12900) - 14, 740, "Younger Dryas", 8.4, "#cfe6ff", 30, "end"),
              label(X(12900), 1200, "12,900", 9.8, "#cfe6ff", 28),
              line([[930, 300], [720, 640]], 4.0, LILAC, 4, "claimed", 1.2), glow(720, 640, 60, 4.8, .9, "scan"), dot(720, 640, 12, "#f5f0ff", 4.8),
              bx(X(12900) - 50, 1070, 100, 30, "none", LILAC, 3, 4, 13.2, style="claimed")] + question(X(12900), 1030, 15.8, 70)}
    shots = [hook, {}, falls, mp, dsec, bedsc, clock, medal, comet, {}]
    ep = _take(scablands, shots, [0, 1, 3, 6, 7, 9])
    return remix(ep, scenes={0: hook, 2: falls, 3: mp, 4: dsec, 5: bedsc, 6: clock, 7: medal, 8: comet}, alias={1: 0, 9: 3}, _rewrite=False,
                 beat_adds={1: (seeing, [1.3, 560, 870]), 5: (route, [1.25, 470, 740])}, line_adds={(2, 1): (lift + tally, None)})


# ---------------------------------------------------------------- 03.03 Half a Million Ovals
def carolina_bays():
    v = View(-84, -73, 30, 40.5, (40, 330, 920, 900))
    base = mapshot(v)
    import random
    rng = random.Random(7)
    ovals = []
    for i in range(90):
        lon = rng.uniform(-82.5, -75.2); lat = rng.uniform(31.2, 36.8)
        x, y = v.p(lon, lat)
        if lon > -76.6 - (lat - 31) * .5:      # keep them on the coastal plain, roughly
            continue
        ang = -16 - (lat - 31) * 8            # the axis swings with latitude
        ovals.append({"k": "poly", "p": [[x + 9 * math.cos(math.radians(a)) * math.cos(math.radians(ang)) - 5 * math.sin(math.radians(a)) * math.sin(math.radians(ang)),
                                          y + 9 * math.cos(math.radians(a)) * math.sin(math.radians(ang)) + 5 * math.sin(math.radians(a)) * math.cos(math.radians(ang))] for a in range(0, 360, 30)],
                      "fill": "rgba(159,208,255,.28)", "c": "#cfe6ff", "w": .9, "curve": True, "in": .2 + i * .012})
    s0 = like(base, cam=[1.5, v.p(-78.8, 34.3)[0], v.p(-78.8, 34.3)[1]], add=ovals + [{"k": "cap", "x": 500, "y": 400, "t": "the Atlantic coastal plain", "in": .1}])
    s1 = like(s0, cam=[1.05, 500, 860], add=[{"k": "num", "x": 500, "y": 1300, "t": "500,000", "u": "ovals", "in": .3, "fx": "pop", "size": 92}])
    # one bay, as a model: a shallow oval basin with a raised rim on the south-east
    bay = [{"t": "flat", "pts": [[80 * math.cos(math.radians(a)), 46 * math.sin(math.radians(a))] for a in range(0, 360, 15)], "y": .1, "c": "#3f86b0", "op": .75},
           {"t": "cyl", "x": 46, "z": 30, "y": 0, "r": 22, "h": 3, "c": "#d9c39a", "n": 24, "edge": "rgba(0,0,0,.2)"},
           L_(0, 2, "shallow · a few metres of sand and mud", "#cfe6ff"), L_(50, 5, "sand rim, highest to the south-east", GOLD, z=34, dy=36)]
    s2 = iso(bay, cam=[1, 500, 900], s=4.2, x=500, y=980, az=-20, spin=1.8, el=.5, table={"r": 110, "rz": 80, "grid": 20, "strata": [{"h": 3, "c": "#a8845c"}, {"h": 9, "c": "#7d6045"}]})
    s2["els"] += [{"k": "label", "x": 500, "y": 1380, "t": "the layers beneath: undisturbed, no sign of a blow", "st": "small", "in": 1.0}]
    # the claim: ejecta fanning from one point
    fan = [{"k": "line", "p": [v.p(-87.5, 44.5), v.p(lon, lat)], "c": OCHRE, "w": 1.2, "op": .6, "style": "claimed", "in": .3 + i * .1, "fx": "draw"}
           for i, (lon, lat) in enumerate([(-81.5, 31.5), (-80, 33), (-78.5, 34.5), (-77, 36), (-75.5, 37.5)])]
    v2 = View(-92, -72, 29, 47, (40, 330, 920, 900))
    s3 = mapshot(v2, extra=[{"k": "line", "p": [v2.p(-87.5, 44.5), v2.p(lon, lat)], "c": OCHRE, "w": 1.4, "op": .7, "style": "claimed", "in": .3 + i * .1, "fx": "draw"}
                            for i, (lon, lat) in enumerate([(-81.5, 31.5), (-80, 33), (-78.5, 34.5), (-77, 36), (-75.5, 37.5)])] +
                 [{"k": "q", "x": v2.p(-87.5, 44.5)[0], "y": v2.p(-87.5, 44.5)[1] - 20, "size": 56, "c": OCHRE, "in": .2, "fx": "pop"},
                  {"k": "label", "x": v2.p(-87.5, 44.5)[0], "y": v2.p(-87.5, 44.5)[1] + 50, "t": "one impact, on the ice sheet?", "c": "#ffb09a", "in": .9}])
    tl, ax = timeline(-110000, 0, [(-100000, "100,000"), (-75000, "75,000"), (-50000, "50,000"), (-25000, "25,000"), (0, "today")], "When the bay sands were laid down · years ago", y=980)
    tl["els"] += [{"k": "band", "x0": ax.x(-109000), "x1": ax.x(-2000), "y": 880, "h": 16, "c": SCAN, "t": "luminescence ages of rims and basins", "in": .3},
                  {"k": "band", "x0": ax.x(-40000), "x1": ax.x(-11000), "y": 800, "h": 22, "c": "#cfe6ff", "t": "most of them", "in": .7},
                  {"k": "line", "p": [[ax.x(-12800), 980], [ax.x(-12800), 700]], "c": OCHRE, "w": 2.2, "style": "claimed", "in": 1.1},
                  {"k": "label", "x": ax.x(-12800), "y": 680, "t": "the proposed impact · 12,800", "c": "#ffb09a", "in": 1.3}]
    s4 = tl
    s5 = stat("31,000", "years", "of lake mud at White Pond, a bay where impact markers were reported. The bay is far older than the event.", "Moore et al. 2019")
    s6 = like(s0, cam=[1.25, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE CAROLINA BAYS][sfx:boom][act:wonder, setting the scene][tune:level]Half a ^million oval hollows... [act:the eerie detail, slower][tune:fall]all pointing the ^*same* way.",
                      "[d:tension][cam:1.15|0|0][act:posing the big question, intrigued][tune:rise]^Craters, from ^one blast in the sky?"], cut=False),
        B("world", 1, ["[d:calm][k:NEW JERSEY TO FLORIDA][act:plain storytelling, a guided tour]They dot the coastal plain, from under a ^hectare to ^thousands of acres. [act:observing closely][tune:fall]Sand ^rims on their ^south-east ends.",
                       "[d:build][go:2|0][sfx:shimmer][act:intrigued, building the mystery]And their long axes@axis swing ^smoothly with latitude, as if fanning out from ^one point."]),
        B("collision", 3, ["[d:build][k:THE CLAIM][act:laying out the claim, fair and vivid]So the idea: a ^comet hit the ice sheet, and chunks of ice rained down across the east, punching half a million craters at ^once."]),
        B("cost", 4, ["[d:aside][k:THE CHILD'S QUESTION][act:playful, childlike curiosity][tune:fall]Now, the question a ^six-year-old asks first: where are the ^rocks that hit? [d:build][k:THE DATES][act:matter of fact, turning a page]Then came the ^dating. [act:slow, spanning the ages][tune:level]Rim sands from a ^hundred and nine thousand years ago... [act:landing it, clear][tune:fall]to ^two thousand. [act:quiet, deliberate][tune:fall]^Built and ^rebuilt, over ages.",
                      "[d:list][go:5|0][act:calm, precise]Beneath them, the older layers lie ^undisturbed. [act:flat, pointed][tune:level]No ^shock. [act:same flat weight][tune:fall]No ^melt."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:leaning in, the decisive detail]Even at White Pond, where impact ^markers were reported, [sfx:hit]the lake mud goes back ^thirty-one thousand years. [act:quiet, certain][tune:fall]The bay was there ^long before."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:calm authority, the slow answer]^Wind@air and waves on old ponds, over ^tens of thousands of years. [act:the other option, even][tune:rise]^One blast? [act:the verdict, firm][tune:fall]*Ruled ^out* by the dates.",
                     "[d:tension][p:0.93][act:fair, generous][tune:fall]The ^pattern is real. [act:a knowing smile, unhurried][tune:level]The ^cause is just... [act:the last word, gentle][tune:fall]^*slower*."]),
    ]
    return EP("carolina-bays", "03.03", "Half a Million Ovals", "carolina-bays", "debunked", "Were the Carolina Bays made by one cosmic impact?", "All pointing the *same* way.", beats, shots,
              "Prouty 1952 · Brooks et al. 2010 · Moore et al. 2016, 2019 · Lundine & Trembanis 2025",
              "500,000 oval basins along the US east coast share an alignment. The impact idea, and the luminescence dates that spread them over 100,000 years.",
              ["#CarolinaBays", "#Geology", "#IceAge", "#Science", "#Mystery"])


def _on_land(lon, lat):
    """True where the 50 m coastline data has land (ray casting on each polygon's outer ring)."""
    from films import _topo
    for poly in _topo():
        r = poly[0]
        xs = [q[0] for q in r]; ys = [q[1] for q in r]
        if not (min(xs) <= lon <= max(xs) and min(ys) <= lat <= max(ys)):
            continue
        inside = False
        for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
            if (y1 > lat) != (y2 > lat) and lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
                inside = not inside
        if inside:
            return True
    return False


def _bays(n=170, seed=11):
    """Carolina-bay sites, schematic: scattered on the Atlantic coastal plain (densest in the Carolinas), on land only."""
    import random
    r = random.Random(seed)
    band = [(31.0, 32.5, -82.6, -81.0, 1), (32.5, 34.0, -81.9, -79.0, 3), (34.0, 35.5, -79.6, -76.8, 3), (35.5, 37.0, -78.0, -76.2, 1.2),
            (37.0, 39.4, -76.4, -75.2, .5), (39.4, 40.0, -75.1, -74.4, .3)]
    W = sum(w for *_, w in band); out = []
    while len(out) < n:
        u = r.uniform(0, W)
        for lat0, lat1, lo0, lo1, w in band:
            if u <= w:
                break
            u -= w
        lon, lat = r.uniform(lo0, lo1), r.uniform(lat0, lat1)
        if _on_land(lon, lat):
            out.append((lon, lat))
    return out


def carolina_bays_m():
    """The Carolina Bays as one continuous take (see mural.py): the ovals line up and fan out, the claimed rain of ice, the sand that
    keeps time like a battery, the flat layers, White Pond's mud, and the slow work of wind and waves are drawn."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN, AU
    WET, SAND = "#24433f", "#d9c39a"
    def ov(cx, cy, a, b, ang, **k):
        c, s = math.cos(ang), math.sin(ang)
        return [[round(cx + a * math.cos(t) * c - b * math.sin(t) * s, 1), round(cy + a * math.cos(t) * s + b * math.sin(t) * c, 1)] for t in [2 * math.pi * j / 24 for j in range(24)]]
    sites = _bays()
    # 0 · the hook: the coastal plain, the ovals appear, all lined up on one far point
    v = View(-84, -73, 30, 40.5, (40, 330, 920, 900))
    C = v.p(-87.5, 44.5)
    hk = []
    for i, (lon, lat) in enumerate(sorted(sites, key=lambda q: math.sin(q[0] * 37.1 + q[1] * 11.3))):
        x, y = v.p(lon, lat); a = math.atan2(C[1] - y, C[0] - x)
        hk.append({"k": "poly", "p": ov(x, y, 8, 4.5, a), "fill": "rgba(159,208,255,.35)", "c": "#cfe6ff", "w": 1.2, "curve": True, "in": round(1.6 + i * .018, 3)})
    axes = []
    for i, (lon, lat) in enumerate(sorted(sites, key=lambda q: q[1])[5::12]):
        x, y = v.p(lon, lat); a = math.atan2(C[1] - y, C[0] - x)
        axes.append(line([[x - 38 * math.cos(a), y - 38 * math.sin(a)], [x + 38 * math.cos(a), y + 38 * math.sin(a)]], 6.0 + .04 * i, AU, 2.5, dur=.5))
    from f01 import mapshot as _ms
    hook = _ms(v, cam=[1.5, 480, 860], extra=hk + axes + [label(*v.p(-75.2, 32.6), "Atlantic", .4, "#9fd0ff", 34, st="ital")] + question(330, 560, 8.6, 90))
    plain = [line([v.p(*q) for q in [(-81.9, 30.7), (-80.6, 32.6), (-79.0, 34.0), (-77.6, 35.4), (-76.6, 37.2), (-75.8, 38.9), (-74.9, 40.0)]], 3.0, AMB, 3, "inferred", 1.6, True),
             label(v.p(-74.9, 40.0)[0] - 14, v.p(-74.9, 40.0)[1] - 22, "New Jersey", 4.8, BN, 30, "end"), label(*v.p(-82.3, 29.4), "Florida", 5.8, BN, 30)]
    # 1 · one bay, from above: the smallest is about a football pitch, the biggest several square kilometres, a sand rim to the south-east
    KM = 180; th = math.radians(38)
    big = ov(500, 930, 1.85 * KM, .75 * KM, th)
    sm = (240, 590)
    pitch = lambda cx, cy, w, h: [[round(cx + px * math.cos(th) - py * math.sin(th), 1), round(cy + px * math.sin(th) + py * math.cos(th), 1)] for px, py in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    cz, cc = 6, (640, 520)
    rim = [[round(500 + 1.85 * KM * math.cos(t) * math.cos(th) - .75 * KM * math.sin(t) * math.sin(th), 1), round(930 + 1.85 * KM * math.cos(t) * math.sin(th) + .75 * KM * math.sin(t) * math.cos(th), 1)]
           for t in [math.radians(d) for d in range(-75, 76, 6)]]
    rim_out = [[round(500 + (1.85 * KM + 34) * math.cos(t) * math.cos(th) - (.75 * KM + 30) * math.sin(t) * math.sin(th), 1), round(930 + (1.85 * KM + 34) * math.cos(t) * math.sin(th) + (.75 * KM + 30) * math.sin(t) * math.cos(th), 1)]
               for t in [math.radians(d) for d in range(75, -76, -6)]]
    plan = {"base": "plan", "bg": "#2b2a1f", "north": [880, 330], "cam": [1.05, 500, 900], "els": [
                {"k": "poly", "p": ov(sm[0], sm[1], .12 * KM / 2, .08 * KM / 2, th), "fill": "#3f86b0", "c": "#cfe6ff", "w": 1.5, "in": .5},
                ring(sm[0], sm[1], 26, .6, BN, 2.5, dur=.5), line([[sm[0] + 24, sm[1] - 8], [cc[0] - 120, cc[1] + 18]], 1.2, BN, 2, dur=.5),
                {"k": "circle", "x": cc[0], "y": cc[1], "r": 122, "fill": "#1d2a26", "c": BN, "w": 2.5, "in": 1.4, "fx": "pop"},
                {"k": "poly", "p": ov(cc[0], cc[1], .12 * KM / 2 * cz, .08 * KM / 2 * cz, th), "fill": "#3f86b0", "c": "#cfe6ff", "w": 2, "in": 1.8},
                {"k": "poly", "p": pitch(cc[0], cc[1], .105 * KM * cz, .068 * KM * cz), "fill": "rgba(120,170,90,.55)", "c": "#f5ecdc", "w": 2.5, "in": 3.8, "fx": "pop"},
                {"k": "line", "p": pitch(cc[0], cc[1], 0, .068 * KM * cz)[1:3], "c": "#f5ecdc", "w": 2, "in": 4.0},
                label(cc[0], cc[1] + 160, "a football pitch", 4.2, BN, 30),
                {"k": "poly", "p": big, "fill": WET, "c": "#9fd0ff", "w": 3, "curve": True, "in": 5.0, "fx": "draw", "dur": 1.4},
                label(500, 930, "several km²", 7.6, "#cfe6ff", 32),
                line([[140, 1330], [140 + KM, 1330]], 8.0, BN, 3, draw=False), line([[140, 1318], [140, 1342]], 8.0, BN, 2, draw=False), line([[140 + KM, 1318], [140 + KM, 1342]], 8.0, BN, 2, draw=False),
                label(140 + KM / 2, 1310, "1 km", 8.0, BN, 28),
                label(500, 980, "shallow", 9.2, "#cfe6ff", 28),
                {"k": "poly", "p": rim + rim_out, "fill": SAND, "c": "#fff3d6", "w": 1.5, "curve": True, "in": 10.8, "fx": "rise"},
                label(rim[len(rim) // 2][0] + 10, rim[len(rim) // 2][1] + 90, "sand rim", 11.5, SAND, 30)]}
    # 2 · the axes on the map: they swing as you go north, as if fanning out from one point; then the claimed rain of ice from it
    v2 = View(-92, -72, 29, 47, (40, 330, 920, 900))
    C2 = v2.p(-87.5, 44.5)
    sub = sorted(sites, key=lambda q: q[1])[::4]
    fan_els = []
    for i, (lon, lat) in enumerate(sub):
        x, y = v2.p(lon, lat); a = math.atan2(C2[1] - y, C2[0] - x)
        fan_els.append({"k": "poly", "p": ov(x, y, 13, 7, a), "fill": "rgba(159,208,255,.4)", "c": "#cfe6ff", "w": 1.2, "curve": True, "in": round(.2 + .015 * i, 3)})
        fan_els.append(line([[x - 24 * math.cos(a), y - 24 * math.sin(a)], [x + 24 * math.cos(a), y + 24 * math.sin(a)]], round(1.0 + .06 * i, 2), AU, 2.5, dur=.4))
    far = [line([v2.p(lon, lat), C2], round(4.4 + .08 * i, 2), AU, 1.6, "claimed", .9) for i, (lon, lat) in enumerate(sub[::4])]
    fan = _ms(v2, cam=[1.15, 525, 840], extra=fan_els + far + [glow(C2[0], C2[1], 90, 6.3, .9, "lamp"), dot(C2[0], C2[1], 8, AU, 6.3)])
    icesh = [(-97, 44.6), (-92, 44.2), (-88, 43.9), (-84, 44.9), (-80, 45.6), (-76, 46.0), (-70, 46.4), (-66, 47.5), (-66, 54), (-97, 54)]
    claim = [{"k": "poly", "p": [v2.p(*q) for q in icesh], "fill": "rgba(235,245,255,.35)", "c": "#ffffff", "w": 2, "style": "inferred", "curve": True, "in": 5.4},
             label(*v2.p(-80, 47.6), "ice sheet", 6.0, "#e6eef6", 34, st="ital"),
             line([[60, 200], [C2[0] - 10, C2[1] - 10]], 4.2, LILAC, 4, "claimed", .9), glow(C2[0], C2[1], 150, 5.6, .9, "red"),
             label(C2[0] + 10, C2[1] - 50, "12,800 years ago?", 2.4, LILAC, 30)] + \
            [arrow([C2, [(C2[0] + x) / 2 - 30, min(C2[1], y) - 120], [x, y]], round(8.2 + .15 * i, 2), LILAC, 2.5, "claimed", .9) for i, (x, y) in
             enumerate([v2.p(lon, lat) for lon, lat in sub[2::6]])] + \
            [glow(*v2.p(-79.0, 34.0), 230, 12.0, .6, "red"), label(*v2.p(-74.5, 31.0), "at once?", 12.6, LILAC, 32)]
    # 4 · the child's question, and the sand's clock: grains charge like batteries in the dark; rims built and rebuilt over ages
    G = 1150
    mound = lambda h: [[520, G], [600, G - h * .7], [670, G - h * .97], [720, G - h], [790, G - h * .9], [860, G - h * .45], [905, G]]
    lay = [(125, "#e3cfa6", 24.2), (95, "#cdb68b", 23.9), (65, "#b89f75", 23.6), (35, "#a38a62", 20.0)]
    CX, CY = 400, 640
    batt = []
    for j, x in enumerate((CX - 80, CX, CX + 80)):
        batt += [bx(x - 20, CY + 40, 40, 70, "#1a1511", "#f5ecdc", 2.5, 5, 8.6 + .15 * j), bx(x - 8, CY + 32, 16, 9, "#f5ecdc", r=2, at=8.6 + .15 * j),
                 bx(x - 15, CY + 46, 30, 58, AU, r=3, at=12.6 + .2 * j, fx="fill", dur=2.6)]
    clock = {"base": "dark", "stars": 60, "cam": [1.2, 525, 905], "els": [
                {"k": "poly", "p": [[-10, G], [190, G], [210, G + 30], [320, G + 52], [430, G + 44], [510, G + 8], [520, G], [1010, G], [1010, 1778], [-10, 1778]], "fill": "#2e251e", "c": "#8c7152", "w": 2, "in": -1},
                {"k": "poly", "p": [[190, G], [520, G], [510, G + 8], [430, G + 44], [320, G + 52], [210, G + 30]], "fill": "#2f5f78", "c": "#9fd0ff", "w": 2, "in": -1},
                {"k": "line", "p": mound(125), "c": SAND, "w": 2, "style": "inferred", "curve": True, "in": -1},
                person(150, G, 105, 1.3, "#e8d6b8")] + question(150, G - 150, 3.0, 60) + [
                {"k": "poly", "p": [[330, G + 30], [350, G + 14], [380, G + 18], [395, G + 36], [360, G + 46]], "fill": "none", "c": LILAC, "w": 2.5, "style": "claimed", "in": 4.0},
                label(362, G + 96, "rocks?", 4.2, LILAC, 28)] + \
            [{"k": "poly", "p": mound(h) + [[520, G]], "fill": c, "c": "#fff3d6", "w": 1.2, "curve": True, "in": t, "fx": "rise"} for h, c, t in lay] + [
                {"k": "circle", "x": CX, "y": CY, "r": 168, "fill": "#1d1813", "c": BN, "w": 2.5, "in": 5.8, "fx": "pop"},
                line([[CX + 120, CY + 118], [700, G - 120]], 6.0, BN, 2, "inferred", .5),
                line([[CX - 150, CY + 25], [CX + 150, CY + 25]], 6.2, SAND, 3, draw=False),
                dot(CX - 90, CY - 105, 16, "#ffe2a8", 10.2), glow(CX - 90, CY - 105, 60, 10.2, .9, "lamp")] + \
            [arrow([[CX - 90 + 40 * j, CY - 80], [CX - 65 + 50 * j, CY + 15]], 10.4 + .1 * j, "#ffe2a8", 2.5, dur=.4, curve=False) for j in range(3)] + batt + [
                bx(CX - 120, CY + 25, 240, 100, "rgba(185,159,117,.45)", r=4, at=11.8), label(CX, CY + 205, "time in the dark", 15.2, AU, 28),
                label(712, G + 70, "109,000 years ago", 21.6, BN, 30), label(720, G - 140, "2,000", 24.6, AU, 30),
                {"k": "line", "p": [[530, G], [630, G - 80], [740, G - 112], [830, G - 100], [890, G - 40], [905, G]], "c": AU, "w": 2, "style": "inferred", "curve": True, "in": 26.0}]}
    # 5 · beneath a bay: flat layers, undisturbed; what a blast would have left (crushed grains, melted rock) is not there
    S0 = 780
    bands = [(S0, "#7a6248"), (S0 + 110, "#5f4c39"), (S0 + 220, "#8a7052"), (S0 + 330, "#4f3f30"), (S0 + 440, "#6b5640")]
    beneath = {"base": "dark", "cam": [1.4, 500, 1090], "els": [bx(40, y, 920, 110, c, r=0, at=-1) for y, c in bands] + [
                {"k": "poly", "p": [[260, S0], [360, S0 + 26], [500, S0 + 34], [640, S0 + 26], [740, S0]], "fill": "#2f5f78", "c": "#9fd0ff", "w": 2, "in": -1, "curve": True},
                label(500, S0 - 30, "a bay", .3, "#cfe6ff", 30)] + \
            [line([[40, y], [960, y]], 1.8 + .25 * k, AU, 2.5, dur=.9) for k, (y, c) in enumerate(bands[1:])] + [
                {"k": "line", "p": [[180, S0 + 110], [320, S0 + 180], [500, S0 + 210], [680, S0 + 180], [820, S0 + 110]], "c": LILAC, "w": 3, "style": "claimed", "curve": True, "in": 4.6, "fx": "draw"},
                {"k": "poly", "p": [[300 + 34 * math.cos(math.radians(a)), 1180 + 34 * math.sin(math.radians(a))] for a in range(0, 360, 60)], "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": 6.0},
                line([[282, 1162], [318, 1198]], 6.2, LILAC, 2, "claimed", .3), line([[318, 1160], [292, 1196]], 6.3, LILAC, 2, "claimed", .3),
                label(300, 1262, "shock", 6.2, LILAC, 30),
                {"k": "poly", "p": [[700, 1146], [730, 1170], [736, 1205], [705, 1222], [672, 1200], [676, 1166]], "fill": "rgba(201,193,238,.15)", "c": LILAC, "w": 3, "style": "claimed", "curve": True, "in": 7.0},
                label(705, 1262, "melt", 7.0, LILAC, 30),
                strike(250, 1230, 350, 1130, 8.2), strike(655, 1235, 755, 1135, 9.2)]}
    # 6 · White Pond: mud settles like dust on a shelf; the core goes down 31,000 years, far below the level of the reported markers
    T0, B0 = 640, 1380
    yrs = lambda ka: T0 + (B0 - T0) * ka / 31
    core = [bx(460, yrs(30 - k), 80, (B0 - T0) / 31 + .5, "#6b5640" if k % 2 else "#87705a", r=0, at=round(6.0 + .1 * k, 2)) for k in range(31)]
    pond = {"base": "dark", "stars": 40, "cam": [1.15, 500, 1020], "els": [
                {"k": "poly", "p": [[-10, 560], [200, 560], [300, 610], [500, 628], [700, 610], [800, 560], [1010, 560], [1010, 1778], [-10, 1778]], "fill": "#3b3028", "c": "#8c7152", "w": 2, "in": -1},
                {"k": "poly", "p": [[200, 560], [800, 560], [700, 610], [500, 628], [300, 610]], "fill": "#2f5f78", "c": "#9fd0ff", "w": 2, "in": -1, "curve": True},
                label(500, 520, "White Pond", .4, "#cfe6ff", 32),
                {"k": "rect", "x": 460, "y": T0, "w": 80, "h": B0 - T0, "fill": "#1a1511", "c": BN, "sw": 2, "in": 1.2, "fx": "fill", "dur": 1.0}] + core + [
                bx(452, yrs(12.8) - 5, 96, 10, "#c9c1ee", r=2, at=3.8), glow(500, yrs(12.8), 80, 3.8, .7, "scan"),
                label(565, yrs(12.8) + 10, "markers reported", 4.2, LILAC, 30, "start"),
                arrow([[420, T0 + 20], [420, B0 - 20]], 11.0, BN, 2.5, dur=1.0, curve=False), label(405, T0 + 40, "newer", 11.0, BN, 28, "end"), label(405, B0 - 10, "older", 11.8, BN, 28, "end"),
                label(565, B0 - 6, "31,000 years", 15.6, AU, 32, "start"),
                line([[555, yrs(12.8) + 30], [555, B0 - 40]], 17.4, AU, 3, dur=.8), glow(500, (yrs(12.8) + B0) / 2, 160, 17.6, .35, "lamp")]}
    # 7 · the slow answer: wind and waves shaping an old pond into an oval over ages; one blast, struck out; the pattern stays
    pondA = [[300, 820], [380, 760], [470, 790], [560, 740], [660, 800], [700, 900], [640, 990], [520, 1010], [420, 980], [330, 930]]
    wind = {"base": "plan", "bg": "#2b2a1f", "north": [880, 330], "cam": [1.05, 500, 955], "els": [
                {"k": "poly", "p": pondA, "fill": "rgba(63,134,176,.45)", "c": "#9fd0ff", "w": 2, "style": "inferred", "curve": True, "in": .3}] + \
            [arrow([[70, 700 + 90 * j], [230, 720 + 90 * j]], .4 + .12 * j, BN, 3, dur=.6, curve=False) for j in range(4)] + \
            [line([[380 + 60 * j, 870 + 30 * (j % 2)], [400 + 60 * j, 860 + 30 * (j % 2)], [420 + 60 * j, 870 + 30 * (j % 2)]], 1.0 + .1 * j, "#cfe6ff", 2, dur=.3, curve=True) for j in range(5)] + [
                {"k": "poly", "p": ov(500, 885, 210, 120, th), "fill": "none", "c": "#9fd0ff", "w": 2, "style": "inferred", "curve": True, "in": 3.0},
                {"k": "poly", "p": ov(500, 890, 260, 110, th), "fill": "rgba(63,134,176,.6)", "c": "#cfe6ff", "w": 3, "curve": True, "in": 5.2, "fx": "draw", "dur": 1.2},
                {"k": "poly", "p": [[round(500 + 260 * math.cos(t) * math.cos(th) - 110 * math.sin(t) * math.sin(th), 1), round(890 + 260 * math.cos(t) * math.sin(th) + 110 * math.sin(t) * math.cos(th), 1)] for t in [math.radians(d) for d in range(-70, 71, 10)]] +
                      [[round(500 + 292 * math.cos(t) * math.cos(th) - 136 * math.sin(t) * math.sin(th), 1), round(890 + 292 * math.cos(t) * math.sin(th) + 136 * math.sin(t) * math.cos(th), 1)] for t in [math.radians(d) for d in range(70, -71, -10)]],
                 "fill": SAND, "c": "#fff3d6", "w": 1.5, "curve": True, "in": 6.4, "fx": "rise"},
                line([[160, 420], [300, 520]], 7.6, LILAC, 4, "claimed", .6), glow(300, 520, 50, 8.0, .9, "scan"), dot(300, 520, 10, "#f5f0ff", 8.0), strike(200, 600, 380, 420, 9.4)] + \
            [{"k": "poly", "p": ov(200 + 150 * j, 1330 - 14 * (j % 2), 46, 20, th), "fill": "rgba(63,134,176,.6)", "c": "#cfe6ff", "w": 2, "curve": True, "in": 11.2 + .15 * j, "fx": "pop"} for j in range(5)]}
    shots = [hook, plan, fan, {}, clock, beneath, pond, wind]
    ep = _take(carolina_bays, shots, [0, 0, 3, 4, 6, 7])
    return remix(ep, scenes={0: hook, 1: plan, 2: fan, 4: clock, 5: beneath, 6: pond, 7: wind}, alias={3: 2}, _rewrite=False,
                 beat_adds={1: (plain, [1.0, 470, 860]), 2: (claim, [1.1, 500, 830])})


# ---------------------------------------------------------------- 03.04 The Comet That Keeps Coming Back
def taurids():
    # the inner solar system, plan view: Sun, Earth's orbit, Encke's stretched orbit, the debris stream
    cx, cy = 500, 900
    AU = 150
    earth = [{"k": "circle", "x": cx, "y": cy, "r": AU, "c": "#cfe6ff", "w": 1.4, "op": .8, "in": .2, "fx": "draw"},
             {"k": "circle", "x": cx, "y": cy, "r": 14, "fill": "#ffe2a8", "c": "none", "w": 0, "in": .1},
             {"k": "glow", "x": cx, "y": cy, "r": 60, "kind": "sun", "op": .8}]
    a, e = 2.22 * AU, .85
    b = a * math.sqrt(1 - e * e); fx = a * e
    ell = [[cx - fx + a * math.cos(math.radians(t)), cy + b * math.sin(math.radians(t))] for t in range(0, 361, 6)]
    encke = {"k": "line", "p": ell, "c": GOLD, "w": 2, "curve": True, "in": .5, "fx": "draw", "dur": 2, "id": "encke"}
    stream = [{"k": "line", "p": [[x + (i - 3) * 5 * math.sin(math.radians(t)), y + (i - 3) * 5] for (x, y), t in zip(ell, range(0, 361, 6))], "c": GOLD, "w": .8, "op": .25, "curve": True, "in": 1 + i * .1} for i in range(7)]
    s0 = {"base": "dark", "stars": 160, "cam": [1.25, cx - 90, cy - 60], "els": earth + [encke] + stream + [
        {"k": "label", "x": cx + AU + 24, "y": cy - 10, "t": "Earth's orbit", "a": "start", "c": "#cfe6ff", "in": .8},
        {"k": "label", "x": cx - fx - a - 20, "y": cy - 20, "t": "comet Encke", "a": "end", "c": GOLD, "in": 1.2},
        {"k": "cap", "x": 500, "y": 360, "t": "the Taurid stream", "in": .2}]}
    s1 = like(s0, cam=[1.1, cx, cy - 100], add=[{"k": "circle", "x": cx + AU * math.cos(math.radians(a_)), "y": cy + AU * math.sin(math.radians(a_)), "r": 9, "fill": "#cfe6ff", "c": "none", "w": 0, "in": .3 + i * .5} for i, a_ in enumerate((200, 20))] +
                [{"k": "label", "x": cx + AU * math.cos(math.radians(200)) - 20, "y": cy + AU * math.sin(math.radians(200)) + 44, "t": "October · November", "st": "small", "a": "end", "c": "#cfe6ff", "in": .5},
                 {"k": "label", "x": cx + AU * math.cos(math.radians(20)) + 20, "y": cy + AU * math.sin(math.radians(20)) - 30, "t": "late June · July", "st": "small", "a": "start", "c": "#cfe6ff", "in": 1.0}])
    s2 = stat("144", "fireballs", "recorded in one 2015 outburst, when Earth crossed the resonant swarm: a bunched-up part of the stream held in step by Jupiter", "Spurný et al. 2017")
    # Tunguska: a flattened forest, radial
    trees = [{"k": "line", "p": [[500 + r * math.cos(math.radians(t)), 900 + r * .55 * math.sin(math.radians(t))], [500 + (r + 26) * math.cos(math.radians(t)), 900 + (r + 26) * .55 * math.sin(math.radians(t))]],
              "c": "#b89a6a", "w": 2.2, "op": .8, "in": .2 + r * .003} for r in range(40, 330, 24) for t in range(0, 360, 15)]
    s3 = {"base": "dark", "cam": [1.1, 500, 880], "els": trees + [{"k": "glow", "x": 500, "y": 900, "r": 200, "kind": "lamp", "op": .35},
          {"k": "cap", "x": 500, "y": 440, "t": "Tunguska · 30 June 1908", "in": .1},
          {"k": "label", "x": 500, "y": 1280, "t": "2,150 km² of forest flattened · no crater", "in": 1.2}]}
    s4 = quote("Clube and Napier proposed that the Taurids are the remains of a giant comet, and that its fragments arrive in bursts. They called it coherent catastrophism.", "the challengers' case · 1982 to 2010", y=700, size=40)
    # the 2025 count: bodies bigger than 100 m
    dots = [{"k": "circle", "x": 190 + (i % 14) * 46, "y": 700 + (i // 14) * 46, "r": 11, "fill": GOLD if i < 12 else "#4a3f33", "c": "none", "w": 0, "in": .2 + i * .015} for i in range(56)]
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": dots + [{"k": "cap", "x": 500, "y": 560, "t": "bodies over 100 m in the swarm · 2025 surveys", "in": .1},
          {"k": "label", "x": 500, "y": 960, "t": "about 9 to 14 found · not hundreds", "c": GOLD, "in": 1.2},
          {"k": "label", "x": 500, "y": 1005, "t": "a parent nearer 10 km than 50 to 100 km", "st": "small", "in": 1.5}]}
    tl, ax = timeline(2024, 2040, [(2024, "2024"), (2028, "2028"), (2032, "2032"), (2036, "2036"), (2040, "2040")], "When the swarm comes close again", y=820)
    tl["els"] += event(ax, 2032, "November 2032", row=0, c=GOLD, i=.3, sub="a survey is called for") + event(ax, 2036, "June 2036", row=1, c=GOLD, i=.7)
    s6 = tl
    s7 = like(s0, cam=[1.2, cx, cy - 60])
    shots = [s0, s1, s2, s3, s4, s5, s6, s7]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE TAURIDS][sfx:boom][act:wonder, setting the scene]^Twice a year, Earth flies through the wreckage of a ^*comet*.",
                      "[d:tension][cam:1.15|0|0][act:reporting the claim, even]Some say it's the comet that ^ended the Ice Age world. [gap:0.4][act:low, a hint of suspense][tune:fall]And it ^isn't finished."], cut=False),
        B("world", 1, ["[d:calm][k:COMET ENCKE][act:plain, informative]The parent is comet ^Encke, five kilometres across, on a ^three-year loop around the Sun.",
                       "[d:build][go:2|0][act:building, a real event]In {2015|twenty fifteen}, Earth crossed a ^dense knot of it. [sfx:shimmer][act:delighted, vivid]Cameras caught a hundred and forty-four ^fireballs. [act:leaning in, weightier]And two ^asteroids in the knot, ^hundreds of metres wide."]),
        B("collision", 3, ["[d:build][k:1908][act:grave, storytelling]In {1908|nineteen oh eight}, something ^exploded over Siberia and flattened two ^thousand square kilometres of forest. [act:pointed, lower][tune:fall]It arrived in ^Taurid season.",
                           "[d:tension][go:4|0][act:laying out the claim, fair]So the idea: a ^giant comet broke up, and its pieces keep ^coming. [act:low, brief][tune:fall]In ^bursts."]),
        B("cost", 5, ["[d:build][k:2025 · THE COUNT][act:brisk, the test][tune:fall]Then astronomers ^counted. [act:precise, reading the result]Bodies over a hundred metres in the swarm: about ^nine to ^fourteen. [d:aside][act:gentle, pointed][tune:fall]Not the ^hundreds a giant would leave. [act:dry, a small smile][tune:fall]Giants are hard to ^misplace."]),
        B("reversal", 6, ["[d:reveal][k:THE TWIST][act:the turn, sincere][tune:fall]But the ^swarm is ^real. [act:clear, looking ahead]And it returns close@adj in November {2032|^twenty thirty-two}, and June {2036|^twenty thirty-six}. [sfx:hit][act:practical, calm urgency][tune:fall]Specialists want telescopes ^ready."]),
        B("tag", 7, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A resonant ^swarm? [act:firm, certain][tune:highfall]^*Established*. [act:the next question, even][tune:rise]A ^giant comet behind the Younger Dryas? [act:the verdict, level-headed][tune:fall]Not ^shown.",
                     "[d:tension][p:0.93][gap:0.4][act:the last word, quiet anticipation][tune:fall]The next test has a ^*date*."]),
    ]
    return EP("taurids", "03.04", "The Comet That Keeps Coming Back", "taurid-stream", "unsupported", "Is a giant comet still breaking up over our heads?", "It isn't *finished*.", beats, shots,
              "Whipple 1940 · Clube & Napier 1982, 1990 · Spurný et al. 2017 · Li et al. 2025 · Wiegert et al. 2025",
              "Earth crosses the Taurid stream twice a year. The giant-comet idea, the 2015 fireball outburst, Tunguska, and the 2025 surveys that counted the swarm.",
              ["#Taurids", "#Comet", "#Tunguska", "#Astronomy", "#Science"])


def taurids_m():
    """The Taurids as one continuous take (see mural.py): the comet's trail and Earth's two crossings, the 2015 knot and its fireballs,
    a forest felled from the sky, the giant-comet idea, the 2025 count, and the dates of the next test are drawn."""
    import random as _r
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN, GREEN, AU
    # 0 · the inner solar system, long axis upright: the Sun, Earth's orbit, comet Encke's stretched loop and its trail of debris
    SX, SY, A1 = 500, 1000, 150
    a, e = 2.22 * A1, .85
    p_ = a * (1 - e * e)
    def P(th, off=0):                                    # a point of Encke's orbit, th from perihelion (straight down), off: drift across the stream
        r = p_ / (1 + e * math.cos(th)) + off
        return [round(SX + r * math.sin(th), 1), round(SY + r * math.cos(th), 1)]
    orbit = [P(math.radians(d)) for d in range(0, 361, 4)]
    cross = math.acos((p_ / A1 - 1) / e)
    XL, XR = P(-cross), P(cross)
    plan = {"base": "dark", "stars": 160, "cam": [1.25, 500, 826], "els": [
                glow(SX, SY, 70, -1, .9, "sun"), dot(SX, SY, 14, "#ffe2a8", -1),
                {"k": "circle", "x": SX, "y": SY, "r": A1, "c": "#cfe6ff", "w": 2, "in": .2, "fx": "draw", "dur": 1.2},
                label(SX + A1 * .72 + 14, SY + A1 * .72 + 22, "Earth's orbit", .8, "#cfe6ff", 28, "start")] + \
           [{"k": "line", "p": [P(math.radians(d), (k - 3) * 7) for d in range(0, 361, 4)], "c": AU, "w": 1.4, "op": .35, "keepop": True, "curve": True, "in": 3.8 + .12 * k, "fx": "draw", "dur": 1.6} for k in range(7)] + \
           [{"k": "line", "p": orbit, "c": AU, "w": 2.2, "curve": True, "in": 3.2, "fx": "draw", "dur": 1.8},
            glow(XL[0], XL[1], 46, 1.0, .9, "scan"), glow(XR[0], XR[1], 46, 1.4, .9, "scan")]}
    hook2 = question(XL[0] - 60, XL[1] - 90, 4.9, 70)
    nuc = P(math.radians(-55))
    shed = []
    rr = _r.Random(5)
    for k in range(46):
        th = math.radians(rr.uniform(20, 340)); q = P(th, rr.uniform(-16, 16))
        shed.append(dot(q[0], q[1], 3.2, "#f2dcb4", round(11.6 + .04 * k, 2), op=.9))
    encke = [glow(nuc[0], nuc[1], 50, .6, .9, "lamp"), dot(nuc[0], nuc[1], 7, BN, .6),
             line([nuc, [nuc[0] - 80 * math.sin(math.radians(55)), nuc[1] + 80 * math.cos(math.radians(55))]], .7, "#fff3d6", 5, dur=.6),
             label(SX - 20, SY + A1 + 52, "comet Encke", 1.6, BN, 30), label(SX - 20, SY + A1 + 88, "5 km wide", 4.6, BN, 28),
             arrow([P(math.radians(d)) for d in range(150, 211, 6)], 6.8, BN, 3, dur=1.0), label(SX, P(math.pi)[1] - 30, "every 3.3 years", 7.2, BN, 28)] + shed + \
            [dot(XL[0], XL[1], 13, "#5fa8c9", 19.8, fx="pop"), label(XL[0] - 26, XL[1] - 30, "Oct · Nov", 20.2, "#cfe6ff", 30, "end"),
             dot(XR[0], XR[1], 13, "#5fa8c9", 22.6, fx="pop"), label(XR[0] + 26, XR[1] - 30, "late June · July", 23.0, "#cfe6ff", 30, "start")]
    # 2 · 2015: Earth runs into a dense knot of the stream, held together by Jupiter; 144 fireballs; two asteroids in the knot
    rr = _r.Random(8)
    band = [dot(round(x, 1), round(620 - .32 * (x - 500) + rr.uniform(-38, 38), 1), round(rr.uniform(1.5, 3.2), 1), "#f2dcb4", .2 + .004 * k, op=.6) for k, x in enumerate([rr.uniform(-20, 1020) for _ in range(150)])]
    knot = [dot(round(560 + rr.gauss(0, 34), 1), round(600 + rr.gauss(0, 22), 1), round(rr.uniform(2, 4), 1), AU, round(2.4 + .01 * k, 2)) for k in range(70)]
    sky_streaks = []
    RX, RY = 760, 800
    while len(sky_streaks) < 144:                       # exactly 144, radiating from one point of the sky, as a meteor shower does
        k = len(sky_streaks)
        ang = math.radians(rr.uniform(100, 178)); d0 = rr.uniform(40, 560); L = rr.uniform(26, 80)
        x0, y0 = RX + d0 * math.cos(ang), RY + d0 * math.sin(ang)
        if not (60 < x0 < 940 and 850 < y0 < 1200):
            continue
        sky_streaks.append(line([[round(x0, 1), round(y0, 1)], [round(x0 + L * math.cos(ang), 1), round(y0 + L * math.sin(ang), 1)]], round(8.6 + .021 * k, 3), "#fff3d6" if k % 3 else AU, 2.4, dur=.25))
    knotp = {"base": "dark", "stars": 120, "cam": [1.0, 500, 880], "els": band + knot + [
                glow(560, 600, 120, 2.8, .6, "lamp"), label(560, 690, "the knot", 3.2, AU, 30),
                dot(330, 760, 15, "#5fa8c9", 1.0), arrow([[300, 790], [400, 720], [520, 630]], 1.4, "#9fd0ff", 3, dur=1.2), label(300, 830, "Earth", 1.4, "#cfe6ff", 28),
                {"k": "circle", "x": 880, "y": 330, "r": 70, "fill": "#c9925a", "c": "#f2c98e", "w": 2, "in": 6.6, "fx": "pop"}] + \
             [line([[830, 330 + 22 * j], [930, 330 + 22 * j]], 6.8, "#8a5a32", 4, draw=False, op=.7) for j in (-2, -1, 0, 1, 2)] + [
                label(880, 440, "Jupiter", 7.0, "#f2c98e", 30),
                line([[820, 370], [640, 560]], 7.2, "#f2c98e", 2.5, "inferred", .8), line([[840, 400], [680, 590]], 7.4, "#f2c98e", 2.5, "inferred", .8),
                {"k": "poly", "p": [[-10, 1260], [300, 1252], [620, 1262], [1010, 1250], [1010, 1778], [-10, 1778]], "fill": "#14110e", "c": "#4a3f33", "w": 2, "in": -1},
                bx(150, 1222, 56, 34, "#2a2622", "#cbbca8", 2, 4, 8.0), dot(178, 1239, 9, "#9fd0ff", 8.0), label(178, 1300, "cameras", 8.2, BN, 28)] + sky_streaks + [
                label(640, 1320, "144 fireballs", 10.2, AU, 34, st="serif"),
                {"k": "poly", "p": [[490, 470], [520, 452], [552, 462], [560, 492], [532, 510], [498, 500]], "fill": "#7d6a58", "c": "#e9d3ab", "w": 2, "curve": True, "in": 11.8, "fx": "pop"},
                {"k": "poly", "p": [[608, 512], [632, 500], [654, 512], [650, 538], [624, 546], [606, 532]], "fill": "#7d6a58", "c": "#e9d3ab", "w": 2, "curve": True, "in": 12.2, "fx": "pop"},
                label(575, 410, "hundreds of metres", 13.6, BN, 30)]}
    # 3 · 1908: a burst in the sky over a forest; trees felled outward over 2,000 km² (a 46 km square); no crater; 30 June
    rr = _r.Random(3)
    trees = [dot(round(x, 1), round(y, 1), 2.6, "#4f6b3a", -1) for x, y in [(rr.uniform(40, 960), rr.uniform(500, 1300)) for _ in range(520)]]
    R0, CXT, CYT = 300, 500, 900
    felled = []
    for rad in range(40, R0 + 1, 22):
        for d in range(0, 360, 12):
            t = math.radians(d + (rad % 3) * 4)
            felled.append(line([[round(CXT + rad * math.cos(t), 1), round(CYT + rad * math.sin(t), 1)], [round(CXT + (rad + 18) * math.cos(t), 1), round(CYT + (rad + 18) * math.sin(t), 1)]],
                               round(5.0 + rad * .008, 2), "#c9a46a", 2.4, dur=.35))
    side = math.sqrt(math.pi) * R0
    tung = {"base": "dark", "cam": [1.05, 500, 920], "els": trees + [
                glow(CXT, CYT, 260, 2.8, .9, "lamp"), glow(CXT, CYT, 120, 2.8, 1, "red")] +
            [ring(CXT, CYT, 60 + 70 * k, 3.0 + .25 * k, "#ffe2a8", 2.5, dur=.5) for k in range(4)] + felled + [
                bx(CXT - side / 2, CYT - side / 2, side, side, "none", BN, 2.5, 2, 9.0, style="inferred"),
                label(CXT, CYT - side / 2 - 18, "46 km", 10.4, BN, 30),
                {"k": "circle", "x": CXT, "y": CYT, "r": 34, "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": 13.6}, strike(CXT - 46, CYT + 40, CXT + 46, CYT - 40, 14.8),
                label(CXT, CYT + 80, "no crater", 15.0, BN, 30),
                label(CXT, 390, "30 June 1908", 16.6, AU, 40, st="serif")]}
    # 4 · the idea: a giant comet breaks up, and its pieces keep coming, in bursts
    GX, GY = 300, 520
    frag = [(GX + 70 * math.cos(math.radians(d)), GY + 46 * math.sin(math.radians(d))) for d in (10, 60, 120, 170, 220, 280, 330)]
    idea = {"base": "dark", "stars": 140, "cam": [1.05, 500, 900], "els": [
                label(500, 380, "1980s", 3.2, LILAC, 40, st="serif"),
                glow(GX, GY, 150, 4.6, .9, "lamp"), {"k": "circle", "x": GX, "y": GY, "r": 46, "fill": "#e8dcc6", "c": "#fff6e6", "w": 2, "in": 4.6, "fx": "pop"},
                line([[GX - 40, GY - 30], [80, 330]], 4.8, "#fff3d6", 10, dur=.8),
                line([[GX - 30, GY - 20], [GX + 10, GY + 10], [GX - 5, GY + 40]], 5.8, "#3a2c20", 3, dur=.4),
                line([[GX + 20, GY - 44], [GX + 5, GY - 5], [GX + 40, GY + 20]], 5.9, "#3a2c20", 3, dur=.4)] + \
            [dot(round(x, 1), round(y, 1), 12 - (k % 3) * 2, "#e8dcc6", 6.2 + .1 * k) for k, (x, y) in enumerate(frag)] + \
            [arrow([[x, y], [x + 200 + 40 * k, y + 380 - 10 * k], [770, 1120]], round(7.6 + .15 * k, 2), LILAC, 2.5, "claimed", 1.0) for k, (x, y) in enumerate(frag[::2])] + [
                dot(800, 1150, 18, "#5fa8c9", 7.4), label(800, 1210, "Earth", 7.4, "#cfe6ff", 28)] + \
            [g for k in range(3) for g in (glow(800, 1150, 70 + 25 * k, 9.0 + .4 * k, .8, "red"), ring(800, 1150, 40 + 30 * k, 9.0 + .4 * k, RD, 3, dur=.4))]}
    # 5 · 2025: a dropped plate makes hundreds of shards; the swarm holds only nine to fourteen big ones; a 10 km parent, not 100 km
    rr = _r.Random(21)
    cells = [(140 + 38 * (k % 20), 700 + 38 * (k // 20)) for k in range(240)]
    found = rr.sample(range(240), 12)
    shards = []
    for k in range(14):
        t = 2 * math.pi * k / 14 + rr.uniform(-.15, .15); d = rr.uniform(150, 200)
        x, y = 500 + d * math.cos(t), 520 + d * .42 * math.sin(t)
        shards.append({"k": "poly", "p": [[round(x + rr.uniform(-14, 14), 1), round(y + rr.uniform(-9, 9), 1)] for _ in range(3)], "fill": "#efe6d4", "c": "none", "w": 0, "in": round(9.3 + .05 * k, 2), "fx": "pop"})
    count = {"base": "dark", "cam": [1.05, 500, 950], "els": [
                label(500, 400, "2025", 1.0, AU, 48, st="serif"),
                {"k": "poly", "p": ellipse(500, 520, 110, 34, 30)[:-1], "fill": "#efe6d4", "c": "#fff", "w": 2, "curve": True, "in": 8.2, "fx": "pop"},
                line([[440, 510], [500, 530], [560, 505]], 9.0, "#8a7a66", 2.5, dur=.3), line([[500, 530], [520, 550]], 9.1, "#8a7a66", 2.5, dur=.3)] + shards + \
             [{"k": "circle", "x": x, "y": y, "r": 10, "fill": "none", "c": LILAC, "w": 1.6, "style": "claimed", "in": round(6.0 + .005 * k, 3)} for k, (x, y) in enumerate(cells)] + \
             [{"k": "circle", "x": cells[k][0], "y": cells[k][1], "r": 12, "fill": AU, "c": "#fff3d0", "w": 1.5, "in": round(13.0 + .08 * j, 2), "fx": "pop"} for j, k in enumerate(found)] + \
             [label(500, 660, "hundreds expected", 6.6, LILAC, 30), label(500, 1180, "9 to 14 found", 13.8, AU, 32),
              {"k": "circle", "x": 300, "y": 1300, "r": 12, "fill": AU, "c": "#fff3d0", "w": 1.5, "in": 19.4, "fx": "pop"}, label(300, 1350, "10 km", 19.6, AU, 30),
              {"k": "circle", "x": 640, "y": 1300, "r": 110, "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": 20.8}, label(640, 1310, "100 km", 21.0, LILAC, 30)]}
    # back on the plan: the swarm is real; it comes back in 2032 and 2036; telescopes; the verdict
    swarmL = [dot(round(XL[0] + rr.gauss(0, 14), 1), round(XL[1] + rr.gauss(0, 10), 1), 3, AU, round(.4 + .01 * k, 2)) for k in range(30)]
    swarmR = [dot(round(XR[0] + rr.gauss(0, 14), 1), round(XR[1] + rr.gauss(0, 10), 1), 3, AU, round(5.8 + .01 * k, 2)) for k in range(30)]
    ahead = swarmL + [glow(XL[0], XL[1], 70, .6, .8, "lamp"), label(XL[0], XL[1] + 66, "2032", 4.6, AU, 34, st="serif")] + swarmR + \
            [glow(XR[0], XR[1], 70, 6.0, .8, "lamp"), label(XR[0], XR[1] + 66, "2036", 6.6, AU, 34, st="serif"),
             {"k": "fan", "x": SX - 20, "y": SY + A1 - 4, "a0": 215, "a1": 255, "r": 260, "c": "#9fd0ff", "n": 7, "in": 8.4}]
    verdict = [ring(XL[0], XL[1], 52, 3.5, GREEN, 4), ring(XR[0], XR[1], 52, 3.7, GREEN, 4),
               {"k": "circle", "x": SX, "y": P(math.pi)[1] + 90, "r": 75, "fill": "rgba(201,193,238,.08)", "c": LILAC, "w": 3, "style": "claimed", "in": 5.0}] + \
              question(SX, P(math.pi)[1] + 120, 11.2, 70) + [glow(XL[0], XL[1] + 56, 80, 14.4, .8, "lamp")]
    shots = [plan, {}, knotp, tung, idea, count, {}, {}]
    ep = _take(taurids, shots, [0, 1, 3, 5, 6, 7])
    return remix(ep, scenes={0: plan, 2: knotp, 3: tung, 4: idea, 5: count}, alias={1: 0, 6: 0, 7: 0}, _rewrite=False,
                 line_adds={(0, 1): (hook2, [1.3, 450, 880])},
                 beat_adds={1: (encke, [1.2, 500, 850]), 4: (ahead, [1.3, 500, 960]), 5: (verdict, [1.2, 500, 850])})


# ---------------------------------------------------------------- 03.05 The Mammoth Mystery
def mammoth(x, y, h, i=.2, c="#1a1511"):
    """A woolly mammoth in silhouette, facing left: domed head, high shoulder hump, a back that slopes to the rump,
    long curved tusks. h is shoulder height in px (a mammoth stood about 3 m; a person 1.7)."""
    s = h / 100
    P = [(-30, -102), (0, -98), (30, -84), (55, -62), (62, -40), (60, -15), (52, 18), (50, 52), (30, 52), (28, 22), (20, 10), (-10, 8), (-40, 12), (-40, 52), (-60, 52),
         (-62, 20), (-66, -20), (-72, -42), (-88, -42), (-98, -25), (-106, 0), (-108, 20), (-114, 28), (-118, 14), (-112, -8), (-104, -32), (-100, -56), (-98, -75), (-90, -90), (-72, -97), (-55, -90)]
    body = [[x + px * s, y + py * s] for px, py in P]
    tusk = [[x + px * s, y + py * s] for px, py in [(-86, -40), (-108, -20), (-128, -26), (-138, -50)]]
    hair = []
    return [{"k": "poly", "p": body, "fill": c, "c": c, "w": 1, "curve": True, "in": i},
            {"k": "line", "p": tusk, "c": "#efe6d4", "w": 4.2 * s, "curve": True, "in": i + .2}] + hair


def megafauna():
    s0 = {"base": "sky", "tod": "night", "ground": 1150, "sun": False, "moon": [760, 500, 28], "cam": [1.3, 500, 990],
          "els": mammoth(470, 1150, 200, .1) + silhouette(780, 1150, 112, t=None, i=.6) + [{"k": "q", "x": 500, "y": 780, "size": 70, "in": 1.2, "fx": "pop"}]}
    # 35 genera: a grid of silhouettes going dark
    kinds = ["mammoth", "mastodon", "horse", "camel", "ground sloth", "sabre-tooth", "dire wolf", "glyptodon", "short-faced bear", "giant beaver"]
    grid = [{"k": "circle", "x": 160 + (i % 7) * 113, "y": 640 + (i // 7) * 113, "r": 34, "fill": "#8c6f4c", "c": "#e9dccb", "w": 1.4, "in": .1 + i * .04} for i in range(35)]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grid + [{"k": "num", "x": 500, "y": 500, "t": "35", "u": "genera lost", "in": .1, "fx": "pop"},
          {"k": "label", "x": 500, "y": 1260, "t": ", ".join(kinds[:6]) + "...", "st": "small", "in": 1.6}]}
    # the black mat: a section
    sec = {"base": "section", "tod": "night", "ground": 700, "lx": 40, "layers": [{"d": 0, "c": "#6f5a43", "t": "younger soils"}, {"d": 250, "c": "#0d0b09", "t": ""}, {"d": 290, "c": "#8a6a4a", "t": "Clovis camp · mammoth bones"}],
           "cam": [1.25, 500, 960], "els": [{"k": "label", "x": 500, "y": 975, "t": "the black mat · c. 12,900 years ago", "c": "#cfe6ff", "in": .4},
                                            {"k": "label", "x": 500, "y": 1060, "t": "the last mammoths lie just beneath it", "st": "small", "in": 1.0}]}
    s2 = sec
    # the staggered dates, continent by continent
    tl, ax = timeline(-50000, 0, [(-50000, "50,000"), (-40000, "40,000"), (-30000, "30,000"), (-20000, "20,000"), (-10000, "10,000"), (0, "today")], "When the giants went · years ago", y=1000)
    tl["els"] += [{"k": "band", "x0": ax.x(-48000), "x1": ax.x(-44000), "y": 900, "h": 18, "c": OCHRE, "t": "Australia's giants", "in": .3},
                  {"k": "band", "x0": ax.x(-13800), "x1": ax.x(-11400), "y": 820, "h": 18, "c": AMBER, "t": "North America", "in": .6},
                  {"k": "band", "x0": ax.x(-14000), "x1": ax.x(-7700), "y": 740, "h": 18, "c": SCAN, "t": "woolly rhino to giant deer", "in": .9},
                  {"k": "band", "x0": ax.x(-5600), "x1": ax.x(-4000), "y": 660, "h": 18, "c": "#cfe6ff", "t": "island mammoths", "in": 1.2},
                  {"k": "line", "p": [[ax.x(-12900), 1000], [ax.x(-12900), 620]], "c": GOLD, "w": 2, "style": "claimed", "in": 1.4},
                  {"k": "label", "x": ax.x(-12900), "y": 600, "t": "Younger Dryas", "c": GOLD, "st": "small", "in": 1.5}]
    s3 = tl
    # Wrangel Island: an iso islet with the last mammoths
    isle = [{"t": "flat", "pts": [[-40, -22], [-10, -34], [30, -28], [46, -4], [30, 22], [-6, 30], [-38, 14]], "y": .2, "c": "#6d7a4a", "op": 1},
            {"t": "person", "x": 0, "y": .2, "z": 0, "h": 5.5}, {"t": "person", "x": 14, "y": .2, "z": 8, "h": 5.5}, {"t": "person", "x": -12, "y": .2, "z": -8, "h": 5.5},
            L_(0, 12, "Wrangel Island · mammoths until c. 4,000 years ago", "#cfe6ff")]
    s4 = iso(isle, cam=[1, 500, 900], s=6, x=500, y=980, az=-30, spin=1.5, el=.5, table={"r": 70, "rz": 55, "grid": 10, "strata": [{"h": 2, "c": "#3f86b0"}, {"h": 6, "c": "#2b5d7d"}], "c": "#3f86b0"})
    s4["els"] += [{"k": "label", "x": 500, "y": 1370, "t": "the pyramids were already old when the last mammoth died", "st": "small", "in": 1.2}]
    s5 = quote("A series of regional collapses, not one global blow: the timing differs from continent to continent, and tends to follow people and the climate swings.", "the mainstream reading", y=700, size=40)
    s6 = like(s0, cam=[1.3, 480, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE ICE AGE GIANTS][sfx:boom][act:wonder, naming the giants][tune:level]Mammoths. [act:same rhythm][tune:level]Mastodons. [act:delighted, a little bigger][tune:fall]Sloths the size of a ^car. [act:slowing down][tune:level]Then... [act:quiet, final][tune:highfall]^*gone*.",
                      "[d:tension][cam:1.15|0|0][act:posing the big question, intrigued][tune:rise]Did ^one blow from the ^sky kill them all?"], cut=False),
        B("world", 1, ["[d:calm][k:NORTH AMERICA][act:plain, sober facts]North America lost about ^thirty-five kinds of large animal. [act:precise, unhurried]Their last dates cluster between ^thirteen thousand eight hundred and ^eleven thousand four hundred years ago.",
                       "[d:build][go:2|0][sfx:shimmer][act:intrigued, a clue]At many sites, a dark layer, the ^black mat, lies right on ^top of the last mammoth bones."]),
        B("collision", 3, ["[d:build][k:THE WORLD][act:the turn, widening the view][tune:fall]But zoom ^out. [act:counting them off, brisk][tune:level]^Australia's giants went ^forty-six thousand years ago. [act:continuing, same pace][tune:level]The woolly ^rhino, ^fourteen thousand. [act:the surprise, a touch slower][tune:fall]The giant ^deer lived on to ^seven thousand seven hundred."]),
        B("cost", 4, ["[d:build][k:WRANGEL ISLAND][act:wonder, a remarkable fact]And on an island in the ^Arctic, [count:4,000|years ago]mammoths survived until about ^four thousand years ago. [d:aside][act:playful, lighter]The ^pyramids were ^already standing. [act:mischievous, childlike delight][tune:fall]Somewhere, a mammoth could have watched the ^news."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:the reveal, clear and deliberate]So the deaths were staggered, continent by continent, [sfx:hit]and they tend to follow two things: the arrival of ^people, and the wild ^climate swings of the melt."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]A ^single cataclysm? [act:the verdict, firm][tune:fall]*Ruled ^out* by the dates. [act:even, open-handed][tune:fall]^Hunting, ^climate, or ^both? [act:honest, level-headed][tune:fall]Still ^argued.",
                     "[d:tension][p:0.93][act:quiet, certain][tune:fall]The giants didn't fall in ^one night. [act:the last word, slow and weighty][tune:fall]They fell over ^*forty thousand years*."]),
    ]
    return EP("mammoths", "03.05", "The Mammoth Mystery", "megafauna-extinction", "debunked", "Did one cataclysm kill the Ice Age giants?", "Then... *gone*.", beats, shots,
              "Faith & Surovell 2009, PNAS · Haynes 2008, PNAS · Roberts et al. 2001, Science · Stuart et al. 2004 · Dehasque et al. 2024, Cell",
              "The Ice Age megafauna vanished, but not all at once: Australia 46,000 years ago, North America c. 13,000, Wrangel Island 4,000. What that does to the one-cataclysm idea.",
              ["#Mammoth", "#IceAge", "#Extinction", "#Science", "#History"])


def _sloth(x, y, h, i=.2, c="#1a1511"):
    """A giant ground sloth on all fours, facing left, in silhouette: small head, heavy humped body, thick tail. h: height at the hips, px."""
    s = h / 100
    P = [(-118, -52), (-122, -66), (-108, -78), (-90, -76), (-72, -92), (-40, -112), (0, -120), (40, -112), (70, -96), (92, -70), (112, -42), (128, -10), (132, 4), (110, 4),
         (96, -12), (80, -20), (76, 4), (54, 4), (50, -34), (-30, -38), (-34, 4), (-56, 4), (-60, -40), (-84, -50), (-100, -44)]
    return [{"k": "poly", "p": [[round(x + px * s, 1), round(y + py * s, 1)] for px, py in P], "fill": c, "c": c, "w": 1, "curve": True, "in": i}]


def mammoths_m():
    """The mammoth mystery as one continuous take (see mural.py): the giants and their vanishing, thirty-five lost kinds and the carbon
    candle, the black mat above the bones, the staggered dates around the world, the last island mammoths, and the weighing are drawn."""
    import random as _r
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN, GREEN, AU
    SKY, GROUND, SIL = "#1d1813", "#2a211a", "#d2b48c"
    # 0 · the hook: a mammoth, a mastodon, a ground sloth the size of a car, a person for scale; then they are gone (ghost outlines)
    G = 1200
    def beast(kind, x, h, at, gone):
        gy = G - .52 * h if kind == "m" else G - .04 * h            # feet on the ground
        b = mammoth(x, gy, h, at, SIL) if kind == "m" else _sloth(x, gy, h, at, SIL)
        er = mammoth(x, gy, h, gone, SKY) if kind == "m" else _sloth(x, gy, h, gone, SKY)
        for e in er:
            e["w"] = (e.get("w") or 1) + 3; e["c"] = SKY
        ghost = [dict(e, fill="none", c="#b3a48c", w=2, style="claimed", **{"in": gone + .3}) for e in b if e["k"] == "poly"]
        return b, er + ghost
    m1, g1 = beast("m", 300, 160, .2, 10.2)
    m2, g2 = beast("m", 680, 130, .9, 10.3)
    m3, g3 = beast("s", 828, 72, 1.6, 10.4)
    car = [{"k": "line", "p": [[722, G], [722, G - 30], [742, G - 36], [771, G - 64], [847, G - 68], [887, G - 38], [927, G - 34], [931, G]], "c": "#cfe6ff", "w": 2.5, "style": "inferred", "in": 2.8, "fx": "draw", "dur": .8},
           {"k": "circle", "x": 757, "y": G - 4, "r": 15, "c": "#cfe6ff", "w": 2.5, "style": "inferred", "in": 3.0}, {"k": "circle", "x": 892, "y": G - 4, "r": 15, "c": "#cfe6ff", "w": 2.5, "style": "inferred", "in": 3.0},
           label(825, G + 60, "a car", 3.2, "#cfe6ff", 28)]
    hook = {"base": "dark", "stars": 150, "cam": [1.15, 500, 960], "els": [
                {"k": "rect", "x": -10, "y": -10, "w": 1020, "h": G + 10, "fill": SKY, "c": "none", "sw": 0, "in": -1},
                {"k": "poly", "p": [[-10, G], [1010, G], [1010, 1778], [-10, 1778]], "fill": GROUND, "c": "#8c7152", "w": 2, "in": -1},
                {"k": "poly", "p": [[-10, G], [-10, G - 60], [180, G - 90], [420, G - 50], [640, G - 100], [860, G - 60], [1010, G - 80], [1010, G]], "fill": "#241d17", "c": "none", "w": 0, "in": -1, "curve": True},
                glow(500, G - 40, 420, -1, .25, "lamp")] +
            m1 + m2 + m3 + [person(450, G, 98, 4.6, "#efe6d4")] + car + g1 + g2 + g3}
    sky_blow = [line([[960, 300], [700, 560]], .6, LILAC, 4, "claimed", 1.0), glow(700, 560, 90, 1.4, .9, "red")] + question(560, 700, 2.6, 80)
    # 1 · thirty-five kinds lost; bones keep time like a candle; the last dates cluster 13,800 to 11,400 years ago
    toks = []
    for k in range(35):
        x, y = 170 + 110 * (k % 7), 420 + 92 * (k // 7)
        toks += [{"k": "circle", "x": x, "y": y, "r": 34, "fill": "#a8845c", "c": "#f2dcb4", "w": 1.5, "in": round(.3 + .04 * k, 2), "fx": "pop"},
                 {"k": "circle", "x": x, "y": y, "r": 34, "fill": "#2a211a", "c": "#6a5a48", "w": 1.5, "in": round(2.0 + .045 * k, 2)}]
    X1 = lambda ya: 150 + 700 * (16000 - ya) / 6000
    rr = _r.Random(4)
    last = [round(rr.triangular(11500, 13700, 12700)) for _ in range(35)]
    hist = {}
    for t in last:
        b = 11500 + 200 * ((t - 11500) // 200) + 100
        hist[b] = hist.get(b, 0) + 1
    cand = []
    for j, (x, h) in enumerate(((420, 130), (560, 85), (700, 40))):
        at = 14.4 + .6 * j
        cand += [bx(x - 22, 1080 - h, 44, h, "#efe6d4", "#fff", 1.5, 4, at, fx="fill"), line([[x, 1080 - h], [x, 1068 - h]], at + .2, "#3a2c20", 2, draw=False),
                 glow(x, 1050 - h, 40, at + .3, .9, "lamp"), dot(x, 1052 - h, 7, "#ffe2a8", at + .3)]
    kinds = {"base": "dark", "cam": [1.08, 500, 910], "els": toks + [
                line([[120, 1080], [880, 1080]], 9.2, "#8c7152", 2, draw=False),
                line([[200, 1060], [290, 1030]], 9.4, "#efe6d4", 12, draw=False), dot(196, 1066, 10, "#efe6d4", 9.4), dot(296, 1026, 10, "#efe6d4", 9.4),
                glow(245, 1045, 70, 10.4, .8, "scan")] + [dot(245 + 30 * math.cos(a), 1045 + 30 * math.sin(a), 3, "#9fd0ff", 10.6 + .05 * k) for k, a in enumerate([0, 1.3, 2.5, 3.8, 5.0])] + cand + [
                line([[150, 1300], [850, 1300]], 17.0, "#e9dccb", 2.5, dur=.8)] + [line([[X1(y), 1290], [X1(y), 1310]], 17.2, "#e9dccb", 2, draw=False) for y in (16000, 14000, 12000, 10000)] + [
                line([[X1(13800), 1262], [X1(11400), 1262]], 19.6, AU, 18, dur=1.4)] +
             [dot(round(X1(b), 1), round(1236 - 13 * j, 1), 5.5, "#f2dcb4", round(18.0 + .04 * (k + j), 2)) for k, (b, n) in enumerate(sorted(hist.items())) for j in range(n)] +
             [label(X1(13800), 1350, "13,800", 20.0, AU, 28), label(X1(11400), 1350, "11,400", 21.6, AU, 28), label(500, 1395, "years ago", 22.4, "#cbbca8", 26)]}
    # 2 · the black mat: layers piling up like pages; the bones beneath, the dark layer just above
    bones = [{"k": "line", "p": [[300, 1110], [360, 1060], [450, 1050], [510, 1075]], "c": "#efe6d4", "w": 9, "curve": True, "in": .8},
             {"k": "line", "p": [[620, 1120], [700, 1112], [770, 1120]], "c": "#efe6d4", "w": 8, "in": 1.0}] + \
            [{"k": "line", "p": [[580 + 28 * j, 1125], [598 + 28 * j, 1078], [616 + 28 * j, 1125]], "c": "#e3d6be", "w": 4, "curve": True, "in": 1.2 + .05 * j} for j in range(5)] + \
            [dot(470, 1120, 14, "#efe6d4", 1.4), dot(820, 1100, 11, "#efe6d4", 1.5)]
    mat = {"base": "dark", "stars": 50, "cam": [1.2, 500, 1020], "els": [
                bx(-10, 1150, 1020, 300, "#5a4632", r=0, at=-1), bx(-10, 1000, 1020, 150, "#8a6a4a", r=0, at=.2)] + bones + [
                label(500, 1205, "the last mammoth bones", 9.6, BN, 30),
                bx(-10, 962, 1020, 38, "#0b0908", r=0, at=3.6, fx="fill", dur=.8), line([[-10, 962], [1010, 962]], 3.6, "#4a4038", 1.5, draw=False),
                bx(-10, 780, 1020, 182, "#6f5a43", r=0, at=11.0, fx="fill", dur=1.0), line([[-10, 780], [1010, 780]], 11.0, "#c9ad85", 2, draw=False),
                label(500, 945, "the black mat · c. 12,900 years ago", 4.6, "#cfe6ff", 30),
                arrow([[150, 1380], [150, 820]], 12.6, AU, 3, dur=1.2, curve=False), label(170, 1380, "older", 12.8, AU, 28, "start"), label(170, 830, "younger", 13.4, AU, 28, "start"),
                line([[200, 990], [880, 990]], 15.0, AU, 2.5, "inferred", .8), label(880, 1030, "just after", 15.4, AU, 28, "end")]}
    # 3 · the whole world: one blow would mean one moment; instead the dates are spread over tens of thousands of years
    v = View(-180, 180, -48, 78, (40, 360, 920, 460))
    X = lambda ya: 280 + 600 * (50000 - ya) / 50000
    rows = [("Australia", 1010, (134, -25), "#ec9a5a"), ("North America", 1070, (-100, 42), AU), ("woolly rhino", 1130, (125, 66), "#c9c1ee"), ("giant deer", 1190, (68, 58), GREEN)]
    from f01 import mapshot as _ms
    world = _ms(v, cam=[1.08, 500, 900], extra=[
                line([[280, 1250], [880, 1250]], .2, "#e9dccb", 2.5, dur=.8)] + [line([[X(y), 1240], [X(y), 1260]], .3, "#e9dccb", 2, draw=False) for y in (50000, 40000, 30000, 20000, 10000, 0)] +
            [label(X(y), 1294, t, .4, "#cbbca8", 26) for y, t in ((50000, "50,000"), (25000, "25,000"), (0, "today"))] + [label(580, 1336, "years ago", .5, "#cbbca8", 26)] +
            [label(266, y + 9, t, .6 + .1 * k, c, 28, "end") for k, (t, y, _, c) in enumerate(rows)] +
            [dot(*v.p(-100, 42), 9, AU, .8), glow(*v.p(-100, 42), 40, .8, .7, "lamp"), line([[X(13800), 1070], [X(11400), 1070]], .9, AU, 14, dur=.5),
             line([[X(12900), 980], [X(12900), 1225]], 7.6, LILAC, 3, "claimed", .8), label(X(12900), 960, "one moment?", 8.2, LILAC, 28),
             dot(*v.p(134, -25), 9, "#ec9a5a", 10.6), glow(*v.p(134, -25), 40, 10.6, .7, "red"), dot(X(46000), 1010, 9, "#ec9a5a", 11.0, fx="pop"), label(X(46000), 990, "46,000", 11.4, "#ec9a5a", 26),
             dot(*v.p(125, 66), 9, "#c9c1ee", 13.6), dot(X(14000), 1130, 9, "#c9c1ee", 13.9, fx="pop"), label(X(14000) - 16, 1123, "14,000", 14.2, "#c9c1ee", 26, "end"),
             dot(*v.p(68, 58), 9, GREEN, 16.6), dot(X(7700), 1190, 9, GREEN, 17.0, fx="pop"), label(X(7700) + 16, 1199, "7,700", 18.6, GREEN, 26, "start")])
    # 4 · the last mammoths on an Arctic island, 4,000 years ago, while the pyramids already stood
    isl = [[180, 640], [260, 560], [420, 540], [560, 570], [640, 640], [600, 720], [440, 760], [280, 740]]
    last_isle = {"base": "map", "cam": [1.1, 500, 900], "els": [
                {"k": "poly", "p": isl, "fill": "#6d7a4a", "c": "#e9d3ab", "w": 2, "curve": True, "in": .3},
                {"k": "poly", "p": [[q[0] + 3, q[1] + 4] for q in isl], "fill": "none", "c": "#cfe6ff", "w": 1, "curve": True, "in": .3, "op": .4, "keepop": True},
                label(420, 830, "an island in the Arctic", 1.4, "#cfe6ff", 30)] +
            mammoth(330, 680, 42, 2.4, SIL) + mammoth(430, 700, 38, 2.6, SIL) + mammoth(520, 670, 34, 2.8, SIL) + [
                {"k": "poly", "p": [[-10, 1290], [1010, 1290], [1010, 1778], [-10, 1778]], "fill": "#b8955e", "c": "#e9d3ab", "w": 2, "in": 6.2},
                {"k": "pyramid", "x": 560, "y": 1290, "w": 330, "in": 6.6, "fx": "rise"}, glow(780, 1010, 60, 6.6, .8, "sun"),
                label(560, 1350, "the pyramids of Egypt", 7.2, BN, 30),
                bx(640, 560, 120, 86, "#efe6d4", "#fff", 1.5, 3, 11.0, fx="pop")] + \
            [line([[652, 580 + 13 * j], [700, 580 + 13 * j]], 11.2, "#3a2c20", 2, draw=False) for j in range(4)] + \
            [{"k": "poly", "p": [[712, 625], [732, 590], [752, 625]], "fill": "#b8955e", "c": "none", "w": 0, "in": 11.2}]}
    # back to the world: staggered; where people spread, the giants vanished soon after; the climate swinging
    swing = [[X(20000) + 6 * k, round(890 + 22 * math.sin(k * .9) * (1 if k % 7 else 1.6), 1)] for k in range(int((X(10000) - X(20000)) / 6))]
    after = [glow(X(46000), 1010, 50, 1.6, .8, "lamp"), glow(X(12600), 1070, 50, 2.0, .8, "lamp"), glow(X(14000), 1130, 50, 2.4, .8, "lamp"), glow(X(7700), 1190, 50, 2.8, .8, "lamp")] + \
            [person(x, y + 6, 46, 7.0 + .25 * k, "#efe6d4") for k, (x, y) in enumerate([(v.p(140, -20)[0] + 26, v.p(140, -20)[1]), (v.p(-95, 40)[0] + 30, v.p(-95, 40)[1]), (v.p(110, 55)[0], v.p(110, 55)[1])])] + \
            [{"k": "line", "p": swing, "c": "#9fd0ff", "w": 3, "in": 13.0, "fx": "draw", "dur": 1.6}, label(X(15000), 846, "climate swings", 13.6, "#9fd0ff", 28)]
    # back to the giants: one blow struck out; hunting or climate on the scales; forty thousand years
    B0, BY = 330, 790
    verdict = [strike(640, 640, 780, 480, 1.8),
               line([[B0, BY + 130], [B0, BY]], 3.8, BN, 4, draw=False), line([[B0 - 140, BY], [B0 + 140, BY]], 3.8, BN, 4, draw=False),
               line([[B0 - 140, BY], [B0 - 170, BY + 60], [B0 - 110, BY + 60], [B0 - 140, BY]], 3.9, BN, 2.5, draw=False),
               line([[B0 + 140, BY], [B0 + 110, BY + 60], [B0 + 170, BY + 60], [B0 + 140, BY]], 3.9, BN, 2.5, draw=False),
               line([[B0 - 178, BY + 44], [B0 - 102, BY + 28]], 4.1, "#c9a46a", 4, draw=False), {"k": "poly", "p": [[B0 - 102, BY + 28], [B0 - 116, BY + 22], [B0 - 114, BY + 36]], "fill": "#efe6d4", "c": "none", "w": 0, "in": 4.1},
               label(B0 - 140, BY + 100, "hunting", 4.2, BN, 28), bx(B0 + 133, BY + 10, 14, 40, "#9fd0ff", r=6, at=4.6), dot(B0 + 140, BY + 56, 12, "#9fd0ff", 4.6), label(B0 + 140, BY + 100, "climate", 4.7, BN, 28),
               glow(560, 670, 110, 5.9, .9, "scan"),
               line([[120, 1330], [880, 1330]], 9.8, AU, 6, dur=2.6), label(120, 1380, "46,000", 9.8, AU, 26, "start"), label(880, 1380, "4,000 years ago", 12.4, AU, 26, "end"),
               label(500, 1300, "forty thousand years", 11.6, AU, 30)]
    shots = [hook, kinds, mat, world, last_isle, {}, {}]
    ep = _take(megafauna, shots, [0, 1, 3, 4, 5, 6])
    return remix(ep, scenes={0: hook, 1: kinds, 2: mat, 3: world, 4: last_isle}, alias={5: 3, 6: 0}, _rewrite=False,
                 line_adds={(0, 1): (sky_blow, None)}, beat_adds={4: (after, [1.08, 500, 900]), 5: (verdict, [1.15, 500, 960])})


# ---------------------------------------------------------------- 03.06 The Ledger
def _ledger_text():
    from f01 import LAURENTIDE as LA
    v = View(-135, -60, 30, 70, (40, 330, 920, 900))
    s0 = mapshot(v, extra=[{"k": "poly", "p": [v.p(*q) for q in LA], "fill": "rgba(235,245,255,.5)", "c": "#ffffff", "w": 1.6, "curve": True, "in": .2},
                           {"k": "label", "x": v.p(-95, 60)[0], "y": v.p(-95, 60)[1], "t": "Laurentide ice sheet", "st": "ital", "c": "#e6eef6", "in": .6}], cam=[1.1, 500, 880])
    grp = lambda title, col, items, y0=560: [{"k": "cap", "x": 500, "y": y0 - 80, "t": title, "c": col, "in": .1}] + \
        [{"k": "label", "x": 500, "y": y0 + i * 92, "t": t, "st": "body", "in": .3 + i * .25} for i, t in enumerate(items)]
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established", "#8fd9b0", ["the Younger Dryas cold snap, 12,900 years ago", "dozens of Ice Age floods across Washington", "a resonant Taurid swarm, crossed in 2015", "the giants went, region by region"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Open", "#f0b06a", ["what tipped the climate: meltwater, most likely", "how big the Scabland floods really were", "hunting or climate, and in what mix"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting discovery", "#c9c1ee", ["a comet at the Younger Dryas boundary", "a flood bed dated to 12,900", "a giant parent for the Taurids"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#e98a8a", ["one blast making the Carolina Bays", "one cataclysm killing all the giants"])}
    s5 = like(s0, cam=[1.25, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE SKY FELL? · THE LEDGER][sfx:boom][act:inviting, taking stock]^Five films on the end of the ^Ice Age. [act:laying out the ledger][tune:level]Here's what's ^real, what's ^open... [act:the sting, lower, deliberate][tune:fall]and what's been *ruled ^out*."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:ticking them off, steady][tune:level]The ^cold snap was real. [act:same steady rhythm][tune:level]The ^floods were real, and there were ^dozens. [act:still steady][tune:level]The comet ^swarm is real, and Earth ^crosses it. [act:quieter, closing the list][tune:fall]The ^giants went, ^region by region."]),
        B("collision", 2, ["[d:build][k:OPEN][act:thoughtful, even-handed]What tipped the ^climate: most likely ^meltwater stalling the ocean. [act:continuing the open list][tune:level]How ^big the floods were. [act:weighing both, balanced][tune:fall]How much was ^hunting, how much was ^weather."]),
        B("cost", 3, ["[d:build][k:AWAITING DISCOVERY][act:listing what's missing, measured][tune:level]A ^comet at the boundary. [act:next item, same weight][tune:level]A ^flood bed dated to the ^Younger Dryas. [act:last item, landing it][tune:fall]A ^giant parent for the Taurids. [d:aside][act:sincere, a little excited][tune:fall]Any ^one of these would ^change the ledger."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][act:firm, naming them][tune:level]^One blast punching ^half a million bays. [act:same steady weight][tune:level]^One night that killed ^every giant. [sfx:hit][gap:0.4][act:the verdict, calm and final][tune:fall]The dates say ^no."]),
        B("tag", 5, ["[d:verdict][k:WHAT WOULD CHANGE OUR MINDS][p:0.95][act:practical, clear, listing the tests][tune:level]^Blind re-sampling of the boundary layers. [act:continuing, steady][tune:level]A crater of the ^right age. [act:looking ahead, hopeful][tune:fall]^Telescopes on the swarm in {2032|^twenty thirty-two}.",
                     "[d:tension][p:0.93][act:sincere, grounded][tune:fall]Something abrupt ^did happen. [act:the last word, curious and warm][tune:fall]We just haven't caught ^*what*."]),
    ]
    return EP("sky-fell-ledger", "03.06", "The Sky Fell? · The Ledger", "younger-dryas-impact", "", "What do we know about the end of the Ice Age?", "What's real, what's open, what's *ruled out*.", beats, shots,
              "Full references for every film in the case files", "Five films, one ledger: what is established about the end of the Ice Age, what is open, and what has been ruled out.",
              ["#IceAge", "#YoungerDryas", "#Comet", "#Science", "#History"])


def ledger():
    """The ledger as one continuous film: a cabinet of the end of the Ice Age, with a sixth niche for the question itself (see cabinet.py)."""
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    curve = [{"k": "line", "p": [[-175, -22], [175, -22]], "c": "#6b5a48", "w": 2},
             {"k": "line", "p": [[-175, -22], [-175, -250]], "c": "#6b5a48", "w": 2},
             {"k": "line", "p": [[-170, -60], [-140, -72], [-122, -185], [-95, -172], [-62, -150], [-40, -158], [-22, -92], [0, -62], [38, -56], [68, -66], [88, -72],
                                 [104, -200], [135, -212], [172, -216]], "c": "#f2c98e", "w": 4, "fx": "draw", "dur": 1.8}]
    snap = [{"k": "rect", "x": -26, "y": -240, "w": 122, "h": 216, "r": 4, "fill": "#9fd0ff", "c": "none", "sw": 0, "op": .16, "keepop": True, "in": .6, "dur": 1.0}]
    LAY = [(-300, -238, "#8a6a48"), (-238, -192, "#a07a50"), (-192, -152, "#7a5c3e"), (-152, -140, "#15100c"), (-140, -82, "#9a7b56"), (-82, -10, "#6b4f35")]
    column = [{"k": "rect", "x": -95, "y": a, "w": 190, "h": b - a, "r": 0, "fill": c, "c": "none", "sw": 0} for a, b, c in LAY] + \
             [{"k": "rect", "x": -95, "y": -300, "w": 190, "h": 290, "r": 2, "fill": "none", "c": "#8a6a48", "sw": 1.5}]
    C = Cabinet([
        {"name": "The cold snap", "model": curve},
        {"name": "The Scablands", "model": mdl(scablands(), 0)},
        {"name": "The Taurid swarm", "model": mdl(taurids(), 0)},
        {"name": "The Ice Age giants", "model": mdl(megafauna(), 0)},
        {"name": "The Carolina Bays", "model": mdl(carolina_bays())},
        {"name": "The boundary layer", "model": column},
    ])
    C.build()
    CS, SC, TA, MA, CB, BL = range(6)
    spherules = C.local(BL, [{"k": "circle", "x": -80 + 17 * k, "y": -146 + (5 if k % 2 else -4), "r": 3.2, "fill": "#f5ecdc", "c": "none", "w": 0, "op": .85, "keepop": True, "in": .6 + .05 * k} for k in range(10)] +
                           [{"k": "rect", "x": -100, "y": -158, "w": 200, "h": 24, "r": 3, "fill": "none", "c": "#c9c1ee", "sw": 2, "style": "claimed", "fx": "draw", "dur": .8, "in": .4}])
    parent = C.local(TA, [{"k": "circle", "x": 110, "y": -250, "r": 44, "fill": "none", "c": "#9fd0ff", "w": 3, "style": "claimed", "in": .4}])
    probe = C.local(BL, [{"k": "line", "p": [[40, -345], [40, -40]], "c": "#9fd0ff", "w": 4, "fx": "draw", "dur": 1.2, "in": .2}] +
                        [{"k": "rect", "x": 32, "y": y - 5, "w": 16, "h": 10, "r": 2, "fill": "#9fd0ff", "c": "none", "sw": 0, "in": 1.0 + .12 * k} for k, y in enumerate((-230, -175, -146, -110, -60))])
    crater = C.local(BL, [{"k": "line", "p": [[108, -52], [122, -26], [150, -14], [178, -26], [192, -52]], "c": "#f2c98e", "w": 3, "curve": True, "style": "inferred", "fx": "draw", "dur": .9, "in": .2}])
    scope = C.local(TA, [{"k": "line", "p": [[-150, -30], [-120, -80]], "c": "#cbbca8", "w": 3, "in": .1}, {"k": "line", "p": [[-90, -30], [-120, -80]], "c": "#cbbca8", "w": 3, "in": .1},
                         {"k": "line", "p": [[-150, -92], [-96, -128]], "c": "#f5ecdc", "w": 11, "in": .2},
                         {"k": "line", "p": [[-96, -128], [60, -250]], "c": "#9fd0ff", "w": 2, "style": "inferred", "fx": "draw", "dur": 1.0, "in": .5}])
    s1 = C.step(C.cam_cell(CS), C.verdict(CS, "established", "12,900 years ago", .2) + C.local(CS, snap))
    s2 = C.step(C.cam_cell(SC), C.verdict(SC, "established", "dozens of floods", .3))
    s3 = C.step(C.cam_cell(TA), C.verdict(TA, "established", "Earth crosses it", .3))
    s4 = C.step(C.cam_cell(MA), C.verdict(MA, "established", "region by region", .3))
    s5 = C.step(C.cam_cell(CS), C.verdict(CS, "open", "meltwater, most likely", .2, frame=False) + C.question(CS, dx=C.w * .34, dy=-280, at=.5, size=60))
    s6 = C.step(C.cam_cell(SC), C.verdict(SC, "open", "how big?", .2, frame=False))
    s7 = C.step(C.cam_cell(MA), C.verdict(MA, "open", "hunting, or weather?", .2, frame=False) + C.people(MA, 2, at=.6))
    s8 = C.step(C.cam_cell(BL), C.verdict(BL, "awaiting", "a comet?", .2) + spherules)
    s9 = C.step(C.cam_cell(SC), C.verdict(SC, "awaiting", "a dated flood bed", .2, frame=False))
    s10 = C.step(C.cam_cell(TA), C.verdict(TA, "awaiting", "a giant parent?", .2, frame=False) + parent)
    s11 = C.step(C.cam_all(), [e for i in (BL, SC, TA) for e in C.wash(i, VCOL["awaiting"], at=.2 + .15 * i, op=.12)])
    s12 = C.step(C.cam_cell(CB), C.verdict(CB, "ruled", at=.2) + C.struck(CB, "one blast", at=.3))
    s13 = C.step(C.cam_cell(MA), C.verdict(MA, "ruled", at=.2) + C.struck(MA, "one night", at=.3))
    s14 = C.step(C.cam_cells([MA, CB]))
    s15 = C.step(C.cam_cell(BL), probe)
    s16 = C.step(C.cam_cell(BL), crater)
    s17 = C.step(C.cam_cell(TA), scope)
    s18 = C.step(C.cam_all())
    s19 = C.step(C.cam_all(k=.86, sy=720), C.question(BL, dx=C.w * .3, dy=-300, at=.8, size=80))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3, (0, 3): "%d|1.1" % s4}),
        2: (s5, {(0, 1): "%d|1.1" % s6, (0, 2): "%d|1.1" % s7}),
        3: (s8, {(0, 1): "%d|1.1" % s9, (0, 2): "%d|1.1" % s10, (0, 3): "%d|1.2" % s11}),
        4: (s12, {(0, 1): "%d|1.1" % s13, (0, 2): "%d|.9" % s14}),
        5: (s15, {(0, 1): "%d|.4" % s16, (0, 2): "%d|1.1" % s17, (1, 0): "%d|1.3" % s18, (1, 1): "%d|3" % s19}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/sky-fell-ledger.json)."""
    import recap
    return recap.recap(ledger, "sky-fell-ledger", None)


def EPISODES():
    return [scablands_m(), carolina_bays_m(), taurids_m(), mammoths_m(), ledger_recap()]
