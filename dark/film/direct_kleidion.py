"""Dark Corners 4, Kleidion (1014). Plain telling. Facts: claude/dark-research-kleidion.md. The blinding has one late source:
always told as the chronicler's claim, with his own hedge, 'as they say'. 'Bulgar-slayer' introduced as a later nickname."""
from _dhead import DELIVERY, finish
T, F = True, False
SCRIPT = [
    ('o1', F, [("In 1014, an emperor captured a whole army of his enemies.", 'firm', 0.7, T)]),
    ('o2', F, [("Then, a chronicler wrote, he sent them home.", 'calm', 0.6, F), ("Blind.", 'grave', 1.0, T)]),
    ('o3', F, [("Everything you're about to hear was written down nine hundred years ago.", 'grave', 1.4, T)]),
    ('x1', F, [("The emperor was Basil the Second.", 'calm', 0.4, T), ("He ruled the Eastern Roman Empire, from Constantinople.", 'calm', 0.8, T)]),
    ('x2', F, [("His enemy was Samuel, tsar of the Bulgarians.", 'calm', 0.4, T), ("They had been at war for almost forty years.", 'firm', 0.9, T)]),
    ('x3', F, [("Basil had once barely escaped an ambush.", 'calm', 0.4, T),
               ("Samuel had once survived a battle by lying among his own dead.", 'grave', 1.0, T)]),
    ('w1', F, [("In the summer of 1014, Samuel blocked a mountain pass with a huge wall.", 'calm', 0.5, T),
               ("The pass was called Kleidion.", 'calm', 0.4, T), ("The key.", 'firm', 1.0, T)]),
    ('w2', F, [("Basil attacked.", 'firm', 0.3, F), ("Again and again.", 'calm', 0.4, T), ("The wall held.", 'firm', 1.0, T)]),
    ('t1', F, [("Then one of his generals took his men over the mountain.", 'calm', 0.4, T), ("And came down behind the wall.", 'firm', 0.9, T)]),
    ('t2', F, [("The defenders panicked.", 'firm', 0.4, T), ("Many were killed.", 'grave', 0.4, T), ("Many more were captured.", 'grave', 1.0, T)]),
    ('s1', F, [("Samuel was nearly caught.", 'calm', 0.4, T), ("His son put him on a horse.", 'calm', 0.4, T), ("And they got away.", 'firm', 1.0, T)]),
    ('r1', F, [("But the war was not over.", 'firm', 0.4, T), ("Soon after, one of Basil's governors was trapped in a gorge and killed.", 'grave', 1.0, T)]),
    ('b1', F, [("Then Basil gave an order.", 'grave', 1.2, T)]),
    ('b2', T, [("The chronicler wrote that he blinded the prisoners.", 'grave', 0.5, T), ("About fifteen thousand,", 'record', 0.3, F),
               ("as they say.", 'record', 1.0, T)]),
    ('b3', F, [("He split them into groups of a hundred.", 'calm', 0.4, T), ("Each group was led by one man with one eye left.", 'grave', 0.5, T),
               ("And he sent them home to their tsar.", 'grave', 1.2, T)]),
    ('d1', F, [("When Samuel saw them coming,", 'calm', 0.3, F), ("he collapsed.", 'grave', 0.9, T)]),
    ('d2', F, [("They woke him with water.", 'calm', 0.4, T), ("He asked for a cup of cold water.", 'calm', 0.4, T), ("He drank it.", 'calm', 0.5, T),
               ("Then his heart gave out.", 'grave', 0.9, T)]),
    ('d3', F, [("Two days later, Samuel was dead.", 'grave', 1.3, T)]),
    ('q1', F, [("But was it true?", 'firm', 0.6, T), ("Another writer of the same century says Basil captured fourteen thousand men.", 'calm', 0.4, T),
               ("He says nothing about blinding.", 'firm', 0.8, T)]),
    ('q2', F, [("Most historians think the real number was far smaller.", 'calm', 1.0, T)]),
    ('f1', F, [("Bulgaria fought on for four more years.", 'calm', 0.5, T), ("And Basil got a nickname.", 'calm', 0.4, T),
               ("The Bulgar Slayer.", 'firm', 0.6, T), ("But nobody called him that while he was alive.", 'calm', 0.4, T),
               ("It came more than a hundred and fifty years later.", 'calm', 1.0, T)]),
    ('f2', T, [("About fifteen thousand, the chronicler wrote.", 'grave', 0.6, T), ("As they say.", 'grave', 1.6, T)]),
]
PRON = {'Kleidion': 'Kly-dee-on', 'tsar': 'zar'}
DIRECTED, QUOTE, LINES, SAY = finish(SCRIPT, PRON)
