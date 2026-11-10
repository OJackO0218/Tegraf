#!/usr/bin/env python3
"""
Main CLI entrypoint for Tegraf - Graph Coloring Algorithms.
Includes:
1. Sudoku Solver via Vertex Coloring (Week 10 Slide 18)
2. Timetabling Problem via Graph Coloring (Week 10 Slide 19)
Department of Informatics, Institut Teknologi Sepuluh Nopember (ITS).
"""

import os
import sys
import argparse
from src.sudoku_graph import SudokuGraph
from src.solver import solve_sudoku_coloring
from src.utils import (
    parse_sudoku_file,
    parse_sudoku_string,
    format_grid,
    verify_chromatic_validity
)
from src.timetabling import (
    parse_timetabling_file,
    solve_timetabling,
    format_timetable_schedule
)


def run_sudoku_file(filepath: str, graph: SudokuGraph):
    clues = parse_sudoku_file(filepath)
    name = os.path.basename(filepath)
    print("=" * 65)
    print(f"SUDOKU GRAPH COLORING: {name}")
    print("=" * 65)
    print(f"Graph Properties: |V| = {graph.NUM_VERTICES}, |E| = {graph.total_edges}, 20-regular")
    print(f"Pre-colored: {len(clues)} / 81 vertices")
    print("Initial Board:")
    print(format_grid(clues))
    print("Solving with recursive backtracking & MRV...")
    success, solution, stats = solve_sudoku_coloring(graph, clues, use_mrv=True)
    if not success:
        print(f"Failed: {stats.get('error', 'No valid coloring found')}\n")
        return False
    print("Solved Proper 9-Coloring:")
    print(format_grid(solution))
    is_valid, msg = verify_chromatic_validity(graph, solution)
    print(f"Validation: {msg}")
    print(f"Elapsed: {stats['elapsed_ms']:.2f} ms | Backtracks: {stats['backtracks']:,}\n")
    return True


def run_timetabling_file(filepath: str):
    from src.timetabling import format_input_matrix

    tg = parse_timetabling_file(filepath)
    name = os.path.basename(filepath)
    print("=" * 65)
    print(f"TIMETABLING PROBLEM COLORING: {name}")
    print("=" * 65)
    print("Input Matrix A (Slide 19 Teaching Requirements):")
    print(format_input_matrix(tg))
    print("-" * 65)
    print(f"Conflict Graph: |V| = {tg.total_sessions} sessions, |E| = {tg.total_edges} constraints")
    theo_min = tg.theoretical_min_slots()
    print(f"Theoretical Lower Bound (Delta(G) via Konig's Theorem): {theo_min} time slots")
    colors, slots_used = solve_timetabling(tg)
    print(f"Assigned Time Slots: {slots_used}")
    print("-" * 65)
    print(format_timetable_schedule(tg, colors))
    print("-" * 65)
    print(f"Status: {'OPTIMAL' if slots_used == theo_min else 'VALID'}\n")
    return True


def run_all(graph: SudokuGraph):
    inputs_dir = os.path.join(os.path.dirname(__file__), "inputs")
    print("\n--- RUNNING ALL BENCHMARKS ---\n")
    sudoku_files = [
        "slide18_sample.txt",
        "easy_sample.txt",
        "medium_sample.txt",
        "hard_sample.txt",
        "invalid_conflict.txt"
    ]
    print("[1] Sudoku Benchmarks:")
    for sf in sudoku_files:
        p = os.path.join(inputs_dir, sf)
        if os.path.exists(p):
            try:
                run_sudoku_file(p, graph)
            except Exception as e:
                print(f"Error {sf}: {e}\n")

    timetable_files = ["timetabling_slide19.txt", "timetabling_sample2.txt"]
    print("[2] Timetabling Benchmarks:")
    for tf in timetable_files:
        p = os.path.join(inputs_dir, tf)
        if os.path.exists(p):
            run_timetabling_file(p)


def main():
    parser = argparse.ArgumentParser(description="Tegraf: Sudoku & Timetabling Graph Coloring.")
    parser.add_argument("mode", nargs="?", choices=["sudoku", "timetabling", "all"], default="all")
    parser.add_argument("file", nargs="?", default=None)
    args = parser.parse_args()

    graph = SudokuGraph()
    inputs_dir = os.path.join(os.path.dirname(__file__), "inputs")

    if args.mode == "sudoku":
        f = args.file if args.file else os.path.join(inputs_dir, "slide18_sample.txt")
        run_sudoku_file(f, graph)
    elif args.mode == "timetabling":
        f = args.file if args.file else os.path.join(inputs_dir, "timetabling_slide19.txt")
        run_timetabling_file(f)
    else:
        run_all(graph)


if __name__ == "__main__":
    main()
