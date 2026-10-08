"""Dark Corners, episode 1: A Hundred Thousand Good Nights (Bamberg, 1628). Narration script.
Each line: (id, text, direction, pace). Letter quotes are marked q=True (voiced a touch slower and closer).
Sources: Junius's letter of 24 July 1628 (Staatsbibliothek Bamberg RB.Msc.148/300, text after Leitschuh 1883 / Bauer 1911),
the trial record (Burr 1896), Spee, Cautio Criminalis (1631), Dubium XLIX. See claude/dark-research-bamberg.md."""
LINES = [
    # THE CABINET: the keeper takes the object from the shelf (hook and open question)
    ("h1", "Come closer. This shelf holds a letter that was never supposed to exist.", "intrigue", 0.97, False),
    ("h2", "Two documents describe the same week, in 1628. One was written by his judges.", "intrigue", 0.97, False),
    ("h3", "The other, in secret, by him. They do not agree.", "intrigue", 0.95, False),
    ("h4", "His name is Johannes Junius. He's in a cell, and his hands are wrecked.", "calm", 0.97, False),
    ("q1", "He writes to his daughter: A hundred thousand good nights, my dearest Veronica.", "wonder", 0.9, True),
    ("q2", "Innocent I came into prison. Innocent I was tortured. Innocent I must die.", "tension", 0.9, True),
    # WORLD
    ("w1", "Bamberg, Germany. Fifty-five years old. Four times mayor.", "calm", 0.98, False),
    ("w2", "Now he's locked in the city's new prison, built for one thing: witches.", "calm", 0.96, False),
    ("w3", "The system is simple: torture people until they give names. Then torture those people.", "build", 0.98, False),
    ("w4", "His wife was named. She was executed before him.", "calm", 0.95, False),
    ("w5", "Then six people named Junius.", "tension", 0.94, False),
    # 28 JUNE
    ("j1", "One witness swears she saw him dancing at a witches' gathering in the forest.", "calm", 0.98, False),
    ("j2", "He asks her: how did you see me? She says: I don't know. He begs the judges to question her properly. They refuse.", "reveal", 0.95, False),
    # 30 JUNE
    ("t1", "Two days later, the executioner comes for him.", "tension", 0.94, False),
    ("t2", "Here the two documents split. The court record: he feels no pain in the thumbscrews.", "list", 0.97, False),
    ("t3", "His letter: they crushed my thumbs until blood ran out of my nails.", "tension", 0.93, True),
    ("t4", "The record: no pain in the leg screws either.", "list", 0.97, False),
    ("t5", "His letter: they tied my hands behind my back, hauled me up on a rope, and let me fall. Eight times.", "tension", 0.93, True),
    ("t6", "I thought heaven and earth were ending.", "verdict", 0.9, True),
    # THE PLEA
    ("p1", "Then the strangest part. Walking him back to his cell, the executioner begs him:", "calm", 0.97, False),
    ("p2", "For God's sake, confess something. True or not. You will never get out anyway.", "tension", 0.93, True),
    # THE LIE
    ("l1", "So Junius does the only thing left. He lies.", "reveal", 0.95, False),
    ("l2", "His letter even marks the exact spot: Now follows my confession. Nothing but lies.", "reveal", 0.95, True),
    ("l3", "He says the devil came to him as a goat, and paid him a gold coin that turned to pottery.", "list", 0.96, False),
    ("l4", "A story isn't enough. They want names.", "tension", 0.94, False),
    ("l5", "Go through the city, they tell him. Street by street.", "build", 0.98, False),
    ("l6", "In his head, he walks his own town. One street alone: eight names.", "build", 0.97, False),
    ("l7", "When he runs out, they hand him a name. And he says it back.", "verdict", 0.95, False),
    # THE LETTER ENDS
    ("e1", "Now the letter has to get out. If it's found, the guards who helped lose their heads.", "calm", 0.96, False),
    ("e2", "And he asks one thing: Swear that I am no witch, but a martyr.", "wonder", 0.92, True),
    ("e3", "Good night. For your father, Johannes Junius, will never see you again.", "verdict", 0.88, True),
    # CODA, and the object goes back on the shelf
    ("c1", "That August, Junius was executed.", "verdict", 0.95, False),
    ("c2", "And the letter? It probably never reached her. The judges filed it with his case. That's why it survived.", "reveal", 0.96, False),
    ("c3", "Three years later, a priest wrote it in one line, in a book he didn't dare sign: torture creates witches who do not exist.", "verdict", 0.94, False),
    ("c4", "Back on the shelf. Next object: a ship's insurance claim from 1781. It's worse than it sounds.", "intrigue", 0.97, False),
]
LEX_ADD = {"junius": "jˈuːniʊs", "johannes": "joʊhˈɑːnəs", "veronica": "vɚɹˈɑːnɪkə", "thumbscrews": "θˈʌmskɹuːz",
           "bamberg": "bˈæmbɜːɡ", "jesuit": "dʒˈɛʒuːɪt"}
