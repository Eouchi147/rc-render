"""The keeper's directed reading of the Bamberg script, phrase by phrase, as a voice actor's marked script.
Each phrase: (text, delivery, pause after in seconds, lands). lands=True: the phrase must land (pitch falls at the
end); False: it stays suspended into what follows. The phrases of a line join to the line's caption text."""
# delivery -> (Chatterbox exaggeration, cfg weight: lower is slower and weightier, temperature)
DELIVERY = {
    'hook':    (0.55, 0.30, 0.72),   # leaning in, intrigued
    'low':     (0.40, 0.28, 0.70),   # confiding, matter-of-fact
    'punch':   (0.60, 0.34, 0.70),   # the line that lands: firm, final
    'wry':     (0.50, 0.32, 0.72),   # a raised eyebrow
    'build':   (0.50, 0.34, 0.70),   # momentum
    'cold':    (0.30, 0.42, 0.65),   # the court record: flat, clerical
    'letter':  (0.62, 0.22, 0.74),   # his own words: heavier, slower
    'break':   (0.75, 0.20, 0.75),   # his words where the voice nearly goes
    'verdict': (0.45, 0.20, 0.68),   # slow, quiet, final
}
T, F = True, False
DIRECTED = {
    'h1': [("Come closer.", 'hook', 0.7, T), ("This shelf holds a letter", 'low', 0.15, F), ("that was never supposed to exist.", 'punch', 0.9, T)],
    'h2': [("Two documents describe the same week, in 1628.", 'low', 0.5, T), ("One was written by his judges.", 'punch', 0.6, T)],
    'h3': [("The other, in secret, by him.", 'low', 0.7, T), ("They do not agree.", 'punch', 1.0, T)],
    'h4': [("His name is Johannes Junius.", 'low', 0.45, T), ("He's in a cell,", 'low', 0.2, F), ("and his hands are wrecked.", 'punch', 0.5, T)],
    'q1': [("He writes to his daughter:", 'low', 0.5, F), ("A hundred thousand good nights,", 'letter', 0.3, F), ("my dearest Veronica.", 'letter', 0.8, T)],
    'q2': [("Innocent I came into prison.", 'letter', 0.55, T), ("Innocent I was tortured.", 'letter', 0.6, T), ("Innocent I must die.", 'break', 0.6, T)],
    'w1': [("Bamberg, Germany.", 'low', 0.4, T), ("Fifty-five years old.", 'low', 0.3, T), ("Four times mayor.", 'punch', 0.6, T)],
    'w2': [("Now he's locked in a new prison,", 'low', 0.2, F), ("built for one thing: witches.", 'punch', 0.7, T)],
    'w3': [("The system is simple:", 'wry', 0.35, F), ("torture people until they give names.", 'build', 0.4, T), ("Then torture those people.", 'punch', 0.7, T)],
    'w4': [("His wife was named.", 'low', 0.6, T), ("She was executed before him.", 'verdict', 0.8, T)],
    'w5': [("Then six people named Junius.", 'punch', 0.9, T)],
    'j1': [("A witness swears she saw him at a witches' dance in the forest.", 'low', 0.6, T)],
    'j2': [("He asks her: how did you see me?", 'low', 0.6, F), ("She says: I don't know.", 'wry', 0.9, T)],
    't1': [("Two days later,", 'low', 0.3, F), ("the executioner comes for him.", 'verdict', 1.0, T)],
    't2': [("Here the two documents split.", 'punch', 0.6, T), ("The court record: he feels no pain in the thumbscrews.", 'cold', 0.7, T)],
    't3': [("His letter: they crushed my thumbs until blood ran out of my nails.", 'letter', 0.8, T)],
    't4': [("The record: no pain in the leg screws either.", 'cold', 0.7, T)],
    't5': [("His letter: they tied my hands behind my back,", 'letter', 0.2, F), ("hauled me up on a rope,", 'letter', 0.25, F),
           ("and let me fall.", 'break', 0.9, T), ("Eight times.", 'break', 1.4, T)],
    't6': [("I thought heaven and earth were ending.", 'break', 1.0, T)],
    'p1': [("Then the strangest part.", 'wry', 0.6, T), ("On the way back, the executioner begs him:", 'build', 0.5, F)],
    'p2': [("For God's sake, confess something.", 'letter', 0.35, T), ("True or not.", 'letter', 0.5, T), ("You will never get out anyway.", 'verdict', 0.6, T)],
    'l1': [("So Junius does the only thing left.", 'low', 0.6, T), ("He lies.", 'punch', 0.9, T)],
    'l2': [("His letter marks the exact spot:", 'wry', 0.4, F), ("Now follows my confession.", 'letter', 0.5, T), ("Nothing but lies.", 'punch', 0.9, T)],
    'l3': [("He says the devil came as a goat,", 'wry', 0.25, F), ("and paid him a gold coin that turned to pottery.", 'wry', 0.8, T)],
    'l4': [("A story isn't enough.", 'low', 0.45, T), ("They want names.", 'punch', 0.8, T)],
    'l5': [("Go through the city, they tell him.", 'build', 0.4, T), ("Street by street.", 'punch', 0.7, T)],
    'l6': [("In his head, he walks his own town.", 'low', 0.5, T), ("One street alone: eight names.", 'punch', 0.8, T)],
    'l7': [("When he runs out, they hand him a name.", 'low', 0.45, T), ("And he says it back.", 'verdict', 1.0, T)],
    'e1': [("The letter has to be smuggled out.", 'build', 0.45, T), ("If it's found, the guards lose their heads.", 'low', 0.8, T)],
    'e2': [("And he asks one thing:", 'low', 0.45, F), ("Swear that I am no witch,", 'letter', 0.3, F), ("but a martyr.", 'letter', 0.9, T)],
    'e3': [("Good night.", 'break', 0.7, T), ("For your father, Johannes Junius,", 'break', 0.3, F), ("will never see you again.", 'break', 1.4, T)],
    'c1': [("That August, Junius was executed.", 'verdict', 1.0, T)],
    'c2': [("And the letter?", 'wry', 0.5, F), ("It probably never reached her.", 'low', 0.45, T), ("The judges filed it away.", 'low', 0.4, T),
           ("That's why it survived.", 'punch', 0.9, T)],
    'c3': [("Three years later, a priest put it in one line:", 'low', 0.5, F), ("torture creates witches who do not exist.", 'verdict', 1.2, T)],
    'c4': [("Back on the shelf.", 'low', 0.6, T), ("Next: a ship's insurance claim, from 1781.", 'hook', 0.5, T), ("It's worse than it sounds.", 'wry', 0.5, T)],
}
# what the voice is given where the written form reads badly (captions keep the written form)
SAY = {"Fifty-five years old.": "Fifty five years old."}
# extra spellings tried for phrases the voice tends to garble; the recogniser picks the clean one
ALT = {}
