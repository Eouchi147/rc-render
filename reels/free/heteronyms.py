"""Heteronyms: words spelled alike but said differently by meaning ('live TV' /laɪv/, 'I live' /lɪv/).
Every heteronym in a script must carry its sense, written word@sense (for example live@adj). The sense decides
what the phone audit expects to hear; word@sense! also forces a respelling on the narrator, for the cases the voice
gets wrong in context. The lint refuses any script with an unmarked heteronym, so none can slip through again.
IPA is General American/RP-neutral, stress marks omitted (the audit compares phones)."""
import re

# word -> {sense: (ipa, respelling for the narrator)}
SENSES = {
    "live": {"verb": ("lɪv", "liv"), "adj": ("laɪv", "lyve")},
    "lives": {"verb": ("lɪvz", "livz"), "noun": ("laɪvz", "lyves")},
    "read": {"present": ("rid", "reed"), "past": ("rɛd", "red")},
    "lead": {"verb": ("lid", "leed"), "metal": ("lɛd", "led")},
    "leads": {"verb": ("lidz", "leeds"), "metal": ("lɛdz", "leds")},
    "wind": {"air": ("wɪnd", "winnd"), "coil": ("waɪnd", "wynd")},
    "winds": {"air": ("wɪndz", "winnds"), "coil": ("waɪndz", "wynds")},
    "wound": {"injury": ("wund", "woond"), "coiled": ("waʊnd", "wownd")},
    "tear": {"cry": ("tɪr", "teer"), "rip": ("tɛr", "tair")},
    "tears": {"cry": ("tɪrz", "teers"), "rip": ("tɛrz", "tairs")},
    "close": {"adj": ("kloʊs", "cloce"), "verb": ("kloʊz", "cloze")},
    "bow": {"archery": ("boʊ", "boh"), "bend": ("baʊ", "bau")},
    "bows": {"archery": ("boʊz", "bohs"), "bend": ("baʊz", "baus")},
    "row": {"line": ("roʊ", "roh"), "quarrel": ("raʊ", "rau")},
    "sow": {"plant": ("soʊ", "soh"), "pig": ("saʊ", "sau")},
    "does": {"verb": ("dʌz", "duz"), "deer": ("doʊz", "doze")},
    "dove": {"bird": ("dʌv", "duv"), "past": ("doʊv", "dohv")},
    "bass": {"fish": ("bæs", "bass"), "music": ("beɪs", "base")},
    "minute": {"time": ("mɪnɪt", "minnit"), "tiny": ("maɪnut", "my-noot")},
    "minutes": {"time": ("mɪnɪts", "minnits")},
    "desert": {"noun": ("dɛzərt", "dezzert"), "verb": ("dɪzɜrt", "dizzert")},
    "deserts": {"noun": ("dɛzərts", "dezzerts"), "verb": ("dɪzɜrts", "dizzerts")},
    "record": {"noun": ("rɛkərd", "reckerd"), "verb": ("rɪkɔrd", "rikord")},
    "records": {"noun": ("rɛkərdz", "reckerds"), "verb": ("rɪkɔrdz", "rikords")},
    "present": {"noun": ("prɛzənt", "prezzent"), "verb": ("prɪzɛnt", "prizzent")},
    "object": {"noun": ("ɑbdʒɛkt", "obbject"), "verb": ("əbdʒɛkt", "ubject")},
    "objects": {"noun": ("ɑbdʒɛkts", "obbjects"), "verb": ("əbdʒɛkts", "ubjects")},
    "project": {"noun": ("prɑdʒɛkt", "proj-ect"), "verb": ("prədʒɛkt", "pruh-ject")},
    "produce": {"noun": ("proʊdus", "proh-dooce"), "verb": ("prədus", "pruh-dooce")},
    "content": {"noun": ("kɑntɛnt", "kon-tent"), "adj": ("kəntɛnt", "kun-tent")},
    "contract": {"noun": ("kɑntrækt", "kon-tract"), "verb": ("kəntrækt", "kun-tract")},
    "conduct": {"noun": ("kɑndʌkt", "kon-duct"), "verb": ("kəndʌkt", "kun-duct")},
    "conflict": {"noun": ("kɑnflɪkt", "kon-flict"), "verb": ("kənflɪkt", "kun-flict")},
    "contest": {"noun": ("kɑntɛst", "kon-test"), "verb": ("kəntɛst", "kun-test")},
    "subject": {"noun": ("sʌbdʒɛkt", "sub-ject"), "verb": ("səbdʒɛkt", "sub-JECT")},
    "suspect": {"noun": ("sʌspɛkt", "sus-pect"), "verb": ("səspɛkt", "suh-spect")},
    "survey": {"noun": ("sɜrveɪ", "sur-vay"), "verb": ("sərveɪ", "ser-VAY")},
    "surveys": {"noun": ("sɜrveɪz", "sur-vays"), "verb": ("sərveɪz", "ser-VAYS")},
    "increase": {"noun": ("ɪnkris", "in-crease"), "verb": ("ɪnkris", "in-CREASE")},
    "decrease": {"noun": ("dikris", "dee-crease"), "verb": ("dɪkris", "de-CREASE")},
    "permit": {"noun": ("pɜrmɪt", "per-mit"), "verb": ("pərmɪt", "pur-MIT")},
    "permits": {"noun": ("pɜrmɪts", "per-mits"), "verb": ("pərmɪts", "pur-MITS")},
    "progress": {"noun": ("prɑgrɛs", "prog-ress"), "verb": ("prəgrɛs", "pruh-gress")},
    "rebel": {"noun": ("rɛbəl", "reb-ul"), "verb": ("rɪbɛl", "ri-bell")},
    "refuse": {"noun": ("rɛfjus", "ref-yoose"), "verb": ("rɪfjuz", "ri-fyooz")},
    "excuse": {"noun": ("ɪkskjus", "ex-kyoose"), "verb": ("ɪkskjuz", "ex-kyooz")},
    "abuse": {"noun": ("əbjus", "a-byoose"), "verb": ("əbjuz", "a-byooz")},
    "use": {"noun": ("jus", "yoose"), "verb": ("juz", "yooz")},
    "used": {"verb": ("juzd", "yoozd"), "to": ("just", "yoost")},
    "house": {"noun": ("haʊs", "hauss"), "verb": ("haʊz", "hauz")},
    "houses": {"noun": ("haʊzɪz", "how-zez"), "verb": ("haʊzɪz", "how-zez")},
    "close": {"adj": ("kloʊs", "cloce"), "verb": ("kloʊz", "cloze")},
    "separate": {"adj": ("sɛpərɪt", "sep-rut"), "verb": ("sɛpəreɪt", "sep-uh-rayt")},
    "estimate": {"noun": ("ɛstɪmɪt", "est-i-mut"), "verb": ("ɛstɪmeɪt", "est-i-mayt")},
    "estimates": {"noun": ("ɛstɪmɪts", "est-i-muts"), "verb": ("ɛstɪmeɪts", "est-i-mayts")},
    "approximate": {"adj": ("əprɑksɪmɪt", "a-prox-i-mut"), "verb": ("əprɑksɪmeɪt", "a-prox-i-mayt")},
    "moderate": {"adj": ("mɑdərɪt", "mod-er-ut"), "verb": ("mɑdəreɪt", "mod-er-ayt")},
    "graduate": {"noun": ("grædʒuɪt", "grad-yoo-ut"), "verb": ("grædʒueɪt", "grad-yoo-ayt")},
    "associate": {"noun": ("əsoʊsiɪt", "a-so-see-ut"), "verb": ("əsoʊsieɪt", "a-so-see-ayt")},
    "alternate": {"adj": ("ɔltərnɪt", "ol-ter-nut"), "verb": ("ɔltərneɪt", "ol-ter-nayt")},
    "deliberate": {"adj": ("dɪlɪbərɪt", "di-lib-er-ut"), "verb": ("dɪlɪbəreɪt", "di-lib-er-ayt")},
    "duplicate": {"noun": ("duplɪkɪt", "doo-pli-kut"), "verb": ("duplɪkeɪt", "doo-pli-kayt")},
    "elaborate": {"adj": ("ɪlæbərɪt", "i-lab-er-ut"), "verb": ("ɪlæbəreɪt", "i-lab-er-ayt")},
    "perfect": {"adj": ("pɜrfɪkt", "per-fect"), "verb": ("pərfɛkt", "pur-FECT")},
    "entrance": {"noun": ("ɛntrəns", "en-truns"), "verb": ("ɪntræns", "in-trance")},
    "invalid": {"adj": ("ɪnvælɪd", "in-val-id"), "noun": ("ɪnvəlɪd", "in-vuh-lid")},
    "compact": {"adj": ("kəmpækt", "kum-pact"), "noun": ("kɑmpækt", "kom-pact")},
    "console": {"noun": ("kɑnsoʊl", "kon-sole"), "verb": ("kənsoʊl", "kun-sole")},
    "digest": {"noun": ("daɪdʒɛst", "dye-jest"), "verb": ("daɪdʒɛst", "di-JEST")},
    "address": {"noun": ("ædrɛs", "ad-ress"), "verb": ("ədrɛs", "uh-dress")},
    "combat": {"noun": ("kɑmbæt", "kom-bat"), "verb": ("kəmbæt", "kum-bat")},
    "export": {"noun": ("ɛkspɔrt", "ex-port"), "verb": ("ɪkspɔrt", "ix-PORT")},
    "import": {"noun": ("ɪmpɔrt", "im-port"), "verb": ("ɪmpɔrt", "im-PORT")},
    "insult": {"noun": ("ɪnsʌlt", "in-sult"), "verb": ("ɪnsʌlt", "in-SULT")},
    "extract": {"noun": ("ɛkstrækt", "ex-tract"), "verb": ("ɪkstrækt", "ix-TRACT")},
    "transfer": {"noun": ("trænsfər", "trans-fer"), "verb": ("trænsfɜr", "trans-FUR")},
    "upset": {"noun": ("ʌpsɛt", "up-set"), "adj": ("ʌpsɛt", "up-SET")},
    "reject": {"noun": ("ridʒɛkt", "ree-ject"), "verb": ("rɪdʒɛkt", "ri-JECT")},
    "recall": {"noun": ("rikɔl", "ree-call"), "verb": ("rɪkɔl", "ri-CALL")},
    "polish": {"verb": ("pɑlɪʃ", "pollish"), "nation": ("poʊlɪʃ", "pohlish")},
    "job": {"work": ("dʒɑb", "job"), "prophet": ("dʒoʊb", "Jobe")},
    "lot": {"amount": ("lɑt", "lot"), "prophet": ("lɑt", "Lot")},
    "number": {"count": ("nʌmbər", "number"), "numbness": ("nʌmər", "nummer")},
    "resume": {"verb": ("rɪzum", "ri-zoom"), "noun": ("rɛzəmeɪ", "rez-oo-may")},
    "axes": {"axe": ("æksɪz", "ak-siz"), "axis": ("æksiz", "ak-seez")},
    "putting": {"place": ("pʊtɪŋ", "putting"), "golf": ("pʌtɪŋ", "puhting")},
    "sewer": {"drain": ("suər", "soo-er"), "stitcher": ("soʊər", "soh-er")},
    "buffet": {"meal": ("bəfeɪ", "buh-fay"), "strike": ("bʌfɪt", "buff-it")},
    "moped": {"bike": ("moʊpɛd", "moh-ped"), "past": ("moʊpt", "mohpt")},
    "wound": {"injury": ("wund", "woond"), "coiled": ("waʊnd", "wownd")},
    "attribute": {"noun": ("ætrɪbjut", "at-tri-byoot"), "verb": ("ətrɪbjut", "a-TRIB-yoot")},
    "frequent": {"adj": ("frikwənt", "free-kwunt"), "verb": ("frikwɛnt", "free-KWENT")},
    "convert": {"noun": ("kɑnvɜrt", "kon-vert"), "verb": ("kənvɜrt", "kun-vert")},
    "convict": {"noun": ("kɑnvɪkt", "kon-vict"), "verb": ("kənvɪkt", "kun-vict")},
    "insert": {"noun": ("ɪnsɜrt", "in-sert"), "verb": ("ɪnsɜrt", "in-SERT")},
    "refund": {"noun": ("rifʌnd", "ree-fund"), "verb": ("rɪfʌnd", "ri-FUND")},
    "torment": {"noun": ("tɔrmɛnt", "tor-ment"), "verb": ("tɔrmɛnt", "tor-MENT")},
    "incline": {"noun": ("ɪnklaɪn", "in-cline"), "verb": ("ɪnklaɪn", "in-CLINE")},
}

MARK = re.compile(r"^(?P<pre>[^A-Za-z]*)(?P<word>[A-Za-z][A-Za-z'’\-]*)@(?P<sense>[a-z]+)(?P<force>!?)(?P<post>.*)$")


def split(token):
    """'live@adj!,' -> ('live', 'adj', True, '', ',') or None."""
    m = MARK.match(token)
    if not m:
        return None
    return m.group("word"), m.group("sense"), bool(m.group("force")), m.group("pre"), m.group("post")


def plain(token):
    """The token as displayed or spoken, marker removed (respelled if forced)."""
    s = split(token)
    if not s:
        return token
    word, sense, force, pre, post = s
    if force:
        resp = SENSES[word.lower()][sense][1]
        resp = resp[0].upper() + resp[1:] if word[0].isupper() else resp
        return pre + resp + post
    return pre + word + post


def display(token):
    s = split(token)
    return token if not s else s[3] + s[0] + s[4]


def ipa(token):
    s = split(token)
    if not s:
        return None
    return SENSES[s[0].lower()][s[1]][0]


def senses_ipa(token):
    s = split(token)
    return {k: v[0] for k, v in SENSES[s[0].lower()].items()} if s else {}


def lint(text):
    """Every heteronym must carry a known sense. Returns a list of problems."""
    bad = []
    clean = re.sub(r"\[[^\]]*\]", " ", text)
    clean = re.sub(r"\{([^|{}]*)\|([^{}]*)\}", r" \2 ", clean)
    for tok in clean.split():
        s = split(tok.replace("*", ""))
        if s:
            if s[0].lower() not in SENSES or s[1] not in SENSES[s[0].lower()]:
                bad.append(f"unknown sense: {tok}")
            continue
        w = re.sub(r"[^a-z'’\-]", "", tok.lower().replace("*", ""))
        if w in SENSES:
            bad.append(f"heteronym without a sense: '{tok}' in: {text[:90]}")
    return bad
