"""
Sudoku and Timetabling Graph Coloring Package.
"""

from .sudoku_graph import SudokuGraph
from .solver import solve_sudoku_coloring, is_safe_to_color
from .utils import (
    parse_sudoku_file,
    parse_sudoku_string,
    format_grid,
    verify_chromatic_validity
)
from .timetabling import (
    TimetableGraph,
    solve_timetabling,
    parse_timetabling_file,
    format_input_matrix,
    format_timetable_matrix,
    format_slot_decomposition,
    format_timetable_schedule
)

__all__ = [
    "SudokuGraph",
    "solve_sudoku_coloring",
    "is_safe_to_color",
    "parse_sudoku_file",
    "parse_sudoku_string",
    "format_grid",
    "verify_chromatic_validity",
    "TimetableGraph",
    "solve_timetabling",
    "parse_timetabling_file",
    "format_input_matrix",
    "format_timetable_matrix",
    "format_slot_decomposition",
    "format_timetable_schedule"
]
