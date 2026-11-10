"""
Automated unit tests for Sudoku Graph Coloring Solver.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.sudoku_graph import SudokuGraph
from src.solver import solve_sudoku_coloring, is_safe_to_color
from src.utils import parse_sudoku_string, verify_chromatic_validity


class TestSudokuGraphColoring(unittest.TestCase):

    def setUp(self):
        self.graph = SudokuGraph()

    def test_graph_structure(self):
        """Validates that G is a 20-regular graph with 81 vertices and 810 edges."""
        self.assertEqual(self.graph.NUM_VERTICES, 81)
        self.assertEqual(self.graph.total_edges, 810)

        # Every vertex must have degree 20
        for v in range(81):
            self.assertEqual(
                len(self.graph.get_neighbors(v)), 20,
                f"Vertex {v} does not have degree 20"
            )

    def test_slide18_sample(self):
        """Tests the exact Sudoku sample from Week 10 Slide 18."""
        sample_str = (
            "000000010"
            "002000034"
            "000051000"
            "000006500"
            "070300080"
            "003000000"
            "000080000"
            "580000900"
            "690000000"
        )
        clues = parse_sudoku_string(sample_str)
        success, solution, stats = solve_sudoku_coloring(self.graph, clues, use_mrv=True)
        self.assertTrue(success, "Solver failed to find 9-coloring for Slide 18 sample.")

        is_valid, msg = verify_chromatic_validity(self.graph, solution)
        self.assertTrue(is_valid, msg)

    def test_immediate_conflict(self):
        """Verifies that duplicate colors on adjacent vertices are rejected immediately."""
        # Two 5s in the first row (vertices 0 and 1)
        invalid_str = "55" + "0" * 79
        clues = parse_sudoku_string(invalid_str)
        success, solution, stats = solve_sudoku_coloring(self.graph, clues)
        self.assertFalse(success)
        self.assertIn("error", stats)

    def test_chromatic_invariance(self):
        """Confirms that chromatic number is exactly 9 and all 9 colors are used."""
        sample_str = (
            "000260701"
            "680070090"
            "190004500"
            "820100040"
            "004602900"
            "050003028"
            "009300074"
            "040050036"
            "703018000"
        )
        clues = parse_sudoku_string(sample_str)
        success, solution, _ = solve_sudoku_coloring(self.graph, clues)
        self.assertTrue(success)
        colors_used = set(solution.values())
        self.assertEqual(colors_used, set(range(1, 10)))


if __name__ == "__main__":
    unittest.main()
