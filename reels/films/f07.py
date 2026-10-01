"""File 07 · Underworlds. Halls cut into rock, and rooms built for sound.
Derinkuyu, the Longyou caves, Malta's temples, temples that sing, cymatic temples and the oracle of Delphi.
Every model is schematic unless it says otherwise; every date carries its hedge."""
import math, random
from films import like, View
from scenes import timeline as _timeline, event, stat, quote, BONE, AMBER, SCAN, OCHRE, GOLD, RED
from f01 import mapshot
from iso3d import shot as iso
from f09 import B, L_
from f06 import box

SERIES = "Underworlds"
TUFF = "#c9b38a"


def timeline(*a, **k):
    k["y"] = 820
    return _timeline(*a, x0=200, x1=810, **k)


def EP(id_, code, title, case, verdict, claim, hook, beats, shots, sources, post, tags):
    return {"id": id_, "code": code, "series": SERIES, "title": title, "case": case, "verdict": verdict, "claim": claim, "mood": "mystery",
            "hook_text": hook, "beats": beats, "shots": shots, "sources": sources, "post": post, "hashtags": tags}


def grp(title, c, items, y=520, size=30):
    return [{"k": "cap", "x": 500, "y": y, "t": title, "c": c, "in": .2}] + [{"k": "label", "x": 500, "y": y + 80 + i * 64, "t": t, "st": "serif", "size": size, "in": .4 + i * .25} for i, t in enumerate(items)]


# ---------------------------------------------------------------- 07.01 Derinkuyu
def derinkuyu():
    gy = 470; px = 10.0                                  # 85 m over 850 px
    rooms = []
    r = random.Random(2)
    for lv in range(8):
        y = gy + 40 + lv * 104
        x = 150 + r.randint(0, 120)
        for k in range(r.randint(2, 3)):
            w = r.randint(90, 170)
            rooms.append({"k": "rect", "x": x, "y": y, "w": w, "h": 56, "fill": "#1a1511", "c": "#8c7452", "sw": 1.2, "in": .3 + lv * .12})
            x += w + r.randint(40, 90)
            if x > 820:
                break
    shafts = [{"k": "line", "p": [[sx, gy], [sx, gy + 830]], "c": "#1a1511", "w": 10, "in": .2} for sx in (300, 620)] + \
             [{"k": "line", "p": [[sx, gy], [sx, gy + 830]], "c": "#8c7452", "w": 1, "op": .6, "in": .2} for sx in (295, 305, 615, 625)]
    sec = {"base": "section", "tod": "day", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": TUFF, "t": "volcanic tuff: soft to carve, hard once exposed", "tex": "blocks", "to": .05}],
           "cam": [1, 500, 900], "els": shafts + rooms +
           [{"k": "dim", "x1": 900, "y1": gy, "x2": 900, "y2": gy + 850, "t": "about 85 m", "lx": -20},
            {"k": "house", "x": 460, "y": gy, "w": 90, "in": .1}, {"k": "label", "x": 500, "y": 420, "t": "Derinkuyu, cut open · schematic", "c": AMBER, "in": .3},
            {"k": "label", "x": 300, "y": gy + 880, "t": "air shafts: more than 50", "st": "small", "c": "#f2dcb4", "in": 1.4}]}
    s0 = sec
    v = View(26, 45, 35, 42.5, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Derinkuyu · Cappadocia", 34.7351, 38.3735, {"c": GOLD}), ("Ankara", 32.85, 39.93, {"a": "end", "lx": -18}), ("Istanbul", 28.97, 41.0, {})],
                 extra=[{"k": "label", "x": v.p(33, 36.2)[0], "y": v.p(33, 36.2)[1], "t": "the Mediterranean", "st": "ital", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    door = [{"k": "rect", "x": 300, "y": 640, "w": 400, "h": 480, "fill": "#1a1511", "c": "#8c7452", "sw": 2, "in": .2},
            {"k": "rect", "x": 180, "y": 560, "w": 640, "h": 80, "fill": TUFF, "c": "none", "sw": 0, "in": .1},
            {"k": "circle", "x": 690, "y": 900, "r": 230, "fill": "#b8a07a", "c": "#fff3dc", "w": 2, "in": .5},
            {"k": "circle", "x": 690, "y": 900, "r": 28, "fill": "#1a1511", "c": "none", "w": 0, "in": .7},
            {"k": "arrow", "p": [[860, 760], [720, 760]], "c": AMBER, "w": 2.4, "in": 1.0},
            {"k": "cap", "x": 500, "y": 500, "t": "a rolling stone door · schematic", "in": .2},
            {"k": "label", "x": 500, "y": 1240, "t": "rolled across from the inside; each level sealed on its own", "c": AMBER, "in": 1.3}]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": door}
    s3 = stat("85", "metres deep", "up to 18 floors reported, more than 50 ventilation shafts, rediscovered in 1963", "Nývlt et al. 2016")
    tl, ax = timeline(-1000, 2050, [(-1000, "1000 BCE"), (1, "1 CE"), (1000, "1000"), (2000, "2000")], "What can be dated")
    tl["els"] += event(ax, -700, "Phrygian start?", row=1, c="#ffb09a", i=.3, sub="proposed, not dated") + \
                 [{"k": "band", "x0": ax.x(780), "x1": ax.x(1180), "y": 700, "h": 16, "c": GOLD, "t": "Arab raids: the city grows", "in": .6}] + \
                 event(ax, 1923, "last used", row=2, c=BONE, i=.9) + event(ax, 1963, "rediscovered", row=0, c=SCAN, i=1.1) + \
                 [{"k": "label", "x": 120, "y": 480, "t": "← an Ice Age shelter, 12,800 years ago? far off this chart", "st": "small", "c": "#ffb09a", "a": "start", "in": 1.4}]
    s4 = tl
    s5 = stat("360+", "underground settlements", "located in Cappadocia so far", "HISTORY 2026; Yamaç & Tok 2026")
    s6 = like(s0, cam=[1.1, 500, 1000])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:DERINKUYU · TURKEY][sfx:boom][act:storytelling, drawing us in]In {1963|nineteen sixty-three}, a man knocked through a wall in his ^basement and found a ^room.",
                      "[d:tension][cam:1.1|0|60][act:the reveal, low and slow]Below it: a ^city, ^eighty-five metres deep."], cut=False),
        B("world", 0, ["[d:calm][k:THE CITY][act:touring it, fascinated]Carved into soft volcanic rock: up to ^eighteen floors, more than ^fifty air shafts, stables, wells and ^chapels.",
                       "[d:build][go:2|0][act:a clever detail, admiring]Each level could be sealed from ^inside with a ^rolling stone door."]),
        B("collision", 4, ["[d:build][k:THE CASE][act:the real puzzle, curious][tune:fall]How old is the ^deepest level? [act:presenting his idea, fairly]Graham Hancock asks whether it began as a shelter from the ^Ice Age cold, twelve ^thousand years ago.",
                           "[d:build][sfx:shimmer][act:conceding, sincere]And he has a ^point: nobody has ever dated the ^digging itself."]),
        B("cost", 4, ["[d:build][k:THE RECORD][act:naming the knowns, confident]What we ^can date: chapels, stables, and written accounts of Arab ^raids from the {700s|seven hundreds} on. [act:plain, respectful]^Byzantine Christians sheltered here.",
                      "[d:build][act:a quiet, human detail]Local Christians still used@verb it until {1923|nineteen twenty-three}."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:widening the view, wonder]And it isn't ^alone: more than ^three hundred and sixty underground settlements have been located in ^Cappadocia.",
                          "[d:build][sfx:hit][act:the catch, thoughtful]But carving ^erases its own history. [act:explaining, slower]Every enlargement scrapes away the ^older surface."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing the two options][tune:fall]Deepest levels from the ^Iron Age, or the ^Ice Age? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:the grounded option][tune:rise]A ^Byzantine refuge city? [act:plain and assured][tune:fall]That's what the evidence ^shows.",
                     "[d:tension][p:0.93][act:reflective, a little poetic]Soft rock keeps ^secrets. [act:the wry twist, light]It ^also keeps getting ^dug."]),
    ]
    return EP("derinkuyu", "07.01", "Derinkuyu: The City Beneath Cappadocia", "derinkuyu", "unsupported", "How old are the deepest levels of Cappadocia's underground cities?", "A city, eighty-five metres *deep*.", beats, shots,
              "Nývlt et al. 2016 · Ousterhout 2017 · Hancock 2015, Magicians of the Gods · Yamaç & Tok 2026",
              "In 1963 a man broke through his basement wall and found a city 85 metres deep: what can be dated, what can't, and why carving erases its own history.",
              ["#Derinkuyu", "#Cappadocia", "#UndergroundCity", "#Turkey", "#Underworlds"])


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


def derinkuyu_m():
    """Derinkuyu as one continuous take (see mural.py): the basement wall, the city opening below it, the rolling door, the dates
    that exist and the one that does not, the scraped walls, and the verdict on the deepest level are drawn."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN, GREEN, AU
    DARK, EDGE = "#1a1511", "#8c7452"
    gy, PXM = 470, 10.0                                   # 85 m over 850 px
    # 0 · the basement, the hidden room, then the city below: 18 floors, 85 m, as deep as a 25-storey building is tall
    sec = {"base": "section", "tod": "day", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": TUFF, "t": "", "tex": "blocks", "to": .05}], "cam": [1.7, 520, 560], "els": [
                {"k": "house", "x": 440, "y": gy, "w": 120, "h": 64, "in": -1},
                bx(450, gy + 14, 100, 52, DARK, EDGE, 1.5, 2, -1), person(480, gy + 64, 40, .6, "#efe6d4"),
                line([[550, gy + 16], [544, gy + 30], [553, gy + 42], [546, gy + 58]], 3.6, BN, 3, dur=.6),
                bx(553, gy + 14, 120, 52, DARK, EDGE, 1.5, 2, 6.4), glow(613, gy + 40, 70, 6.6, .8, "lamp")]}
    r = random.Random(2)
    rooms, levels = [], []
    for lv in range(18):
        y = gy + 80 + lv * 43
        x = 140 + r.randint(0, 90); row = []
        for k in range(r.randint(2, 4)):
            w = r.randint(60, 140)
            if x + w > 760:
                break
            row.append((x, y, w)); x += w + r.randint(30, 70)
        levels.append(row)
        rooms += [bx(x0, y0, w0, 26, DARK, EDGE, 1.2, 2, round(.8 + lv * .16, 2)) for x0, y0, w0 in row]
    shafts = [line([[sx, gy + 66], [sx, gy + 850]], .6, DARK, 8, dur=2.4) for sx in (300, 600)]
    deep = shafts + rooms + [
                line([[930, gy], [930, gy + 850]], 2.4, BN, 2.5, dur=1.0), line([[916, gy], [944, gy]], 2.4, BN, 2.5, draw=False), line([[916, gy + 850], [944, gy + 850]], 3.4, BN, 2.5, draw=False),
                label(912, gy + 440, "85 m", 3.2, BN, 32, "end"),
                {"k": "rect", "x": 790, "y": gy, "w": 70, "h": 850, "fill": "rgba(245,236,220,.05)", "c": "#f5ecdc", "sw": 1.5, "style": "inferred", "in": 4.4}] + \
           [line([[792, gy + 34 * j], [858, gy + 34 * j]], 4.6, "#f5ecdc", 1, draw=False, op=.4) for j in range(1, 25)] + [label(825, gy + 890, "25 storeys", 5.4, BN, 28)]
    lv3, lv6 = levels[3][0], levels[7][-1]
    well_x = levels[12][-1][0] + levels[12][-1][2] + 18
    tour = [label(130, gy + 46, "tuff", 2.8, "#3a2c20", 34, "start", halo=False, st="serif"),
            line([[100, gy + 80], [100, gy + 850]], 7.0, AU, 3, dur=1.0), label(110, gy + 900, "up to 18 floors", 7.6, AU, 30, "start")] + \
           [line([[sx, gy + 66], [sx, gy + 820]], 8.6 + .15 * k, DARK, 5, dur=.8) for k, sx in enumerate((200, 420, 520, 700))] + \
           [label(660, gy + 40, "more than 50 air shafts", 9.4, BN, 28),
            label(lv3[0] + lv3[2] / 2, lv3[1] + 20, "stables", 10.3, AU, 26),
            line([[well_x, levels[10][0][1]], [well_x, levels[14][0][1] + 26]], 10.8, "#5fa8c9", 4, dur=.5), bx(well_x - 9, levels[14][0][1] + 14, 18, 14, "#5fa8c9", r=3, at=11.1),
            label(well_x + 14, levels[12][0][1] + 20, "well", 11.0, "#9fd0ff", 26, "start"),
            label(lv6[0] + lv6[2] / 2, lv6[1] + 20, "chapel", 11.6, AU, 26)]
    # 2 · the rolling stone door, seen from inside: it rests in its slot, then rolls across the doorway
    door = {"base": "dark", "cam": [1.15, 500, 940], "els": [
                bx(80, 600, 840, 700, TUFF, "#e9dccb", 1.5, 6, -1), bx(80, 600, 840, 700, "rgba(0,0,0,.12)", r=6, at=-1),
                {"k": "poly", "p": [[260, 1250], [260, 960], [290, 900], [370, 876], [450, 900], [480, 960], [480, 1250]], "fill": DARK, "c": EDGE, "w": 2, "in": -1},
                label(500, 560, "seen from inside", 1.6, BN, 30),
                {"k": "circle", "x": 690, "y": 1060, "r": 190, "fill": "rgba(184,160,122,.35)", "c": "#fff3dc", "w": 3, "style": "inferred", "in": 3.6},
                dot(690, 1060, 22, DARK, 3.8),
                arrow([[640, 820], [520, 800], [430, 830]], 5.6, AU, 4, dur=1.0),
                {"k": "circle", "x": 370, "y": 1060, "r": 190, "fill": "#b8a07a", "c": "#fff3dc", "w": 3, "in": 7.0, "fx": "pop"}, dot(370, 1060, 22, DARK, 7.2)]}
    # 3 · how old is the deepest level? 13,000 years of time: the dated part is a sliver at the end; the claim far back. A room is empty space
    X = lambda ya: 120 + 760 * (13000 - ya) / 13000
    when = {"base": "dark", "cam": [1.05, 500, 900], "els": [
                line([[120, 700], [880, 700]], .3, "#e9dccb", 2.5, dur=.9)] + [line([[X(y), 688], [X(y), 712]], .4, "#e9dccb", 2, draw=False) for y in (12000, 9000, 6000, 3000, 0)] +
             [label(X(12000), 750, "12,000", .5, "#cbbca8", 26), label(X(3000), 750, "3,000", .5, "#cbbca8", 26), label(X(0), 750, "today", .5, "#cbbca8", 26), label(500, 800, "years ago", .6, "#cbbca8", 26),
              line([[X(1244), 680], [X(0), 680]], 1.6, AU, 14, dur=.4), label(X(600), 640, "dated", 1.8, AU, 28),
              line([[X(12000), 600], [X(12000), 700]], 8.0, LILAC, 3, "claimed", .6), dot(X(12000), 600, 9, LILAC, 8.0), label(X(12000) - 16, 570, "Ice Age shelter?", 8.2, LILAC, 30, "start"),
              line([[X(12000) + 20, 620], [X(1244) - 10, 660]], 9.8, LILAC, 2, "claimed", 1.2),
              {"k": "poly", "p": [[300, 1300], [300, 1080], [340, 1000], [500, 960], [660, 1000], [700, 1080], [700, 1300]], "fill": DARK, "c": EDGE, "w": 3, "in": 14.0}] +
             question(500, 1180, 20.8, 80) + [
              {"k": "vase", "x": 400, "y": 1300, "h": 70, "in": 24.6, "fx": "rise"}, glow(600, 1270, 50, 24.8, .9, "lamp"), dot(600, 1280, 8, "#ffe2a8", 24.8),
              bx(760, 1120, 120, 150, "#efe6d4", "#fff", 1.5, 4, 26.0, fx="pop")] +
             [line([[776, 1146 + 22 * j], [864, 1146 + 22 * j]], 26.2, "#3a2c20", 2, draw=False) for j in range(5)] +
             [dot(400, 1200, 10, GREEN, 25.0), dot(600, 1200, 10, GREEN, 25.2), dot(820, 1100, 10, GREEN, 26.4)]}
    # 4 · what can be dated: chapels, stables, written accounts of raids from the 700s; Byzantine Christians; used until 1923; found 1963
    Y = lambda yr: 120 + 760 * (yr - 500) / 1500
    dated = {"base": "dark", "cam": [1.1, 500, 940], "els": [
                line([[120, 1050], [880, 1050]], .2, "#e9dccb", 2.5, dur=.9)] + [line([[Y(y), 1038], [Y(y), 1062]], .3, "#e9dccb", 2, draw=False) for y in (500, 1000, 1500, 2000)] +
             [label(Y(y), 1100, t, .4, "#cbbca8", 26) for y, t in ((500, "500 CE"), (1000, "1000"), (1500, "1500"), (2000, "2000"))] + [
                {"k": "poly", "p": [[300, 700], [300, 600], [335, 560], [370, 600], [370, 700]], "fill": "none", "c": AU, "w": 3, "in": 3.2, "fx": "draw"}, label(335, 740, "chapels", 3.4, AU, 28),
                bx(560, 650, 120, 50, "none", AU, 3, 4, 3.8), line([[570, 675], [670, 675]], 3.9, AU, 2, draw=False), label(620, 740, "stables", 4.0, AU, 28),
                line([[Y(780), 1010], [Y(1180), 1010]], 6.4, AU, 16, dur=1.0),
                bx(Y(980) - 50, 780, 100, 110, "#efe6d4", "#fff", 1.5, 4, 5.4, fx="pop")] + [line([[Y(980) - 38, 800 + 20 * j], [Y(980) + 38, 800 + 20 * j]], 5.6, "#3a2c20", 2, draw=False) for j in range(5)] + [
                label(Y(980), 762, "written accounts", 5.8, AU, 28), label(Y(980), 1100 + 40, "raids", 6.8, AU, 28)] +
             [person(Y(900) + 40 * k, 998, 56, 9.0 + .2 * k, "#efe6d4") for k in range(3)] + [
                line([[Y(1923), 1050], [Y(1923), 880]], 14.8, BN, 2.5, dur=.4), label(Y(1923) - 8, 862, "1923", 15.0, BN, 30, "end"),
                line([[Y(1963), 1050], [Y(1963), 1180]], 17.6, "#9fd0ff", 2.5, dur=.4), label(Y(1963) - 8, 1210, "1963", 17.8, "#9fd0ff", 30, "end")]}
    # 5 · not alone: more than 360 underground settlements located in Cappadocia (dots schematic)
    v = View(26, 45, 35, 42.5, (40, 330, 920, 900))
    from f01 import mapshot as _ms
    D = v.p(34.7351, 38.3735)
    rr = random.Random(9)
    pts = []
    while len(pts) < 360:
        a, d = rr.uniform(0, 2 * math.pi), math.sqrt(rr.random()) * 90
        pts.append((round(D[0] + 1.35 * d * math.cos(a), 1), round(D[1] + d * math.sin(a), 1)))
    many = _ms(v, cam=[1.9, D[0] + 10, D[1] + 40], pins=[("Derinkuyu", 34.7351, 38.3735, {"c": GOLD, "in": .3}), ("Ankara", 32.85, 39.93, {"a": "end", "lx": -18, "in": .3})],
               extra=[dot(x, y, 2.2, AU, round(3.0 + .006 * k, 3), fx="fade") for k, (x, y) in enumerate(pts)] +
                     [{"k": "poly", "p": ellipse(D[0], D[1], 135, 100, 40), "fill": "none", "c": AU, "w": 2, "style": "inferred", "curve": True, "in": 6.0},
                      label(D[0], D[1] + 140, "Cappadocia", 6.4, AU, 32, st="ital"), label(D[0], D[1] - 120, "360+", 3.4, AU, 40, st="serif")])
    # 6 · carving erases its own history: the room enlarged, the older surface scraped away
    old = [[380, 1180], [380, 1020], [420, 960], [500, 940], [580, 960], [620, 1020], [620, 1180]]
    new = [[280, 1250], [280, 1000], [340, 900], [500, 860], [660, 900], [720, 1000], [720, 1250]]
    scrape = {"base": "dark", "cam": [1.15, 500, 980], "els": [
                bx(60, 700, 880, 680, TUFF, "#e9dccb", 1.5, 6, -1),
                {"k": "poly", "p": new, "fill": DARK, "c": EDGE, "w": 3, "in": 4.0, "fx": "rise"},
                {"k": "poly", "p": old, "fill": "rgba(26,21,17,.6)", "c": LILAC, "w": 3, "style": "claimed", "in": .4}] +
             [line([[x, y], [x + 14, y - 10]], 1.0 + .05 * k, LILAC, 2.5, dur=.2) for k, (x, y) in enumerate([(392, 1150), (392, 1100), (395, 1050), (430, 975), (480, 953), (540, 953), (590, 975), (603, 1050), (606, 1100), (606, 1150)])] + [
                label(500, 1080, "older surface", 5.8, LILAC, 28), label(500, 830, "today's wall", 7.0, BN, 28)] + \
             [line([[x, y], [x + 16, y - 12]], 7.4 + .05 * k, "#cbbca8", 2.5, dur=.2) for k, (x, y) in enumerate([(292, 1220), (292, 1120), (300, 1020), (350, 920), (440, 878), (560, 878), (650, 920), (700, 1020), (706, 1120), (706, 1220)])]}
    # the verdict, back on the city: the deepest level undated; a Byzantine refuge shown; and someone still digging
    bot = gy + 80 + 17 * 43
    verdict = [line([[86, bot - 120], [86, bot + 30]], .6, LILAC, 4, "claimed", .8)] + question(160, bot - 30, 4.9, 60) + [
               line([[86, gy + 80], [86, gy + 340]], 9.2, GREEN, 4, dur=.8), label(110, gy + 360, "Byzantine refuge", 9.8, GREEN, 28, "start"),
               person(560, bot + 26, 34, 13.6, "#efe6d4"), line([[566, bot - 2], [590, bot + 8]], 13.8, "#c9a46a", 3, draw=False),
               line([[600, bot + 13], [700, bot + 13]], 14.6, DARK, 18, dur=1.4)]
    shots = [sec, {}, door, when, dated, many, scrape, {}]
    ep = _take(derinkuyu, shots, [0, 0, 3, 4, 5, 7])
    return remix(ep, scenes={0: sec, 2: door, 3: when, 4: dated, 5: many, 6: scrape}, alias={1: 0, 7: 0}, _rewrite=False,
                 line_adds={(0, 1): (deep, [1.05, 500, 890])}, beat_adds={1: (tour, [1.05, 500, 890]), 5: (verdict, [1.05, 500, 890])})


# ---------------------------------------------------------------- 07.02 The Longyou caves
def longyou():
    hall = [{"t": "slab", "x0": -24, "x1": 24, "z0": -18, "z1": 18, "y": 0, "c": "#6f6a60"}] + \
           [box(x, z, 0, 2.4, 2.4, 14, "#9a8f7c", "rgba(0,0,0,.3)") for x, z in ((-8, -4), (8, 4), (0, 10))] + \
           [{"t": "quad", "p": [[-24, 16, -18], [24, 12, -18], [24, 12, 2], [-24, 16, 2]], "n": [0.08, 1, 0], "c": "#8a8070", "op": .85, "over": 3},
            {"t": "ext", "axis": "x", "x": 0, "y": 0, "at": -17, "d": 2, "prof": [[-22, 0], [-4, 0], [-4, 8], [-10, 8], [-22, 2]], "c": "#7a7266", "edge": "rgba(0,0,0,.3)"},
            {"t": "person", "x": 14, "y": 0, "z": 10, "h": 1.7},
            L_(0, 16, "a roof that slopes with the rock layers", GOLD, z=-8, dy=-24), L_(-8, 14, "pillars left in the rock", "#f2dcb4", z=-4, dy=-10),
            L_(0, 0, "Cavern No. 2 · about 1,057 m², up to 18 m high · schematic", "#cfe6ff", z=18, dy=40)]
    s0 = iso(hall, cam=[1, 500, 900], s=11, x=500, y=1060, az=-26, spin=1.2, el=.45, table=None)
    v = View(108, 124, 22, 34, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Longyou", 119.2, 29.08, {"c": GOLD}), ("Hangzhou", 120.16, 30.27, {}), ("Shanghai", 121.47, 31.23, {})],
                 extra=[{"k": "label", "x": v.p(113, 31)[0], "y": v.p(113, 31)[1], "t": "China", "st": "ital", "c": "#c9ad85"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(200), "t": "200 km"}])
    wall = [{"k": "rect", "x": 120, "y": 560, "w": 760, "h": 640, "fill": "#8a8070", "c": "#c9c0ae", "sw": 1.4, "in": .1}] + \
           [{"k": "line", "p": [[120 + k * 48, 1200], [120 + k * 48 + 300, 560]], "c": "#5b5448", "w": 3, "op": .8, "in": .3 + k * .05} for k in range(-6, 16) if 0 <= 120 + k * 48 + 300 and 120 + k * 48 <= 880] + \
           [{"k": "cap", "x": 500, "y": 500, "t": "chisel marks in bands 50–60 cm apart · schematic", "in": .2}]
    for e in wall[1:-1]:
        (x0, y0), (x1, y1) = e["p"]
        t0 = max(0, (120 - x0) / (x1 - x0)) if x0 < 120 else 0
        t1 = min(1, (880 - x0) / (x1 - x0)) if x1 > 880 else 1
        e["p"] = [[x0 + (x1 - x0) * t0, y0 + (y1 - y0) * t0], [x0 + (x1 - x0) * t1, y0 + (y1 - y0) * t1]]
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": wall}
    s3 = stat("24", "caverns", "cut by hand into siltstone beside the Qu River; found full of water in 1992", "Yang, Yue & Li 2011")
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("seven theories, none settled", AMBER, ["quarries", "tombs", "storage", "a retreat", "a secret army camp", "a place of sacrifice", "a palace"], y=460, size=30)}
    s5 = stat("0.55", "metres", "the thinnest wall between two neighbouring caverns, and not one breakthrough", "Yang, Yue & Li 2011")
    s6 = like(s0, cam=[1.15, 500, 1000])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:LONGYOU · CHINA][sfx:boom][act:storytelling, growing wonder]In {1992|nineteen ninety-two}, villagers pumped the water out of a pond, and found a hall the size of a ^cathedral, cut by ^hand into rock.",
                      "[d:tension][cam:1.12|0|0][act:the kicker, quietly amazed]Then they found ^twenty-three more."], cut=False),
        B("world", 0, ["[d:calm][k:THE CAVES][act:touring the space, awed][tune:level]^Floors of up to ^thirteen hundred square metres. [act:looking up][tune:level]^Roofs up to eighteen metres high, sloping with the ^rock layers. [act:a quick inventory][tune:fall]^Pillars, ^stairs, ^drainage.",
                       "[d:build][go:2|0][act:close up, admiring]And ^every surface covered in neat bands of ^chisel marks."]),
        B("collision", 5, ["[d:build][k:THE MYSTERY][act:precise, intrigued]Neighbouring caverns are separated by walls just ^half a metre thick. [act:quiet emphasis][tune:fall]Not ^one breaks through.",
                           "[d:build][sfx:shimmer][act:hushed, the real puzzle]And there's not a ^single record@noun of who dug them, or ^why."]),
        B("cost", 3, ["[d:build][k:THE DATE][act:a solid clue, steady]Pottery from the ^Western Han dynasty, about two ^thousand years old, was found inside.",
                      "[d:aside][act:a careful caveat, lighter][tune:fallrise]That dates when the ^pots arrived. [act:pointed, simple][tune:fall]Not the ^digging."]),
        B("reversal", 4, ["[d:reveal][k:THE THEORIES][act:opening the options, lively]The engineers who studied them list seven possibilities, from ^quarries to a ^palace.",
                          "[d:build][sfx:hit][act:practical, weighing it]Quarrying is the ^simplest: soft, even stone, right beside a ^river. [act:the catch, even][tune:fall]But ^nobody has traced the stone to a ^building."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Dug as ^quarries? [act:the verdict, honest][tune:fall]^*Open question*. [act:fair, with a reservation][tune:fallrise]The simplest answer, still ^unconfirmed.",
                     "[d:tension][p:0.93][act:warm, admiring, the last word]Two thousand years of ^silence, carved with remarkable ^care."]),
    ]
    return EP("longyou-caves", "07.02", "The Longyou Caves: Halls Carved in Silence", "longyou-caves", "contested", "Who dug the Longyou caverns, and what were they for?", "Then they found twenty-three *more*.", beats, shots,
              "Yang, Yue & Li 2011, Tunnelling and Underground Space Technology · Li et al. 2009",
              "In 1992 villagers drained a pond in China and found a cathedral-sized hall cut by hand into rock, then 23 more: the chisel marks, the Han pottery and seven theories.",
              ["#Longyou", "#China", "#Caves", "#Mystery", "#Underworlds"])


# ---------------------------------------------------------------- 07.03 Malta's temples
def malta():
    stones = [{"t": "slab", "x0": -26, "x1": 26, "z0": -20, "z1": 20, "y": 0, "c": "#9c8a6a"}]
    for cx, cz, rx, rz in ((-7, -6, 7, 5), (7, -6, 7, 5), (-6, 7, 6, 4.5), (6, 7, 6, 4.5)):
        n = 11
        for k in range(n):
            a = math.pi * .15 + 2 * math.pi * k / n
            if (cz < 0 and math.sin(a) > .8) or (cz > 0 and math.sin(a) < -.8):
                continue
            x, z = cx + rx * math.cos(a), cz + rz * math.sin(a)
            stones.append(box(x, z, 0, 2.2, 1.4, 4 + (k % 3), "#d8c7a2", "rgba(0,0,0,.3)"))
    stones += [box(0, 13, 0, 1.6, 1.6, 5.5, "#e2d3b0"), box(3, 13, 0, 1.6, 1.6, 5.5, "#e2d3b0"), {"t": "person", "x": 14, "y": 0, "z": 15, "h": 1.7},
               L_(0, 7, "Ġgantija, Gozo · lobed chambers · schematic", GOLD, z=-10, dy=-24), L_(0, 0, "walls still up to about 6 m high", "#cfe6ff", z=18, dy=40)]
    s0 = iso(stones, cam=[1, 500, 900], s=13, x=500, y=1000, az=-24, spin=1.2, el=.5, table=None)
    v = View(11.8, 16.2, 35.4, 38.3, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Ġgantija · Gozo", 14.269, 36.047, {"c": GOLD, "a": "end", "lx": -18}), ("the Hypogeum", 14.5069, 35.8697, {"c": GOLD}), ("Syracuse · Sicily", 15.29, 37.07, {})],
                 extra=[{"k": "label", "x": v.p(13, 36.5)[0], "y": v.p(13, 36.5)[1], "t": "about 100 km of open sea", "st": "small", "c": "#9fd0ff"}, {"k": "scale", "x": 80, "y": 1240, "w": v.km(50), "t": "50 km"}])
    s2 = stat("c. 3600", "BCE", "when temple building began at Ġgantija: centuries before Egypt's pyramids", "UNESCO; Trump 2002")
    gy = 560
    s3 = {"base": "section", "tod": "day", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": "#d8c7a2", "t": "Globigerina limestone", "tex": "blocks", "to": .05}], "cam": [1, 500, 900],
          "els": [{"k": "rect", "x": 200 + k * 130, "y": gy + 90 + lv * 180, "w": 100, "h": 90, "fill": "#1a1511", "c": "#8c7452", "sw": 1.2, "in": .3 + lv * .3 + k * .05} for lv in range(3) for k in range(4 - lv)] +
          [{"k": "label", "x": 500, "y": 500, "t": "the Ħal Saflieni Hypogeum · three levels cut into rock · schematic", "c": AMBER, "in": .2},
           {"k": "label", "x": 500, "y": gy + 700, "t": "the remains of about 7,000 people", "c": "#f2dcb4", "in": 1.4}]}
    tl, ax = timeline(-7500, -2000, [(-7000, "7000 BCE"), (-5500, "5500"), (-4000, "4000"), (-2500, "2500")], "Malta's deep past, as dated")
    tl["els"] += event(ax, -6500, "hunter-gatherers arrive", row=1, c=SCAN, i=.3, sub="by sea") + event(ax, -5500, "farmers from Sicily", row=0, c=BONE, i=.6) + \
                 [{"k": "band", "x0": ax.x(-3600), "x1": ax.x(-2500), "y": 700, "h": 16, "c": GOLD, "t": "the temples", "in": .9},
                  {"k": "label", "x": 120, "y": 480, "t": "← Ice Age temples? nothing dated there", "st": "small", "c": "#ffb09a", "a": "start", "in": 1.3}]
    s4 = tl
    s5 = stat("100", "km", "of open sea crossed by hunter-gatherers to reach Malta about 8,500 years ago", "Scerri et al. 2025, Nature")
    s6 = like(s0, cam=[1.15, 500, 960])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:MALTA][sfx:boom][act:enticing, setting the scene][tune:level]Stone temples ^older than the pyramids. [act:lower, a little eerie][tune:level]An underground city of the ^dead. [act:the tantalising one, hushed][tune:fall]And stories of sanctuaries under the ^sea.",
                      "[d:tension][cam:1.12|0|0][act:genuinely curious][tune:fall]How ^far back does@verb Malta go?"], cut=False),
        B("world", 0, ["[d:calm][k:THE TEMPLES][act:grounded, admiring]Ġgantija, on Gozo: walls still six metres high, built around {3600|thirty-six hundred} BCE. [go:2|0][act:letting it sink in, wonder]Centuries ^older than Egypt's pyramids."]),
        B("collision", 4, ["[d:build][k:THE CASE][act:fair, presenting the bold idea]Graham Hancock goes ^further: maybe the temples are far older, from the ^Ice Age, with more of them now under the sea.",
                           "[d:build][act:storytelling, adventurous]In {2002|two thousand two}, he ^dived after a reported ^underwater temple."]),
        B("cost", 3, ["[d:build][k:THE DATES][act:methodical, stacking the evidence]But radiocarbon from inside and beneath the temples, pottery sequences, and farm villages built over, all point between {3600|thirty-six hundred} and {2500|twenty-five hundred} BCE.",
                      "[d:build][act:with care, quiet]The ^Hypogeum's seven thousand dead ^too."]),
        B("reversal", 5, ["[d:reveal][k:THE TWIST][act:the twist, leaning in]And yet the experts were ^surprised in {2025|twenty twenty-five}. [act:vivid, full of wonder]^Hunter-gatherers reached Malta about eighty-five hundred years ago, across a ^hundred kilometres of open sea.",
                          "[d:build][sfx:hit][act:the payoff, firm][tune:fall]A ^thousand years ^before the farmers."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]^Ice Age temples? [act:the verdict, firm and exact]*Ruled ^out*: ^nothing from them is older than about {3600|thirty-six hundred} BCE. [act:brightening, curious][tune:rise]An ^older Malta? [act:delighted, open][tune:fall]Still being ^found.",
                     "[d:tension][p:0.93][act:warm, a gentle smile]Older than the pyramids is ^already astonishing."]),
    ]
    return EP("malta-temples", "07.03", "Malta's Temples: Older Than the Pyramids, but Ice Age?", "malta-temples", "debunked", "Were Malta's megalithic temples built in the Ice Age by a people now lost beneath the sea?", "How far back does Malta *go*?", beats, shots,
              "Trump 2002 · Renfrew 1973 · Malone et al. 2020 · Scerri et al. 2025, Nature · UNESCO · Hancock 2002, Underworld",
              "Europe's oldest freestanding stone temples and an underground city of the dead: the claim they go back to the Ice Age, and what 2025's seafaring hunter-gatherers changed.",
              ["#Malta", "#Megaliths", "#Ggantija", "#Archaeology", "#Underworlds"])


# ---------------------------------------------------------------- 07.04 Temples that sing
def acoustics():
    vault = [{"k": "poly", "p": [[140, 1200], [140, 760], [260, 600], [500, 540], [740, 600], [860, 760], [860, 1200]], "fill": "#2a221b", "c": "#c9ad85", "w": 3, "curve": True, "in": .1},
             {"k": "person", "x": 500, "y": 1180, "h": 150, "t": False, "in": .3}] + \
            [{"k": "circle", "x": 500, "y": 1060, "r": 50 + k * 55, "fill": "none", "c": GOLD, "w": 2, "op": .8 - k * .1, "in": .6 + k * .2} for k in range(6)] + \
            [{"k": "cap", "x": 500, "y": 460, "t": "the stone answers · schematic", "in": .2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": vault}
    s1 = stat("16", "seconds", "of reverberation at 63 Hz in the Oracle Room of Malta's Hypogeum, at most", "Till 2017")
    ax0, ax1 = 140, 860
    X = lambda f: ax0 + (ax1 - ax0) * f / 400
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": [{"k": "line", "p": [[ax0, 1000], [ax1, 1000]], "c": "#8c7152", "w": 2, "in": .1}] +
          [{"k": "label", "x": X(f), "y": 1040, "t": f"{f} Hz", "st": "small", "in": .2} for f in (0, 100, 200, 300, 400)] +
          [{"k": "rect", "x": X(85), "y": 900, "w": X(180) - X(85), "h": 60, "fill": "#6a645c", "c": "none", "sw": 0, "op": .7, "in": .4},
           {"k": "label", "x": X(132), "y": 880, "t": "a man's speaking voice", "st": "small", "c": "#e9dccb", "in": .5},
           {"k": "rect", "x": X(95), "y": 760, "w": X(120) - X(95), "h": 60, "fill": GOLD, "c": "none", "sw": 0, "in": .9},
           {"k": "label", "x": X(107), "y": 740, "t": "six chambers: 95–120 Hz", "st": "small", "c": GOLD, "in": 1.1},
           {"k": "cap", "x": 500, "y": 560, "t": "six ancient chambers · Britain and Ireland · 1996", "in": .2}]}
    duct = [{"k": "rect", "x": 140, "y": 620, "w": 300, "h": 200, "fill": "#2a221b", "c": "#c9ad85", "sw": 2, "in": .1},
            {"k": "line", "p": [[440, 700], [620, 700], [620, 1000], [860, 1000]], "c": GOLD, "w": 10, "op": .8, "in": .5, "fx": "draw"},
            {"k": "rect", "x": 700, "y": 1020, "w": 180, "h": 120, "fill": "#8a9a5b", "c": "#e9dccb", "sw": 1.4, "in": .7}] + \
           [{"k": "line", "p": [[200 + i * 50, 760], [215 + i * 50, 720], [235 + i * 50, 740], [230 + i * 50, 770], [200 + i * 50, 760]], "c": "#f2e8d6", "w": 3, "curve": True, "in": .3 + i * .08} for i in range(5)] + \
           [{"k": "label", "x": 290, "y": 860, "t": "a gallery: conch-shell trumpets", "st": "small", "in": .9},
            {"k": "label", "x": 790, "y": 1180, "t": "the plaza", "st": "small", "in": 1.1},
            {"k": "cap", "x": 500, "y": 540, "t": "Chavín de Huántar, Peru · schematic", "in": .2},
            {"k": "label", "x": 500, "y": 1260, "t": "ducts carry the trumpets' tones 10–20 dB louder", "c": AMBER, "in": 1.4}]
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": duct}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("designed for sound? site by site", AMBER, ["Chavín: instruments + ducts · likely", "painted caves: weak but tenable", "Malta's Hypogeum: real, inconsistent", "Stonehenge: doubted by its modellers", "Giza's King's Chamber: size explains it"], y=460, size=28)}
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the viral claims, September 2026", "#ffb09a", ["a hall at Ellora ringing for 15–20 seconds", "carved flowers as keys to frequencies"], y=560, size=30) +
          [{"k": "label", "x": 500, "y": 900, "t": "published measurements found: none, yet", "c": "#9fd0ff", "in": 1.4}]}
    s6 = like(s0, cam=[1.1, 500, 900])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:TEMPLES THAT SING][sfx:boom][act:playful, inviting]Hum in the ^right ancient chamber, and the stone hums ^back.",
                      "[d:tension][cam:1.1|0|0][act:matter of fact, a nod]Physicists have ^measured it. [act:the real puzzle, curious][tune:rise]Did the builders ^plan it?"], cut=False),
        B("world", 2, ["[d:calm][k:THE MEASUREMENTS][act:laying out the study, clear]In {1996|nineteen ninety-six}, researchers tested ^six Stone Age and Iron Age chambers in Britain and ^Ireland. [act:the striking result, crisp]^Every one resonated between ninety-five and a hundred and ^twenty hertz.",
                       "[d:aside][act:a light aside, intrigued]Right in the range of a ^man's voice."]),
        B("collision", 1, ["[d:build][k:THE HYPOGEUM][act:hushed, almost listening]In Malta's underground Hypogeum, a low note can ^hang in the air for up to ^sixteen seconds.",
                           "[d:build][sfx:shimmer][act:impressed, building]Far more ^bass@music than a concert hall, or a ^cathedral."]),
        B("cost", 4, ["[d:build][k:THE CATCH][act:the catch, calm and clear]But ^every room rings at pitches set by its ^size. [act:explaining, patient]A chamber built for ^people will resonate like a voice.",
                      "[d:aside][act:dry, a gentle maxim][tune:fall]A ^measured effect is not a ^design brief."]),
        B("reversal", 3, ["[d:reveal][k:THE BEST CASE][act:brightening, the best case]Chavín de Huántar, in ^Peru. [act:vivid, building][tune:level]Twenty ^conch-shell trumpets, found in a ^gallery. [sfx:hit][act:the clever part, leaning in]And stone ^ducts that carry their sound into the ^plaza. [act:warm, convinced][tune:fall]That looks ^designed.",
                          "[d:build][go:5|0][act:turning to the news][tune:rise]And the ^viral claims this month? [act:reporting it, neutral]A hall at ^Ellora ringing for ^twenty seconds. [act:careful, honest]We found no ^published measurement. [gap:0.4][act:open, a small smile][tune:fallrise]^Yet."]),
        B("tag", 4, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Temples ^designed for sound? [act:the verdict, balanced][tune:fall]^*Mixed record@noun*. [act:going site by site][tune:level]^Likely at Chavín. [act:same measured pace][tune:level]^Unclear in Malta. [act:calm, closing the round][tune:fall]Not ^needed at Giza.",
                     "[d:tension][p:0.93][act:warm, affirming][tune:fall]The stones ^do sing. [act:thoughtful, the last word]Whether anyone ^wrote the song, we weigh site by ^site."]),
    ]
    return EP("temple-acoustics", "07.04", "Temples That Sing: Sound and Ancient Stone", "temple-acoustics", "mixed", "Did ancient builders design their sacred spaces for sound?", "The stone hums *back*.", beats, shots,
              "Jahn, Devereux & Ibison 1996 · Till 2017 · Kolar 2013 · Cox, Fazenda & Greaney 2020 · Fazenda et al. 2017 · The Joe Rogan Experience #2558, 2026",
              "Hum in the right chamber and the stone answers: what physicists have measured in Malta, Ireland and Peru, which temples look built for sound, and the viral claims still unmeasured.",
              ["#Archaeoacoustics", "#AncientTemples", "#Sound", "#Malta", "#Underworlds"])


# ---------------------------------------------------------------- 07.05 Cymatic temples
def chladni(n=3, m=5, N=70, x0=180, y0=540, W=640):
    """Sand on a vibrating square plate: dots where cos(n x)cos(m y) - cos(m x)cos(n y) is near zero (a textbook Chladni figure)."""
    out = []
    for i in range(N + 1):
        for j in range(N + 1):
            x, y = math.pi * i / N, math.pi * j / N
            f = math.cos(n * x) * math.cos(m * y) - math.cos(m * x) * math.cos(n * y)
            if abs(f) < .09:
                out.append({"k": "circle", "x": round(x0 + W * i / N, 1), "y": round(y0 + W * j / N, 1), "r": 3.4, "fill": "#f2e8d6", "c": "none", "w": 0, "in": .6 + (abs(i - N / 2) + abs(j - N / 2)) * .012})
    return out


def cymatic():
    plate = [{"k": "rect", "x": 170, "y": 530, "w": 660, "h": 660, "fill": "#2a2d31", "c": "#9fb0c0", "sw": 2, "in": .1}] + chladni() + \
            [{"k": "cap", "x": 500, "y": 470, "t": "sand on a vibrating plate · a Chladni figure", "in": .2}]
    s0 = {"base": "dark", "cam": [1, 500, 860], "els": plate}
    bor = [{"t": "slab", "x0": -40, "x1": 40, "z0": -40, "z1": 40, "y": 0, "c": "#5f7a45"}] + \
          [box(0, 0, i * 2.2, 62 - i * 8, 62 - i * 8, 2.2, "#8c8a7c" if i % 2 else "#9a978a", "rgba(0,0,0,.3)") for i in range(6)] + \
          [{"t": "cyl", "x": 0, "z": 0, "y": 13.2 + i * 1.6, "r": 11 - i * 3, "h": 1.6, "c": "#a8a597", "n": 32, "edge": "rgba(0,0,0,.25)"} for i in range(3)]
    for ring, (rr, nn) in enumerate(((9.5, 32), (6.5, 24), (3.8, 16))):
        for k in range(nn // 2):
            a = 2 * math.pi * k / (nn // 2)
            bor.append({"t": "cyl", "x": rr * math.cos(a), "z": rr * math.sin(a), "y": 14.8 + ring * 1.6, "r": .7, "h": 1.4, "c": "#b8b5a6", "n": 10, "edge": "rgba(0,0,0,.25)"})
    bor += [{"t": "cyl", "x": 0, "z": 0, "y": 18, "r": 2.4, "h": 3.2, "c": "#c9c6b6", "n": 20, "edge": "rgba(0,0,0,.25)"},
            {"t": "person", "x": 34, "y": 0, "z": 34, "h": 1.7},
            L_(0, 22, "Borobudur, Java · c. 780–833 CE", GOLD, z=0, dy=-24), L_(0, 0, "six square terraces, three round ones · 123 m across · schematic", "#cfe6ff", z=36, dy=40)]
    s1 = iso(bor, cam=[1, 500, 900], s=6.4, x=500, y=1020, az=-24, spin=1.2, el=.5, table=None)
    v = View(105, 115.5, -9, -5.4, (40, 330, 920, 900))
    s2 = mapshot(v, pins=[("Borobudur", 110.2038, -7.6079, {"c": GOLD}), ("Yogyakarta", 110.37, -7.8, {"a": "start", "ly": 34}), ("Jakarta", 106.85, -6.2, {})],
                 extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    s3 = stat("1787", "", "Ernst Chladni publishes his sound figures: sand gathers along the lines where a vibrating plate stays still", "Chladni 1787")
    s4 = stat("0.6", "grams", "roughly the most sound in air has held up; a 25-tonne standing stone is about 40 million times heavier", "levitation experiments; our calculation")
    s5 = {"base": "dark", "cam": [1, 500, 860], "els": grp("two different claims", AMBER, ["temple plans copied from sound patterns", "stones lifted by sound"], y=560) +
          [{"k": "label", "x": 500, "y": 900, "t": "the first: untested · the second: physics says no", "c": "#9fd0ff", "in": 1.4}]}
    s6 = like(s0, cam=[1.1, 500, 860])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:CYMATIC TEMPLES][sfx:boom][act:playful, a little experiment][tune:level]Put ^sand on a ^metal plate. [act:one more step][tune:level]Play a ^note. [act:the magic moment, wonder]The grains draw a ^mandala.",
                      "[d:tension][cam:1.1|0|0][act:posing it, intrigued][tune:rise]Did ancient builders ^copy these patterns? [act:raising the stakes, curious][tune:rise]Or even ^lift stones with ^sound?"], cut=False),
        B("world", 3, ["[d:calm][k:THE PHYSICS][act:reassuring, a smile]It's ^real, and it's old news: Ernst ^Chladni described it in {1787|seventeen eighty-seven}. [act:explaining, clear]Sand gathers along the lines where the plate ^doesn't move.",
                       "[d:aside][act:light, quick]Change the ^note, and you get a ^new pattern."]),
        B("collision", 1, ["[d:build][k:THE CLAIM][act:reporting it, fair and neutral]On one of the world's biggest podcasts this month, a music producer, Tyler Engle, read@past temples like ^Borobudur as ^sound patterns in stone.",
                           "[d:build][sfx:shimmer][act:describing the idea, intrigued]Carved ^flowers as keys to ^frequencies."]),
        B("cost", 2, ["[d:build][k:THE DESIGN IDEA][act:respectful, grounded]Borobudur, in Java, around {800|eight hundred} CE: a Buddhist ^mandala in stone, laid out with cords and ^pegs.",
                      "[d:build][act:careful, evidence-minded]No ^text, ^tool or ^workshop anywhere shows vibration patterns used@verb to design a temple. [d:aside][act:fair, even-handed][tune:fall]^Untested isn't ^refuted."]),
        B("reversal", 4, ["[d:reveal][k:THE LIFTING IDEA][sfx:hit][act:the bigger claim, curious][tune:rise]^Lifting stones with sound? [act:a delightful fact, precise]The heaviest thing sound in air has held up is about ^half a gram.",
                          "[d:build][act:doing the maths, dry]A twenty-five-tonne stone is forty ^million times heavier."]),
        B("tag", 5, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]Temples ^designed from sound patterns? [act:the verdict, level-headed][tune:fall]*Awaiting ^evidence*. [act:the second claim][tune:rise]Stones ^lifted by sound? [act:simple, kind, final][tune:fall]Physics says ^no.",
                     "[d:tension][p:0.93][act:warm, appreciative]The patterns are ^beautiful. [act:gentle, firm, the last word][tune:fall]The evidence has to be in the ^stone."]),
    ]
    return EP("cymatic-temples", "07.05", "Cymatic Temples: Did Sound Shape the Stones?", "cymatic-temples", "unsupported", "Was sound a working technology for designing or building ancient monuments?", "The sand draws a *mandala*.", beats, shots,
              "Chladni 1787 · Rossing & Fletcher 2004 · Andrade et al. 2016 · UNESCO, Borobudur · The Joe Rogan Experience #2558, 2026",
              "Sand on a singing plate draws mandalas. Did temple builders copy them, or lift stones with sound? The physics, Borobudur, and the two claims weighed separately.",
              ["#Cymatics", "#Borobudur", "#Sound", "#AncientTemples", "#Underworlds"])


# ---------------------------------------------------------------- 07.06 Delphi
def delphi():
    temple = [{"t": "ext", "axis": "x", "x": 0, "y": 0, "at": 0, "d": 40, "prof": [[-40, 0], [40, 0], [40, 22], [10, 10], [-40, 6]], "c": "#8a8a70", "edge": "rgba(0,0,0,.25)"},
              box(-4, 0, 8.2, 24, 12, 1.2, "#e2d8c4")] + \
             [{"t": "cyl", "x": -14 + i * 4, "z": z, "y": 9.4, "r": .7, "h": 6, "c": "#efe6d2", "n": 12, "edge": "rgba(0,0,0,.2)"} for i in range(7) for z in (-5, 5)] + \
             [box(-4, 0, 15.4, 25, 13, 1, "#e2d8c4"),
              {"t": "line", "p": [[-40, 5.8, -6], [40, 20, 6]], "c": RED, "w": 4, "op": .9}, {"t": "line", "p": [[-6, 7, -20], [2, 8.5, 20]], "c": RED, "w": 4, "op": .9},
              {"t": "glow", "x": -3, "y": 9, "z": 0, "r": 90, "kind": "lamp", "pulse": True},
              {"t": "person", "x": 16, "y": 12.5, "z": 12, "h": 1.7},
              L_(-4, 16.4, "the Temple of Apollo · 4th century BCE rebuild · schematic", GOLD, z=0, dy=-24), L_(20, 18, "the Delphi fault", "#ffb09a", z=6, dy=-14), L_(2, 8.5, "the Kerna fault", "#ffb09a", z=20, dy=36)]
    s0 = iso(temple, cam=[1, 500, 900], s=9, x=500, y=1040, az=-24, spin=1.2, el=.45, table=None)
    v = View(19.8, 26.2, 36.2, 40.8, (40, 330, 920, 900))
    s1 = mapshot(v, pins=[("Delphi", 22.501, 38.4824, {"c": GOLD}), ("Athens", 23.73, 37.98, {})], extra=[{"k": "scale", "x": 80, "y": 1240, "w": v.km(100), "t": "100 km"}])
    gy = 600
    s2 = {"base": "section", "tod": "dusk", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": "#b8b0a0", "t": "limestone, with hydrocarbons"}, {"d": 420, "c": "#8a8270", "t": ""}], "cam": [1, 500, 900],
          "els": [{"k": "line", "p": [[380, 1300], [520, gy]], "c": RED, "w": 4, "in": .3}, {"k": "line", "p": [[700, 1300], [520, gy]], "c": RED, "w": 4, "in": .5}] +
          [{"k": "arrow", "p": [[520 + dx, 900], [520 + dx, gy + 20]], "c": "#9fd0ff", "w": 2, "in": .9 + i * .15} for i, dx in enumerate((-30, 0, 30))] +
          [{"k": "rect", "x": 440, "y": gy - 120, "w": 160, "h": 120, "fill": "#e2d8c4", "c": "#fff", "sw": 1.2, "in": .2},
           {"k": "label", "x": 520, "y": gy - 150, "t": "the adyton, the inner room", "st": "small", "in": .4},
           {"k": "label", "x": 500, "y": 1370, "t": "two faults cross beneath; springs once flowed; gas still leaks", "c": AMBER, "in": 1.5}]}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("the ancient reports", AMBER, ["a breath rising from the ground · Strabo", "a sweet smell in the waiting room · Plutarch", "weaker in his day · Plutarch"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("what leaks today", "#9fd0ff", ["methane", "ethane", "carbon dioxide"]) +
          [{"k": "label", "x": 500, "y": 900, "t": "ethylene: far too little for a trance", "c": "#ffb09a", "in": 1.4}]}
    tl, ax = timeline(-850, 450, [(-800, "800 BCE"), (-400, "400 BCE"), (1, "1 CE"), (400, "400 CE")], "A thousand years of answers")
    tl["els"] += [{"k": "band", "x0": ax.x(-800), "x1": ax.x(390), "y": 700, "h": 16, "c": GOLD, "t": "the oracle speaks", "in": .3}] + \
                 event(ax, -373, "an earthquake destroys the temple", row=1, c=RED, i=.6) + event(ax, 100, "Plutarch serves as priest", row=2, c=BONE, i=.9) + event(ax, 390, "the end", row=0, c=BONE, i=1.2)
    s5 = tl
    s6 = like(s0, cam=[1.15, 500, 980])
    shots = [s0, s1, s2, s3, s4, s5, s6]
    beats = [
        B("hook", 0, ["[d:intrigue][k:THE ORACLE OF DELPHI][sfx:boom][act:storytelling, with reverence]For a ^thousand years, a priestess sat in Apollo's temple and spoke for the ^god. [act:hushed, evocative]Ancient writers said a ^sweet vapour rose from the ^rock beneath her.",
                      "[d:tension][cam:1.12|0|0][act:plain, setting up the turn]Scholars called it a ^myth. [act:the twist, quietly pleased]Then ^geologists found the ^faults."], cut=False),
        B("world", 3, ["[d:calm][k:THE REPORTS][act:quoting the ancients, respectful]Strabo described a ^breath rising from the ground. [act:a trusted witness, careful]Plutarch, who served as a ^priest at Delphi, wrote of a sweet smell, and said it was ^weaker in his day."]),
        B("collision", 2, ["[d:build][k:THE FAULTS][act:a detective's pleasure, building]Around {2000|the year two thousand}, a geologist and an archaeologist mapped two faults crossing right ^beneath the temple, and the deposits of old ^springs.",
                           "[d:build][sfx:shimmer][act:quiet wonder, present tense]Gas ^still leaks there today."]),
        B("cost", 4, ["[d:build][k:THE GAS][act:naming the suspect, intrigued]Their suspect@noun: ^ethylene, a sweet-smelling gas once used@verb as an ^anaesthetic. [act:lighter, a small smile]Mild doses bring ^euphoria.",
                      "[d:build][act:the complication, even]But later surveys@noun found mostly ^methane, ^ethane and carbon ^dioxide. [act:plain, closing that door][tune:fall]Far too ^little ethylene for a trance."]),
        B("reversal", 0, ["[d:reveal][k:THE TWIST][sfx:hit][act:satisfied, counting it off]So half the old story holds: the ^faults, the ^springs, the ^gas.",
                          "[d:build][act:careful, fair]The ^other half, the drug, is not ^established. [act:thinking aloud, lighter][tune:level]Maybe ^ritual. [act:another idea, same tone][tune:fall]Maybe less ^oxygen in a closed room."]),
        B("tag", 6, ["[d:verdict][k:THE VERDICT][p:0.95][act:weighing it, calm authority][tune:rise]The Pythia's trance, from ^gas? [act:the verdict, honest][tune:fall]^*Open question*. [act:the other part][tune:rise]The ^vapour from the rock? [act:simple and sure][tune:highfall]^Real.",
                     "[d:tension][p:0.93][act:respectful, warm]The ancient writers ^weren't making it up. [act:gentle, the last word][tune:fall]They may just not have ^known what they were smelling."]),
    ]
    return EP("delphi", "07.06", "The Oracle of Delphi: Did the Earth Speak Through Her?", "delphi", "contested", "Did gas from faults under the temple put the Pythia into her trance?", "Then geologists found the *faults*.", beats, shots,
              "de Boer, Hale & Chanton 2001, Geology · Spiller, Hale & de Boer 2002 · Etiope et al. 2006 · Strabo 9.3.5 · Plutarch, De defectu oraculorum",
              "Ancient writers said a sweet vapour rose beneath Apollo's temple at Delphi. Geologists found the faults and the gas: whether it put the Pythia in a trance is still open.",
              ["#Delphi", "#Oracle", "#AncientGreece", "#Geology", "#Underworlds"])


def _iso_of(sh):
    return next(e for e in sh["els"] if e.get("k") == "iso")


def _ov(sh, items, at, **kw):
    """Items drawn with a shot's own iso projection (they turn with the model), built at `at`."""
    b = _iso_of(sh)
    e = {k: b[k] for k in ("x", "y", "s", "az", "spin", "el") if k in b}
    e.update({"k": "iso", "items": list(items), "in": at})
    e.update(kw)
    return e


def _wisp(x, y, h, at, c="#cfe6ff", ph=0.0, n=9, amp=14, op=.75, dur=1.2):
    """A thread of vapour rising from (x, y), h tall."""
    from illus import line
    return line([[round(x + amp * math.sin(k * .9 + ph), 1), round(y - h * k / (n - 1), 1)] for k in range(n)], at, c, 3, dur=dur, curve=True, op=op)


def malta_m():
    """Malta's temples as one continuous take (see mural.py): a six-metre wall beside a two-storey house, a thousand years before
    the pyramids, the drowned-temple claim and the dive, layers that date the temples from below, the Hypogeum, and the crossing."""
    import copy
    from mural import remix, rewritten
    import illus as I
    ep = rewritten(copy.deepcopy(malta()))              # authored times below follow the rewritten words (about 2.4 words a second)
    S = ep["shots"]
    STONE = "#d8c7a2"
    s0 = copy.deepcopy(S[0])
    iso0 = _iso_of(s0)
    iso0["items"] = [it for it in iso0["items"] if it.get("t") != "label"] + [L_(0, 7, "Ġgantija", GOLD, z=-10, dy=-24)]
    # 0, beat 1 · a wall six metres high, about two storeys of a house (1.7 m person for scale; 6 m = 210 px)
    K = 35
    wall = [I.box(250, 600 - 6 * K, 170, 6 * K, STONE, "#8c7152", 2, 4, 5.0, fx="fill", dur=.9)] + \
           [I.line([[250, 600 - j * K * 1.5], [420, 600 - j * K * 1.5]], 5.4, "#8c7152", 1.5, draw=False) for j in range(1, 4)] + \
           [{"k": "dim", "x1": 200, "y1": 600, "x2": 200, "y2": 600 - 6 * K, "t": "6 m", "in": 6.2, "c": GOLD}, I.person(460, 600, 1.7 * K, 6.6),
            I.box(560, 600 - 6 * K, 170, 6 * K, "#8e7152", "#e8d6b8", 2, 2, 8.0, fx="rise"), I.line([[560, 600 - 3 * K], [730, 600 - 3 * K]], 8.2, "#e8d6b8", 2, draw=False)] + \
           [I.box(x, y, 34, 40, "#ffe2a8", r=2, at=8.4) for x in (590, 665) for y in (600 - 5 * K, 600 - 2 * K)] + \
           [I.line([[150, 600], [850, 600]], 4.8, "#8c7152", 3, draw=False), I.label(645, 650, "two storeys", 8.8, I.BONE, 28)]
    # 2 · a thousand years before the pyramids (4000 to 2000 BCE across 760 px)
    X = lambda yr: round(120 + (4000 - yr) * .38, 1)
    pyr = [I.line([[100, 1000], [900, 1000]], .2, I.BONE, 3, dur=.8)] + \
          [x for yr, t in ((4000, "4000 BCE"), (3000, "3000"), (2000, "2000")) for x in (I.line([[X(yr), 988], [X(yr), 1012]], .4, I.BONE, 2, draw=False), I.label(X(yr), 1060, t, .4, "#cbbca8", 28))] + \
          [I.box(X(3600) - 60, 820, 36, 110, STONE, "#8c7152", 2, 3, .8, fx="rise"), I.box(X(3600) + 24, 820, 36, 110, STONE, "#8c7152", 2, 3, .8, fx="rise"),
           I.box(X(3600) - 75, 790, 150, 32, STONE, "#8c7152", 2, 3, 1.0, fx="rise"), I.line([[X(3600), 940], [X(3600), 990]], .9, GOLD, 3, dur=.3),
           I.label(X(3600), 740, "Ġgantija", 1.0, GOLD, 32),
           {"k": "pyramid", "x": X(2600), "y": 930, "w": 260, "ghost": True, "style": "inferred", "color": I.BONE, "in": 2.6},
           I.line([[X(2600), 940], [X(2600), 990]], 2.8, I.BONE, 3, "inferred", .3), I.label(X(2600), 720, "the pyramids", 3.0, I.BONE, 32),
           I.arrow([[X(3600), 1130], [X(2600), 1130]], 5.4, GOLD, 4, "known", 1.0, False), I.label((X(3600) + X(2600)) / 2, 1190, "about 1,000 years", 6.4, GOLD, 32)]
    # 4 · the claim: temples from the Ice Age, when the sea stood lower, more of them under water; the 2002 dive
    coast = {"k": "poly", "p": [[60, 700], [380, 700], [470, 820], [620, 960], [790, 1140], [940, 1290], [940, 1420], [60, 1420]], "fill": "#6a5640", "c": "#c9ad85", "w": 2, "in": .2}
    temple = lambda x, y, at, ghost=False: ([I.box(x - 40, y - 46, 22, 46, "none" if ghost else STONE, I.LILAC if ghost else "#8c7152", 2, 3, at, style="claimed" if ghost else "known"),
                                             I.box(x + 18, y - 46, 22, 46, "none" if ghost else STONE, I.LILAC if ghost else "#8c7152", 2, 3, at, style="claimed" if ghost else "known"),
                                             I.box(x - 48, y - 62, 96, 16, "none" if ghost else STONE, I.LILAC if ghost else "#8c7152", 2, 3, at, style="claimed" if ghost else "known")])
    claim = [{"k": "water", "y": 820, "h": 600, "x0": 400, "x1": 1000, "op": .55, "in": .1}, coast] + temple(220, 700, .6) + \
            [I.label(220, 760, "today", .8, I.BONE, 28), I.label(880, 800, "sea today", 1.0, I.BLUE, 28, "end"),
             I.line([[560, 1200], [940, 1200]], 7.2, I.BLUE, 3, "inferred", .8), I.label(930, 1250, "Ice Age sea?", 7.8, I.BLUE, 28, "end")] + \
            temple(560, 935, 9.2, True) + temple(720, 1105, 9.8, True) + I.question(640, 1060, 10.4, 60)
    dive = [{"k": "boat", "x": 820, "y": 818, "w": 120, "in": .6}, I.label(820, 760, "2002", 1.0, I.BONE, 30),
            I.arrow([[800, 850], [740, 950], [700, 1040]], 2.0, I.BONE, 3, "inferred", 1.2), I.oval(705, 1050, 26, 11, "#e8d6b8", "none", 0, 1, 3.2), I.dot(684, 1044, 9, "#e8d6b8", 3.2)]
    # 3 · dated from below: a floor seals what lies beneath; charcoal and bone, pottery styles, the farm village underneath; 3600 to 2500 BCE
    lay = [I.box(60, 720, 880, 150, "#a8977c", r=0, at=.3, fx="fill"), I.box(60, 870, 880, 220, "#7a6248", r=0, at=.6, fx="fill"), I.box(60, 1090, 880, 90, "#5a4632", r=0, at=.9, fx="fill"),
           I.box(160, 700, 680, 22, "#efe6d2", "#8c7152", 2, 2, 3.0, fx="rise")] + \
          [I.box(200 + 130 * k, 700 - 110 - 20 * (k % 2), 70, 110 + 20 * (k % 2), STONE, "#8c7152", 2, 4, round(3.2 + .1 * k, 2), fx="rise") for k in range(5)] + \
          [I.ring(500, 795, 90, 5.4, GOLD, 3, dur=.6), I.label(870, 650, "the floor", 3.4, I.BONE, 28, "end")] + \
          [I.dot(x, y, 7, "#1a1511", round(8.0 + .03 * k, 2)) for k, (x, y) in enumerate(I.scatter(18, 400, 600, 745, 850, 4))] + \
          [I.box(x, y, 26, 8, "#efe6d2", r=4, at=round(9.0 + .1 * k, 2)) for k, (x, y) in enumerate(((430, 770), (520, 815), (565, 760), (470, 830)))] + \
          [I.arrow([[600, 790], [640, 728]], 11.4, GOLD, 3, "known", .5, False), I.label(170, 810, "charcoal, bone", 8.6, "#cbbca8", 28, "start")] + \
          [{"k": "vase", "x": 640 + 95 * k, "y": 1060, "h": 70, "w": 46, "profile": pf, "in": round(14.0 + .4 * k, 2), "fx": "rise"} for k, pf in enumerate((
              [[0, .3], [.2, .5], [.6, .5], [1, .25]], [[0, .45], [.1, .4], [.5, .55], [1, .2]], [[0, .2], [.3, .3], [.7, .55], [1, .35]]))] + \
          [I.label(735, 1130, "pottery", 15.0, "#cbbca8", 28)] + \
          [{"k": "house", "x": 140 + 120 * k, "y": 1060, "w": 90, "h": 60, "in": round(16.8 + .2 * k, 2), "fx": "rise"} for k in range(3)] + \
          [I.label(320, 1130, "older village", 17.4, "#cbbca8", 28)]
    XA = lambda yr: round(140 + (4000 - yr) * .36, 1)
    lay += [I.line([[120, 1300], [880, 1300]], 19.6, I.BONE, 3, dur=.6)] + \
           [I.box(XA(3600), 1286, XA(2500) - XA(3600), 28, GOLD, r=14, at=20.6, fx="fill"), I.label(XA(3600), 1360, "3600", 21.0, GOLD, 30), I.label(XA(2500), 1360, "2500 BCE", 21.6, GOLD, 30)]
    # 5 · the Hypogeum: three levels cut into the rock; the remains of some seven thousand people, of the same age
    hyp = copy.deepcopy(S[3])
    hyp["els"] = [e for e in hyp["els"] if e.get("k") != "label"] + \
        [I.label(500, 500, "the Hypogeum", .4, GOLD, 34), {"k": "dim", "x1": 890, "y1": 560, "x2": 890, "y2": 1100, "t": "3 levels", "in": 4.0, "c": GOLD, "lx": -10},
         I.glow(500, 900, 260, 6.0, .35, "lamp"), I.label(500, 1260, "about 7,000 people", 7.6, "#f2dcb4", 32), I.label(500, 1330, "same age", 10.6, GOLD, 30)]
    # 1 · the map, at last: hunter-gatherers cross about 100 km of open sea, about 8,500 years ago; farmers a thousand years later
    mp = copy.deepcopy(S[1])
    mp["els"] = [e for e in mp["els"] if not (e.get("k") == "label" and "open sea" in e.get("t", ""))]
    v = View(11.8, 16.2, 35.4, 38.3, (40, 330, 920, 900))
    (ax_, ay_), (bx_, by_) = v.p(14.8, 36.72), v.p(14.45, 36.08)
    cross = [I.arrow([[ax_, ay_], [ax_ - 60, (ay_ + by_) / 2], [bx_ + 6, by_ - 6]], 9.2, I.BLUE, 4, "inferred", 1.4),
             {"k": "boat", "x": ax_ - 52, "y": (ay_ + by_) / 2 + 10, "w": 70, "in": 9.6}, I.label(ax_ - 90, (ay_ + by_) / 2 - 20, "about 100 km", 10.6, I.BLUE, 28, "end"),
             I.label(ax_ - 90, (ay_ + by_) / 2 + 20, "8,500 years ago", 7.4, I.BLUE, 28, "end")]
    farm = [I.arrow([[ax_ + 30, ay_ + 4], [ax_ + 10, (ay_ + by_) / 2], [bx_ + 30, by_ - 4]], .6, I.BONE, 3, "known", 1.0),
            I.label(ax_ + 60, (ay_ + by_) / 2 + 10, "farmers", 1.2, I.BONE, 28, "start"), I.label(ax_ + 60, (ay_ + by_) / 2 + 50, "1,000 years later", 1.8, I.BONE, 28, "start")]
    ep["beats"][4]["visual"]["from"] = 1                 # the crossing is told on the map (shot 5 now holds the Hypogeum)
    return remix(ep, _rewrite=False, scenes={0: s0, 1: mp, 2: {"base": "dark", "cam": [1, 500, 900], "els": pyr}, 3: {"base": "dark", "cam": [1, 500, 900], "els": lay},
                                             4: {"base": "dark", "cam": [1, 500, 900], "els": claim}, 5: hyp},
                 alias={6: 0}, cams={6: [1.15, 500, 960]}, adds={1: cross},
                 beat_adds={1: (wall, None)}, line_adds={(0, 1): (I.question(860, 470, .3, 80), None), (2, 1): (dive, None), (4, 1): (farm, None)})


def delphi_m():
    """Delphi as one continuous take (see mural.py): the vapour, the two witnesses, the faults and springs under the temple,
    the suspect gas and the gas actually measured, and the half of the story that holds."""
    import copy
    from mural import remix, rewritten
    import illus as I
    ep = rewritten(copy.deepcopy(delphi()))             # authored times below follow the rewritten words (about 2.4 words a second)
    S = ep["shots"]
    FAULT, VAP = "#ff8a7a", "#cfe6ff"
    # 0 · the temple, without its faults: the vapour rises first; the faults are found on the next line
    s0 = copy.deepcopy(S[0])
    iso0 = _iso_of(s0)
    faults = [it for it in iso0["items"] if it.get("t") == "line"]
    iso0["items"] = [it for it in iso0["items"] if it.get("t") not in ("line", "label")]
    vapour = [I.label(500, 1370, "Temple of Apollo", .6, GOLD, 32)] + [_wisp(470 + 30 * k, 800, 230, round(15.4 + .3 * k, 2), VAP, 2.1 * k, 9, 14, .8, 1.4) for k in range(3)]
    found = [_ov(s0, [dict(f, w=5) for f in faults], 6.0, fx="draw", dur=1.2),
             _ov(s0, [L_(20, 18, "Delphi fault", FAULT, z=6, dy=-14), L_(2, 8.5, "Kerna fault", FAULT, z=20, dy=36)], 7.0)]
    # 3 · the witnesses: Strabo's breath from the ground, Plutarch's sweet smell in the waiting room, weaker in his day
    scroll = lambda x, y, at: [I.box(x, y, 150, 110, "#e9d6ad", "#8a6a3e", 2, 6, at), I.box(x - 10, y - 8, 14, 126, "#c9ad7d", r=6, at=at), I.box(x + 146, y - 8, 14, 126, "#c9ad7d", r=6, at=at)] + \
                            [I.line([[x + 20, y + 26 + 20 * j], [x + 130 - 15 * (j % 2), y + 26 + 20 * j]], at + .2, "#8a6a3e", 2, draw=False) for j in range(4)]
    wit = scroll(120, 420, .4) + [I.label(195, 590, "Strabo", .8, I.BONE, 30), I.line([[380, 620], [900, 620]], .9, "#8c7152", 3, draw=False)] + \
          [_wisp(460 + 110 * k, 610, 170, round(2.2 + .3 * k, 2), VAP, k) for k in range(4)] + \
          [I.label(640, 680, "a breath", 3.6, VAP, 30)] + \
          [I.person(150, 1010, 130, 5.0), I.label(150, 1060, "Plutarch", 5.6, I.BONE, 30),
           I.box(380, 760, 500, 260, "rgba(42,34,27,.9)", "#c9ad85", 3, 8, 8.4), I.line([[380, 900], [380, 1000]], 8.4, "rgba(42,34,27,1)", 6, draw=False)] + \
          [I.person(560 + 110 * k, 1010, 90, round(9.0 + .2 * k, 2)) for k in range(3)] + \
          [I.line([[300, 930], [360, 920], [440, 945], [520, 925], [600, 950], [680, 930]], 10.2, "#f2c98e", 3, dur=1.2, curve=True, op=.8), I.label(560, 1060, "a sweet smell", 10.8, "#f2c98e", 30)] + \
          [_wisp(x, 1290, h, round(15.0 + .6 * k, 2), VAP, k, 7, 10) for k, (x, h) in enumerate(((330, 200), (500, 130), (670, 65)))] + \
          [I.line([[260, 1300], [740, 1300]], 14.6, "#8c7152", 3, draw=False), I.arrow([[300, 1335], [700, 1335]], 16.6, I.AMBER, 3, "known", .8, False),
           I.label(260, 1390, "long ago", 15.0, I.BONE, 28, "start"), I.label(740, 1390, "his day", 16.4, I.BONE, 28, "end")]
    # 2 · beneath the temple: two faults cross; blocks grind; limestone holding hydrocarbons; springs once rose; gas still seeps
    gy = 600
    fx0, fy0 = 520, gy                                   # where the faults meet the floor of the inner room
    temple = [I.box(380, gy - 30, 280, 30, "#e2d8c4", "#fff", 1.2, 2, .4)] + [I.box(398 + 40 * k, gy - 150, 18, 120, "#efe6d2", r=2, at=.5) for k in range(7)] + \
             [{"k": "poly", "p": [[370, gy - 150], [670, gy - 150], [520, gy - 210]], "fill": "#e2d8c4", "c": "#fff", "w": 1.2, "in": .6}, I.glow(fx0, gy - 60, 90, .8, .6, "lamp")]
    fl = [I.line([[330, 1380], [fx0, fy0]], 5.4, FAULT, 5, dur=1.0), I.line([[760, 1380], [fx0, fy0]], 6.4, FAULT, 5, dur=1.0),
          I.label(300, 1300, "Delphi fault", 7.2, FAULT, 30, "end"), I.label(790, 1300, "Kerna fault", 7.6, FAULT, 30, "start")]
    grind = [I.arrow([[330, 1180], [380, 920]], 12.0, I.BONE, 4, "known", .7, False), I.arrow([[470, 900], [420, 1160]], 12.4, I.BONE, 4, "known", .7, False),
             I.glow(415, 1040, 70, 13.0, .6, "red")]
    hc = [I.dot(x, y, 5, "#2a2219", round(20.0 + .02 * k, 2)) for k, (x, y) in enumerate(I.scatter(60, 140, 900, 700, 1400, 11))] + [I.label(900, 760, "hydrocarbons", 21.6, I.AMBER, 30, "end")]
    springs = [I.arrow([[fx0 + 14, 1180 - 120 * k], [fx0 + 8, 1080 - 120 * k]], round(26.6 + .3 * k, 2), I.BLUE, 3, "known", .5, False) for k in range(4)] + \
              [{"k": "poly", "p": [[600, gy], [880, gy], [860, gy - 22], [640, gy - 26]], "fill": "#efe6d2", "c": "#c9ad85", "w": 2, "in": 29.0, "fx": "fill"},
               I.label(760, gy - 50, "old springs", 29.6, I.BLUE, 30)]
    sec = {"base": "section", "tod": "dusk", "ground": gy, "lx": 130, "layers": [{"d": 0, "c": "#b8b0a0", "t": ""}, {"d": 420, "c": "#8a8270", "t": ""}], "cam": [1, 500, 900],
           "els": temple + fl + grind + hc + springs}
    seep = [I.line([[fx0, fy0 + 140], [fx0 - 40, fy0 + 90]], 3.6, FAULT, 2, dur=.4), I.line([[fx0, fy0 + 220], [fx0 + 50, fy0 + 170]], 3.9, FAULT, 2, dur=.4)] + \
           [I.dot(fx0 + (9 if k % 2 else -9), 1200 - 75 * k, 6 + (k % 3), VAP, round(.5 + .45 * k, 2), "rise", .8) for k in range(9)] + \
           [_wisp(fx0, gy - 20, 120, 4.8 + .5 * k, VAP, k) for k in range(2)] + [I.label(fx0, gy - 250, "gas today", 2.2, VAP, 32)]
    # 4 · the suspect: ethylene (an old anaesthetic, a sweet smell); then what the surveys measured
    eth = [I.line([[400, 470], [520, 470]], 1.0, I.BONE, 4, draw=False), I.line([[400, 486], [520, 486]], 1.0, I.BONE, 4, draw=False),
           I.dot(400, 478, 34, "#5a534c", .8), I.dot(520, 478, 34, "#5a534c", .8)] + \
          [I.dot(x, y, 18, "#efe8da", 1.1) for x, y in ((340, 420), (340, 536), (580, 420), (580, 536))] + \
          [I.label(460, 610, "ethylene", 1.6, I.AMBER, 34),
           I.box(120, 760, 220, 30, "#8c7152", r=6, at=4.6), I.oval(150, 740, 26, 22, "#e8d6b8", "none", 0, 1, 4.8), I.box(176, 728, 150, 34, "#e8d6b8", r=12, at=4.8),
           I.label(230, 840, "asleep", 6.0, I.LILAC, 30)] + \
          [I.glow(230 + 60 * k, 680 - 30 * (k % 2), 50, round(9.0 + .3 * k, 2), .7, "lamp") for k in range(3)] + \
          [I.line([[700, 800], [760, 680]], 12.8, "#c9ad85", 4, draw=False), I.line([[820, 800], [760, 680]], 12.8, "#c9ad85", 4, draw=False), I.line([[760, 800], [760, 680]], 12.8, "#c9ad85", 4, draw=False),
           I.person(760, 680, 110, 13.0, "#e8d6b8")] + [_wisp(760, 800, 90, 13.6, "#f2c98e", 0, 7, 10)] + \
          [I.arrow([[560, 470], [650, 520], [700, 580]], 14.4, I.AMBER, 3, "inferred", .8)]
    bars = [I.line([[110, 1340], [890, 1340]], .2, "#8c7152", 3, draw=False), I.label(500, 900, "schematic", 1.0, "#9a938a", 28)] + \
           [I.box(x, 1340 - h, 140, h, c, r=6, at=at, fx="fill", dur=.9) for x, h, c, at in ((130, 330, I.BLUE, 4.4), (320, 140, "#8fd9b0", 5.4), (510, 290, "#cbd2d8", 6.6), (700, 6, I.AMBER, 11.6))] + \
           [I.label(x + 70, 1390, t, at, c, 28) for x, t, c, at in ((130, "methane", I.BLUE, 4.6), (320, "ethane", "#8fd9b0", 5.6), (510, "CO2", "#cbd2d8", 6.8), (700, "ethylene", I.AMBER, 11.8))] + \
           [I.glow(770, 1336, 50, 12.0, .8, "lamp"), I.line([[690, 1010], [850, 1010]], 13.6, FAULT, 3, "inferred", .6), I.label(850, 980, "for a trance", 14.0, FAULT, 28, "end"),
            I.arrow([[770, 1320], [770, 1030]], 14.4, FAULT, 2, "claimed", .6, False)]
    # 0 again: half the story holds (faults, springs, gas); the other half (drug, ritual, oxygen) stays open
    tick = lambda x, y, at, c=I.GREEN: I.line([[x - 16, y], [x - 4, y + 14], [x + 20, y - 16]], at, c, 5, dur=.4)
    holds = [I.box(110, 280, 780, 110, "rgba(18,13,10,.8)", I.GREEN, 2, 14, .2)] + \
            [x for k, (t, at) in enumerate((("faults", 2.0), ("springs", 3.0), ("gas", 4.0))) for x in (tick(190 + 250 * k, 335, at), I.label(225 + 250 * k, 346, t, at, I.BONE, 32, "start"))]
    rest = [I.box(110, 405, 780, 155, "rgba(18,13,10,.8)", I.LILAC, 2, 14, .2, style="claimed")] + \
           [I.dot(205, 455, 18, "#5a534c", 1.4), I.dot(265, 455, 18, "#5a534c", 1.4), I.line([[205, 450], [265, 450]], 1.4, I.BONE, 3, draw=False), I.line([[205, 461], [265, 461]], 1.4, I.BONE, 3, draw=False),
            I.label(235, 535, "a drug?", 2.0, I.LILAC, 28)] + \
           [I.glow(500, 455, 60, 4.6, .8, "lamp"), I.dot(500, 465, 12, "#ffd27a", 4.6), I.label(500, 535, "ritual?", 5.0, I.LILAC, 28)] + \
           [I.box(715, 420, 100, 72, "none", "#c9ad85", 3, 6, 8.6)] + [I.dot(x, y, 5, I.BLUE, round(8.9 + .1 * k, 2)) for k, (x, y) in enumerate(((735, 440), (790, 455), (755, 475)))] + \
           [I.label(765, 535, "less oxygen?", 9.4, I.LILAC, 28)] + I.question(860, 470, 14.0, 50)
    return remix(ep, _rewrite=False, scenes={0: s0, 2: sec, 3: {"base": "dark", "cam": [1, 500, 880], "els": wit}, 4: {"base": "dark", "cam": [1, 500, 880], "els": eth}},
                 alias={1: 0, 5: 0, 6: 0}, cams={6: [1.15, 500, 980]}, adds={0: vapour},
                 beat_adds={4: (holds, [1.1, 500, 900])},
                 line_adds={(0, 1): (found, None), (2, 1): (seep, None), (3, 1): (bars, None), (4, 1): (rest, None)})


# ---------------------------------------------------------------- 07.07 The ledger
def _ledger_text():
    v = View(-95, 140, -25, 52, (40, 330, 920, 900))
    s0 = mapshot(v, pins=[("Derinkuyu", 34.74, 38.37, {"c": GOLD}), ("Longyou", 119.2, 29.08, {"a": "end", "lx": -18}), ("Malta", 14.4, 35.9, {"a": "end", "lx": -18}),
                          ("Delphi", 22.5, 38.48, {"a": "end", "lx": -18, "ly": -22}), ("Chavín", -77.18, -9.59, {"a": "start"}), ("Borobudur", 110.2, -7.6, {"a": "end", "lx": -18})], cam=[1, 500, 860])
    s1 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Established · likely", "#8fd9b0", ["Malta's temples, from c. 3600 BCE", "Derinkuyu grew as a Byzantine refuge", "Chavín was built to carry sound"])}
    s2 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Open question", "#e8b87a", ["who dug Longyou's halls, and why", "whether gas moved the Pythia"])}
    s3 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Awaiting evidence", "#9fd0ff", ["Ice Age depths under Derinkuyu", "temple plans taken from sound patterns"])}
    s4 = {"base": "dark", "cam": [1, 500, 860], "els": grp("Ruled out", "#ff8a7a", ["Ice Age temples on Malta", "stones lifted by sound"])}
    s5 = like(s0, cam=[1.12, 500, 880])
    shots = [s0, s1, s2, s3, s4, s5]
    beats = [
        B("hook", 0, ["[d:intrigue][k:UNDERWORLDS][sfx:boom][act:inviting, a warm opener]Cities under the ^ground, halls cut in ^silence, rooms that ^sing. [act:brisk, friendly][tune:fall]Here's the ^ledger."], cut=False),
        B("world", 1, ["[d:calm][k:ESTABLISHED][act:confident, ticking them off][tune:level]Malta's temples are ^older than the pyramids. [act:same assurance][tune:level]Derinkuyu grew as a ^Byzantine refuge. [act:the last one, settled][tune:fall]And at Chavín, the builders almost ^certainly worked with ^sound."]),
        B("collision", 2, ["[d:build][k:OPEN QUESTIONS][act:open, curious][tune:level]^Who dug the Longyou halls, and ^why. [act:the second puzzle][tune:fall]Whether ^gas moved the oracle of Delphi."]),
        B("cost", 3, ["[d:build][k:AWAITING EVIDENCE][act:fair, even][tune:level]^Ice Age depths beneath Derinkuyu. [act:same tone][tune:fall]Temples laid out from ^sound patterns. [d:aside][act:candid, lighter][tune:fallrise]^Possible. [act:plain, honest][tune:fall]Not ^yet shown."]),
        B("reversal", 4, ["[d:reveal][k:RULED OUT][sfx:hit][act:crisp, closing doors][tune:level]^Ice Age temples on Malta. [act:same, and final][tune:fall]Stones ^lifted by sound."]),
        B("tag", 5, ["[d:verdict][k:THE MORAL][p:0.95][act:reflective, calm authority]Underground, the evidence is ^hard to date and ^easy to erase. [go:5|1.5][act:warm, gently firm]That's a reason to dig ^carefully, not to fill the gaps with ^wishes.",
                     "[d:tension][p:0.93][act:the motto, quiet and sure][tune:fall]^Coherence is the measure. [gap:0.45][act:gentle, the closing note][tune:fall]Not ^final demonstration."]),
    ]
    return EP("underworlds-ledger", "07.07", "Underworlds · The Ledger", "", "mixed", "What the underground and the singing stones really tell us.", "Here's the *ledger*.", beats, shots,
              "Every source in the case files of File 07",
              "The verdicts of Underworlds in one ledger: what is established, what is still open, what awaits evidence, and what is ruled out.",
              ["#History", "#Archaeology", "#UndergroundCity", "#Underworlds", "#WeighItYourself"])


def ledger():
    """The ledger as one continuous film: six underworlds in a cabinet (see cabinet.py)."""
    import math as _m
    from cabinet import Cabinet, VCOL, retime
    def mdl(ep, k=None):
        if k is not None:
            return ep["shots"][k]
        sh = next((sh for sh in ep["shots"] if any(e.get("k") == "iso" for e in sh["els"])), ep["shots"][0])
        return next((e for e in sh["els"] if e.get("k") == "iso"), sh)
    C = Cabinet([
        {"name": "Malta's temples", "model": mdl(malta())},
        {"name": "Derinkuyu", "model": mdl(derinkuyu(), 0)},
        {"name": "Temple acoustics", "model": mdl(acoustics(), 0)},
        {"name": "The Longyou caves", "model": mdl(longyou())},
        {"name": "Delphi", "model": mdl(delphi())},
        {"name": "Sound patterns", "model": mdl(cymatic(), 0)},
    ])
    C.build()
    MA, DE, TA, LY, DL, CY = range(6)
    arc = lambda r, a0, a1: [[round(r * _m.cos(_m.radians(a)), 1), round(-170 + r * .8 * _m.sin(_m.radians(a)), 1)] for a in range(a0, a1 + 1, 8)]
    waves = C.local(TA, [{"k": "line", "p": arc(r, a0, a1), "c": "#f2c98e", "w": 2.5, "curve": True, "fx": "draw", "dur": .6, "in": .7 + .22 * k}
                         for k, r in enumerate((40, 70, 100, 130)) for a0, a1 in ((-50, 50), (130, 230))])
    gas = C.local(DL, [{"k": "line", "p": [[x + 8 * _m.sin(k * .9 + x), -20 - 12 * k] for k in range(17)], "c": "#c8e6a0", "w": 2.5, "curve": True, "style": "inferred", "fx": "draw", "dur": 1.2, "in": .6 + .15 * j}
                       for j, x in enumerate((-50, 0, 50))])
    deeper = C.local(DE, [{"k": "arrow", "p": [[150, -250], [150, -60]], "c": "#c9c1ee", "w": 3, "style": "claimed", "fx": "draw", "dur": 1.0, "in": .6}])
    s1 = C.step(C.cam_cell(MA), C.verdict(MA, "established", "older than the pyramids", .4))
    s2 = C.step(C.cam_cell(DE), C.verdict(DE, "established", "a Byzantine refuge", .3) + C.people(DE, 3, at=.8))
    s3 = C.step(C.cam_cell(TA), C.verdict(TA, "strong", "Chavín worked with sound", .3) + waves)
    s4 = C.step(C.cam_cell(LY), C.verdict(LY, "open", "who dug them, and why?", .2) + C.question(LY, dx=C.w * .32, dy=-250, at=.6, size=70))
    s5 = C.step(C.cam_cell(DL), C.verdict(DL, "open", "gas, or not?", .2) + gas)
    s6 = C.step(C.cam_cell(DE), C.verdict(DE, "awaiting", "Ice Age depths?", .2, frame=False) + deeper)
    s7 = C.step(C.cam_cell(CY), C.verdict(CY, "awaiting", "laid out by sound?", .2))
    s8 = C.step(C.cam_all(), [e for k, i in enumerate((DE, CY)) for e in C.wash(i, VCOL["awaiting"], at=.1 + .2 * k, op=.13)])
    s9 = C.step(C.cam_cell(MA), C.verdict(MA, "ruled", at=.1) + C.struck(MA, "Ice Age temples", at=.2))
    s10 = C.step(C.cam_cell(CY), C.verdict(CY, "ruled", at=.1, frame=False) + C.struck(CY, "stones lifted by sound", at=.2))
    s11 = C.step(C.cam_cells([DE, LY]))
    s12 = C.step(C.cam_all(), [e for i in range(6) for e in C.wash(i, "#f2b36b", at=.3 + .1 * i, op=.11)])
    s13 = C.step(C.cam_all(k=.86, sy=720))
    beats = retime(_ledger_text()["beats"], {
        0: (0, {}),
        1: (s1, {(0, 1): "%d|1.1" % s2, (0, 2): "%d|1.1" % s3}),
        2: (s4, {(0, 1): "%d|1.1" % s5}),
        3: (s6, {(0, 1): "%d|1.1" % s7, (0, 2): "%d|1.2" % s8}),
        4: (s9, {(0, 1): "%d|1.1" % s10}),
        5: (s11, {(0, 1): "%d|1.2" % s12, (1, 0): "%d|3" % s13}),
    })
    old = _ledger_text()
    old.update(beats=beats, shots=C.shots)
    return old


def acoustics_m():
    """Temples that sing as one continuous take (see mural.py): the ringing, the rooms and the claims are drawn."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN, GREEN, AU
    ep = acoustics()
    short = lambda e: e.get("k") == "label" and len(e.get("t", "")) <= 26
    # 1 · how long a low note hangs: a concert hall, a cathedral, the Hypogeum
    def wave(y, T, c, at, dur):
        pts = [[140 + 720 * t / 16, round(y + 60 * math.exp(-3 * t / T) * math.sin(t * 7), 1)] for t in [16 * k / 320 for k in range(321)] if t <= T * 1.15]
        return [line(pts, at, c, 3, dur=dur)]
    ring_ = {"base": "dark", "cam": [1, 500, 900], "els": [line([[140, 1260], [860, 1260]], .1, "#8c7152", 2, draw=False)] +
             [label(140 + 720 * t / 16, 1300, "%d s" % t, .2, BN, 24) for t in (0, 4, 8, 12, 16)] +
             wave(640, 2.2, "#cbd2d8", .4, .6) + [label(140, 560, "concert hall", .4, "#cbd2d8", 26, "start")] +
             wave(860, 6, "#c8743c", .9, 1.2) + [label(140, 780, "cathedral", .9, "#c8743c", 26, "start")] +
             wave(1080, 16, AU, 1.6, 3.2) + [label(140, 1000, "the Hypogeum", 1.6, AU, 26, "start"), glow(860, 1080, 90, 4.6, .5)]}
    # 4 · every room rings at its own size: small, middle, large, each with its standing wave and a person for scale
    rooms = []
    for k, (x, w, n) in enumerate(((120, 200, 1), (360, 250, 1), (650, 290, 1))):
        at = .4 + .8 * k
        rooms += [bx(x, 1180 - w * 1.1, w, w * 1.1, "#2a221b", "#c9ad85", 3, 10, at), person(x + w * .3, 1180, 120, at + .2)] + \
                 [line([[x + w * j / 40, round(1180 - w * .55 + w * .35 * math.sin(math.pi * n * j / 40), 1)] for j in range(41)], at + .4, AU, 3, dur=.6)]
    rooms += [bx(390, 560, 220, 160, "none", LILAC, 3, 6, 5.6, style="claimed")] + question(500, 680, 6.2, 70)
    # 5 · the viral claims: a phone, a ringing hall, and no published measurement
    viral = {"base": "dark", "cam": [1, 500, 900], "els": [bx(170, 620, 280, 520, "#15100c", "#cbd2d8", 4, 30, .2)] +
             [bx(200 + 45 * k, 780, 22, 220, "#c9a86a", r=3, at=.5 + .05 * k) for k in range(5)] + [bx(195, 760, 230, 24, "#c9a86a", r=3, at=.5)] +
             [ring(310, 890, 60 + 40 * k, 1.2 + .3 * k, AMB, 2, dur=.5) for k in range(3)] + [label(310, 1100, "20 s?", 2.4, AMB, 30),
              bx(570, 700, 250, 330, "none", LILAC, 3, 6, 4.0, style="claimed")] + [line([[600, 760 + 40 * j], [790, 760 + 40 * j]], 4.3 + .1 * j, LILAC, 2, "claimed", .4) for j in range(6)] +
             question(695, 900, 6.4, 90)}
    ep["beats"][5]["visual"]["from"] = 6
    sites = [bx(120, 1230, 760, 150, "rgba(18,13,10,.8)", "#c9ad85", 2, 14, .2)] + \
            [label(x, 1300, t, .5 + .5 * k, c, 30) for k, (x, t, c) in enumerate(((240, "Chavín", GREEN), (500, "Malta", AMB), (760, "Giza", "#9a938a")))] + \
            [dot(x, 1345, 10, c, 1.0 + .5 * k) for k, (x, c) in enumerate(((240, GREEN), (500, AMB), (760, "#9a938a")))]
    return remix(ep, scenes={1: ring_, 4: {"base": "dark", "cam": [1, 500, 900], "els": rooms}, 5: viral}, alias={6: 0}, keep=short,
                 drop=("para", "num", "title", "q", "cap", "label"), beat_adds={5: (sites, [1.02, 500, 930])}, cams={2: [1.35, 500, 930], 3: [1.15, 500, 880]})


def cymatic_m():
    """Cymatic temples as one continuous take (see mural.py): Chladni's plates, the plan, the missing workshop and the weight of a stone are drawn."""
    import random as _r
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN, GREEN, AU
    ep = cymatic()
    SAND = "#e8dcc2"
    def plate(cx, cy, pattern, at):
        out = [bx(cx - 170, cy - 170, 340, 340, "#3a3f45", "#8a939c", 2, 6, at)]
        r = _r.Random(int(cx))
        pts = []
        for k in range(90):
            t = k / 89
            if pattern == "cross":
                pts += [(cx - 160 + 320 * t, cy + r.uniform(-5, 5)), (cx + r.uniform(-5, 5), cy - 160 + 320 * t)]
            else:
                a = 2 * math.pi * t
                pts += [(cx + 110 * math.cos(a) + r.uniform(-4, 4), cy + 110 * math.sin(a) + r.uniform(-4, 4)), (cx - 160 + 320 * t + r.uniform(-4, 4), cy - 160 + 320 * t)]
        out += [dot(round(x, 1), round(y, 1), 3, SAND, round(at + .6 + .006 * k, 3), None) for k, (x, y) in enumerate(pts)]
        return out
    physics = {"base": "dark", "cam": [1, 500, 880], "els": [label(500, 520, "1787", .2, AU, 44, st="serif"),
               line([[150, 820], [420, 560]], .6, "#c9a86a", 5), line([[150, 820], [420, 560], [440, 580]], .6, "#c9a86a", 2, draw=False)] +
               plate(330, 820, "cross", 1.2) + [label(330, 620, "♪", 1.2, BN, 44)] + plate(670, 1180, "ring", 8.0) + [label(670, 980, "♫", 8.0, BN, 44)]}
    # 2 · Borobudur as it was laid out: terraces and circles set out with cords and pegs
    plan = {"base": "plan", "bg": "#2b2219", "north": False, "cam": [1, 500, 880], "els":
            [bx(500 - 330 + 30 * k, 880 - 330 + 30 * k, 660 - 60 * k, 660 - 60 * k, "none", "#c9ad85", 3, 2, .4 + .3 * k) for k in range(6)] +
            [ring(500, 880, 150 - 35 * k, 2.4 + .3 * k, "#c9ad85", 3) for k in range(3)] + [dot(500, 880, 16, "#c9ad85", 3.4)] +
            [dot(x, y, 7, AU, .2) for x, y in ((170, 550), (830, 550), (830, 1210), (170, 1210))] +
            [line([[170, 550], [830, 1210]], .3, AU, 1.5, "inferred", 1.2), line([[830, 550], [170, 1210]], .3, AU, 1.5, "inferred", 1.2)]}
    missing = [bx(120 + 270 * k, 1250, 210, 160, "rgba(18,13,10,.85)", LILAC, 2.5, 8, .3 + .4 * k, style="claimed") for k in range(3)] + \
              [line([[160, 1300], [290, 1300]], .5, LILAC, 3, "claimed", .4), line([[160, 1330], [290, 1330]], .55, LILAC, 3, "claimed", .4), line([[160, 1360], [260, 1360]], .6, LILAC, 3, "claimed", .4),
               bx(440, 1290, 110, 80, "none", LILAC, 3, 4, .9, style="claimed"),
               {"k": "poly", "p": [[700, 1380], [700, 1310], [765, 1270], [830, 1310], [830, 1380]], "fill": "none", "c": LILAC, "w": 3, "style": "claimed", "in": 1.3}] + \
              [label(225 + 270 * k, 1240, "?", 1.8 + .2 * k, LILAC, 44, st="big") for k in range(3)]
    # 4 · the heaviest thing sound has held up, and a 25-tonne stone
    lift = {"base": "dark", "floor": 1250, "cam": [1, 500, 900], "els": [
                bx(150, 1150, 160, 60, "#3a3f45", "#8a939c", 2, 6, .3), bx(150, 760, 160, 40, "#3a3f45", "#8a939c", 2, 6, .3)] +
            [line([[160, 1130 - 40 * k], [300, 1130 - 40 * k]], .5 + .08 * k, BLUE, 2, "inferred", .3) for k in range(8)] +
            [dot(230, 950, 7, BN, 1.0), glow(230, 950, 40, 1.0, .8), label(230, 1300, "½ g", 1.4, BN, 34),
             bx(460, 700, 400, 550, "#8a7a66", "#cbbca8", 2, 6, 4.4, fx="rise"), label(660, 1300, "25 t", 4.8, BN, 34),
             label(500, 620, "× 40,000,000", 6.0, AU, 40)]}
    verdicts = {"base": "dark", "cam": [1, 500, 880], "els": [bx(110, 700, 360, 360, "none", BLUE, 4, 12, .3, style="inferred")] +
                [bx(170 + 25 * k, 760 + 25 * k, 240 - 50 * k, 240 - 50 * k, "none", "#c9ad85", 2, 2, .5 + .15 * k) for k in range(4)] + question(290, 900, 1.6, 80, BLUE) +
                [bx(530, 700, 360, 360, "none", RD, 4, 12, 3.6), bx(600, 820, 220, 180, "#8a7a66", "#cbbca8", 2, 4, 3.8)] +
                [line([[610, 1030], [810, 1030]], 3.9, BLUE, 2, "inferred", .3)] + [strike(560, 1040, 860, 720, 5.0)]}
    return remix(ep, scenes={2: plan, 3: physics, 4: lift, 5: verdicts}, alias={6: 0}, cams={6: [1.1, 500, 860], 1: [1.2, 500, 960]},
                 drop=("para", "num", "title", "q", "cap"), line_adds={(3, 1): (missing, [1, 500, 960])},
                 adds={1: [ring(500, 900, 260 + 40 * k, 2.0 + .3 * k, LILAC, 2, "claimed", 1.0) for k in range(3)]})


def longyou_m():
    """Longyou as one continuous take (see mural.py): the thin walls, the pot that dates nothing, the seven guesses are drawn."""
    from mural import remix
    from illus import person, arrow, line, glow, label, dot, box as bx, oval, question, ring, strike, ellipse, AMBER as AMB, BLUE, LILAC, RED as RD, BONE as BN, GREEN, AU
    ep = longyou()
    ROCK = "#6f5a44"
    cav = lambda pts, at: {"k": "poly", "p": pts, "fill": "#1a120c", "c": "#c9ad85", "w": 3, "in": at, "curve": True}
    walls = {"base": "plan", "bg": ROCK, "north": False, "cam": [1, 500, 880], "els": [
                cav([[160, 620], [470, 600], [485, 900], [470, 1150], [180, 1180], [140, 900]], .3), cav([[510, 610], [840, 640], [860, 900], [830, 1170], [525, 1150], [512, 900]], .6),
                bx(482, 860, 34, 80, "none", AU, 3, 2, 1.4), label(500, 830, "0.5 m", 1.6, AU, 32), glow(498, 900, 60, 1.8, .7),
                bx(330, 1260, 340, 120, "rgba(18,13,10,.8)", LILAC, 3, 8, 5.2, style="claimed")] + question(500, 1350, 5.8, 70)}
    pot = {"base": "dark", "floor": 1180, "cam": [1, 500, 900], "els": [
                {"k": "poly", "p": [[120, 1180], [120, 760], [300, 560], [700, 560], [880, 760], [880, 1180]], "fill": "#2a221b", "c": "#c9ad85", "w": 3, "curve": True, "in": .1},
                {"k": "vase", "x": 500, "y": 1180, "h": 150, "in": .8, "fx": "rise"}, glow(500, 1110, 120, 1.0, .6),
                label(500, 960, "c. 2,000 years", 2.4, AU, 38, st="serif"),
                arrow([[500, 985], [500, 1020]], 4.2, AU, 3, dur=.4, curve=False),
                arrow([[560, 950], [760, 800], [840, 760]], 5.4, LILAC, 3, "claimed", .8)] + question(760, 720, 6.0, 70)}
    th = ["quarry", "tomb", "store", "retreat", "camp", "altar", "palace"]
    guesses = {"base": "dark", "cam": [1, 500, 880], "els": [label(500 + 300 * math.cos(-math.pi / 2 + 2 * math.pi * k / 7), 880 + 300 * math.sin(-math.pi / 2 + 2 * math.pi * k / 7), t, .5 + .35 * k,
                                                                   BN if k else AU, 34) for k, t in enumerate(th)] +
               [ring(500, 580 - 12, 90, 5.4, AU, 4), line([[140, 1320], [300, 1300], [500, 1330], [700, 1300], [880, 1320]], 6.2, BLUE, 6, curve=True)] +
               [bx(520 + 40 * k, 1190 - 10 * k, 36, 30, "#b9ab94", r=3, at=6.8 + .15 * k, fx="pop") for k in range(3)] +
               [arrow([[660, 1180], [760, 1150], [800, 1110]], 8.4, LILAC, 3, "claimed", .8), bx(780, 1010, 110, 95, "none", LILAC, 3, 4, 8.8, style="claimed")] + question(835, 990, 9.3, 60)}
    return remix(ep, scenes={3: pot, 4: guesses, 5: walls}, alias={6: 0}, cams={0: [1.2, 500, 960], 6: [1.15, 500, 1000]},
                 drop=("para", "num", "title", "q", "cap"), beat_adds={1: ([], [1.45, 500, 1000])})


def ledger_recap():
    """The ledger as a science-show recap: every case gets its moment in the cabinet (see recap.py; narration in rewrite/ledgers/underworlds-ledger.json)."""
    import recap
    return recap.recap(ledger, "underworlds-ledger", None)


def EPISODES():
    return [derinkuyu_m(), longyou_m(), malta_m(), acoustics_m(), cymatic_m(), delphi_m(), ledger_recap()]
