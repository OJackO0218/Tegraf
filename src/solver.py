"""
Graph Vertex Coloring Solver for Sudoku.
Based on Graph Theory Lecture Week 10:
- Slide 7: Backtracking Algorithm (isSafeToColor + colorGraph)
- Slide 9: Degree / Saturation Ordering (MRV heuristic for constraint satisfaction)
"""

import time
from typing import Dict, List, Optional, Tuple
from .sudoku_graph import SudokuGraph


def is_safe_to_color(graph: SudokuGraph, vertex: int, color: int, colors: Dict[int, int]) -> bool:
    """
    Direct implementation of Slide 7: isSafeToColor(graph, verticesColor)
    Checks whether assigning 'color' to 'vertex' causes a conflict with any adjacent vertex.
    Returns:
        True if safe (no adjacent vertex shares the same color), False otherwise.
    """
    for neighbor in graph.get_neighbors(vertex):
        if colors.get(neighbor) == color:
            return False
    return True


def solve_sudoku_coloring(
    graph: SudokuGraph,
    initial_colors: Dict[int, int],
    use_mrv: bool = True
) -> Tuple[bool, Optional[Dict[int, int]], dict]:
    """
    Solves Sudoku as an exact 9-vertex coloring problem using recursive backtracking.
    
    Parameters:
        graph: SudokuGraph instance (81 vertices, 810 edges)
        initial_colors: Dict mapping vertex_id (0..80) to pre-assigned color (1..9)
        use_mrv: If True, uses Minimum Remaining Values (MRV / Degree of Saturation)
                 heuristic to pick the next most constrained vertex.
                 If False, uses sequential vertex scanning.

    Returns:
        (success: bool, solution: Dict[int, int], stats: dict)
    """
    # Verify initial clues for conflicts
    for v, c in initial_colors.items():
        for neighbor in graph.get_neighbors(v):
            if neighbor in initial_colors and initial_colors[neighbor] == c:
                return False, None, {
                    "error": f"Initial conflict detected between vertices {v} and {neighbor} both having color {c}",
                    "backtracks": 0,
                    "nodes_visited": 0,
                    "elapsed_ms": 0.0
                }

    colors = dict(initial_colors)
    unassigned = [v for v in range(graph.NUM_VERTICES) if v not in colors]
    
    stats = {
        "backtracks": 0,
        "nodes_visited": 0,
        "elapsed_ms": 0.0
    }

    start_time = time.perf_counter()

    def get_candidate_colors(v: int) -> List[int]:
        """Finds all valid colors (1..9) for vertex v given current partial coloring."""
        used = {colors[nbr] for nbr in graph.get_neighbors(v) if nbr in colors}
        return [c for c in range(1, 10) if c not in used]

    def select_next_vertex() -> Optional[int]:
        """
        Picks the next unassigned vertex:
        - If MRV is enabled: selects the vertex with the FEWEST legal color options
          (ties broken by highest unassigned neighbor degree).
        - If MRV is disabled: selects the first unassigned vertex.
        """
        if not unassigned:
            return None
        if not use_mrv:
            return unassigned[0]

        best_v = None
        min_options = 10
        for v in unassigned:
            options_count = len(get_candidate_colors(v))
            if options_count < min_options:
                min_options = options_count
                best_v = v
                if min_options == 0:
                    break
        return best_v

    def backtrack() -> bool:
        stats["nodes_visited"] += 1

        # Base case: All 81 vertices colored
        if len(colors) == graph.NUM_VERTICES:
            return True

        v = select_next_vertex()
        if v is None:
            return True

        candidates = get_candidate_colors(v)
        if not candidates:
            # Dead-end: Prune branch
            return False

        unassigned.remove(v)

        for color in candidates:
            # Slide 7: Assign option to verticesColor[currentVertex]
            colors[v] = color

            if backtrack():
                return True

            # Slide 7: Reset color of verticesColor[currentVertex] (backtrack)
            del colors[v]
            stats["backtracks"] += 1

        unassigned.append(v)
        return False

    success = backtrack()
    stats["elapsed_ms"] = (time.perf_counter() - start_time) * 1000.0

    if success:
        return True, colors, stats
    return False, None, stats
