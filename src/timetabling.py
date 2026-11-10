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


def format_input_matrix(graph: TimetableGraph) -> str:
    """Renders the original requirements matrix A exactly as shown on Slide 19."""
    col_w = max(max(len(c) for c in graph.classes), 4) + 2
    row_label_w = max(max(len(l) for l in graph.lecturers), 4) + 2

    header = "A".ljust(row_label_w) + "".join(c.rjust(col_w) for c in graph.classes)
    lines = [header]

    for i, lec in enumerate(graph.lecturers):
        row_str = lec.ljust(row_label_w) + "".join(str(graph.matrix[i][j]).rjust(col_w) for j in range(len(graph.classes)))
        lines.append(row_str)

    return "\n".join(lines)


def format_timetable_matrix(graph: TimetableGraph, colors: Dict[int, int]) -> str:
    """
    Renders the solved schedule as a Lecturer x Class matrix just like Slide 19.
    Each cell displays the assigned time slot(s) (e.g. T1, T2, or -).
    """
    cell_slots = defaultdict(list)
    for s_idx, slot in colors.items():
        s = graph.sessions[s_idx]
        cell_slots[(s.lecturer, s.class_group)].append(f"T{slot}")

    # Determine column width based on longest cell content
    max_cell_len = 1
    for slots_list in cell_slots.values():
        val = ",".join(sorted(slots_list))
        if len(val) > max_cell_len:
            max_cell_len = len(val)

    col_w = max(max(len(c) for c in graph.classes), max_cell_len) + 4
    row_label_w = max(max(len(l) for l in graph.lecturers), 4) + 2

    header = "A".ljust(row_label_w) + "".join(c.rjust(col_w) for c in graph.classes)
    lines = [header]

    for lec in graph.lecturers:
        row_str = lec.ljust(row_label_w)
        for cls in graph.classes:
            val = ",".join(sorted(cell_slots.get((lec, cls), [])))
            cell_str = val if val else "-"
            row_str += cell_str.rjust(col_w)
        lines.append(row_str)

    return "\n".join(lines)


def format_slot_decomposition(graph: TimetableGraph, colors: Dict[int, int]) -> str:
    """
    Renders the decomposition of matrix A into individual 0/1 slot matrices:
        A = P_1 + P_2 + ... + P_n
    where each P_k contains at most one 1 per row and column.
    """
    slots_used = max(colors.values()) if colors else 0
    slot_assignments = defaultdict(lambda: defaultdict(int))

    for s_idx, slot in colors.items():
        s = graph.sessions[s_idx]
        slot_assignments[slot][(s.lecturer, s.class_group)] += 1

    col_w = max(max(len(c) for c in graph.classes), 4) + 2
    row_label_w = max(max(len(l) for l in graph.lecturers), 4) + 2

    lines = []
    for slot in range(1, slots_used + 1):
        lines.append(f"Time Slot T{slot} (0/1 Matching Matrix):")
        header = f"P{slot}".ljust(row_label_w) + "".join(c.rjust(col_w) for c in graph.classes)
        lines.append(header)
        for lec in graph.lecturers:
            row_str = lec.ljust(row_label_w)
            for cls in graph.classes:
                val = str(slot_assignments[slot].get((lec, cls), 0))
                row_str += val.rjust(col_w)
            lines.append(row_str)
        lines.append("")

    return "\n".join(lines).rstrip()


def format_timetable_schedule(graph: TimetableGraph, colors: Dict[int, int]) -> str:
    """Full comprehensive output combining matrix, slot decomposition, and list summary."""
    slots = defaultdict(list)
    for s_idx, slot in colors.items():
        session = graph.sessions[s_idx]
        slots[slot].append(session)

    res = []
    res.append("Output Schedule Matrix (Assigned Time Slots per Lecturer-Class pair):")
    res.append(format_timetable_matrix(graph, colors))
    res.append("")
    res.append("Slot Decomposition Matrices (A = P1 + P2 + ... + Pn):")
    res.append(format_slot_decomposition(graph, colors))
    res.append("")
    res.append("Schedule Summary by Slot:")
    for slot in sorted(slots.keys()):
        assigned = slots[slot]
        items = ", ".join(f"{s.lecturer} teaches {s.class_group}" for s in assigned)
        res.append(f"  Slot T{slot}: {items}")

    return "\n".join(res)
