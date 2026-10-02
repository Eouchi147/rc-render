"""Narrator voices for the reels: engines, pronunciation, and each character's sound design.

Two engines, both open and usable commercially:
  * Kokoro (Apache-2.0), 82M. Phoneme timings come out of the model, and names can be spelled in IPA.
  * Supertonic 3 (MIT code, OpenRAIL-M weights), via sherpa-onnx. Smoother, more human prosody. It reads
    characters, not phonemes, so hard names are respelled; word timings come from a speech recogniser
    (Parakeet TDT 0.6B) run over each sentence.
Every voice returns 48 kHz mono audio plus word start/end times, so captions and effects stay on the syllable.

A character = an engine voice + pace + a sound-design chain (pitch, harmoniser, room, ring modulation, radio band...).
"""
import os, re, json, hashlib, subprocess, tempfile
import numpy as np

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))


def _first(*paths):
    for x in paths:
        if x and os.path.exists(x):
            return x
    return paths[-1]


KOKORO_DIR = os.environ.get("RC_TTS_DIR") or _first(os.path.join(HERE, "models"), "/home/claude/tts")
SUPERTONIC_DIR = os.environ.get("RC_SUPERTONIC") or _first(os.path.join(HERE, "models", "supertonic"),
                                                             "/home/claude/tts2/sherpa-onnx-supertonic-3-tts-int8-2026-05-11")
ASR_DIR = os.environ.get("RC_ASR") or _first(os.path.join(HERE, "models", "parakeet"),
                                              "/home/claude/tts2/sherpa-onnx-nemo-parakeet-tdt-0.6b-v2-int8")

# ------------------------------------------------------------------ pronunciation
# Checked by ear-proxy: each override was synthesised and transcribed by Parakeet until it came back right.
LEX = {  # word (no punctuation, case-insensitive) -> IPA for Kokoro
    "göbekli": "ɡøbɛklˈi", "gobekli": "ɡøbɛklˈi", "tepe": "tɛpˈɛ",
    "khafre": "kˈɑːfɹeɪ", "khafre's": "kˈɑːfɹeɪz",
    "upuaut": "ˌuːpuːwˈaʊt",
    "kalambo": "kəlˈɑːmboʊ",
    "dryas": "dɹˈaɪəs",
    "clovis": "klˈoʊvɪs",
    "gantenbrink": "ɡˈɑːntənbɹɪŋk",
    "djedi": "dʒˈɛdiː",
    "karahan": "kˌɑːɹəhˈɑːn",
    "şanlıurfa": "ʃˌɑːnlɯˈʊɹfɑː", "sanliurfa": "ʃˌɑːnlɯˈʊɹfɑː",
}

# Names and rare words for the IPA narrator (Kokoro): the pronunciation an educated English-speaking presenter uses.
# Reviewed entry by entry; espeak-ng's own guess is kept wherever it was already right.
LEX.update({ "quran": "kəɹˈɑːn", "ce": "sˌiːˈiː", "solomon": "sˈɑːləmən", "plato": "plˈeɪɾoʊ", "thamud": "θɑːmˈuːd", "denisovans": "dᵻnˈiːsəvənz", "tiwanaku": "tˌiːwɑːnˈɑːkuː", "iram": "ˈɪɹəm", "gibeon": "ɡˈɪbiən", "aksum": "ˈɑːksʊm", "dwarka": "dwˈɑːɹkə", "indus": "ˈɪndəs", "knossos": "nˈɒsəs", "flores": "flˈɔːɹɛs", "gilgamesh": "ɡˈɪlɡəmˌɛʃ", "uruk": "ˈuːɹʊk", "sodom": "sˈɑːdəm", "joshua": "dʒˈɑːʃuːə", "bimini": "bˈɪmɪni", "punku": "pˈuːŋkuː", "pentagon": "pˈɛntəɡˌɑːn", "badon": "bˈeɪdən", "chavín": "tʃɑːvˈiːn", "cayce": "kˈeɪsi", "merer": "mˈɛɹɚ", "schoch": "ʃˈɑːk", "siberia": "saɪbˈɪɹiə", "luzon": "luːzˈɑːn", "enmebaragesi": "ˌɛnməbˌɑːɹəɡˈɛsi", "ubar": "ˈuːbɑːɹ", "ramesses": "ɹˈæməsˌiːz", "canaan": "kˈeɪnən", "aijalon": "ˈeɪdʒəlˌɑːn", "solon": "sˈoʊlən", "yonaguni": "jˌoʊnəɡˈuːni", "gunung": "ɡˈuːnʊŋ", "padang": "pˈɑːdɑːŋ", "khambhat": "kˈʌmbɑːt", "posnansky": "pɑːznˈænski", "cusco": "kˈuːskoʊ", "laos": "lˈaʊs", "strabo": "stɹˈeɪboʊ", "ingstad": "ˈɪŋstɑːd", "newfoundland": "nˈuːfənlənd", "gildas": "ɡˈɪldəs", "nazca": "nˈɑːzkə", "engle": "ˈɛŋɡəl", "borobudur": "bˌɔːɹoʊbuːdˈʊɹ", "hipparchus": "hɪpˈɑːɹkəs", "adena": "ədˈiːnə", "stonehenge": "stˈoʊnhˌɛndʒ", "apophis": "ɐpˈɑːfɪs", "tallet": "tɑːlˈeɪ", "tura": "tˈuːɹə", "akhetkhufu": "ˌɑːkɛtkˈuːfuː", "ankhhaf": "ˈɑːŋkhɑːf", "zahi": "zˈɑːhi", "hawass": "hɐwˈɑːs", "abydos": "ɐbˈaɪdɑːs", "osireion": "ˌoʊsɪɹˈiːɑːn", "basalt": "bɐsˈɔlt", "diorite": "dˈaɪəɹˌaɪt", "saqqara": "səkˈɑːɹə", "apis": "ˈeɪpɪs", "amasis": "ɐmˈeɪsɪs", "cambyses": "kæmbˈaɪsiːz", "denisovan": "dᵻnˈiːsəvən", "encke": "ˈɛŋki", "nuh": "nˈuː", "xia": "ʃjˈɑː", "lajia": "lˈɑːdʒjɑː", "urartu": "ʊɹˈɑːɹtuː", "berossus": "bᵻɹˈɑːsəs", "targum": "tˈɑːɹɡʊm", "cudi": "dʒˈuːdi", "etemenanki": "ˌɛtɛmɛnˈɑːŋki", "marduk": "mˈɑːɹduːk", "nebuchadnezzar": "nˌɛbəkədnˈɛzɚ", "nabataean": "nˌæbətˈiːən", "nabataeans": "nˌæbətˈiːənz", "tunguska": "tʊŋɡˈuːskə", "bab": "bˈɑːb", "kenyon": "kˈɛnjən", "dom": "dˈoʊm", "sheba": "ʃˈiːbə", "marib": "mˈɑːɹɪb", "derbent": "dɛɹbˈɛnt", "darial": "dˌɑːɹiˈɑːl", "dhulqarnayn": "ðˌʊlkɑːɹnˈaɪn", "kathir": "kəθˈiːɹ", "ariadaeus": "ˌæɹiːədˈiːəs", "arabah": "ˈæɹəbə", "heracles": "hˈɛɹəkliːz", "swallowed": "swˈɑːloʊd", "gibraltar": "dʒɪbɹˈɔːltɚ", "helike": "hˈɛlɪki", "masaaki": "mˌɑːsɑːˈɑːki", "kimura": "kiːmˈʊɹə", "atlit": "ɑːtlˈiːt", "yam": "jˈɑːm", "ngurunderi": "ŋˈʊɹʊndəɹi", "mahabharata": "məhˌɑːbˈɑːɹətə", "gujarat": "ɡˌuːdʒəɹˈɑːt", "lanka": "lˈɑːŋkə", "ramayana": "ɹɑːmˈɑːjənə", "heliopolis": "hˌiːliˈɑːpəlɪs", "jeanpierre": "ʒˌɑːnpjˈɛɹ", "cieza": "siˈeɪsə", "león": "leɪˈoʊn", "natawidjaja": "nˌɑːtəwiːdʒˈɑːdʒə", "columnar": "kəlˈʌmnɚ", "churchward": "tʃˈɜːtʃwɚd", "saudeleur": "sˈaʊdəlɜː", "isokelekel": "ˌiːsoʊkˈɛləkɛl", "xieng": "siˈɛŋ", "diquís": "diːkˈiːs", "finca": "fˈiːŋkə", "nan": "nˈɑːn", "madol": "mədˈoʊl", "sacsayhuamán": "sˌæksiwˈɑːmɑːn", "macon": "mˈeɪkən", "gondola": "ɡˈɑːndələ", "uap": "jˌuːˌeɪpˈiː", "oxyrhynchus": "ˌɑːksɪɹˈɪŋkəs", "rongorongo": "ɹˌɑːŋɡoʊɹˈɑːŋɡoʊ", "phaistos": "fˈaɪstɑːs", "elamite": "ˈiːləmˌaɪt", "tamil": "tˈɑːmɪl", "voynichese": "vˌɔɪnɪtʃˈiːz", "herculaneum": "hˌɜːkjəlˈeɪniəm", "pompeii": "pɑːmpˈeɪ", "aurelian": "ɔːɹˈiːliən", "piri": "pˈiːɹi", "reis": "ɹˈaɪs", "voynich": "vˈɔɪnɪtʃ", "hisarlık": "hˌɪsɑːɹlˈɪk", "calvert": "kˈælvɚt", "heinrich": "hˈaɪnɹɪk", "hittite": "hˈɪtˌaɪt", "wilios": "wˈɪliɑːs", "ilion": "ˈɪliɑːn", "alaksandu": "ˌɑːlæksˈænduː", "alexandros": "ˌælɪɡzˈændɹoʊs", "leif": "lˈiːf", "helge": "hˈɛlɡə", "stine": "stˈiːnə", "santorini": "sˌæntəɹˈiːni", "hittites": "hˈɪtˌaɪts", "ugarit": "ˌuːɡəɹˈiːt", "ashkelon": "ˈæʃkəlˌɑːn", "upano": "uːpˈɑːnoʊ", "kuikuro": "kwiːkˈʊɹoʊ", "xingu": "ʃɪŋɡˈuː", "tintagel": "tɪntˈædʒəl", "monmouth": "mˈɑːnməθ", "riothamus": "ɹiːˈɑːθəməs", "zurich": "zˈʊɹɪk", "oklo": "ˈoʊkloʊ", "kuroda": "kuːɹˈoʊdə", "klerksdorp": "klˈɛɹksdɔːɹp", "ica": "ˈiːkə", "erich": "ˈɛɹɪk", "däniken": "dˈɛnɪkən", "pakal": "pɑːkˈɑːl", "han": "hˈɑːn", "ġgantija": "dʒəɡɑːntˈiːjə", "huántar": "wˈɑːntɑːɹ", "ellora": "ɛlˈɔːɹə", "ernst": "ˈɛɹnst", "chladni": "klˈɑːdni", "plutarch": "plˈuːtɑːɹk", "pythia": "pˈɪθiə", "longyou": "lˌɔːŋjˈoʊ", "alamos": "ˈæləmˌoʊs", "trinil": "tɹˈiːnɪl", "ishango": "ɪʃˈɑːŋɡoʊ", "patagonia": "pˌætəɡˈoʊniə", "monte": "mˈɑːnteɪ", "sierpe": "siˈɛɹpeɪ", "pisco": "pˈiːskoʊ" })

LEX.update({"dummies": "dˈʌmiz", "copies": "kˈɑːpiz"})   # espeak ends these in ɪz: she said "dumms"
# File 15 (Carthage and Before): names espeak gets wrong
LEX.update({"tunis": "tˈuːnɪs", "diodorus": "dˌaɪəˈdɔːɹəs", "djerid": "dʒəɹˈiːd", "chott": "ʃˈɑːt", "chotts": "ʃˈɑːts", "dougga": "dˈuːɡə",
            "gruet": "ɡɹuːˈeɪ", "guettar": "ɡɛtˈɑːɹ", "michel": "miːʃˈɛl", "irhoud": "ɪɹhˈuːd", "jeanjacques": "ʒˌɑːnʒˈɑːk", "hublin": "uːblˈæn",
            "kerkouane": "kˌɛɹkuˈɑːn", "libycoberber": "lˌɪbɪkoʊbˈɜːbɚ", "libycopunic": "lˌɪbɪkoʊpjˈuːnɪk", "maghreb": "mˈɑːɡɹəb",
            "melrhir": "mɛlɡˈiːɹ", "pantelleria": "pˌæntɛləɹˈiːə", "tanit": "tˈɑːnɪt", "tifinagh": "tˌɪfɪnˈɑːɡ", "tritonis": "tɹaɪtˈoʊnɪs",
            "tuareg": "twˈɑːɹɛɡ", "tophet": "tˈoʊfɛt", "hermaion": "hˈɜːmaɪɑːn", "marrakech": "mˌæɹəkˈɛʃ", "sapiens": "sˈeɪpiənz"})
# File 14 (Arabia Unearthed)
LEX.update({"a'ali": "ˈɑːli", "alula": "ælˈuːlə", "arabic": "ˈæɹəbɪk", "dilmun": "dˈɪlmʊn", "eanasir": "ˌeɪənˈɑːsɪɹ", "faya": "fˈaɪə",
            "inzak": "ˈɪnzæk", "magan": "mˈɑːɡən", "nabonidus": "nˌæbənˈaɪdəs", "nanni": "nˈɑːni", "nefud": "nɛfˈuːd", "ri'mum": "ɹˈiːmuːm",
            "sîn": "sˈiːn", "tayma": "tˈaɪmə", "tema": "tˈiːmə", "yagliel": "jˌæɡliˈɛl", "mustatil": "mʊstətˈiːl", "mustatils": "mʊstətˈiːlz",
            "oman": "oʊmˈɑːn", "alhait": "ælhˈaɪt"})
# File 16 (When the Sahara Was Green)
LEX.update({"almásy": "ˈɔːlmɑːʃi", "bodélé": "boʊdˈeɪleɪ", "fezzan": "fɛzˈæn", "garamantes": "ɡˌæɹəmˈæntiːz", "gobero": "ɡoʊbˈɛɹoʊ",
            "kebira": "kəbˈiːɹə", "megachad": "mˌɛɡətʃˈæd", "nabta": "nˈɑːbtə", "sereno": "səɹˈeɪnoʊ", "takarkori": "tˌɑːkɑːɹkˈɔːɹi",
            "tassili": "tæsˈiːli", "tutankhamun": "tˌuːtɑːŋkˈɑːmuːn", "chalcedony": "kælsˈɛdəni", "foggaras": "fˈɑːɡəɹəz", "abu": "ˈɑːbuː",
            "n'ajjer": "nˈædʒɚ"})

RESPELL = {  # for Supertonic, which reads letters
    "bce": "B.C.E", "apophis": "Apoffis", "archaic": "ar-kay-ick", "flores": "Flor-ess", "cubit": "kyoo-bit",   # read as three letters, all of them (checked phone by phone)
    "göbekli": "Göbekli", "tepe": "Tepeh", "khafre": "Kafray", "khafre's": "Kafray's", "upuaut": "Oopoo Out",
    "kalambo": "Kalahmbo", "dryas": "Dryus", "djedi": "Jeddy", "karahan": "Karahahn", "muons": "mew-ons", "airbursts": "air-bursts", "sulawesi": "Soolahwaysee", "sulawesi:": "Soolahwaysee:",
    "khufu": "Koofoo", "khufu's": "Koofoo's", "merer": "Mehrer", "merer's": "Mehrer's", "tallet": "Tahlay", "tallet's": "Tahlay's",
    "ankhhaf": "Ankh-haf", "tura": "Toora", "akhetkhufu": "Ahket-Koofoo", "lehner": "Layner", "cayce": "Kay-see", "wadi": "Wahdee",
    "verde": "Verdeh", "chile": "Chilly", "chile,": "Chilly,", "orion": "O-Ryan", "orion's": "O-Ryan's", "schoch": "Shock", "schoch's": "Shock's", "zahi": "Zahhee", "osireion": "Ossy-ree-on", "abydos": "Ah-bye-doss", "seked": "Seh-ked",
    "djoser's": "Joe-ser's", "djoser": "Joe-ser", "apis": "Ay-pis", "amasis": "Ah-may-sis", "cambyses": "Cam-bye-seez", "khababash": "Kha-ba-bash",
    # File 09
    "stele": "stee-lee", "lajia": "Lah-jyah", "lajia's": "Lah-jyah's", "enmebaragesi": "En-meh-bah-rah-ghess-ee", "cudi": "Joo-dee", "dağı": "Dah-uh", "etemenanki": "Eh-temen-ankee",
    "shisr": "Shisser", "ubar": "Oo-bar", "zarins": "Zarrins", "thamud": "Tha-mood", "hegra": "Hegg-ra", "hegra's": "Hegg-ra's", "ruwafa": "Roo-wah-fa", "al-hijr": "al-Hidger", "nabataean": "Nabba-tee-an",
    "tayma": "Tay-ma", "hammam": "Ham-mam", "numeira": "Noo-may-ra", "salih": "Saa-lih", "atrahasis": "Atra-hah-sis", "shuruppak": "Shoo-roop-pak", "nabopolassar": "Nabbo-po-lassar", "sennacherib": "Sen-nack-er-ib",
    "durupınar": "Doo-roo-pun-ar", "facades": "fuh-sahds", "facade": "fuh-sahd",
    # File 10
    "merneptah": "Mer-nep-tah", "qantir": "Kan-teer", "pi-ramesses": "Pee-Ram-eh-seez", "ramesses": "Ram-eh-seez", "hyksos": "Hik-soss", "gibeon": "Gib-ee-on", "aijalon": "Ay-ja-lon",
    "azekah": "Az-ee-ka", "jashar": "Jay-shar", "faynan": "Fay-nahn", "timna": "Tim-na", "khirbat": "Kheer-bat", "en-nahas": "en-Na-hass", "shishak": "Shy-shak", "shishak's": "Shy-shak's",
    "marib": "Mah-rib", "sirwah": "Seer-wah", "sabaean": "Sa-bee-an", "sabaic": "Sa-bay-ik", "sargon": "Sar-gon", "derbent": "Der-bent", "darial": "Dar-ee-ahl", "gorgan": "Gor-gahn",
    "sasanian": "Sa-say-nee-an", "josephus": "Jo-see-fuss", "kathir": "Ka-theer", "dhul-qarnayn": "Dhool-Car-nine", "dhul-qarnayn,": "Dhool-Car-nine,", "aksum": "Ak-soom", "elephantine": "El-eh-fan-tee-nee",
    "kebra": "Keb-ra", "nagast": "Na-gast", "tacitus": "Tass-it-us", "pompey": "Pom-pee", "magi": "May-jye", "pisces": "Pie-seez", "ariadaeus": "Ari-a-dee-us", "mina": "Mee-na",
    "rille": "rill", "graben": "grah-ben", "dom.": "dohm.", "dom": "dohm", "kenyon": "Ken-yon", "kenyon's": "Ken-yon's", "levites": "Lee-vites", "hancock": "Han-cock", "urartu": "Oo-rar-too", "jishi": "Jee-shr", "erlitou": "Er-lee-toe", "sodom": "Sod-um", "gomorrah": "Go-mor-ra",
}
RESPELL.update({  # File 06 Impossible Stones, File 13 The Files
    "baalbek": "Bahl-bek", "beqaa": "Beh-kah", "trilithon": "try-lith-on", "tiwanaku": "Tee-wah-nah-koo", "titicaca": "Tee-tee-kah-kah", "posnansky": "Poz-nan-skee",
    "andesite": "an-deh-zite", "sacsayhuamán": "Sak-sai-wah-mahn", "sacsayhuaman": "Sak-sai-wah-mahn", "cusco": "Koos-ko", "cieza": "See-eh-sah", "león": "Leh-own",
    "protzen": "Prot-sen", "gunung": "Goo-noong", "padang": "Pah-dahng", "natawidjaja": "Nah-tah-wee-jah-jah", "pohnpei": "Pohn-pay", "pohnpeians": "Pohn-pay-uns",
    "pohnpeian": "Pohn-pay-un", "madol": "Mah-dol", "saudeleur": "Sow-deh-lur", "isokelekel": "Ee-so-keh-leh-kel", "xieng": "Syeng", "khouang": "Kwahng",
    "colani": "Ko-lah-nee", "diquís": "Dee-kees", "diquis": "Dee-kees", "finca": "Feen-kah", "koltypin": "Kol-tee-pin", "grusch": "Grush", "tuskegee": "Tus-kee-ghee",
    "voynich": "Voy-nitch", "voynichese": "Voy-nitch-eez", "greshko": "Gresh-ko", "philodemus": "Fil-oh-dee-mus", "herculaneum": "Her-kyoo-lay-nee-um", "seales": "Seels",
    "qumran": "Koom-rahn", "piri": "Pee-ree", "reis": "Rice", "rongorongo": "Rong-oh-rong-oh", "phaistos": "Fy-stos", "elamite": "Ee-luh-mite", "tamil": "Tah-mil", "nadu": "Nah-doo",
    "hisarlık": "His-ar-luk", "hisarlik": "His-ar-luk", "wilusa": "Wee-loo-sah", "wilios": "Wee-lee-os", "ilion": "Ill-ee-on", "alaksandu": "Ah-lak-san-doo",
    "schliemann": "Shlee-mahn", "ingstad": "Ing-stahd", "knossos": "Knoss-os", "thera": "Theer-uh", "peleset": "Pel-eh-set", "ugarit": "Oo-gah-reet",
    "ashkelon": "Ash-keh-lon", "upano": "Oo-pah-no", "kuikuro": "Kwee-koo-ro", "xingu": "Shing-goo", "gildas": "Gil-das", "badon": "Bay-don",
    "tintagel": "Tin-tadge-ul", "riothamus": "Ree-oh-tham-us", "monmouth": "Mon-muth",
    "oklo": "Oh-klo", "gabon": "Gah-bon", "kuroda": "Koo-ro-dah", "klerksdorp": "Klerks-dorp", "coso": "Ko-so", "ica": "Ee-kah", "däniken": "Den-ee-ken", "daniken": "Den-ee-ken",
    "nazca": "Nahz-kah", "palenque": "Pah-len-kay", "pakal": "Pah-kahl", "derinkuyu": "Deh-rin-koo-yoo", "cappadocia": "Kap-pa-doe-sha", "longyou": "Long-yo",
    "hypogeum": "Hy-po-jee-um", "ġgantija": "Jgan-tee-ya", "ggantija": "Jgan-tee-ya", "mnajdra": "Im-nigh-dra", "saflieni": "Saf-lee-eh-nee", "pythia": "Pith-ee-uh",
    "chladni": "Klahd-nee", "borobudur": "Bo-ro-boo-door", "chavín": "Cha-veen", "chavin": "Cha-veen", "cymatics": "sy-mat-iks", "cymatic": "sy-mat-ik",
    "nebra": "Neb-rah", "mittelberg": "Mit-tel-berg", "mitterberg": "Mit-ter-berg", "basel": "Bah-zel", "hipparchus": "Hip-ar-kus", "berossus": "Beh-ross-us",
    "valhalla": "Val-hal-uh", "hesiod": "Hee-see-od", "adena": "Uh-dee-nuh", "edfu": "Ed-foo", "peratt": "Peh-rat", "pleiades": "Ply-uh-deez", "yuga": "Yoo-guh",
    "trinil": "Tree-nil", "blombos": "Blom-boss", "muna": "Moo-nah", "ishango": "Ee-shan-go", "swabian": "Sway-bee-an", "sierpe": "See-er-peh", "pisco": "Pee-sko",
    "khipu": "Kee-poo", "olmec": "Ol-mek",
    "luminescence": "loo-mi-ness-ence",
    "mandala": "mahn-dah-lah", "pythia's": "Pith-ee-uh's", "hypogeum's": "Hy-po-jee-um's",
    "hittite": "Hit-tight", "hittites": "Hit-tights", "leif": "Leef",
    "metre": "meeter", "trough": "troff", "troughs": "troffs", "buxtun": "Bux-tun", "macon": "May-kun", "oxyrhynchus": "Ox-ee-ring-kus", "uap": "U.A.P", "army": "armee", "heliopolis": "Hee-lee-op-oh-lis", "nandauwas": "Nahn-dow-wahs",
    "ʿād": "Aad", "ād": "Aad", "ténéré": "Ten-eh-ray",
})
# transliterated names with ʿ / macrons: espeak spells them out letter by letter ("letter 2bf, A macron, d")
LEX.update({"ʿād": "ˈɑːd", "ād": "ˈɑːd", "ténéré": "tˌɛnɛɹˈeɪ"})
# wave 2 names (1 Oct 2026): espeak said "dee-hull", "mew-sa", "lutt", "men-kaw-ra"...
LEX.update({"dhul": "ðˈʊl", "qarnayn": "kɑːɹnˈaɪn", "musa": "mˈuːsə", "sulayman": "sˌʊleɪmˈɑːn", "lut": "lˈuːt", "salih": "sˈɑːlɪ",
            "hud": "hˈuːd", "yajuj": "jɑːdʒˈuːdʒ", "majuj": "mɑːdʒˈuːdʒ", "menkaure": "mɛŋkˈaʊɹeɪ", "shuruppak": "ʃʊɹˈʊpæk",
            "erlitou": "ˈɜːliːtˌoʊ", "thera": "θˈɪɹə", "qumran": "kʊmɹˈɑːn", "kerna": "kˈɛɹnə", "faynan": "feɪnˈɑːn",
            "wilusa": "wiːlˈuːsə", "gorgan": "ɡɔːɹɡˈɑːn"})
# long-form names (2 Oct 2026): espeak said "tim-ee-us", "krish-uz", "sighs", "kon-eers", "gaw-ree", "hyoor-ir-a"...
LEX.update({"necmi": "nˈɛdʒmi", "karul": "kɑːɹˈuːl", "timaeus": "taɪmˈiːəs", "critias": "kɹˈɪtiəs", "sais": "sˈeɪɪs",
            "ignatius": "ɪɡnˈeɪʃəs", "azores": "əzˈɔːɹz", "spartel": "spɑːɹtˈɛl", "bahamas": "bəhˈɑːməz",
            "akrotiri": "ˌɑːkɹoʊtˈɪɹi", "minoans": "mɪnˈoʊənz", "heracleides": "hˌɛɹəklˈaɪdiːz", "biondi": "biˈɑːndi",
            "malanga": "məlˈɑːŋɡə", "conyers": "kˈɑːnjɚz", "luis": "luːˈiːs", "gauri": "ɡˈaʊɹi", "hureyra": "huːɹˈeɪɹə",
            "agassiz": "ˈæɡəsi", "microspherules": "mˌaɪkɹoʊsfˈɪɹuːlz"})
# long-form round 2 names (2 Oct 2026)
LEX.update({"fravor": "fɹˈeɪvɚ", "trilithon": "tɹaɪlˈɪθɑːn", "djehutihotep": "dʒɛhˌuːtihˈoʊtɛp", "ollantaytambo": "ˌoʊjɑːntaɪtˈɑːmboʊ",
            "lutfi": "lˈuːtfi", "kaymakli": "kaɪmˈɑːklə", "ozkonak": "ˈɜːzkoʊnˌɑːk", "nevsehir": "nˈɛvʃɛhˌɪɹ", "yima": "jˈiːmə",
            "malakopi": "məlˈɑːkoʊpi", "asikli": "ˌɑːʃʊklˈʌ", "hoyuk": "hˈɜːjʊk", "katafygia": "kˌɑːtɑːfˈiːjiə", "kayseri": "kˈaɪsɛɹi",
            "imam": "ɪmˈɑːm", "henri": "ɑːnɹˈiː", "hathor": "hˈæθɔːɹ", "harsomtus": "hɑːɹsˈɑːmtəs", "palenque": "pɑːlˈɛŋkeɪ",
            "ruz": "ɹˈuːs", "johannes": "joʊhˈɑːnɛs", "marci": "mˈɑːɹtsi", "kircher": "kˈɪɹkɚ", "beinecke": "bˈaɪnəki",
            "fagin": "fˈeɪɡɪn", "schinner": "ʃˈɪnɚ", "torsten": "tˈɔːɹstən", "ducats": "dˈʌkəts"})


def _key(w):
    return re.sub(r"[^\wöüışçğ'’]", "", w.lower()).replace("’", "'")


# ------------------------------------------------------------------ engines
def to_kokoro(ipa):
    """Our hand-written IPA in the exact symbols the IPA voice was trained on (espeak-ng's American style):
    ASCII g is not in its alphabet (it would be silently dropped), plain r is a trill, and its long vowels carry ː."""
    s = ipa.replace("g", "ɡ")
    s = s.replace("ər", "ɚ").replace("ɜr", "ɜː").replace("ɜːː", "ɜː")
    s = re.sub(r"r", "ɹ", s)
    s = re.sub(r"i(?!ː)(?![əɪ])", "iː", s)
    s = re.sub(r"u(?!ː)", "uː", s)
    s = re.sub(r"ɑ(?!ː)", "ɑː", s)
    s = re.sub(r"ɔ(?![ːɪ])", "ɔː", s)
    return s


_VN = re.compile(r"aɪ|eɪ|oʊ|aʊ|ɔɪ|ər|ɜr|[aeiouæɑɒɔəɛɜɪʊʌy]")


def hn_ipa(token, kv=None):
    """IPA for a heteronym in its marked sense, with a primary stress (Kokoro needs it): the respelling's capitals if it
    has them; else a reduced first vowel (against a full one in the other sense) puts the stress on the second syllable
    (reCORD, preSENT); else the dictionary's own stress for the word."""
    import heteronyms as HN
    w, sense = HN.split(token)[:2]
    ipa, resp = HN.SENSES[w.lower()][sense]
    nuc = [m.start() for m in _VN.finditer(ipa)]
    if len(nuc) <= 1:
        return ipa[:nuc[0]] + "ˈ" + ipa[nuc[0]:] if nuc else "ˈ" + ipa
    parts = [p for p in resp.split("-") if p]
    k = next((i for i, p in enumerate(parts) if p.isupper() and len(parts) == len(nuc)), None)
    if k is None:
        others = [v[0] for s2, v in HN.SENSES[w.lower()].items() if s2 != sense]
        red = ipa[nuc[0]] in "əɪ" and any((m := _VN.search(o)) and m.group(0)[0] not in "əɪ" for o in others)
        k = 1 if red else 0
        if not red and kv is not None:
            try:
                d = kv.k.tokenizer.phonemize(w, "en-us")
                i = d.find("ˈ")
                if i > 0:
                    k = min(len(nuc) - 1, len(_VN.findall(d[:i])))
            except Exception:
                pass
    k = HN_STRESS.get((w.lower(), sense), k)
    i = nuc[min(k, len(nuc) - 1)]                  # the mark sits right before the stressed vowel, as espeak writes it
    return ipa[:i] + "ˈ" + ipa[i:]


HN_STRESS = {("minute", "tiny"): 1, ("deliberate", "adj"): 1, ("deliberate", "verb"): 1, ("elaborate", "adj"): 1, ("elaborate", "verb"): 1,
             ("approximate", "adj"): 1, ("approximate", "verb"): 1, ("associate", "noun"): 1, ("associate", "verb"): 1, ("invalid", "adj"): 1,
             ("compact", "adj"): 1, ("entrance", "verb"): 1, ("digest", "verb"): 1, ("desert", "verb"): 1, ("deserts", "verb"): 1,
             ("rebel", "verb"): 1, ("refuse", "verb"): 1, ("excuse", "noun"): 1, ("excuse", "verb"): 1, ("abuse", "noun"): 1, ("abuse", "verb"): 1,
             ("address", "verb"): 1, ("combat", "verb"): 1, ("console", "verb"): 1, ("increase", "verb"): 1, ("decrease", "verb"): 1,
             ("permit", "verb"): 1, ("permits", "verb"): 1, ("perfect", "verb"): 1, ("export", "verb"): 1, ("import", "verb"): 1, ("insult", "verb"): 1,
             ("extract", "verb"): 1, ("transfer", "verb"): 1, ("upset", "adj"): 1, ("reject", "verb"): 1, ("recall", "verb"): 1,
             ("contract", "verb"): 1, ("conduct", "verb"): 1, ("conflict", "verb"): 1, ("contest", "verb"): 1, ("content", "adj"): 1,
             ("subject", "verb"): 1, ("suspect", "verb"): 1, ("survey", "verb"): 1, ("surveys", "verb"): 1, ("progress", "verb"): 1,
             ("object", "verb"): 1, ("objects", "verb"): 1, ("project", "verb"): 1, ("produce", "verb"): 1, ("record", "verb"): 1,
             ("records", "verb"): 1, ("present", "verb"): 1, ("torment", "verb"): 1, ("incline", "verb"): 1, ("refund", "verb"): 1,
             ("minute", "time"): 0, ("minutes", "time"): 0, ("upset", "noun"): 0, ("import", "noun"): 0, ("compact", "noun"): 0,
             ("convert", "noun"): 0, ("incline", "noun"): 0, ("digest", "noun"): 0, ("invalid", "noun"): 0, ("alternate", "adj"): 0,
             ("alternate", "verb"): 0, ("produce", "noun"): 0}


class Kokoro:
    sr = SR

    def __init__(self, spec, cache, intone=False):
        self.spec, self.cache, self._k, self._style, self.intone = spec, cache, None, None, intone
        self.lang = "en-gb" if spec.split(":")[0].lstrip("-").startswith("b") else "en-us"
        os.makedirs(cache, exist_ok=True)

    @property
    def k(self):                                    # loaded only when a sentence is not in the cache
        if self._k is None:
            from kokoro_onnx import Kokoro as K
            self._k = K(os.path.join(KOKORO_DIR, "kokoro-v1.0-r11.onnx"), os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
        return self._k

    @property
    def style(self):
        if self._style is None:
            parts = [p.split(":") for p in self.spec.split("+")]
            self._style = sum(self.k.get_voice_style(n) * float(w) for n, w in parts) if len(parts) > 1 or len(parts[0]) > 1 \
                else self.k.get_voice_style(self.spec)
        return self._style

    def phon_word(self, w):
        import heteronyms as HN
        if HN.split(w.replace("*", "")):                 # word@sense: the sense's own IPA, with its stress
            tail = re.sub(r"^.*?([,.;:?!…]*)$", r"\1", w)
            return to_kokoro(hn_ipa(w.replace("*", ""))) + tail
        k = _key(_plain(w))
        if k not in LEX and (k.endswith("'s") and k[:-2] in LEX):          # Khufu's: the name, then its 's'
            tail = re.sub(r"^.*?([,.;:?!…]*)$", r"\1", w)
            base = LEX[k[:-2]].replace("g", "ɡ")
            return base + ("ᵻz" if re.search(r"[szʃʒ]$|tʃ$|dʒ$", base) else "s" if re.search(r"[ptkfθ]$", base) else "z") + tail
        if k in LEX:
            tail = re.sub(r"^.*?([,.;:?!…]*)$", r"\1", w)
            return LEX[k].replace("g", "ɡ") + tail
        return None

    def phonemes(self, words):
        """Phonemise a sentence, swapping in the lexicon for hard names."""
        out, run = [], []
        for w in words:
            p = self.phon_word(w)
            if p is None:
                run.append(w)
            else:
                if run:
                    out.append(self._run_before(run)); run = []
                out.append(p)
        if run:
            out.append(self.k.tokenizer.phonemize(" ".join(run), self.lang))
        return " ".join(x.strip() for x in out if x.strip())

    def _run_before(self, run):
        """Phonemise words that run up to a lexicon word, with a stand-in noun after them so espeak keeps the weak
        forms it would use in the sentence ('a' as /ɐ/, not the letter name; 'to' as /tə/)."""
        txt = " ".join(run)
        if re.search(r"[,.;:?!…]$", txt):
            return self.k.tokenizer.phonemize(txt, self.lang)
        ph = self.k.tokenizer.phonemize(txt + " thing", self.lang).rstrip(" .")
        for tail in (" θˈɪŋ", "θˈɪŋ", " θɪŋ", "θɪŋ"):
            if ph.endswith(tail):
                return ph[: -len(tail)].rstrip()
        return self.k.tokenizer.phonemize(txt, self.lang)

    def nwords(self, w):
        if self.phon_word(w) is not None:
            return 1
        s = re.sub(r"[^\w'’\- ]", " ", w).strip()
        return len(self.k.tokenizer.phonemize(s, self.lang).split()) if s else 0

    directed = property(lambda self: self.intone == "directed")
    phrases = property(lambda self: self.intone == "directed")      # directed: voiced by breath group, like Supertonic

    def say(self, words, speed, direction="calm", act=None):
        """words: list of spoken strings. Returns (audio 48k, [(start, end)] per word)."""
        marked = list(words)
        raw = [w.replace("*", "").replace("^", "") for w in words]
        words = [_plain(w) for w in words]
        lex = json.dumps({k: v for k, v in LEX.items() if any(_key(w) == k for w in words)}, sort_keys=True)
        if self.intone == "directed":
            tag = f"|d2|{direction}|{json.dumps(DIRECTION.get(direction))}|{json.dumps(act or {}, sort_keys=True)}|{json.dumps(ACT)}|{PERFORM2_V}"
        else:
            tag = f"|i1|{direction}|{json.dumps(DIRECTION.get(direction))}|{json.dumps(INTONE)}" if self.intone else ""
        key = hashlib.sha1(f"k3|{self.spec}|{speed:.3f}|{' '.join(marked if self.intone else words)}|{lex}{tag}".encode()).hexdigest()[:16]
        p = os.path.join(self.cache, key + ".npz")
        self.used = getattr(self, "used", []); self.used.append(os.path.basename(p))
        if os.path.exists(p):
            z = np.load(p, allow_pickle=True)
            return z["a"], [tuple(x) for x in z["w"]]
        ph = self.phonemes(raw)
        a, sr, tm = self.k.create_timed(ph, voice=self.style, speed=speed, lang=self.lang, is_phonemes=True)
        a = np.asarray(a, np.float32)
        spans = self._align(raw, a, [(x.phoneme, float(x.start), float(x.end)) for x in tm], sr)
        from scipy.signal import resample_poly
        a = resample_poly(a, 2, 1).astype(np.float32)
        if self.intone == "directed":                 # the stage note for this sentence, played on her own voice
            try:
                a, spans = perform2(marked, a, spans, direction, act)
            except Exception as ex:
                self.log = getattr(self, "log", []); self.log.append(("direction skipped", str(ex)[:80]))
        elif self.intone:                             # the same performance layer as the spelling-reading voice: melody, timing
            try:
                a, spans = perform(words, a, spans, direction)
            except Exception as ex:
                self.log = getattr(self, "log", []); self.log.append(("performance skipped", str(ex)[:80]))
        np.savez(p, a=a, w=np.array(spans))
        return a, spans

    def say_line(self, sents):
        """A whole line (breath group) voiced in one go, so every sentence gets the intonation the voice gives it in
        context (her own melody: nothing is pitch-shifted, nothing is time-stretched). Pace is set per sentence the
        way an actor slows for a punchline: the whole line is voiced once per pace it needs, and each sentence is
        taken from the take at its own pace, cut in the silences between sentences. Pauses are her own, lengthened
        only where the script holds a beat ([gap:x], or the house rule for a question and its answer).
        sents: [(words, speed, direction, act)]. Returns [(audio, spans, extra_silence_after)] per sentence."""
        from scipy.signal import resample_poly
        allw = [w for s_ in sents for w in s_[0]]
        plain = [_plain(w) for w in allw]
        read = [w.replace("*", "").replace("^", "") for w in allw]
        speeds = [round(float(s_[1]), 3) for s_ in sents]
        lex = json.dumps({k: v for k, v in LEX.items() if any(_key(w) == k for w in plain)}, sort_keys=True)
        import heteronyms as HN
        hn = [to_kokoro(hn_ipa(w.replace("*", "").replace("^", ""))) for w in allw if HN.split(w.replace("*", "").replace("^", ""))]
        key = hashlib.sha1(f"kl5|{self.spec}|{json.dumps(speeds)}|{json.dumps([(s_[0], (s_[3] or {}).get('gap')) for s_ in sents], sort_keys=True)}|{lex}|{json.dumps(hn)}|"
                           f"{MOTHER}|dc1".encode()).hexdigest()[:14]
        paths = [os.path.join(self.cache, f"{key}{i:02d}.npz") for i in range(len(sents))]
        self.used = getattr(self, "used", [])
        self.used += [os.path.basename(p) for p in paths]
        if all(os.path.exists(p) for p in paths):
            out = []
            for p in paths:
                z = np.load(p, allow_pickle=True)
                out.append((z["a"], [tuple(x) for x in z["w"]], float(z["g"])))
            return out
        R = SR
        bounds, i0 = [], 0
        for s_ in sents:
            bounds.append((i0, i0 + len(s_[0]) - 1)); i0 += len(s_[0])
        ph = self.phonemes(read)
        takes = {}
        for sp in sorted(set(speeds)):                   # one take of the whole line per pace it needs
            a, sr, tm = self.k.create_timed(ph, voice=self.style, speed=sp, lang=self.lang, is_phonemes=True)
            a = np.asarray(a, np.float32)
            spans = self._align2(read, [(x.phoneme, float(x.start), float(x.end)) for x in tm]) or spread(read, 0.05, len(a) / sr - 0.05)
            a = resample_poly(a, 2, 1).astype(np.float32)                   # 24k -> 48k; times are unchanged
            cuts = [0]
            for (a0_, b0_), (a1_, b1_) in zip(bounds, bounds[1:]):
                te, tb = spans[b0_][1], spans[a1_][0]
                lo, hi = int(te * R), max(int(te * R) + 1, int(tb * R))
                e = np.convolve(a[lo:hi] ** 2, np.ones(480) / 480, mode="same") if hi - lo > 960 else None
                cuts.append(lo + int(np.argmin(e)) if e is not None else (lo + hi) // 2)
            cuts.append(len(a))
            takes[sp] = (a, spans, cuts)
        out = []
        for si, (s_, (w0, w1)) in enumerate(zip(sents, bounds)):
            a, spans, cuts = takes[speeds[si]]
            c0, c1 = cuts[si], cuts[si + 1]
            seg = a[c0:c1].copy()
            loc = [(round(x - c0 / R, 3), round(y - c0 / R, 3)) for x, y in spans[w0:w1 + 1]]
            seg = seg - np.float32(np.median(np.concatenate([seg[:480], seg[-480:]])))   # silence at true zero: no step, no click
            fz = min(len(seg) // 4, int(0.008 * R))
            if fz > 0:
                seg[:fz] *= np.linspace(0, 1, fz, dtype=np.float32); seg[-fz:] *= np.linspace(1, 0, fz, dtype=np.float32)
            extra = 0.0
            if si + 1 < len(sents):                        # a held beat before the next sentence
                g = (sents[si + 1][3] or {}).get("gap")
                if g:
                    a2, sp2, _ = takes[speeds[si + 1]]
                    nat = max(0.0, sp2[bounds[si + 1][0]][0] - spans[w1][1])
                    extra = max(0.0, float(g) - nat)
            np.savez(paths[si], a=seg, w=np.array(loc), g=np.array(extra))
            out.append((seg, loc, extra))
        return out

    def _align2(self, words, tm):
        """Word spans from the model's own phoneme clock, robust to espeak merging words in context ('for the' ->
        'fɚðə'): each word's own phonemes are lined up against the phonemes actually voiced (edit-distance alignment),
        and every voiced phoneme is credited to the word it belongs to."""
        skip = set(" ˈˌː.,;:?!…\"'()-—–")
        H = [(i, p) for i, (p, s_, e_) in enumerate(tm) if p and not all(ch in skip for ch in p)]
        E = []
        for wi, w in enumerate(words):
            p = self.phon_word(w)
            if p is None:
                q = re.sub(r"[^\w'’\- ]", " ", w).strip()
                p = self.k.tokenizer.phonemize(q, self.lang) if q else ""
            E += [(wi, ch) for ch in p if ch not in skip]
        n, m = len(E), len(H)
        if not n or not m:
            return None
        D = np.zeros((n + 1, m + 1)); B = np.zeros((n + 1, m + 1), np.int8)
        D[:, 0] = np.arange(n + 1); D[0, :] = np.arange(m + 1); B[1:, 0] = 1; B[0, 1:] = 2
        for i in range(1, n + 1):
            ei = E[i - 1][1]
            for j in range(1, m + 1):
                c0 = D[i - 1, j - 1] + (0 if ei == H[j - 1][1] else 1)
                c1 = D[i - 1, j] + 1; c2 = D[i, j - 1] + 1
                if c0 <= c1 and c0 <= c2: D[i, j], B[i, j] = c0, 0
                elif c1 <= c2: D[i, j], B[i, j] = c1, 1
                else: D[i, j], B[i, j] = c2, 2
        lab = [None] * m
        i, j = n, m
        while i > 0 or j > 0:
            k = B[i, j] if i > 0 and j > 0 else (1 if i > 0 else 2)
            if k == 0:
                lab[j - 1] = E[i - 1][0]; i -= 1; j -= 1
            elif k == 1:
                i -= 1
            else:
                lab[j - 1] = E[min(i, n) - 1][0] if i > 0 else E[0][0]; j -= 1
        spans = [[None, None] for _ in words]
        for (ti, _), wi in zip(H, lab):
            s_, e_ = float(tm[ti][1]), float(tm[ti][2])
            if spans[wi][0] is None or s_ < spans[wi][0]: spans[wi][0] = s_
            if spans[wi][1] is None or e_ > spans[wi][1]: spans[wi][1] = e_
        for wi in range(len(words)):                      # a word with nothing voiced of its own: a sliver between neighbours
            if spans[wi][0] is None:
                prev_e = next((spans[k][1] for k in range(wi - 1, -1, -1) if spans[k][1] is not None), 0.0)
                spans[wi] = [prev_e, prev_e + 0.05]
        for wi in range(1, len(words)):                   # keep them in order
            spans[wi][0] = max(spans[wi][0], spans[wi - 1][0] + 0.01)
            spans[wi][1] = max(spans[wi][1], spans[wi][0] + 0.03)
        return [(round(a_, 3), round(b_, 3)) for a_, b_ in spans]

    def _align(self, words, audio, tm, sr):
        sp2 = self._align2(words, tm) if self.intone == "directed" else None
        if sp2:
            return sp2
        pw, cur = [], []
        for ph, s, e in tm:
            if ph == " ":
                if cur:
                    pw.append((cur[0][1], cur[-1][2])); cur = []
            elif re.search(r"\w|[ˈˌəɪʊæɑɔɛʌθðŋʃʒɹɾʔːøɯ]", ph):
                cur.append((ph, s, e))
        if cur:
            pw.append((cur[0][1], cur[-1][2]))
        need = [max(1, self.nwords(w)) for w in words]
        if sum(need) == len(pw) and pw:
            out, i = [], 0
            for n in need:
                out.append((pw[i][0], pw[i + n - 1][1])); i += n
            return out
        return spread(words, pw[0][0] if pw else 0.05, pw[-1][1] if pw else len(audio) / sr - 0.05)


def spread(words, a0, a1):
    wts = [max(1, len(re.sub(r"\W", "", w))) for w in words]
    tot, acc, out = sum(wts), 0, []
    for x in wts:
        s = a0 + (a1 - a0) * acc / tot; acc += x
        out.append((s, a0 + (a1 - a0) * acc / tot))
    return out


_ST, _ASR = {}, [None]


def asr():
    if _ASR[0] is None:
        import sherpa_onnx as s
        D = ASR_DIR + "/"
        _ASR[0] = s.OfflineRecognizer.from_transducer(encoder=D + "encoder.int8.onnx", decoder=D + "decoder.int8.onnx",
                                                      joiner=D + "joiner.int8.onnx", tokens=D + "tokens.txt",
                                                      model_type="nemo_transducer", num_threads=max(1, (os.cpu_count() or 2)))
    return _ASR[0]


def transcribe(a, sr):
    """Text and per-word start times from Parakeet."""
    from scipy.signal import resample_poly
    from math import gcd
    a = np.asarray(a, np.float32)
    g = gcd(sr, 16000); x = resample_poly(a, 16000 // g, sr // g).astype(np.float32)
    st = asr().create_stream(); st.accept_waveform(16000, x); asr().decode_stream(st)
    r = st.result
    words = []
    for tok, t in zip(r.tokens, r.timestamps):
        if tok.startswith(" ") or not words:
            words.append([tok.strip(), float(t)])
        else:
            words[-1][0] += tok
    return r.text.strip(), [(w, t) for w, t in words if w]


NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}


def _norm(w):
    w = re.sub(r"@[a-z]+!?", "", w)   # heteronym sense markers are not spoken words
    return re.sub(r"[^a-z0-9]", "", w.lower().replace("ö", "o"))


def _close(a, b):
    from difflib import SequenceMatcher
    return SequenceMatcher(None, a, b).ratio() >= 0.8


NUMWORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen "
               "eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million billion and".split())


def _heard(words, a):
    """(ratio, problems): script words the recogniser could not find anything close to, and words it heard that
    are close to nothing in the script (a phantom syllable). Fuzzy, so a name spelled differently is not a problem."""
    from difflib import SequenceMatcher
    sw = [_norm(w) for w in words if re.search(r"[A-Za-zÀ-ÿ]", w) and not set(re.split(r"[-\s]", w.lower().strip(".,;:?!…"))) <= NUMWORDS]
    hw = [_norm(w) for w in transcribe(a, SR)[0].replace("-", " ").split() if not re.fullmatch(r"[\d,.%]+", w)]
    hw = [w for w in hw if w and w not in NUMWORDS]
    ratio = SequenceMatcher(None, sw, hw, autojunk=False).ratio()
    near = lambda x, pool: any(x == y or (len(x) > 2 and SequenceMatcher(None, x, y).ratio() >= 0.66) or (len(x) > 3 and (x in y or y in x)) for y in pool)
    joined = "".join(sw)
    names = {_norm(w) for w in words if _key(_plain(w)) in RESPELL or _key(_plain(w)) in LEX}
    nm = lambda y: any(SequenceMatcher(None, y, x).ratio() >= 0.5 for x in names)
    bad = {("miss", x) for x in sw if x not in names and not near(x, hw) and x not in "".join(hw)}
    bad |= {("extra", y) for y in hw if not near(y, sw) and y not in joined and not nm(y)}
    return ratio, bad


def _heard_ok(words, a):
    """How much of the script the recogniser hears in this audio (0..1, numbers ignored)."""
    return _heard(words, a)[0]


def _no_worse(words, before, after):
    """True when the edit made nothing harder to hear: no new missed word, no new phantom word."""
    r0, b0 = before; r1, b1 = _heard(words, after)
    return not (b1 - b0) and r1 >= r0 - 0.02


def voiced(a, sr, thr_db=-38):
    """First and last voiced instants (s)."""
    hop = int(sr * 0.01)
    e = np.array([np.sqrt(np.mean(a[i:i + hop] ** 2) + 1e-12) for i in range(0, max(1, len(a) - hop), hop)])
    on = np.where(20 * np.log10(e / (e.max() + 1e-9)) > thr_db)[0]
    if not len(on):
        return 0.0, len(a) / sr
    return on[0] * 0.01, (on[-1] + 1) * 0.01


def align_asr(words, a, sr):
    """Map script words onto the recogniser's word starts; interpolate what it spelled differently (numbers...)."""
    from difflib import SequenceMatcher
    _, hw = transcribe(a, sr)
    v0, v1 = voiced(a, sr)
    sw = [_norm(w) for w in words]
    hn = [_norm(w) for w, _ in hw]
    anchors = {}
    for blk in SequenceMatcher(None, sw, hn, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            anchors[blk.a + k] = hw[blk.b + k][1]
    starts = [None] * len(words)
    starts[0] = anchors.get(0, v0)
    for i in range(1, len(words)):
        starts[i] = anchors.get(i)
    # fill gaps by character weight between anchors
    known = [i for i, s in enumerate(starts) if s is not None] + [len(words)]
    ends_t = v1
    for a_i, b_i in zip(known, known[1:]):
        t0 = starts[a_i]; t1 = starts[b_i] if b_i < len(words) else ends_t
        seg = words[a_i:b_i]
        wts = [max(1, len(re.sub(r"\W", "", w))) for w in seg]; tot = sum(wts); acc = 0
        for j, w in enumerate(seg):
            starts[a_i + j] = t0 + (t1 - t0) * acc / tot; acc += wts[j]
    starts = [max(v0 - 0.02, s) for s in starts]
    out = []
    for i, s in enumerate(starts):
        e = starts[i + 1] - 0.03 if i + 1 < len(starts) else v1
        out.append((round(s, 3), round(max(s + 0.06, e), 3)))
    return out


def _phones(words, a):
    """Phone-level flags from the universal recogniser, when it is installed (the cloud build has it; the render machine
    only replays cached takes and never needs it)."""
    try:
        import phonecheck
    except Exception:
        return []
    try:
        return phonecheck.audit(words, a)
    except Exception:
        return []


_JK = [None]


def _ipa_starts_j(w):
    """Does the dictionary pronunciation of this word begin with the /j/ glide (university, Europe, usual)?"""
    try:
        if _JK[0] is None:
            _JK[0] = Kokoro("af_heart", "/tmp/_kc").k
        ph = _JK[0].tokenizer.phonemize(re.sub(r"[^\w'’\-]", "", w), "en-us").replace("ˈ", "").replace("ˌ", "")
        return ph.startswith("j")
    except Exception:
        return False


class Supertonic:
    sr = SR
    phrases = True                                  # voiced a whole line at a time; pauses and melody shaped after

    def __init__(self, sid, cache, steps=12, intone=True):
        self.sid, self.steps, self.cache, self.spec, self.intone = int(sid), steps, cache, f"supertonic:{sid}", intone
        os.makedirs(cache, exist_ok=True)

    @property
    def t(self):                                    # loaded only on a cache miss
        if "st" not in _ST:
            import sherpa_onnx as s
            D = SUPERTONIC_DIR + "/"
            c = s.OfflineTtsConfig(model=s.OfflineTtsModelConfig(supertonic=s.OfflineTtsSupertonicModelConfig(
                duration_predictor=D + "duration_predictor.int8.onnx", text_encoder=D + "text_encoder.int8.onnx",
                vector_estimator=D + "vector_estimator.int8.onnx", vocoder=D + "vocoder.int8.onnx", tts_json=D + "tts.json",
                unicode_indexer=D + "unicode_indexer.bin", voice_style=D + "voice.bin"), num_threads=max(1, os.cpu_count() or 2)))
            _ST["st"] = s.OfflineTts(c)
        return _ST["st"]

    def text(self, words):
        out = []
        ws = [_plain(x) for x in words]
        # a sentence that opens on a /juː/ word ('Universities.', 'Unique...') loses its /j/ in this model: spell the glide out
        if ws and re.match(r"^[Uu]n?i|^[Uu]s[eu]|^[Uu]t[io]", ws[0]) and _key(ws[0]) not in RESPELL:
            k0 = ws[0]
            if _ipa_starts_j(k0):
                ws[0] = ("Y" if k0[0].isupper() else "y") + ("ou" + k0[1:] if k0[0] in "Uu" else "ou" + k0[2:])
        for w in ws:
            k = _key(w)
            if k in RESPELL:
                tail = re.sub(r"^.*?([,.;:?!…]*)$", r"\1", w)
                out.append(RESPELL[k] + tail)
            else:
                out.append(w)
        return " ".join(out)

    def say(self, words, speed, direction="calm"):
        txt = self.text(words)
        self.used = getattr(self, "used", [])
        key = hashlib.sha1(f"st13|{MOTHER}|{direction}|{json.dumps(DIRECTION.get(direction))}|{self.intone}|{json.dumps(INTONE)}|{self.sid}|{self.steps}|{speed:.3f}|{txt}".encode()).hexdigest()[:16]
        p = os.path.join(self.cache, key + ".npz")
        self.used.append(os.path.basename(p))
        if os.path.exists(p):
            z = np.load(p, allow_pickle=True)
            return z["a"], [tuple(x) for x in z["w"]]
        import sherpa_onnx as s
        from scipy.signal import resample_poly
        hard = [_norm(w) for w in words if _key(_plain(w)) in RESPELL]
        pw = [_plain(w) for w in words]
        best = None
        for attempt in range(6):                     # take the cleanest of a few reads: every word heard, no phantom
            g = s.GenerationConfig(); g.sid = self.sid; g.speed = speed * (1 + 0.012 * attempt * (-1) ** attempt)
            g.num_steps = self.steps; g.extra = {"lang": "en"}
            r = self.t.generate(txt, g)
            a = np.asarray(r.samples, np.float32)
            a = resample_poly(a, 160, 147).astype(np.float32)            # 44.1k -> 48k
            a0, a1 = voiced(a, SR, -50)                                      # trim the model's lead-in and tail, never a soft onset
            a = a[max(0, int((a0 - 0.06) * SR)): int((a1 + 0.11) * SR)].copy()
            fi = int(0.008 * SR); a[:fi] *= np.linspace(0, 1, fi, dtype=np.float32)
            heard = [_norm(w) for w in transcribe(a, SR)[0].split()]
            names_ok = all(any(_close(h, x) for x in heard) for h in hard)
            ratio, bad = _heard(pw, a)
            pf = _phones(pw, a)                          # phone-level check: a dropped /j/ or /h/ counts against a take
            score = len(bad) + 2 * len(pf) + (0 if names_ok else 5) - ratio
            if best is None or score < best[0]:
                best = (score, a)
            if names_ok and not bad and not pf:
                break
        a = best[1]
        pw = [_plain(w) for w in words]
        spans = align_asr(pw, a, SR)
        base = _heard(pw, a)
        self.log = getattr(self, "log", [])
        p0 = len(_phones(pw, a))
        if self.intone:                              # the performance: melody and timing as directed; same safety net
            a3, sp3 = perform(words, a, spans, direction)
            if _no_worse(pw, base, a3) and len(_phones(pw, a3)) <= p0:
                a, spans = a3, sp3
            else:                                    # try the melody without the timing stretch before giving up
                a4, sp4 = perform(words, a, spans, direction, cfg={"len_final": 1.0, "len_comma": 1.0, "len_emph": 1.0})
                if _no_worse(pw, base, a4) and len(_phones(pw, a4)) <= p0:
                    a, spans = a4, sp4; self.log.append(("melody only", " ".join(pw)))
                else:
                    self.log.append(("performance skipped", " ".join(pw)))
        np.savez(p, a=a, w=np.array(spans))
        return a, spans


# ------------------------------------------------------------------ sound design
def detone(x, prom=14):
    """Notch out the thin whistles a quantised vocoder can leave (narrow, steady spectral peaks above 1.5 kHz)."""
    from scipy.signal import welch, find_peaks, iirnotch, filtfilt
    if len(x) < 8192:
        return x
    if len(x) < SR * 8:                               # tones only show up reliably in a long stretch of speech
        return x
    fr, p = welch(x, SR, nperseg=16384)
    db = 10 * np.log10(p + 1e-20)
    pk, pr = find_peaks(db, prominence=max(prom, 16), width=(None, 4))
    pk = [k for _, k in sorted(zip(-pr["prominences"], pk))][:6]   # at most a handful of the strongest whistles
    y = x.astype(np.float64)
    for k in pk:
        if 1500 < fr[k] < SR / 2 - 500:
            b, a = iirnotch(fr[k], 25, SR); y = filtfilt(b, a, y)
    return y.astype(np.float32)


def _ffmpeg(x, af):
    with tempfile.TemporaryDirectory() as d:
        a, b = os.path.join(d, "a.wav"), os.path.join(d, "b.wav")
        import soundfile as sf
        sf.write(a, x, SR, subtype="FLOAT")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a, "-af", af, "-ar", str(SR), "-ac", "1", "-c:a", "pcm_f32le", b], check=True)
        y, _ = sf.read(b, dtype="float32")
    n = len(x)
    return (np.pad(y, (0, max(0, n - len(y))))[:n]).astype(np.float32)


def pitch(x, semis, formant=True):
    if not semis:
        return x
    return _ffmpeg(x, f"rubberband=pitch={2 ** (semis / 12):.5f}" + (":formant=preserved" if formant else "") + ":transients=smooth")


def bq(x, kind, f, q=0.707, g=0.0):
    """RBJ biquad."""
    from scipy.signal import lfilter
    w = 2 * np.pi * f / SR; al = np.sin(w) / (2 * q); c = np.cos(w); A = 10 ** (g / 40)
    if kind == "hp":
        b = [(1 + c) / 2, -(1 + c), (1 + c) / 2]; a = [1 + al, -2 * c, 1 - al]
    elif kind == "lp":
        b = [(1 - c) / 2, 1 - c, (1 - c) / 2]; a = [1 + al, -2 * c, 1 - al]
    elif kind == "peak":
        b = [1 + al * A, -2 * c, 1 - al * A]; a = [1 + al / A, -2 * c, 1 - al / A]
    elif kind == "lowshelf":
        s = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) - (A - 1) * c + s), 2 * A * ((A - 1) - (A + 1) * c), A * ((A + 1) - (A - 1) * c - s)]
        a = [(A + 1) + (A - 1) * c + s, -2 * ((A - 1) + (A + 1) * c), (A + 1) + (A - 1) * c - s]
    elif kind == "highshelf":
        s = 2 * np.sqrt(A) * al
        b = [A * ((A + 1) + (A - 1) * c + s), -2 * A * ((A - 1) + (A + 1) * c), A * ((A + 1) + (A - 1) * c - s)]
        a = [(A + 1) - (A - 1) * c + s, 2 * ((A - 1) - (A + 1) * c), (A + 1) - (A - 1) * c - s]
    return lfilter(np.array(b) / a[0], np.array(a) / a[0], x).astype(np.float32)


def eq(x, *bands):
    for b in bands:
        x = bq(x, *b)
    return x


def _ir(secs, bright=5000, predelay=0.02, seed=3, early=True, metal=0.0):
    r = np.random.default_rng(seed)
    n = int(secs * SR); t = np.arange(n) / SR
    ir = r.standard_normal(n).astype(np.float32) * np.exp(-6.9 * t / secs)
    ir = bq(ir, "lp", bright); ir = bq(ir, "hp", 180)
    if early:                                   # a few early reflections so it reads as a space, not a smear
        for d, g in ((0.011, .5), (0.017, .38), (0.023, .3), (0.031, .22), (0.043, .16)):
            ir[int(d * SR)] += g * (1 if r.random() > .5 else -1)
    if metal:                                   # tuned resonances: a hull, a chamber of steel
        for f in (310, 470, 830, 1290):
            ir += metal * np.sin(2 * np.pi * f * t) * np.exp(-t / (secs * .35)) * .05
    ir = np.concatenate([np.zeros(int(predelay * SR), np.float32), ir])
    return ir / np.sqrt(np.sum(ir ** 2))


def room(x, secs, wet, bright=5000, predelay=0.02, metal=0.0, hp=260):
    from scipy.signal import fftconvolve
    y = fftconvolve(x, _ir(secs, bright, predelay, metal=metal))[: len(x)].astype(np.float32)
    y = bq(y, "hp", hp)
    y *= np.sqrt(np.mean(x ** 2) + 1e-12) / (np.sqrt(np.mean(y ** 2)) + 1e-12)
    return x + wet * y


def ringmod(x, f, depth):
    t = np.arange(len(x)) / SR
    return (x * (1 - depth + depth * np.sin(2 * np.pi * f * t))).astype(np.float32)


def sat(x, drive=1.5):
    return (np.tanh(x * drive) / np.tanh(drive)).astype(np.float32)


def comp(x, thr=-20, ratio=3, att=0.005, rel=0.12, makeup=True):
    """Feed-forward RMS compressor."""
    env = np.abs(x); a_ = np.exp(-1 / (att * SR)); r_ = np.exp(-1 / (rel * SR))
    from scipy.signal import lfilter
    e = lfilter([1 - r_], [1, -r_], env)          # simple smoothing (release-weighted)
    db = 20 * np.log10(e + 1e-6)
    over = np.maximum(0, db - thr); gain = -over * (1 - 1 / ratio)
    gain = lfilter([1 - a_], [1, -a_], gain)
    y = x * 10 ** (gain / 20)
    if makeup:
        y *= np.sqrt(np.mean(x ** 2)) / (np.sqrt(np.mean(y ** 2)) + 1e-9)
    return y.astype(np.float32)


def deess(x, f=6500, amt=0.5):
    hi = bq(x, "hp", f, 0.8)
    env = np.convolve(np.abs(hi), np.ones(240) / 240, mode="same")
    ref = np.convolve(np.abs(x), np.ones(240) / 240, mode="same") + 1e-6
    g = 1 - amt * np.clip((env / ref - 0.25) * 2, 0, 1)
    return (x - hi + hi * g).astype(np.float32)


def layer(x, semis, gain_db, lp=None, hp=None):
    y = pitch(x, semis, formant=False)
    if lp: y = bq(y, "lp", lp)
    if hp: y = bq(y, "hp", hp)
    return x + y * 10 ** (gain_db / 20)


def chorus(x, depth_ms=3.5, rate=0.35, mix=0.35, base_ms=14):
    n = len(x); t = np.arange(n) / SR
    out = x.copy()
    for ph in (0, 2.1):
        d = (base_ms + depth_ms * np.sin(2 * np.pi * rate * t + ph)) * SR / 1000
        idx = np.clip(np.arange(n) - d, 0, n - 1)
        out += mix * np.interp(idx, np.arange(n), x).astype(np.float32) / 2
    return out


def clean(x):
    """The base every character shares: rumble out, mud down, presence up, gentle glue."""
    x = eq(x, ("hp", 75), ("peak", 280, 1.0, -2.0), ("peak", 3200, 1.1, 1.5), ("highshelf", 9000, .7, 1.0))
    x = deess(x, 5200, 0.7)
    return comp(x, -22, 2.4)


# Each chain takes the dry narration (48k mono) and returns the designed voice.
def fx_narrator(x):       # a person in the room with you: no echo trail, no grit; warmth, evenness, a hint of space
    x = clean(x)
    x = eq(x, ("hp", 80), ("lowshelf", 180, .7, 1.5), ("peak", 3000, 1.0, 0.8), ("lp", 15000))
    x = comp(x, -24, 1.8, att=0.015, rel=0.25)
    return room(x, 0.35, 0.05, 6000, 0.006)


def fx_documentary(x):   # close, warm, a small wooden room
    x = clean(x); x = eq(x, ("lowshelf", 140, .7, 2.0)); x = sat(x * 0.9, 1.3)
    return room(x, 0.5, 0.12, 4500, 0.008)


def fx_oracle(x):        # intimate and low, in a vast dark space
    x = pitch(clean(x), -1.0)
    x = eq(x, ("lowshelf", 180, .7, 2.5), ("highshelf", 8000, .7, -1.5))
    return room(x, 3.4, 0.22, 3200, 0.045)


def fx_shipai(x):        # a ship's intelligence: crisp, faintly synthetic shimmer, a steel room
    x = clean(x); x = eq(x, ("peak", 2500, 1.2, 1.5), ("highshelf", 7000, .7, 2.0))
    x = ringmod(x, 34, 0.07)
    x = chorus(x, 1.2, 0.8, 0.22, 7)
    return room(x, 0.9, 0.16, 7000, 0.012, metal=1.0)


def fx_sentinel(x):      # a vast machine intelligence: deep, a sub-octave under it, cathedral dark
    x = pitch(clean(x), -2.5)
    x = layer(x, -12, -15, lp=420)
    x = ringmod(x, 55, 0.07)
    x = eq(x, ("lowshelf", 120, .7, 2.0), ("peak", 2800, 1.0, 2.0))
    x = comp(x, -20, 3)
    return room(x, 3.0, 0.2, 2600, 0.05, metal=0.6)


def fx_commander(x):     # the hero's log: present, confident, a hint of helmet comms
    x = clean(x); x = eq(x, ("peak", 1800, 0.9, 2.0), ("lowshelf", 150, .7, 1.0))
    x = sat(x, 1.6); x = comp(x, -18, 3.2)
    return room(x, 0.35, 0.1, 6000, 0.006)


def fx_twin(x):          # one voice, two beings: an octave-up ghost and an octave-down shadow, in unison
    x = clean(x)
    x = layer(x, 12, -19, hp=900); x = layer(x, -12, -17, lp=600)
    x = chorus(x, 2.0, 0.25, 0.2)
    return room(x, 2.2, 0.2, 4200, 0.03)


def fx_signal(x):        # a transmission from far away, now warmer and closer: soft band edges, a light touch of air
    x = clean(x)
    x = eq(x, ("hp", 150), ("lp", 7800), ("lowshelf", 220, .7, 2.2), ("peak", 1500, 0.9, 1.2), ("peak", 3400, 1.2, -1.2))
    x = sat(x, 1.35)
    d = int(0.16 * SR); y = x.copy(); y[d:] += 0.06 * bq(x[:-d], "lp", 3500)      # a faint trail, not an echo
    n = np.random.default_rng(5).standard_normal(len(y)).astype(np.float32)
    y += bq(bq(n, "hp", 2000), "lp", 6000) * 0.0008
    y = comp(y, -22, 2.0, att=0.012, rel=0.2)       # smooth, even, close
    return room(y, 0.6, 0.06, 4200, 0.008)


def fx_nocturne(x):      # a late-night storyteller, very close, candle-lit room
    x = clean(x); x = eq(x, ("lowshelf", 200, .7, 3.0), ("highshelf", 10000, .7, 1.5))
    x = comp(x, -26, 3.5)
    return room(x, 1.1, 0.14, 3800, 0.02)


def fx_monolith(x):      # stone speaking: slow, very deep, a hall carved from rock
    x = pitch(clean(x), -3.5)
    x = layer(x, -12, -18, lp=300)
    x = eq(x, ("lowshelf", 110, .7, 2.5), ("peak", 3000, 1.0, 2.5))
    x = comp(x, -20, 3)
    return room(x, 2.6, 0.2, 2400, 0.06)


def fx_starborn(x):      # bright and weightless, a shimmer of light trailing behind
    from scipy.signal import fftconvolve
    x = clean(x); x = eq(x, ("highshelf", 6000, .7, 2.5), ("peak", 250, 1, -1.5))
    sh = pitch(x, 12, formant=False); sh = bq(sh, "hp", 1500)
    tail = fftconvolve(sh, _ir(3.8, 9000, 0.08))[: len(x)].astype(np.float32)
    tail *= 0.09 * np.sqrt(np.mean(x ** 2)) / (np.sqrt(np.mean(tail ** 2)) + 1e-9)
    return room(x, 2.0, 0.16, 7000, 0.03) + tail


FX = {"documentary": fx_documentary, "oracle": fx_oracle, "shipai": fx_shipai, "sentinel": fx_sentinel,
      "commander": fx_commander, "twin": fx_twin, "signal": fx_signal, "narrator": fx_narrator, "nocturne": fx_nocturne,
      "monolith": fx_monolith, "starborn": fx_starborn}

# ------------------------------------------------------------------ the cast
CAST = {
    "archivist":   {"n": 1, "name": "The Archivist", "who": "Male, British. Warm, close, a real documentary narrator. The least effects.",
                    "engine": "kokoro", "spec": "bm_george:0.55+bm_lewis:0.3+bm_fable:0.15", "speed": 0.97, "fx": "documentary"},
    "oracle":      {"n": 2, "name": "The Oracle", "who": "Female, low and hushed, speaking from a vast dark space. Pure mystery.",
                    "engine": "supertonic", "sid": 2, "speed": 0.96, "fx": "oracle"},
    "vessel":      {"n": 3, "name": "Vessel", "who": "Female ship intelligence. Crisp, calm, faintly synthetic shimmer. Sci-fi.",
                    "engine": "kokoro", "spec": "af_nova:0.45+bf_emma:0.35+af_kore:0.2", "speed": 1.0, "fx": "shipai"},
    "sentinel":    {"n": 4, "name": "Sentinel", "who": "Male machine intelligence. Deep, with a sub-octave and a dark hall. The cosmic robot.",
                    "engine": "kokoro", "spec": "am_onyx:0.5+am_fenrir:0.3+bm_daniel:0.2", "speed": 0.95, "fx": "sentinel"},
    "commander":   {"n": 5, "name": "Commander", "who": "Male, human hero of a space saga. Confident, present, a hint of helmet comms.",
                    "engine": "supertonic", "sid": 8, "speed": 1.03, "fx": "commander"},
    "twin":        {"n": 6, "name": "The Twin", "who": "One voice, two beings: an octave ghost above and a shadow below. Otherworldly.",
                    "engine": "supertonic", "sid": 7, "speed": 0.98, "fx": "twin"},
    "signal":      {"n": 7, "name": "Deep Signal", "who": "Female, a transmission from very far away. Band-limited, a delay trail.",
                    "engine": "supertonic", "sid": 4, "speed": 0.98, "fx": "signal"},
    "signal-ipa":  {"n": 11, "name": "Deep Signal (IPA)", "who": "Deep Signal's delivery on a voice that reads the phonetic alphabet: every word said as the dictionary gives it.",
                    "engine": "kokoro", "spec": "af_heart", "speed": 0.98, "fx": "signal", "intone": True},
    "narrator":    {"n": 13, "name": "The Narrator (directed)", "who": "Reads the phonetic alphabet, so every word is said as the dictionary gives it; acted sentence by sentence from the stage notes in the script.",
                    "engine": "kokoro", "spec": "af_heart", "speed": 0.98, "fx": "narrator", "intone": "directed"},
    "signal-ipa-uk": {"n": 12, "name": "Deep Signal (IPA, British)", "who": "The same, British.",
                    "engine": "kokoro", "spec": "bf_emma:0.6+bf_isabella:0.4", "speed": 0.98, "fx": "signal", "intone": True},
    "nocturne":    {"n": 8, "name": "Nocturne", "who": "Female, British, a late-night storyteller, very close. Intimate, no gimmicks.",
                    "engine": "kokoro", "spec": "bf_isabella:0.5+bf_emma:0.3+bf_alice:0.2", "speed": 0.96, "fx": "nocturne"},
    "monolith":    {"n": 9, "name": "Monolith", "who": "Male, stone speaking. Slow, very deep, a hall carved from rock.",
                    "engine": "supertonic", "sid": 9, "speed": 0.94, "fx": "monolith"},
    "starborn":    {"n": 10, "name": "Starborn", "who": "Female, bright and weightless, a shimmer of light trailing. Energetic.",
                    "engine": "supertonic", "sid": 3, "speed": 1.05, "fx": "starborn"},
}


def engine(c, cache):
    if c["engine"] == "kokoro":
        return Kokoro(c["spec"], cache, intone=c.get("intone", False))
    return Supertonic(c["sid"], cache)


def design(name, dry):
    """dry: 48k mono narration track. Returns the finished voice, peak-safe."""
    y = FX[CAST[name]["fx"]](np.asarray(dry, np.float32))
    y = bq(detone(y, 15), "lp", 15500)
    return (y / (np.abs(y).max() + 1e-9) * 0.9).astype(np.float32)


SAMPLE = ["Eleven thousand six hundred years ago, someone raised stone giants on a hill in Turkey.",
          "No metal. No writing.", "This is Göbekli Tepe.",
          "And after thirty years of digging, nine-tenths of it is still underground."]


def demo(out, names=None):
    import soundfile as sf
    os.makedirs(out, exist_ok=True)
    res = []
    for nm in names or CAST:
        c = CAST[nm]; e = engine(c, os.path.join(out, "cache"))
        parts = []
        for s in SAMPLE:
            a, _ = e.say(s.split(), c["speed"]); parts += [a, np.zeros(int(0.42 * SR), np.float32)]
        dry = np.concatenate([np.zeros(int(0.25 * SR), np.float32)] + parts)
        y = design(nm, dry)
        wav = os.path.join(out, f"{c['n']:02d}-{nm}.wav"); sf.write(wav, y, SR)
        txt, _ = transcribe(y, SR)
        res.append({"id": nm, "wav": wav, "heard": txt})
        print(c["n"], nm, "|", txt, flush=True)
    return res


if __name__ == "__main__":
    import sys
    demo(sys.argv[1] if len(sys.argv) > 1 else "voice-lab", sys.argv[2:] or None)


def hear_check(sentences):
    """sentences: [(words, audio48k)]. Runs the recogniser over every sentence and lists script words it did not
    hear (numbers, which it writes as digits, are skipped). Catches mispronounced names before anyone else does."""
    from difflib import SequenceMatcher
    bad = []
    for words, a in sentences:
        txt, _ = transcribe(a, SR)
        sw = [_norm(w) for w in words if re.search(r"[A-Za-zÀ-ÿ]", w) and not set(re.split(r"[-\s]", w.lower().strip(".,;:?!"))) <= NUMWORDS]
        hw = [_norm(w) for w in txt.split()]
        sm = SequenceMatcher(None, sw, hw, autojunk=False)
        miss = [sw[i] for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag in ("replace", "delete") for i in range(i1, i2)]
        ratio = sm.ratio()
        if miss:
            bad.append({"script": " ".join(words), "heard": txt, "missed": miss, "match": round(ratio, 2)})
    return bad


# ------------------------------------------------------------------ rhythm: the music of the narration
def pause_plan(words, i):
    """How long a narrator lets the silence sit after word i (seconds). A human pauses by meaning, not by a clock:
    a beat after a question, a held breath before a reveal, quick steps through a list of fragments."""
    w = words[i].rstrip("\"'’”)")
    nxt = words[i + 1:]
    j = 0
    while j < len(nxt) and not re.search(r"[.?!…]$", nxt[j].rstrip("\"'’”)")):
        j += 1
    next_len = j + 1                                        # length of the sentence that follows
    k = i
    while k > 0 and not re.search(r"[.?!…:]$", words[k - 1].rstrip("\"'’”)")):
        k -= 1
    this_len = i - k + 1                                    # length of the sentence that just ended
    import zlib
    jit = ((zlib.crc32(" ".join(words[max(0, i - 2): i + 2]).encode()) % 7) - 3) * 0.01   # small human variation, the same on every machine
    if w.endswith("...") or w.endswith("…"):
        return 0.72 + jit
    if w.endswith("?"):
        return 0.52 + jit
    if w.endswith(".") or w.endswith("!"):
        if this_len <= 3 and next_len <= 3:
            return 0.33 + jit                               # "No metal. No writing." : a steady walk
        if next_len <= 3:
            return 0.5 + jit                                # a short line after a long one lands harder
        return 0.42 + jit
    if w.endswith(":"):
        return 0.3 + jit
    if w.endswith(",") or w.endswith(";"):
        return None                                         # keep the model's own comma breath (clamped)
    return 0.0


def shape_pauses(words, a, spans, sr=SR):
    """Re-time the silences inside a generated phrase to the pause plan, and give every word a true end.
    Only real silences are touched (never a stop closure inside a word, never a soft 's' onset): the last clear
    gap before the next word, edited in its latter part."""
    hop = int(0.005 * sr)
    n = len(a) // hop
    e = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2) + 1e-12) for i in range(n)])
    db = 20 * np.log10(e / (e.max() + 1e-9))
    quiet = db < -42
    edits, bounds = [], []
    starts = [s for s, _ in spans]
    for i in range(len(words) - 1):
        lo = int((starts[i] + 0.12) / 0.005); hi = min(n, int((starts[i + 1] + 0.15) / 0.005))
        runs, f = [], lo
        while f < hi:
            if quiet[f]:
                g = f
                while g < n and quiet[g]:
                    g += 1
                if (g - f) * 0.005 >= 0.04:
                    runs.append((f, g))
                f = g
            else:
                f += 1
        if not runs:
            target = pause_plan(words, i)
            if target and target >= 0.3 and hi > lo:          # a full stop the model ran through: open it at the quietest instant
                fmin = lo + int(np.argmin(db[lo:hi]))
                if db[fmin] < -30:
                    b = fmin * 0.005; bounds.append((b, b)); edits.append((b, target, b, b)); continue
            b = max(starts[i] + 0.06, starts[i + 1] - 0.02); bounds.append((b, b)); continue
        r0, r1 = runs[-1]
        q0, q1 = r0 * 0.005, r1 * 0.005
        bounds.append((q0, q1))
        target = pause_plan(words, i)
        have = q1 - q0
        if target is None:                                  # comma: keep, within human limits
            target = min(max(have, 0.12), 0.28)
        if target == 0.0 or abs(target - have) < 0.025:
            continue
        edits.append((q0 + 0.6 * (q1 - q0), target - have, q0, q1))
    # apply edits back to front so earlier positions stay valid
    out = a.copy()
    for mid, d, q0, q1 in sorted(edits, reverse=True):
        p = int(mid * sr)
        if d > 0:
            out = np.concatenate([out[:p], np.zeros(int(d * sr), np.float32), out[p:]])
        else:
            cut = int(min(-d, max(0.0, (q1 - q0) - 0.1)) * sr)          # always keep some of the original air each side
            if cut > 0:
                c0, c1 = p - cut // 2, p + cut - cut // 2
                fade = min(240, c0, len(out) - c1)
                if fade > 0:
                    w_ = np.linspace(1, 0, fade, dtype=np.float32)
                    out[c0 - fade:c0] = out[c0 - fade:c0] * w_ + out[c1:c1 + fade] * (1 - w_)
                out = np.concatenate([out[:c0], out[c1 + fade:]]) if fade > 0 else np.concatenate([out[:c0], out[c1:]])
    def shift(t, inclusive=False):
        s = 0.0
        for mid, d, q0, q1 in edits:
            if t > mid or (inclusive and t >= mid):
                s += d if d > 0 else -min(-d, max(0.0, (q1 - q0) - 0.1))
        return t + s
    new = []
    for i, (s, e_) in enumerate(spans):
        s2 = shift(s if i == 0 else bounds[i - 1][1], inclusive=True)
        e2 = shift(bounds[i][0]) if i < len(bounds) else shift(e_)
        new.append((round(s2, 3), round(max(s2 + 0.06, e2), 3)))
    return out.astype(np.float32), new


# ------------------------------------------------------------------ intonation: give the melody back
INTONE = {"range": 1.33, "decl": 0.8, "final": 1.3, "comma": 0.6, "emph": 1.9, "emph_db": 1.8,
          "len_final": 1.14, "len_comma": 1.06, "len_emph": 1.1}

# The director's notes. Every line of every film carries one of these (written into the script as [d:...]),
# so the narrator knows before she speaks whether a line is a hook, an aside, the turn of the story or the verdict.
#   reg    register shift (semitones)         rng   melody width (x the voice's own)
#   tempo  speaking rate                      final how the line lands: fall, suspend, lift
#   gain   level (dB)                         decl  how much the pitch settles through a sentence
MOTHER = -0.35   # a touch lower and softer overall: warm, unhurried, reassuring
DIRECTION = {
    "intrigue": {"reg": -0.4, "rng": 1.38, "tempo": 0.97, "final": "fall", "gain": 0.0, "decl": 0.9},
    "calm":     {"reg": 0.0, "rng": 1.25, "tempo": 1.0, "final": "fall", "gain": 0.0, "decl": 0.8},
    "build":    {"reg": 0.35, "rng": 1.35, "tempo": 1.03, "final": "fall", "gain": 0.5, "decl": 0.6},
    "wonder":   {"reg": 0.25, "rng": 1.48, "tempo": 0.95, "final": "fall", "gain": 0.0, "decl": 0.9},
    "aside":    {"reg": 0.6, "rng": 1.18, "tempo": 1.06, "final": "fall", "gain": -1.5, "decl": 0.5},
    "list":     {"reg": 0.0, "rng": 1.2, "tempo": 1.0, "final": "fall", "gain": 0.0, "decl": 0.4},
    "tension":  {"reg": -0.8, "rng": 1.28, "tempo": 0.95, "final": "suspend", "gain": -0.5, "decl": 0.4},
    "reveal":   {"reg": -0.3, "rng": 1.45, "tempo": 0.94, "final": "fall", "gain": 0.8, "decl": 1.0},
    "verdict":  {"reg": -1.0, "rng": 1.15, "tempo": 0.93, "final": "fall", "gain": 0.0, "decl": 1.1},
}
ROLE_DIRECTION = {"hook": "intrigue", "world": "calm", "collision": "build", "cost": "calm", "reversal": "reveal", "tag": "verdict"}
WH = {"what", "what's", "where", "where's", "who", "who's", "why", "how", "which", "when"}


def _plain(w):
    import heteronyms as _HN
    return _HN.plain(w.replace("*", "").replace("^", ""))


def perform(words, a, spans, direction="calm", sr=SR, cfg=None):
    """Deliver the line as directed, with PSOLA (Praat): pitch and timing reshaped together, no joins, no splices.
    Melody: widened around the speaker's median, shifted to the line's register, settling through each sentence
    and resetting at the next; statements fall on the last word, yes/no questions lift, wh-questions fall,
    a suspended line hangs; a small lift before commas; marked *words* get a pitch accent.
    Timing: the last word of a sentence stretches (phrase-final lengthening, the strongest cue of a human
    speaker), a little before commas, and on accented words. Word times are carried through the new timing."""
    import parselmouth
    from parselmouth.praat import call
    c = dict(INTONE, **(cfg or {}))
    d = DIRECTION.get(direction, DIRECTION["calm"])
    snd = parselmouth.Sound(a.astype(np.float64), sr)
    dur = snd.duration
    man = call(snd, "To Manipulation", 0.01, 70, 420)
    pt = call(man, "Extract pitch tier")
    n = call(pt, "Get number of points")
    if n < 5:
        return a, spans
    T = np.array([call(pt, "Get time from index", i + 1) for i in range(n)])
    F = np.array([call(pt, "Get value at index", i + 1) for i in range(n)])
    med = np.median(F)
    st = 12 * np.log2(F / med)
    new = st * d["rng"] + d["reg"] + MOTHER
    pw = [_plain(w) for w in words]
    sent, s0 = [], 0
    for i, w in enumerate(pw):
        if re.search(r"[.?!…]['\"’”)]*$", w) or i == len(pw) - 1:
            sent.append((s0, i)); s0 = i + 1
    for a_, b_ in sent:
        t0, t1 = spans[a_][0], spans[b_][1]
        m = (T >= t0) & (T <= t1)
        if t1 > t0:
            new[m] += d["decl"] * (1 - 2 * (T[m] - t0) / (t1 - t0))
        last = pw[b_].rstrip("\"'’”)")
        w0, w1 = spans[b_]
        mw = (T >= w0) & (T <= w1)
        if not mw.any():
            continue
        u = (T[mw] - w0) / max(0.05, w1 - w0)
        first = re.sub(r"[^a-z']", "", pw[a_].lower())
        if last.endswith("?"):
            if first in WH or first == "or":
                new[mw] -= c["final"] * u                    # a real question for information falls
            else:
                new[mw] += 2.0 * np.clip((u - 0.2) / 0.8, 0, 1)   # yes/no and topic questions lift
        elif last.endswith("...") or last.endswith("…") or (d["final"] == "suspend" and b_ == len(pw) - 1):
            new[mw] = new[mw] * 0.6 + 0.3                    # held in the air
        else:
            new[mw] -= c["final"] * u
    for i, w in enumerate(words):
        w0, w1 = spans[i]
        mw = (T >= w0) & (T <= w1)
        if not mw.any():
            continue
        u = (T[mw] - w0) / max(0.05, w1 - w0)
        if _plain(w).endswith(","):
            new[mw] += c["comma"] * np.clip((u - 0.4) / 0.6, 0, 1)
        if w.startswith("*"):
            new[mw] += c["emph"] * np.sin(np.pi * np.clip(u, 0, 1)) ** 0.7
    new = np.where(new > 0, 7.5 * np.tanh(new / 7.5), np.maximum(new, -9))   # never shrill, never growled
    call(pt, "Remove points between", 0, dur)
    for t, v in zip(T, new):
        call(pt, "Add point", float(t), float(med * 2 ** (v / 12)))
    call([pt, man], "Replace pitch tier")
    # ---- timing: a relative-duration curve on a 10 ms grid
    grid = np.arange(0, dur + 0.01, 0.01)
    k = np.ones(len(grid))
    vo = np.zeros(len(grid))                         # stretch only where the voice is voiced: a stretched
    idx = np.clip(np.round(T / 0.01).astype(int), 0, len(grid) - 1)   # consonant burst would sound like an extra syllable
    vo[idx] = 1
    vo = np.convolve(vo, np.ones(3) / 3, mode="same")
    vo = (vo > 0.3).astype(float)
    vo = np.convolve(vo, np.ones(5) / 5, mode="same")        # soft edges
    def region(t0, t1, f, soft=0.03):
        if t1 - t0 < 0.04:
            return
        rise = np.clip((grid - t0) / soft, 0, 1) * np.clip((t1 - grid) / soft, 0, 1) * vo
        k[:] = np.maximum(k, 1 + (f - 1) * rise)
    for a_, b_ in sent:
        w0, w1 = spans[b_]
        region(w0 + (w1 - w0) * 0.35, w1, c["len_final"])   # the last syllables of the sentence
    for i, w in enumerate(words):
        w0, w1 = spans[i]
        if _plain(w).endswith(",") and not re.search(r"[.?!…]$", _plain(w)):
            region(w0 + (w1 - w0) * 0.4, w1, c["len_comma"])
        if w.startswith("*"):
            region(w0, w1, c["len_emph"])
    dt = call("Create DurationTier", "d", 0, dur)
    for t, v in zip(grid, k):
        call(dt, "Add point", float(t), float(v))
    call([dt, man], "Replace duration tier")
    out = np.asarray(call(man, "Get resynthesis (overlap-add)").values[0], np.float32)
    cum = np.concatenate([[0], np.cumsum((k[1:] + k[:-1]) / 2 * 0.01)])
    remap = lambda t: float(np.interp(t, grid, cum))
    new_spans = [(round(remap(s_), 3), round(remap(e_), 3)) for s_, e_ in spans]
    # accents also get a touch more level; the line gets its own level
    g = np.full(len(out), 10 ** (d["gain"] / 20), np.float32)
    for i, w in enumerate(words):
        if w.startswith("*"):
            i0, i1 = int(new_spans[i][0] * sr), min(len(out), int(new_spans[i][1] * sr))
            if i1 > i0:
                h = np.sin(np.linspace(0, np.pi, i1 - i0)) ** 0.5
                g[i0:i1] *= (1 + (10 ** (c["emph_db"] / 20) - 1) * h).astype(np.float32)
    return out * g, new_spans


# ------------------------------------------------------------------ direction (the play script)
# Every sentence can carry a stage note in the script:
#   [act:dry, one eyebrow up]   what the actor is thinking (for people; it also sets the tune when it names one)
#   [tune:fall|rise|risefall|fallrise|level|highfall]   how the sentence lands
#   ^word                        the word she leans on (the nuclear accent; *word* also glows in the caption)
#   [beat:0.3]                   a held silence before this word, inside the sentence
#   [gap:0.8]                    the silence before this sentence (overrides the pause plan)
# Unmarked sentences get a sensible default: the last content word carries the accent, statements fall,
# yes/no questions rise, wh-questions fall, a trailing comma or '...' stays level.
PERFORM2_V = 7
ACT = {"rng": 0.35, "post": 0.45, "acc": 2.4, "hi": 4.2, "low": -3.4, "rise": 4.6, "fr_rise": 2.2, "len_final": 1.06, "len_focus": 1.06,
       "foc_db": 1.5, "post_db": -1.8, "prenuc": 1.5}
FUNC_W = set("a an the and of in on at to by for with from as is are was were be been it its it's his her their our your this that "
             "these those or but so if then than into onto not no just also very".split())
TUNE_WORDS = {"rise": "rise", "rising": "rise", "question": "rise", "ironic": "risefall", "irony": "risefall", "surprised": "risefall",
              "incredulous": "risefall", "reservation": "fallrise", "but": "fallrise", "doubtful": "fallrise", "continuing": "level",
              "list": "level", "suspended": "level", "emphatic": "highfall", "certain": "fall", "flat": "fall"}


def default_tune(pw, direction):
    last = pw[-1].rstrip("\"'’”)")
    first = re.sub(r"[^a-z']", "", pw[0].lower())
    if last.endswith("?"):
        return "fall" if first in WH or first == "or" else "rise"
    if last.endswith(",") or last.endswith("...") or last.endswith("…") or last.endswith(":"):
        return "level"
    return "fall"


def perform2(words, a, spans, direction="calm", act=None, sr=SR):
    """Directed delivery. Her own melody and rhythm are kept; only what the stage note asks is changed:
    one nuclear accent on the focus word (the peak of the sentence), prenuclear accents on earlier marked words,
    everything after the focus compressed and lowered (deaccenting: the strongest cue that a person means what
    they say), the sentence's tune at the end (fall, rise, rise-fall, fall-rise, level, high fall), lengthening
    where a speaker slows (the focus, the last syllables), a little more level on the focus and less after it,
    and held beats of silence where the note asks for them."""
    import parselmouth
    from parselmouth.praat import call
    act = act or {}
    c = ACT
    d = DIRECTION.get(direction, DIRECTION["calm"])
    pw = [_plain(w) for w in words]
    n = len(words)
    if n == 0:
        return a, spans
    marks = [i for i, w in enumerate(words) if w.startswith("^")] or [i for i, w in enumerate(words) if w.startswith("*")]
    if not marks:
        cont = [i for i, w in enumerate(pw) if re.sub(r"[^a-z']", "", w.lower()) not in FUNC_W]
        marks = [cont[-1] if cont else n - 1]
    f = marks[-1]
    tune = act.get("tune")
    if not tune and act.get("note"):
        tune = next((TUNE_WORDS[t] for t in re.findall(r"[a-z]+", act["note"].lower()) if t in TUNE_WORDS), None)
    tune = tune or default_tune(pw, direction)
    snd = parselmouth.Sound(a.astype(np.float64), sr)
    dur = snd.duration
    man = call(snd, "To Manipulation", 0.01, 75, 500)
    pt = call(man, "Extract pitch tier")
    npt = call(pt, "Get number of points")
    explicit = any(w.startswith("^") for w in words)
    if npt >= 5:
        T = np.array([call(pt, "Get time from index", i + 1) for i in range(npt)])
        F = np.array([call(pt, "Get value at index", i + 1) for i in range(npt)])
        med = np.median(F)
        nat = 12 * np.log2(F / med) * (1 + (d["rng"] - 1) * c["rng"])        # her own melody, semitones around her median
        new = nat.copy()
        s0 = spans[0][0]
        f0, f1 = spans[f]
        vf = T[(T >= f0) & (T <= f1)]                                            # the voiced part of the focus word
        v0, v1 = (vf[0], vf[-1]) if len(vf) >= 2 else (f0, f0 + 0.6 * (f1 - f0))
        t_end = max(v1, T[-1])                                                   # the last voiced moment, not the silence after
        bump = lambda t, at, h, s_: h * np.exp(-0.5 * ((t - at) / s_) ** 2)
        for i in marks[:-1]:                                                     # earlier marked words: prenuclear accents
            vv = T[(T >= spans[i][0]) & (T <= spans[i][1])]
            if len(vv) >= 2:
                new += bump(T, vv[0] + 0.4 * (vv[-1] - vv[0]), c["prenuc"], max(0.035, 0.3 * (vv[-1] - vv[0])))
        pre = T < v0
        if pre.any() and v0 > s0:
            new[pre] -= d["decl"] * 0.5 * (T[pre] - s0) / max(0.2, v0 - s0)      # a gentle settle towards the focus
        top = (np.max(new[pre]) if pre.any() else 0.0)
        base = np.median(new)
        pk_h = max(top + 1.2, base + 2.6) if explicit else base + 2.4             # a marked focus is the peak of the sentence
        pk = v0 + 0.4 * (v1 - v0)
        # the nuclear tune: a target contour from the focus to the last voiced moment, her micro-melody kept on top
        TUN = {"fall":     [(v0, pk_h - 1.0), (pk, pk_h), (t_end, base - 4.0)],
               "highfall": [(v0, pk_h - 0.5), (pk, pk_h + 1.8), (t_end, base - 5.0)],
               "rise":     [(v0, base - 1.0), (pk, base - 2.0), (v1, base + 1.5), (t_end, base + 5.5)],
               "risefall": [(v0, base - 0.5), (v0 + 0.65 * (v1 - v0), pk_h + 1.5), (t_end, base - 4.0)],
               "fallrise": [(v0, pk_h - 0.8), (pk, pk_h), (pk + 0.7 * (t_end - pk), base - 2.5), (t_end, base + 2.5)],
               "level":    [(v0, base + 0.5), (pk, base + 1.6), (t_end, base + 0.6)]}[tune]
        if t_end - v0 < 0.12:                                                   # a very short tail: keep the shape inside it
            TUN = [(max(v0, t_end - 0.12) + (x - v0) * 0.12 / max(1e-3, t_end - v0), y) for x, y in TUN]
        tx, ty = zip(*TUN)
        nuc = T >= v0
        if nuc.any():
            tgt = np.interp(T[nuc], tx, ty)
            res = nat[nuc] - np.polyval(np.polyfit(T[nuc], nat[nuc], 1), T[nuc]) if nuc.sum() > 3 else 0
            blend = np.clip((T[nuc] - v0) / 0.06, 0, 1)                         # 60 ms into the focus, the tune takes over
            new[nuc] = (1 - blend) * new[nuc] + blend * (tgt + 0.35 * res)
        new = new + d["reg"] + MOTHER
        new = np.where(new > 0, 8.0 * np.tanh(new / 8.0), np.maximum(new, -10))
        call(pt, "Remove points between", 0, dur)
        for t, v in zip(T, new):
            call(pt, "Add point", float(t), float(med * 2 ** (v / 12)))
        call([pt, man], "Replace pitch tier")
    # ---- timing
    grid = np.arange(0, dur + 0.01, 0.01)
    k = np.ones(len(grid))
    def region(t0, t1, fct, soft=0.03):
        if t1 - t0 < 0.04:
            return
        r = np.clip((grid - t0) / soft, 0, 1) * np.clip((t1 - grid) / soft, 0, 1)
        k[:] = np.maximum(k, 1 + (fct - 1) * r)
    if act.get("tempo"):                                  # a sentence paced apart from its line ([p:0.93])
        k[:] = k / float(act["tempo"])
    w0, w1 = spans[-1]
    region(w0 + (w1 - w0) * 0.4, w1, c["len_final"] * (1.04 if tune in ("rise", "fallrise") else 1.0) / float(act.get("tempo", 1.0)))
    f0, f1 = spans[f]
    if f != n - 1:
        region(f0 + (f1 - f0) * 0.2, f0 + (f1 - f0) * 0.8, c["len_focus"])
    dt = call("Create DurationTier", "d", 0, dur)
    for t, v in zip(grid, k):
        call(dt, "Add point", float(t), float(v))
    call([dt, man], "Replace duration tier")
    out = np.asarray(call(man, "Get resynthesis (overlap-add)").values[0], np.float32)
    cum = np.concatenate([[0], np.cumsum((k[1:] + k[:-1]) / 2 * 0.01)])
    remap = lambda t: float(np.interp(t, grid, cum))
    sp = [(remap(s_), remap(e_)) for s_, e_ in spans]
    # ---- level: a little more on the focus, less after it
    g = np.ones(len(out), np.float32)
    i0, i1 = int(sp[f][0] * sr), min(len(out), int(sp[f][1] * sr))
    if i1 > i0:
        g[i0:i1] *= (1 + (10 ** (c["foc_db"] / 20) - 1) * np.sin(np.linspace(0, np.pi, i1 - i0)) ** 0.5).astype(np.float32)
    if f < n - 1:
        j0 = int(sp[f][1] * sr); ramp = min(len(out) - j0, int(0.08 * sr))
        if ramp > 0:
            g[j0:j0 + ramp] *= np.linspace(1, 10 ** (c["post_db"] / 20), ramp).astype(np.float32)
            g[j0 + ramp:] *= 10 ** (c["post_db"] / 20)
    out = out * g * 10 ** (d["gain"] / 20)
    # ---- beats: held silences inside the sentence, cut where the voice is quietest near the word's start
    for i in sorted(act.get("beats", {}), key=lambda x: -int(x)):
        secs = float(act["beats"][i]); i = int(i)
        if not (0 < i < n) or secs <= 0:
            continue
        at = int(sp[i][0] * sr); win = int(0.03 * sr)
        lo, hi = max(1, at - win), min(len(out) - 1, at + win)
        e = np.convolve(out[lo:hi] ** 2, np.ones(64) / 64, mode="same")
        cut = lo + int(np.argmin(e)) if hi > lo else at
        fd = int(0.006 * sr)
        left, right = out[:cut].copy(), out[cut:].copy()
        left[-fd:] *= np.linspace(1, 0, fd, dtype=np.float32); right[:fd] *= np.linspace(0, 1, fd, dtype=np.float32)
        out = np.concatenate([left, np.zeros(int(secs * sr), np.float32), right])
        tc = cut / sr
        sp = [(s_ + (secs if s_ >= tc - 0.001 else 0), e_ + (secs if e_ > tc else 0)) for s_, e_ in sp]
    return out.astype(np.float32), [(round(x, 3), round(y, 3)) for x, y in sp]


GENTLE = {"acc": 2.0, "post": 0.65, "post_low": -1.0, "rise": 3.6, "level": 0.5, "rf": 2.4, "hf": 2.6, "fr": 1.8}


def perform3(words, a, spans, act=None, sr=SR):
    """Directed delivery, gently. The voice already acts (it was trained on people); this only adds what the stage
    note asks for and she did not do on her own, and never touches timing: a modest lift on a marked focus word,
    the words after it a little lower and flatter, a rise on the last word of a real question or a continuing list
    item, a held (not falling) end for a suspended line. Small moves only (a few semitones), pitch marks taken
    with a female voice's range so the overlap-add resynthesis stays clean. Nothing at all when nothing is asked."""
    import parselmouth
    from parselmouth.praat import call
    act = act or {}
    c = GENTLE
    pw = [_plain(w) for w in words]
    n = len(words)
    if n == 0:
        return a, spans
    marks = [i for i, w in enumerate(words) if w.startswith("^")]
    tune = act.get("tune") or default_tune(pw, "calm")
    want_focus = bool(marks) and n > 1
    if not want_focus and tune in ("fall",):
        return a, spans                                   # her own reading already lands a statement
    snd = parselmouth.Sound(a.astype(np.float64), sr)
    dur = snd.duration
    man = call(snd, "To Manipulation", 0.01, 120, 420)
    pt = call(man, "Extract pitch tier")
    npt = call(pt, "Get number of points")
    if npt < 5:
        return a, spans
    T = np.array([call(pt, "Get time from index", i + 1) for i in range(npt)])
    F = np.array([call(pt, "Get value at index", i + 1) for i in range(npt)])
    st = 12 * np.log2(F / np.median(F))
    add = np.zeros(len(T))
    voiced = lambda i: T[(T >= spans[i][0]) & (T <= spans[i][1])]
    if want_focus:
        f = marks[-1]
        vf = voiced(f)
        if len(vf) >= 2:
            v0, v1 = vf[0], vf[-1]
            pk = v0 + 0.4 * (v1 - v0); sg = max(0.035, 0.28 * (v1 - v0))
            lift = c["acc"] if tune not in ("rise",) else 0.6
            lift = c["rf"] if tune == "risefall" else c["hf"] if tune == "highfall" else lift
            add += lift * np.exp(-0.5 * ((T - pk) / sg) ** 2)
            # deaccent only to the end of the focus's own phrase: after a comma, colon or dash a new phrase starts
            # with its own accent, as any reader does ("...exploded, | somewhere between...")
            nb = next((j for j in range(f + 1, n) if re.search(r"[,;:—–]['\"’”)]*$", pw[j - 1])), None)
            t_b = spans[nb][0] - 0.01 if nb is not None else 1e9
            post = (T > v1 + 0.02) & (T < t_b)
            if post.sum() > 2 and tune != "rise":
                m_ = np.mean(st[post])
                add[post] += (m_ + (st[post] - m_) * c["post"] + c["post_low"]) - st[post]
    lw = voiced(n - 1)
    if len(lw) >= 2:
        l0, l1 = lw[0], lw[-1]
        u = np.clip((T - l0) / max(0.05, l1 - l0), 0, 1)
        inl = (T >= l0)
        if tune == "rise":
            add[inl] += c["rise"] * u[inl] ** 1.5
        elif tune == "level":
            drop = st[inl] - st[inl][0]
            add[inl] += np.where(drop < 0, -drop * c["level"], 0)
        elif tune == "fallrise":
            add[inl] += np.where(u[inl] > 0.55, c["fr"] * ((u[inl] - 0.55) / 0.45) ** 1.4, 0)
    if np.abs(add).max() < 0.4:
        return a, spans
    add = np.convolve(add, np.ones(5) / 5, mode="same")        # no corners
    call(pt, "Remove points between", 0, dur)
    for t, v, fr in zip(T, add, F):
        call(pt, "Add point", float(t), float(fr * 2 ** (v / 12)))
    call([pt, man], "Replace pitch tier")
    out = np.asarray(call(man, "Get resynthesis (overlap-add)").values[0], np.float32)
    m = min(len(out), len(a)); o = np.zeros(len(a), np.float32); o[:m] = out[:m]
    return o, spans


def intonate(words, a, spans, sr=SR, cfg=None):
    return perform(words, a, spans, "calm", sr, cfg)[0]


# ------------------------------------------------------------------ breath
def breath(level_rms, dur=0.36, seed=0):
    """A soft inhale: turbulent air shaped by an open vocal tract (formant-like resonances), swelling in and
    releasing. Mixed far below the voice: felt more than heard, it is what tells the ear a person is speaking."""
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    x = r.standard_normal(n).astype(np.float32)
    x = bq(bq(x, "hp", 350), "lp", 5200)
    x = bq(x, "peak", 1100, 1.6, 7) ; x = bq(x, "peak", 2600, 2.0, 5); x = bq(x, "peak", 4200, 2.5, 3)
    t = np.linspace(0, 1, n)
    env = np.clip(t / 0.55, 0, 1) ** 1.6 * np.clip((1 - t) / 0.25, 0, 1) ** 0.8
    env *= 1 + 0.12 * np.sin(2 * np.pi * r.uniform(5, 8) * t * dur)
    x *= env
    return (x / (np.sqrt(np.mean(x[env > 0.3] ** 2)) + 1e-9) * level_rms * 10 ** (-27 / 20)).astype(np.float32)
