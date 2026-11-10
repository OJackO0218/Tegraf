import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.timetabling import TimetableGraph, solve_timetabling, parse_timetabling_file


class TestTimetabling(unittest.TestCase):
    def test_slide19_case(self):
        filepath = os.path.join(os.path.dirname(__file__), "..", "inputs", "timetabling_slide19.txt")
        tg = parse_timetabling_file(filepath)
        self.assertEqual(tg.total_sessions, 11)
        self.assertEqual(tg.theoretical_min_slots(), 4)

        colors, slots = solve_timetabling(tg)
        self.assertEqual(slots, 4)

        for u in range(tg.total_sessions):
            for v in tg.adj[u]:
                self.assertNotEqual(colors[u], colors[v])


if __name__ == "__main__":
    unittest.main()
