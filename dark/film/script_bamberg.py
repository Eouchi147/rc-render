"""Dark Corners, episode 1: A Hundred Thousand Good Nights (Bamberg, 1628). Narration script.
Each line: (id, text, direction, pace). Letter quotes are marked q=True (voiced a touch slower and closer).
Sources: Junius's letter of 24 July 1628 (Staatsbibliothek Bamberg RB.Msc.148/300, text after Leitschuh 1883 / Bauer 1911),
the trial record (Burr 1896), Spee, Cautio Criminalis (1631), Dubium XLIX. See claude/dark-research-bamberg.md."""
LINES = [
    # COLD OPEN
    ("h1", "There are two records of what happened to this man.", "intrigue", 0.97, False),
    ("h2", "One was written by his judges.", "intrigue", 0.97, False),
    ("h3", "The other was never meant to exist.", "intrigue", 0.95, False),
    ("h4", "Bamberg, sixteen twenty-eight. His hands are crippled.", "calm", 0.97, False),
    ("q1", "Many hundred thousand good nights, my heart's dearest daughter, Veronica.", "wonder", 0.9, True),
    ("q2", "Innocent I came into prison. Innocent I was tortured. Innocent I must die.", "tension", 0.9, True),
    # WORLD
    ("w1", "Johannes Junius. Fifty-five. Several times mayor of this city.", "calm", 0.98, False),
    ("w2", "Now, a prisoner of its new witch house.", "calm", 0.96, False),
    ("w3", "Under torture, the accused named others, who named others.", "build", 0.98, False),
    ("w4", "His wife was named. She was executed before him.", "calm", 0.95, False),
    ("w5", "Then six voices named Junius.", "tension", 0.94, False),
    # 28 JUNE
    ("j1", "A woman says she saw him dancing in the forest.", "calm", 0.98, False),
    ("j2", "How did she see him? She does not know.", "reveal", 0.95, False),
    # 30 JUNE
    ("t1", "Friday, the thirtieth of June. The executioner comes.", "tension", 0.94, False),
    ("t2", "The court record says: he feels no pain in the thumbscrews.", "list", 0.97, False),
    ("t3", "His letter says: the blood ran out at my nails.", "tension", 0.93, True),
    ("t4", "The record says: he feels no pain in the leg screws.", "list", 0.97, False),
    ("t5", "His letter says: they hoisted me up, and let me fall. Eight times.", "tension", 0.93, True),
    ("t6", "I thought heaven and earth were ending.", "verdict", 0.9, True),
    # THE PLEA
    ("p1", "On the way back to his cell, the executioner begs him:", "calm", 0.97, False),
    ("p2", "For God's sake, confess something. Even if you bear it all, you will never get out.", "tension", 0.93, True),
    # THE LIE
    ("l1", "So he decides to lie.", "reveal", 0.95, False),
    ("l2", "In his letter he writes: Now follows my confession. Nothing but lies.", "reveal", 0.95, True),
    ("l3", "A goat. A coin that turns into a shard.", "list", 0.96, False),
    ("l4", "Then they want names.", "tension", 0.94, False),
    ("l5", "Street by street, they tell him.", "build", 0.98, False),
    ("l6", "So he walks his own city in his mind. The long street: eight names.", "build", 0.97, False),
    ("l7", "When he runs out, they give him a name. He repeats it.", "verdict", 0.95, False),
    # THE LETTER ENDS
    ("e1", "Hide this letter, he writes. If it is found, the guards will be beheaded.", "calm", 0.96, False),
    ("e2", "Swear for me that I am no witch, but a martyr.", "wonder", 0.92, True),
    ("e3", "Good night. For your father, Johannes Junius, will never see you more.", "verdict", 0.88, True),
    # CODA
    ("c1", "He was executed that August.", "verdict", 0.95, False),
    ("c2", "It probably never reached her. It ended up in his judges' files, which is why it survives.", "reveal", 0.96, False),
    ("c3", "Three years later, a Jesuit wrote: the force of torture brings forth witches who do not exist.", "verdict", 0.94, False),
]
LEX_ADD = {"junius": "jˈuːniʊs", "johannes": "joʊhˈɑːnəs", "veronica": "vɚɹˈɑːnɪkə", "thumbscrews": "θˈʌmskɹuːz",
           "bamberg": "bˈæmbɜːɡ", "jesuit": "dʒˈɛʒuːɪt"}
