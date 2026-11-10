# 🧩 Tegraf: Sudoku Solver via Graph Vertex Coloring
> **Informatics ITS — Graph Theory (Teori Graf) Week 10 Assignment**  
> Department of Informatics, Institut Teknologi Sepuluh Nopember (ITS)

---

## 👥 Student Identity
* **Course:** Graph Theory (Teori Graf)
* **Institution:** Department of Informatics, Institut Teknologi Sepuluh Nopember (ITS)
* **Topic Selected:** **Coloring — Option 1: Implement Sudoku Solver using Vertex Coloring**
* **Author:** Athar Rozy Rasyidan
* **NRP / Student ID:** 5025251009
* **Class:** IUP Informatics

---

## 📖 Theoretical Formulation: Sudoku as Graph Coloring

In graph theory, **Vertex Coloring** is the assignment of labels (or "colors") to the vertices of a graph such that **no two adjacent vertices share the same color** (*Week 10 Lecture, Slide 3*).

A standard $9 \times 9$ Sudoku puzzle can be formally modeled as an **Exact 9-Vertex Coloring Problem** on an undirected graph $G = (V, E)$:

```
           9x9 Board (81 Cells)                 Graph Formulation G = (V, E)
     +-------+-------+-------+                  • Vertices |V| = 81 cells
     | . . . | . . . | . 1 . |                  • Edges    |E| = 810 constraint edges
     | . . 2 | . . . | . 3 4 |     ======>      • Degree   deg(v) = 20 (20-regular graph)
     | . . . | . 5 1 | . . . |                  • Palette  C = {1, 2, 3, 4, 5, 6, 7, 8, 9}
     +-------+-------+-------+                  • Target   Chromatic number χ(G) = 9
```

### 1. Graph Elements
1. **Vertices ($V$):**  
   Each of the 81 cells is a vertex:
   $$V = \{v_{r, c} \mid 0 \le r < 9,\ 0 \le c < 9\}, \quad |V| = 81$$
2. **Edges ($E$):**  
   An edge $(u, v) \in E$ exists if and only if cells $u$ and $v$ are distinct and share a mutual constraint:
   - Same Row: $r_u = r_v$ (8 neighbors)
   - Same Column: $c_u = c_v$ (8 neighbors)
   - Same $3 \times 3$ Subgrid (Box): $\lfloor r_u / 3 \rfloor = \lfloor r_v / 3 \rfloor$ and $\lfloor c_u / 3 \rfloor = \lfloor c_v / 3 \rfloor$ (4 non-row/non-column neighbors)
   
   Every vertex has an exact degree of $20$, forming a **20-regular graph**.  
   The total number of edges is:
   $$|E| = \frac{|V| \times \text{deg}(v)}{2} = \frac{81 \times 20}{2} = 810 \text{ edges}$$

3. **Colors ($\mathcal{C}$):**  
   The available color palette is $\mathcal{C} = \{1, 2, 3, 4, 5, 6, 7, 8, 9\}$.

4. **Chromatic Number ($\chi(G)$):**  
   Because every row, column, and $3 \times 3$ box forms a complete subgraph (clique $K_9$), the graph requires at least 9 colors ($\chi(G) \ge 9$). A solved Sudoku corresponds to a valid proper coloring where $\chi(G) = 9$.

5. **Pre-colored Vertices (Clues):**  
   The given numbers in the puzzle represent a subset of pre-colored vertices $V_{\text{fixed}} \subset V$ whose assignments are immutable.

---

## 🧠 Algorithm Implementation

The solver is implemented strictly following the algorithms presented in the **Week 10 Lecture**:

### 1. Recursive Backtracking (`src/solver.py`)
Directly maps to **Slide 7** of the lecture slides:
```text
isSafeToColor(graph, verticesColor):
    For each neighbor of currentVertex:
        If neighbor has the same color:
            Return false
    Return true

colorGraph(graph, colorOptions, currentVertex, verticesColor):
    If all vertices are colored:
        Return true
    For each color in colorOptions:
        If isSafeToColor(graph, currentVertex, color):
            Assign color to verticesColor[currentVertex]
            If colorGraph(graph, nextVertex) is true:
                Return true
            Reset color (backtrack)
    Return false
```

### 2. Degree of Saturation / MRV Heuristic (`use_mrv=True`)
Inspired by the **Welsh-Powell Algorithm (Slide 9)** which prioritizes high-constraint vertices:
* Instead of arbitrary sequential vertex coloring, the solver dynamically prioritizes the uncolored vertex with the **Minimum Remaining Values (MRV)** (the fewest legal color options left).
* This dramatically prunes fruitless branches, solving complex 9x9 puzzles in milliseconds.

---

## 📁 Repository Structure

```
Tegraf/
├── inputs/
│   ├── slide18_sample.txt       # The exact Sudoku puzzle from Week 10 Slide 18
│   ├── easy_sample.txt          # 36 clues benchmark (instant solve)
│   ├── medium_sample.txt        # 28 clues benchmark
│   ├── hard_sample.txt          # 21 clues benchmark
│   └── invalid_conflict.txt     # Invalid puzzle with duplicate clues to test conflict detection
├── src/
│   ├── __init__.py
│   ├── sudoku_graph.py          # 81-vertex, 810-edge 20-regular graph model
│   ├── solver.py                # Graph coloring recursive backtracking + MRV heuristic
│   └── utils.py                 # File parsing, ASCII grid renderer, chromatic validation
├── tests/
│   └── test_solver.py           # Automated unit test suite
├── main.py                      # Main CLI program
├── requirements.txt             # Pure Python standard library
└── README.md                    # Project documentation
```

---

## 🚀 How to Run

### Prerequisites
* **Python 3.8+**
* Pure Python Standard Library (no third-party dependencies required).

### 1. Run the Default Week 10 Slide 18 Sample
```bash
python main.py
```

### 2. Solve a Specific Input File
```bash
python main.py inputs/slide18_sample.txt
python main.py inputs/easy_sample.txt
python main.py inputs/hard_sample.txt
```

### 3. Run All Benchmark Samples
```bash
python main.py --all
```

### 4. Interactive Mode (Paste Your Own Puzzle)
```bash
python main.py --interactive
```

### 5. Run Automated Unit Tests
```bash
python tests/test_solver.py
```

---

## 📊 Sample Run Results

### Benchmark Summary Table

| Input File | Clues Given | Graph Status | Result | Execution Time | Backtracks | Chromatic Check |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| **`slide18_sample.txt`** *(Slide 18)* | 18 | Valid | **SOLVED** | 1,392.14 ms | 22,489 | $\chi(G) = 9$ Valid |
| **`easy_sample.txt`** | 36 | Valid | **SOLVED** | 2.02 ms | 0 | $\chi(G) = 9$ Valid |
| **`medium_sample.txt`** | 24 | Valid | **SOLVED** | 44.24 ms | 395 | $\chi(G) = 9$ Valid |
| **`hard_sample.txt`** | 21 | Valid | **SOLVED** | 224.84 ms | 3,437 | $\chi(G) = 9$ Valid |
| **`invalid_conflict.txt`** | 2 | Conflicting Clues | **REJECTED** | 0.00 ms | 0 | Conflict Caught |

### Console Output for Week 10 Slide 18:
```text
=================================================================
🧩 ANALYZING SUDOKU GRAPH: slide18_sample.txt (Slide 18)
=================================================================
Graph Properties:
  • Vertices (|V|) : 81 cells
  • Edges    (|E|) : 810 constraints (20-regular graph)
  • Pre-colored    : 18 / 81 vertices fixed by clues
  • Chromatic Goal : Proper 9-coloring (\chi(G) = 9)
-----------------------------------------------------------------
INITIAL GRAPH STATE:
+-------+-------+-------+
| . . . | . . . | . 1 . |
| . . 2 | . . . | . 3 4 |
| . . . | . 5 1 | . . . |
+-------+-------+-------+
| . . . | . . 6 | 5 . . |
| . 7 . | 3 . . | . 8 . |
| . . 3 | . . . | . . . |
+-------+-------+-------+
| . . . | . 8 . | . . . |
| 5 8 . | . . . | 9 . . |
| 6 9 . | . . . | . . . |
+-------+-------+-------+
-----------------------------------------------------------------
Running Backtracking Vertex Coloring with MRV/Saturation Heuristic...
✅ PROPER 9-COLORING FOUND!
+-------+-------+-------+
| 8 4 9 | 2 6 3 | 7 1 5 |
| 1 5 2 | 8 7 9 | 6 3 4 |
| 7 3 6 | 4 5 1 | 8 9 2 |
+-------+-------+-------+
| 2 1 8 | 7 9 6 | 5 4 3 |
| 9 7 5 | 3 1 4 | 2 8 6 |
| 4 6 3 | 5 2 8 | 1 7 9 |
+-------+-------+-------+
| 3 2 1 | 9 8 5 | 4 6 7 |
| 5 8 4 | 6 3 7 | 9 2 1 |
| 6 9 7 | 1 4 2 | 3 5 8 |
+-------+-------+-------+
-----------------------------------------------------------------
Graph Theory Verification: Valid proper 9-coloring verified! |V| = 81, |E| = 810, chi(G) = 9.
Performance Metrics:
  • Time Elapsed : 1392.14 ms
  • Nodes Visited: 22,553
  • Backtracks   : 22,489
=================================================================
```

---

## 🤖 AI Tools Usage Disclosure

In compliance with the homework policy regarding honest academic integrity and AI disclosure:
* **AI Tool Used:** Google Antigravity (Gemini-powered coding assistant)
* **Scope of Assistance:**
  1. Designing the modular graph representation ($G = (V, E)$ with $|V| = 81, |E| = 810$) mapping Sudoku constraints to adjacency lists.
  2. Synthesizing the recursive backtracking algorithm from Lecture Slide 7 with the MRV heuristic inspired by Welsh-Powell (Slide 9).
  3. Generating benchmark dataset files including the exact digit placement from Lecture Slide 18.
  4. Structuring the repository and documentation to ensure clarity and reproducibility.
* **Verification Conducted by Student:**
  All code was independently executed, tested, and verified against classical graph theory proofs ($\chi(G) = 9$, no adjacent vertices with identical colors, and rejection of conflicting inputs).
