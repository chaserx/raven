MAX_LEVEL = 3
TRAINS_PER_LEVEL = 3
MAX_TRAININGS = TRAINS_PER_LEVEL * (MAX_LEVEL - 1)

FULL = 100
SAD_BELOW = 40
SAD_AFTER_S = 90 * 60  # a freshly fed raven looks sad after 90 minutes of running
DECAY_PER_S = (FULL - SAD_BELOW) / SAD_AFTER_S


class Pet:
    def __init__(self, fullness=FULL, trainings=0):
        self.fullness = fullness
        self.trainings = trainings

    @property
    def level(self):
        return 1 + self.trainings // TRAINS_PER_LEVEL

    @property
    def progress(self):
        # training presses banked towards the next level
        return self.trainings % TRAINS_PER_LEVEL

    def is_sad(self):
        return self.fullness < SAD_BELOW

    def tick(self, seconds):
        self.fullness = max(0, self.fullness - DECAY_PER_S * seconds)

    def feed(self):
        self.fullness = FULL

    def train(self):
        # returns "maxed" once there's nothing left to learn, "level_up" when
        # this press completes a level, otherwise "trained"
        if self.trainings >= MAX_TRAININGS:
            return "maxed"
        self.trainings += 1
        return "level_up" if self.trainings % TRAINS_PER_LEVEL == 0 else "trained"

    def save(self):
        return {"fullness": int(self.fullness), "trainings": self.trainings}

    def load(self, state):
        self.fullness = max(0, min(FULL, state["fullness"]))
        self.trainings = max(0, min(MAX_TRAININGS, state["trainings"]))
