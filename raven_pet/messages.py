# (tier, text). tier is the raven level needed to send it. keep to plain ASCII,
# and keep each tier within its length limit so the QR code stays scannable on
# the badge screen (see tests/test_pet.py).
MESSAGES = [
    (1, "Winter is coming."),
    (1, "The North remembers."),
    (1, "Valar morghulis."),
    (1, "All bugs must die."),
    (1, "A raven sends its regards."),
    (2, "A Maester of Engineering sends word."),
    (2, "Hold the door. Ship the fix."),
    (2, "The realm needs a hotfix by dawn."),
    (2, "Fear cuts deeper than swords. So do bugs."),
    (3, "The night is dark and full of terrors, and failing builds."),
    (3, "Seven kingdoms, one repository, and no tests. Winter is here."),
    (3, "By order of the Maester: deploy on Friday and face the Wall."),
    (3, "A raven flew all night to tell you: your PR needs a review."),
]
