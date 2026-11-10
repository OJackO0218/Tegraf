# Tegraf: Graph Coloring Algorithms (Sudoku & Timetabling)
Informatics ITS - Graph Theory Week 10 Assignment

## Student Identity
Course: Graph Theory (Teori Graf)
Institution: Department of Informatics, Institut Teknologi Sepuluh Nopember (ITS)
Topic Selected: Coloring
Author: Athar Rozy Rasyidan
NRP: 5025251009
Class: IUP Informatics

## Overview
This repository implements two graph coloring applications from the Week 10 lecture:
1. Sudoku Solver using Vertex Coloring (Slide 7 & Slide 18)
2. Timetabling Problem Implementation (Slide 15 & Slide 19)

## 1. Sudoku Solver (Vertex Coloring)
* Formulation: Undirected graph G = (V, E) with |V| = 81 vertices and |E| = 810 edges (20-regular graph).
* Constraints: Edges connect cells in the same row, column, or 3x3 block.
* Palette: C = {1, 2, 3, 4, 5, 6, 7, 8, 9}. Chromatic number chi(G) = 9.
* Algorithm: Recursive backtracking (Slide 7) with Minimum Remaining Values / Degree of Saturation heuristic (Slide 9).

## 2. Timetabling Problem (Conflict Graph Coloring)
* Formulation: Scheduling L lecturers across C classes given requirement matrix A_ij.
* Conflict Graph: Each lecture period is a vertex. Edges connect sessions sharing the same lecturer or class.
* Theory: Konig's Line Coloring Theorem guarantees chromatic index chi'(G) = Delta(G), where Delta(G) is the maximum degree (maximum row/column sum in A).
* Slide 19 Example: Maximum degree is 4 (L1 and C4), yielding an optimal 4-slot conflict-free timetable.

## Repository Structure
Tegraf/
├── inputs/
│   ├── slide18_sample.txt
│   ├── easy_sample.txt
│   ├── medium_sample.txt
│   ├── hard_sample.txt
│   ├── invalid_conflict.txt
│   ├── timetabling_slide19.txt
│   └── timetabling_sample2.txt
├── src/
│   ├── sudoku_graph.py
│   ├── solver.py
│   ├── utils.py
│   └── timetabling.py
├── tests/
│   ├── test_solver.py
│   └── test_timetabling.py
├── main.py
├── requirements.txt
└── README.md

## How to Run

Run all benchmarks:
python main.py all

Run Sudoku solver:
python main.py sudoku inputs/slide18_sample.txt

Run Timetabling solver:
python main.py timetabling inputs/timetabling_slide19.txt

Run unit tests:
python -m unittest discover tests

## Results

Sudoku (Slide 18):
Proper 9-coloring found, all 810 edges verified non-monochromatic, chi(G) = 9.

Timetabling (Slide 19):
Total sessions: 11
Theoretical minimum slots: 4 (Delta(G) = 4)
Assigned time slots: 4
Result: OPTIMAL

## AI Tools Usage Disclosure
Assistance used for code organization, test matrix formulation, and documentation formatting. Code was independently verified and tested against graph coloring properties.
