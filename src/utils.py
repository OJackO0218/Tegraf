"""
Utility functions for file I/O, parsing, ASCII grid rendering,
and formal Graph Theory verification.
"""

from typing import Dict, Tuple
from .sudoku_graph import SudokuGraph


def parse_sudoku_file(filepath: str) -> Dict[int, int]:
    """
    Parses a Sudoku puzzle from a text file into a dictionary of initial colors:
    {vertex_idx: color (1..9)}

    Accepts:
    - 9 lines of 9 numbers (space-separated, comma-separated, or contiguous digits)
    - 0 or . indicates an unassigned vertex.
    """
    initial_colors = {}
    digits = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Extract valid tokens
            for char in line:
                if char.isdigit():
                    digits.append(int(char))
                elif char in (".", "-"):
                    digits.append(0)

    if len(digits) != 81:
        raise ValueError(f"Invalid input: expected 81 cells, found {len(digits)} in {filepath}")

    for idx, val in enumerate(digits):
        if 1 <= val <= 9:
            initial_colors[idx] = val

    return initial_colors


def parse_sudoku_string(grid_str: str) -> Dict[int, int]:
    """Parses a raw 81-character string or multiline grid."""
    digits = []
    for char in grid_str:
        if char.isdigit():
            digits.append(int(char))
        elif char in (".", "-"):
            digits.append(0)

    if len(digits) != 81:
        raise ValueError(f"Invalid grid string: expected 81 cells, found {len(digits)}")

    return {idx: val for idx, val in enumerate(digits) if 1 <= val <= 9}


def format_grid(colors: Dict[int, int], highlight_original: Dict[int, int] = None) -> str:
    """
    Renders an 81-cell coloring as an aesthetic ASCII Sudoku grid.
    Distinguishes 3x3 blocks with box-drawing borders.
    """
    lines = []
    horizontal_border = "+-------+-------+-------+"

    for r in range(9):
        if r % 3 == 0:
            lines.append(horizontal_border)

        row_parts = []
        for c in range(9):
            idx = r * 9 + c
            val = colors.get(idx, 0)
            char_repr = str(val) if val > 0 else "."
            row_parts.append(char_repr)

        # Format into 3 blocks of 3
        b1 = " ".join(row_parts[0:3])
        b2 = " ".join(row_parts[3:6])
        b3 = " ".join(row_parts[6:9])
        lines.append(f"| {b1} | {b2} | {b3} |")

    lines.append(horizontal_border)
    return "\n".join(lines)


def verify_chromatic_validity(graph: SudokuGraph, colors: Dict[int, int]) -> Tuple[bool, str]:
    """
    Performs formal verification that:
    1. Every vertex v in V is assigned a color in {1..9}.
    2. For every edge (u, v) in E, color(u) != color(v).
    3. Chromatic number chi(G) = 9 is achieved.
    """
    if len(colors) != graph.NUM_VERTICES:
        return False, f"Incomplete coloring: only {len(colors)}/81 vertices assigned."

    distinct_colors = set(colors.values())
    if not distinct_colors.issubset(set(range(1, 10))):
        return False, f"Invalid color palette used: {distinct_colors}"

    # Verify edge constraints
    conflicts = 0
    for u in range(graph.NUM_VERTICES):
        c_u = colors[u]
        for v in graph.get_neighbors(u):
            if u < v and colors[v] == c_u:
                conflicts += 1

    if conflicts > 0:
        return False, f"Edge violation: found {conflicts} monochromatic edges."

    return True, f"Valid proper 9-coloring verified! |V| = 81, |E| = 810, chi(G) = {len(distinct_colors)}."
