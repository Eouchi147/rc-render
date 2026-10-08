"""Bamberg, version 3: the plain telling. Short sentences, one idea each, full context, no irony.
Signature opening (every episode): "In [year], [the situation in one sentence]. Everything you're about to hear really happened."
Each line: list of phrases (text, delivery, pause after in seconds, lands). quote=True lines are his own words."""
DELIVERY = {      # (exaggeration, cfg weight: lower = slower and graver, temperature)
    'calm':   (0.40, 0.20, 0.68),   # clear, steady telling
    'grave':  (0.45, 0.17, 0.68),   # weight on the hard facts
    'firm':   (0.52, 0.24, 0.68),   # the line that has to land
    'letter': (0.55, 0.17, 0.72),   # his words, slower, closer
    'record': (0.32, 0.30, 0.65),   # the court record, flat
}
T, F = True, False
SCRIPT = [
    # THE OPENING (signature formula)
    ('o1', F, [("In 1628, a German mayor was arrested and accused of being a witch.", 'firm', 0.7, T)]),
    ('o2', F, [("In prison, he wrote a secret letter to his daughter.", 'calm', 0.8, T)]),
    ('o3', F, [("Everything you're about to hear really happened.", 'grave', 1.4, T)]),
    # CONTEXT
    ('x1', F, [("His name was Johannes Junius.", 'calm', 0.5, T), ("He lived in Bamberg, in Germany.", 'calm', 0.9, T)]),
    ('x2', F, [("At that time, many people believed that witches caused storms, sickness and failed harvests.", 'calm', 0.6, T),
               ("And the rulers of Bamberg decided to hunt them down.", 'grave', 1.0, T)]),
    ('x3', F, [("Their method was simple.", 'firm', 0.6, T), ("Arrest someone.", 'calm', 0.4, T),
               ("Torture them until they give names.", 'grave', 0.5, T), ("Then arrest those people.", 'firm', 1.0, T)]),
    ('x4', F, [("Junius's wife was named.", 'grave', 0.5, T), ("She was executed.", 'grave', 0.9, T)]),
    ('x5', F, [("Then six people named him.", 'firm', 1.1, T)]),
    # THE ACCUSATION
    ('a1', F, [("In court, a woman said she saw him dancing with witches in the forest.", 'calm', 0.6, T)]),
    ('a2', F, [("He asked her how she could have seen that.", 'calm', 0.6, T), ("She said: I don't know.", 'firm', 0.7, T)]),
    ('a3', F, [("The judges didn't care.", 'grave', 1.1, T)]),
    # THE TORTURE: two versions
    ('t1', F, [("Two days later, they tortured him.", 'grave', 0.8, T)]),
    ('t2', F, [("The court wrote down that he felt no pain.", 'record', 0.9, T)]),
    ('t3', T, [("In his letter, he wrote something very different.", 'calm', 0.6, T),
               ("They crushed his thumbs until blood came out from under his nails.", 'letter', 0.6, T)]),
    ('t4', T, [("They tied his hands behind his back,", 'letter', 0.3, F), ("pulled him up by a rope,", 'letter', 0.3, F),
               ("and dropped him.", 'grave', 0.8, T), ("Eight times.", 'grave', 1.4, T)]),
    # THE TURN
    ('k1', F, [("Then something strange happened.", 'firm', 0.7, T)]),
    ('k2', F, [("The executioner, the man who had just tortured him, begged him:", 'calm', 0.5, F)]),
    ('k3', T, [("Confess to something.", 'letter', 0.4, T), ("True or not.", 'letter', 0.5, T),
               ("If you don't, they will never stop.", 'grave', 1.1, T)]),
    # THE LIE
    ('l1', F, [("So Junius lied.", 'firm', 0.6, T), ("He made up a story about meeting the devil.", 'calm', 0.8, T)]),
    ('l2', F, [("Then they wanted names.", 'firm', 0.6, T)]),
    ('l3', F, [("They made him walk through his own town in his mind, street by street, and name people.", 'calm', 0.7, T)]),
    ('l4', F, [("When he couldn't think of anyone, they gave him a name.", 'calm', 0.5, T), ("And he repeated it.", 'grave', 1.2, T)]),
    # THE LETTER
    ('e1', F, [("He wrote all of this to his daughter, Veronica,", 'calm', 0.3, F), ("over several days,", 'calm', 0.3, F),
               ("with hands that barely worked.", 'grave', 0.8, T)]),
    ('e2', F, [("He asked her to hide the letter.", 'calm', 0.6, T)]),
    ('e3', T, [("He wrote: I am innocent.", 'letter', 0.8, T)]),
    ('e4', T, [("And he ended with: Good night.", 'letter', 0.6, T), ("Your father will never see you again.", 'letter', 1.5, T)]),
    # THE END
    ('f1', F, [("That August, Johannes Junius was executed.", 'grave', 1.2, T)]),
    ('f2', F, [("His letter probably never reached his daughter.", 'calm', 0.6, T), ("The court kept it in his file.", 'calm', 0.7, T)]),
    ('f3', F, [("And that is why, almost four hundred years later,", 'calm', 0.3, F), ("we can still read it.", 'firm', 1.5, T)]),
]
DIRECTED = {lid: ph for lid, q, ph in SCRIPT}
QUOTE = {lid: q for lid, q, ph in SCRIPT}
LINES = [(lid, ' '.join(p[0] for p in ph), '', 1.0, q) for lid, q, ph in SCRIPT]
SAY = {}
