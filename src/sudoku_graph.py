"""
Graph Representation for Sudoku.
Models a standard 9x9 Sudoku board as a 20-regular undirected graph G = (V, E):
- |V| = 81 vertices (each cell on the 9x9 board)
- |E| = 810 undirected edges (connecting cells in the same row, column, or 3x3 box)
- Degree of each vertex deg(v) = 20
"""

from collections import defaultdict


class SudokuGraph:
    """
    Represents the Sudoku constraint graph.
    Vertices are indexed 0 to 80, mapped from (row, col):
        index = row * 9 + col
    """
    NUM_VERTICES = 81
    GRID_SIZE = 9
    BOX_SIZE = 3

    def __init__(self):
        self.adj = defaultdict(set)
        self._build_graph()

    @staticmethod
    def to_index(r: int, c: int) -> int:
        """Converts (row, col) (0-indexed) to vertex index 0..80."""
        return r * 9 + c

    @staticmethod
    def to_coord(idx: int) -> tuple:
        """Converts vertex index 0..80 to (row, col) tuple."""
        return idx // 9, idx % 9

    def _build_graph(self):
        """Constructs the 810 edges connecting conflicting cells."""
        for r in range(self.GRID_SIZE):
            for c in range(self.GRID_SIZE):
                u = self.to_index(r, c)

                # 1. Row neighbors
                for c2 in range(self.GRID_SIZE):
                    if c2 != c:
                        self._add_edge(u, self.to_index(r, c2))

                # 2. Column neighbors
                for r2 in range(self.GRID_SIZE):
                    if r2 != r:
                        self._add_edge(u, self.to_index(r2, c))

                # 3. 3x3 Box neighbors
                box_r, box_c = (r // self.BOX_SIZE) * self.BOX_SIZE, (c // self.BOX_SIZE) * self.BOX_SIZE
                for br in range(box_r, box_r + self.BOX_SIZE):
                    for bc in range(box_c, box_c + self.BOX_SIZE):
                        if br != r or bc != c:
                            self._add_edge(u, self.to_index(br, bc))

    def _add_edge(self, u: int, v: int):
        self.adj[u].add(v)
        self.adj[v].add(u)

    def get_neighbors(self, v: int) -> set:
        """Returns the set of adjacent vertex indices for vertex v."""
        return self.adj[v]

    @property
    def total_edges(self) -> int:
        """Computes the total number of undirected edges in G."""
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2
