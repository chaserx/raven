import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "raven"))

import flight


class FlightTest(unittest.TestCase):
    def test_enters_from_left_edge_facing_right(self):
        x, _, flipped, _ = flight.flight(0)
        self.assertEqual(x, -flight.SPRITE_W)
        self.assertFalse(flipped)

    def test_leaves_through_right_edge(self):
        x, _, flipped, _ = flight.flight(flight.CROSS_MS - 1)
        self.assertGreater(x, flight.SCREEN_W - 1)
        self.assertFalse(flipped)

    def test_out_of_sight_while_away(self):
        for t in (flight.CROSS_MS, flight.CROSS_MS + flight.AWAY_MS // 2,
                  flight.CROSS_MS + flight.AWAY_MS - 1):
            self.assertIsNone(flight.flight(t))

    def test_returns_from_the_same_right_edge_facing_left(self):
        x, _, flipped, _ = flight.flight(flight.CROSS_MS + flight.AWAY_MS)
        self.assertEqual(x, flight.SCREEN_W)
        self.assertTrue(flipped)

    def test_gone_after_round_trip(self):
        self.assertIsNone(flight.flight(flight.TOTAL_MS))
        self.assertIsNone(flight.flight(flight.TOTAL_MS + 5000))

    def test_not_started(self):
        self.assertIsNone(flight.flight(-1))

    def test_flap_frames_stay_within_the_sheet(self):
        for t in range(0, flight.CROSS_MS, 7):
            self.assertIn(flight.flight(t)[3], range(4))

    def test_raven_stays_on_screen_vertically(self):
        for t in range(0, flight.TOTAL_MS, 13):
            pos = flight.flight(t)
            if pos:
                self.assertTrue(0 <= pos[1] <= 120 - 24)


if __name__ == "__main__":
    unittest.main()
