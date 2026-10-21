import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "raven_pet"))

import pet
from messages import MESSAGES

TIER_LIMITS = {1: 30, 2: 45, 3: 70}


class PetTest(unittest.TestCase):
    def test_starts_full_untrained_and_happy(self):
        p = pet.Pet()
        self.assertEqual(p.fullness, pet.FULL)
        self.assertEqual(p.level, 1)
        self.assertFalse(p.is_sad())

    def test_not_sad_just_before_ninety_minutes(self):
        p = pet.Pet()
        p.tick(pet.SAD_AFTER_S - 1)
        self.assertFalse(p.is_sad())

    def test_sad_after_ninety_minutes(self):
        p = pet.Pet()
        p.tick(pet.SAD_AFTER_S + 1)
        self.assertTrue(p.is_sad())

    def test_hunger_never_goes_below_zero(self):
        p = pet.Pet()
        p.tick(10 ** 7)
        self.assertEqual(p.fullness, 0)

    def test_feeding_makes_a_sad_raven_happy_again(self):
        p = pet.Pet()
        p.tick(10 ** 7)
        p.feed()
        self.assertEqual(p.fullness, pet.FULL)
        self.assertFalse(p.is_sad())

    def test_three_trainings_make_a_level(self):
        p = pet.Pet()
        self.assertEqual(p.train(), "trained")
        self.assertEqual(p.train(), "trained")
        self.assertEqual(p.progress, 2)
        self.assertEqual(p.train(), "level_up")
        self.assertEqual(p.level, 2)
        self.assertEqual(p.progress, 0)

    def test_top_level_is_reached_in_six_presses_and_stays_there(self):
        p = pet.Pet()
        results = [p.train() for _ in range(6)]
        self.assertEqual(results.count("level_up"), 2)
        self.assertEqual(p.level, pet.MAX_LEVEL)
        self.assertEqual(p.train(), "maxed")
        self.assertEqual(p.level, pet.MAX_LEVEL)
        self.assertEqual(p.trainings, pet.MAX_TRAININGS)

    def test_save_and_load_round_trip(self):
        p = pet.Pet()
        p.tick(1000)
        p.train()
        p.train()
        q = pet.Pet()
        q.load(p.save())
        self.assertEqual(q.trainings, 2)
        self.assertEqual(q.fullness, int(p.fullness))

    def test_load_clamps_corrupt_state(self):
        p = pet.Pet()
        p.load({"fullness": 900, "trainings": 99})
        self.assertEqual(p.fullness, pet.FULL)
        self.assertEqual(p.trainings, pet.MAX_TRAININGS)
        p.load({"fullness": -5, "trainings": -1})
        self.assertEqual(p.fullness, 0)
        self.assertEqual(p.trainings, 0)


class MessageTest(unittest.TestCase):
    def test_every_tier_has_messages(self):
        for tier in TIER_LIMITS:
            self.assertTrue([m for t, m in MESSAGES if t == tier], tier)

    def test_messages_fit_their_tier_and_are_ascii(self):
        for tier, text in MESSAGES:
            self.assertLessEqual(len(text), TIER_LIMITS[tier], text)
            text.encode("ascii")

    def test_lower_levels_only_send_messages_they_have_earned(self):
        for level in (1, 2, 3):
            for pick in range(len(MESSAGES)):
                index = pet.pick_message(MESSAGES, level, lambda n, pick=pick: pick % n)
                self.assertLessEqual(MESSAGES[index][0], level)

    def test_top_level_can_send_every_message(self):
        seen = {pet.pick_message(MESSAGES, 3, lambda n, k=k: k % n)
                for k in range(len(MESSAGES))}
        self.assertEqual(seen, set(range(len(MESSAGES))))


if __name__ == "__main__":
    unittest.main()
