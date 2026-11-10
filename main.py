#!/usr/bin/env python3
"""
Main CLI entrypoint for Tegraf - Sudoku Solver via Graph Vertex Coloring.
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


def solve_and_display(filepath_or_name: str, initial_colors: dict, graph: SudokuGraph):
    print("=" * 65)
    print(f"🧩 ANALYZING SUDOKU GRAPH: {filepath_or_name}")
    print("=" * 65)
    print(f"Graph Properties:")
    print(f"  • Vertices (|V|) : {graph.NUM_VERTICES} cells")
    print(f"  • Edges    (|E|) : {graph.total_edges} constraints (20-regular graph)")
    print(f"  • Pre-colored    : {len(initial_colors)} / 81 vertices fixed by clues")
    print(f"  • Chromatic Goal : Proper 9-coloring (\\chi(G) = 9)")
    print("-" * 65)
    print("INITIAL GRAPH STATE:")
    print(format_grid(initial_colors))
    print("-" * 65)

    print("Running Backtracking Vertex Coloring with MRV/Saturation Heuristic...")
    success, solution, stats = solve_sudoku_coloring(graph, initial_colors, use_mrv=True)

    if not success:
        print("❌ COLORING FAILED!")
        error_msg = stats.get("error", "No valid 9-coloring exists for this graph configuration.")
        print(f"Reason: {error_msg}")
        print("=" * 65 + "\n")
        return False

    print("✅ PROPER 9-COLORING FOUND!")
    print(format_grid(solution))
    print("-" * 65)

    # Formal Graph Theory Verification
    is_valid, msg = verify_chromatic_validity(graph, solution)
    print(f"Graph Theory Verification: {msg}")
    print(f"Performance Metrics:")
    print(f"  • Time Elapsed : {stats['elapsed_ms']:.2f} ms")
    print(f"  • Nodes Visited: {stats['nodes_visited']:,}")
    print(f"  • Backtracks   : {stats['backtracks']:,}")
    print("=" * 65 + "\n")
    return True


def run_all_samples(graph: SudokuGraph):
    inputs_dir = os.path.join(os.path.dirname(__file__), "inputs")
    if not os.path.exists(inputs_dir):
        print(f"[!] Inputs directory not found: {inputs_dir}")
        return

    sample_files = sorted([f for f in os.listdir(inputs_dir) if f.endswith(".txt")])
    print(f"\n🚀 Running all {len(sample_files)} benchmark sample inputs...\n")

    results = []
    for f in sample_files:
        path = os.path.join(inputs_dir, f)
        try:
            clues = parse_sudoku_file(path)
            res = solve_and_display(f, clues, graph)
            results.append((f, "SOLVED" if res else "FAILED/CONFLICT"))
        except Exception as e:
            print(f"[!] Error processing {f}: {e}\n")
            results.append((f, f"ERROR: {e}"))

    print("\n" + "=" * 50)
    print("BENCHMARK SUMMARY")
    print("=" * 50)
    for name, status in results:
        print(f"{name:<30} : {status}")
    print("=" * 50 + "\n")


def run_interactive(graph: SudokuGraph):
    print("\n--- Interactive Sudoku Graph Coloring Mode ---")
    print("Enter the 9 rows of the Sudoku puzzle (use numbers 1-9, and 0 or . for blanks):")
    lines = []
    for i in range(9):
        try:
            line = input(f"Row {i + 1}: ").strip()
            lines.append(line)
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            return

    raw_text = "\n".join(lines)
    try:
        clues = parse_sudoku_string(raw_text)
        solve_and_display("Interactive Input", clues, graph)
    except Exception as e:
        print(f"Error parsing puzzle: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Tegraf: Sudoku Solver via Exact 9-Vertex Graph Coloring."
    )
    parser.add_argument(
        "file",
        nargs="?",
        default=None,
        help="Path to Sudoku input text file (e.g., inputs/slide18_sample.txt)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all sample benchmark puzzles in the inputs/ folder"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Enter puzzle interactively via terminal"
    )

    args = parser.parse_args()
    graph = SudokuGraph()

    if args.all:
        run_all_samples(graph)
    elif args.interactive:
        run_interactive(graph)
    elif args.file:
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            sys.exit(1)
        clues = parse_sudoku_file(args.file)
        solve_and_display(os.path.basename(args.file), clues, graph)
    else:
        # Default behavior: run Slide 18 sample
        default_file = os.path.join(os.path.dirname(__file__), "inputs", "slide18_sample.txt")
        if os.path.exists(default_file):
            print("[*] No arguments provided. Running default Week 10 Slide 18 sample...\n")
            clues = parse_sudoku_file(default_file)
            solve_and_display("slide18_sample.txt (Slide 18)", clues, graph)
            print("Tip: Run 'python main.py --all' to test all benchmark graphs or 'python main.py --help'.")
        else:
            parser.print_help()


if __name__ == "__main__":
    main()
