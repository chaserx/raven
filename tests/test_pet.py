import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "raven_pet"))

import pet


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


if __name__ == "__main__":
    unittest.main()
