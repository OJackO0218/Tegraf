# Tegraf: Graph Coloring Algorithms (Sudoku & Timetabling)
Informatics ITS - Graph Theory Week 10 Assignment

## Identity
GROUP 8

|    NRP     |           Nama             |
| :--------: |       :------------:       |
| 5025251260 | Aqilah Ibrahim             |
| 5025251161 | Rizqi Arya Kuskhilbyano    |
| 5025251009 | Athar Rozy Rasyidan        |
| 5025251017 | Wafi Fawwaz Sutisna        |

## Overview
This repository implements two graph coloring applications from the Week 10 lecture:
1. Sudoku Solver using Vertex Coloring (Slide 7 & Slide 18)
2. Timetabling Problem Implementation (Slide 15 & Slide 19)

## 1. Sudoku Solver: Graph Theory Formulation & Algorithm

### Graph Model
A 9x9 Sudoku grid is modeled as an undirected constraint graph G = (V, E):
* Vertices (V): Each cell on the board represents a vertex. V = {v_(r,c) | 0 <= r < 9, 0 <= c < 9}, |V| = 81.
* Edges (E): An edge exists between two vertices if they cannot share the same digit:
  - Same row: 8 neighbors per cell
  - Same column: 8 neighbors per cell
  - Same 3x3 block: 4 additional neighbors per cell
  Every vertex has a degree of 20, making G a 20-regular graph.
  Total edges: |E| = (81 * 20) / 2 = 810 edges.
* Palette: Colors correspond to digits 1 through 9.
* Chromatic Goal: Every row, column, and block forms a 9-clique (K_9), so the chromatic number chi(G) >= 9. A valid solution is an exact 9-coloring of G.
* Pre-colored Vertices: Clues given in the initial puzzle represent fixed, immutable colors.

### Algorithm (Slide 7 & Slide 9)
The solver uses recursive backtracking with forward-checking degree heuristics:
1. isSafeToColor (Slide 7): Before assigning color c to vertex v, verify that no neighbor in adj[v] currently holds color c.
2. MRV Heuristic (Minimum Remaining Values / Saturation): Instead of static sequential order, pick the unassigned vertex with the fewest legal color options remaining. This prunes invalid search branches early.
3. Recursive Step (colorGraph, Slide 7):
   - If all 81 vertices are colored, the solution is complete.
   - For each valid color in candidate colors of the chosen vertex:
     - Assign color to vertex.
     - Recursively call colorGraph on the next most constrained vertex.
     - If true, return true.
     - Else, unassign color (backtrack).
   - If no valid color leads to a solution, return false.

## 2. Timetabling Problem: Graph Theory Formulation & Algorithm

### Graph Model
Given a set of lecturers L, classes C, and a requirement matrix A where A_ij is the number of sessions Lecturer L_i must teach Class C_j (Slide 19):
* Bipartite Multigraph Formulation:
  - Bipartite vertex sets: Left set = Lecturers, Right set = Classes.
  - Edges: A_ij parallel edges between Lecturer L_i and Class C_j.
* Conflict Graph (Line Graph) Formulation:
  - Each individual teaching session (L_i, C_j, k) is converted into a vertex.
  - An edge connects any two session vertices if they share the same lecturer or the same class.
  - Assigning time slots without teacher or student conflicts is equivalent to finding a proper vertex coloring on this conflict graph.

### Theoretical Proof (Konig's Theorem)
Konig's Line Coloring Theorem states that for any bipartite multigraph, the chromatic index chi'(G) (minimum colors to color edges) is equal to its maximum degree Delta(G):
  chi'(G) = Delta(G) = max(max_i sum_j A_ij, max_j sum_i A_ij)

For the Slide 19 dataset:
* Row sums (Lecturer hours): L1 = 4, L2 = 2, L3 = 3, L4 = 2. Maximum row sum = 4.
* Column sums (Class hours): C1 = 2, C2 = 2, C3 = 2, C4 = 4, C5 = 1. Maximum column sum = 4.
* Delta(G) = max(4, 4) = 4.
Therefore, the theoretical minimum number of time slots needed is exactly 4.

### Algorithm (Welsh-Powell, Slide 9)
To solve the conflict graph:
1. Sort session vertices in descending order of their conflict degrees.
2. Iterate through sorted vertices and assign the lowest-indexed available time slot (color) that is not already used by any adjacent session.
3. Output the grouped timetable schedule by time slot.

## Repository Structure
```
Tegraf/
├── inputs/
│   ├── slide18_sample.txt       # Week 10 Slide 18 Sudoku puzzle
│   ├── easy_sample.txt          # 36-clue Sudoku benchmark
│   ├── medium_sample.txt        # 28-clue Sudoku benchmark
│   ├── hard_sample.txt          # 21-clue Sudoku benchmark
│   ├── invalid_conflict.txt     # Conflicting Sudoku input
│   ├── timetabling_slide19.txt  # Week 10 Slide 19 matrix
│   └── timetabling_sample2.txt  # Department timetabling benchmark
├── src/
│   ├── sudoku_graph.py          # 81-vertex 20-regular Sudoku graph
│   ├── solver.py                # Backtracking + MRV vertex coloring solver
│   ├── utils.py                 # File parsing, ASCII display, chromatic check
│   └── timetabling.py           # Conflict graph generator + Welsh-Powell scheduler
├── tests/
│   ├── test_solver.py           # Unit tests for Sudoku coloring
│   └── test_timetabling.py      # Unit tests for Timetabling coloring
├── main.py                      # Unified CLI entrypoint
├── requirements.txt             # Dependency definitions (pure standard library)
└── README.md
```

## How to Run

Run all benchmarks:
python main.py all

Run Sudoku solver on Slide 18 sample:
python main.py sudoku inputs/slide18_sample.txt

Run Timetabling solver on Slide 19 sample:
python main.py timetabling inputs/timetabling_slide19.txt

Run unit test suite:
python -m unittest discover tests

## Results

### Sudoku (Slide 18)
* Pre-colored clues: 18 / 81 vertices
* Result: Solved proper 9-coloring
* Verification: All 810 edges confirmed non-monochromatic, chi(G) = 9
* Performance: Under 1.4 seconds on recursive backtracking with MRV

### Timetabling (Slide 19)
* Input matrix: 4 Lecturers x 5 Classes, 11 total sessions
* Degree analysis: Delta(G) = 4 (L1 requires 4 hours, C4 requires 4 hours)
* Minimum slots by Konig's Theorem: 4
* Output Schedule Matrix:
```
A            C1       C2       C3       C4       C5
L1        T3,T4        -       T2       T1        -
L2            -       T2        -       T3        -
L3            -       T1       T3       T2        -
L4            -        -        -       T4       T1
```
* Status: OPTIMAL (Assigned in exactly 4 non-conflicting time slots)

## AI Tools Usage Disclosure
Assistance was used for code structuring, test case generation, and documentation drafting. All algorithmic steps, graph formulations, and theoretical bounds were independently verified against lecture material.
