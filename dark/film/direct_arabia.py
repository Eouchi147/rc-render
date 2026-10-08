"""Dark Corners 3, Arabia (c. 600): the man who bought girls' lives. Plain telling. Facts: claude/dark-research-arabia.md.
Rules: never 'the Arabs buried their daughters'; no depiction or voice of revered figures; numbers shown as disputed."""
from _dhead import DELIVERY, finish
T, F = True, False
SCRIPT = [
    ('o1', F, [("Around the year 600, in Arabia, a man went looking for two lost camels.", 'firm', 0.7, T)]),
    ('o2', F, [("What he found that night changed the rest of his life.", 'calm', 0.8, T)]),
    ('o3', F, [("Everything you're about to hear comes from the old Arabic records.", 'grave', 1.4, T)]),
    ('x1', F, [("His name was Sasaa.", 'calm', 0.4, T), ("A nobleman of the Tamim tribe.", 'calm', 0.9, T)]),
    ('x2', F, [("Life there was hard.", 'calm', 0.4, T), ("In years of hunger, some families saw a newborn girl as one more mouth.", 'calm', 0.5, T),
               ("And some buried her alive.", 'grave', 1.0, T)]),
    ('x3', F, [("Not every family.", 'firm', 0.3, F), ("Many hated it.", 'calm', 0.4, T), ("But it happened.", 'grave', 1.1, T)]),
    ('s1', F, [("Sasaa followed the tracks into open desert.", 'calm', 0.4, T), ("Late at night, he saw two tents.", 'calm', 0.8, T)]),
    ('s2', F, [("In one, a very old man.", 'calm', 0.4, T), ("He said: we found your camels.", 'calm', 0.4, T),
               ("Their milk has kept my family alive.", 'calm', 0.9, T)]),
    ('s3', F, [("Then a woman called from the other tent.", 'calm', 0.4, T), ("She had just given birth.", 'firm', 0.9, T)]),
    ('s4', T, [("The old man asked: boy or girl?", 'calm', 0.5, T), ("If it is a boy, he is one of us.", 'record', 0.4, T),
               ("If it is a girl, bury her.", 'record', 1.0, T)]),
    ('s5', F, [("It was a girl.", 'grave', 1.3, T)]),
    ('b1', F, [("Sasaa asked to buy her.", 'calm', 0.4, T), ("The old man was insulted.", 'calm', 0.4, T),
               ("A free man does not sell his children.", 'firm', 0.9, T)]),
    ('b2', T, [("Sasaa answered:", 'calm', 0.4, F), ("I am not buying her as a slave.", 'letter', 0.5, T), ("I am buying her life.", 'letter', 1.3, T)]),
    ('b3', F, [("The price was his two pregnant camels,", 'calm', 0.3, F), ("their calves,", 'calm', 0.3, F),
               ("and the camel he was riding.", 'firm', 1.0, T)]),
    ('v1', F, [("He walked home without them.", 'calm', 0.5, T), ("And that night, he made a promise.", 'firm', 0.5, T),
               ("Every girl he heard of, he would save.", 'grave', 1.1, T)]),
    ('v2', F, [("The old records cannot agree how many he saved.", 'calm', 0.5, T), ("Thirty.", 'calm', 0.3, F), ("Ninety-six.", 'calm', 0.3, F),
               ("Three hundred and sixty.", 'calm', 0.3, F), ("Four hundred.", 'calm', 0.7, T), ("Every number was a girl.", 'grave', 1.3, T)]),
    ('z1', F, [("He was not alone.", 'firm', 0.4, T), ("In Mecca, a man named Zayd did the same.", 'calm', 0.8, T)]),
    ('z2', T, [("When a father was about to kill his daughter, Zayd told him:", 'calm', 0.4, F), ("Do not kill her.", 'letter', 0.4, T),
               ("I will pay for her keep.", 'letter', 1.0, T)]),
    ('z3', F, [("He raised the girl.", 'calm', 0.4, T), ("And when she was grown, he told the father:", 'calm', 0.3, F),
               ("if you want her back, take her.", 'firm', 1.1, T)]),
    ('g1', F, [("Years later, Sasaa's grandson became one of the most famous poets in Arabia.", 'calm', 0.5, T),
               ("One line was about his grandfather.", 'firm', 0.7, T)]),
    ('g2', T, [("He gave life to the buried girl,", 'letter', 0.4, F), ("so she was not buried.", 'letter', 1.4, T)]),
    ('f1', F, [("Nobody knows how many girls he really saved.", 'calm', 0.6, T), ("But somewhere in that desert, a girl grew up,", 'calm', 0.4, F),
               ("because a man went looking for his camels.", 'grave', 1.6, T)]),
]
PRON = {'Sasaa': 'Sasa-ah', 'Tamim': 'Tameem', 'Zayd': 'Zade'}
DIRECTED, QUOTE, LINES, SAY = finish(SCRIPT, PRON)
