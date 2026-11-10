"""
Timetabling Problem Solver using Graph Vertex Coloring.
Reference: Week 10 Lecture Slide 19.

Models teacher-class scheduling as a conflict graph:
- Each individual lecture session is a vertex.
- An edge connects any two sessions that share the same lecturer or the same class.
- Vertex coloring assigns non-conflicting time slots (colors).
- Minimum time slots = Maximum vertex degree in the underlying bipartite multigraph Delta(G) (Konig's Theorem).
"""

from collections import defaultdict
from typing import Dict, List, Tuple


class TimetableSession:
    def __init__(self, session_id: int, lecturer: str, class_group: str, period_idx: int):
        self.session_id = session_id
        self.lecturer = lecturer
        self.class_group = class_group
        self.period_idx = period_idx

    def __repr__(self):
        return f"{self.lecturer}-{self.class_group}"


class TimetableGraph:
    def __init__(self, lecturers: List[str], classes: List[str], matrix: List[List[int]]):
        self.lecturers = lecturers
        self.classes = classes
        self.matrix = matrix
        self.sessions: List[TimetableSession] = []
        self.adj = defaultdict(set)
        self._build()

    def _build(self):
        s_id = 0
        for i, lec in enumerate(self.lecturers):
            for j, cls in enumerate(self.classes):
                count = self.matrix[i][j]
                for p in range(count):
                    self.sessions.append(TimetableSession(s_id, lec, cls, p + 1))
                    s_id += 1

        n = len(self.sessions)
        for i in range(n):
            for j in range(i + 1, n):
                s1 = self.sessions[i]
                s2 = self.sessions[j]
                if s1.lecturer == s2.lecturer or s1.class_group == s2.class_group:
                    self.adj[i].add(j)
                    self.adj[j].add(i)

    @property
    def total_sessions(self) -> int:
        return len(self.sessions)

    @property
    def total_edges(self) -> int:
        return sum(len(v) for v in self.adj.values()) // 2

    def theoretical_min_slots(self) -> int:
        max_lec = max(sum(row) for row in self.matrix) if self.matrix else 0
        num_cols = len(self.classes)
        max_cls = max(sum(self.matrix[r][c] for r in range(len(self.lecturers))) for c in range(num_cols)) if num_cols else 0
        return max(max_lec, max_cls)


def solve_timetabling(graph: TimetableGraph) -> Tuple[Dict[int, int], int]:
    """
    Applies Welsh-Powell degree-ordered vertex coloring to assign minimum time slots.
    Returns:
        (session_colors: Dict[session_id, slot_id], num_slots_used: int)
    """
    sorted_nodes = sorted(range(graph.total_sessions), key=lambda x: len(graph.adj[x]), reverse=True)
    colors = {}

    for node in sorted_nodes:
        neighbor_colors = {colors[nbr] for nbr in graph.adj[node] if nbr in colors}
        color = 1
        while color in neighbor_colors:
            color += 1
        colors[node] = color

    slots_used = max(colors.values()) if colors else 0
    return colors, slots_used


def parse_timetabling_file(filepath: str) -> TimetableGraph:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    if len(lines) < 3:
        raise ValueError("Invalid format: expected lecturers, classes, and matrix rows.")

    lecturers = lines[0].split()
    classes = lines[1].split()
    matrix = []

    for row_line in lines[2:2 + len(lecturers)]:
        row = [int(x) for x in row_line.split()]
        if len(row) != len(classes):
            raise ValueError(f"Matrix row length mismatch: expected {len(classes)} columns, got {len(row)}")
        matrix.append(row)

    return TimetableGraph(lecturers, classes, matrix)


def format_timetable_schedule(graph: TimetableGraph, colors: Dict[int, int]) -> str:
    slots = defaultdict(list)
    for s_idx, slot in colors.items():
        session = graph.sessions[s_idx]
        slots[slot].append(session)

    res = []
    res.append(f"Total Sessions: {graph.total_sessions} | Slots Required: {len(slots)}")
    for slot in sorted(slots.keys()):
        assigned = slots[slot]
        items = ", ".join(f"{s.lecturer} -> {s.class_group}" for s in assigned)
        res.append(f"  Slot {slot}: {items}")

    return "\n".join(res)
