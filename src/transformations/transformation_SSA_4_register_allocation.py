

import copy
from collections import defaultdict
from typing import Any, DefaultDict, Dict, List, Set, Tuple

from src.analyses.analysis import Analysis
from src.analyses.live_variables import LiveVariables
from src.cfg.cfg import CFG
from src.cfg.IMP.command import (AssignmentCommand, LoadsCommand, NegCommand,
                                 ParallelAssigmentCommand, PosCommand,
                                 StoresCommand)
from src.cfg.IMP.expression import ID, variables_in_expression
from src.transformations.transformation import SingleStepTransformation
from src.util.table_printer import TableFormatter


class Register_Allocation(SingleStepTransformation):
    colors = [
        'blue',
        'purple',
        'orange',
        'pink',
        'cyan',
        'magenta',
        'gold',
        'navy',
        'teal',
        'maroon',
        'olive',
        'lime'
    ]

    def __init__(self) -> None:
        self.LA = LiveVariables()

    def dependencies(self):
        return [self.LA]

    @staticmethod
    def name() -> str:
        return "Register Allocation"

    @staticmethod
    def description() -> str:
        return "Determine a suitable register allocation"

    @staticmethod
    def calculate_live_ranges(cfg: CFG, L) -> Dict[ID, List[str]]:
        """Calculate live ranges for each variable in the CFG."""
        live_ranges: Dict[ID, List[str]] = {}
        # Assuming LA is the key for live analysis results

        for node in cfg.sort_nodes("forward"):
            live = L[node]
            for var in sorted(live, key=lambda x: x.name):
                if var not in live_ranges:
                    live_ranges[var] = []
                live_ranges[var].append(node.name)

        return live_ranges

    @staticmethod
    def build_interference_graph(live_ranges: Dict[ID, List[str]]) -> Set[Tuple[ID, ID]]:
        """Build interference graph from live ranges."""
        return {
            (x, y) for x in live_ranges
            for y in live_ranges
            if x != y and set(live_ranges[x]) & set(live_ranges[y])
        }

    @staticmethod
    def calculate_intervals(cfg: CFG, live_ranges: Dict[ID, List[str]]) -> Dict[ID, List[Tuple[str, str]]]:
        """Calculate intervals for each variable."""
        intervals: Dict[ID, List[Tuple[str, str]]] = {}

        for var, live in live_ranges.items():
            intervals[var] = []
            start = None
            for node in cfg.sort_nodes("forward"):
                if node.name in live:
                    if start is None:
                        start = node.name
                else:
                    if start is not None:
                        intervals[var].append((start, node.name))
                        start = None
            if start is not None:
                intervals[var].append((start, "∞"))

        return intervals

    @staticmethod
    def calculate_max_colors(cfg: CFG, live_ranges: Dict[ID, List[str]]) -> int:
        """Calculate the maximum number of colors needed."""
        max_live: DefaultDict[str, int] = defaultdict(int)
        for node in cfg.sort_nodes("forward"):
            for var, live in live_ranges.items():
                if node.name in live:
                    max_live[node.name] += 1
        return max(max_live.values())

    @staticmethod
    def color_graph(cfg: CFG, intervals: Dict[ID, List[Tuple[str, str]]], k: int) -> Dict[Tuple[ID, str, str], int]:
        """Color the graph using the calculated intervals."""
        free = list(range(k))
        itvs = [(var, u, v) for var, itv in intervals.items() for u, v in itv]

        init: Dict[str, List[tuple[ID, str, str]]] = defaultdict(list)
        exit: Dict[str, List[tuple[ID, str, str]]] = defaultdict(list)
        color: Dict[tuple[ID, str, str], int] = {}

        # Initialize intervals
        for I in itvs:
            var, u, v = I
            init[u].insert(0, I)
            if v != "∞":
                exit[v].insert(0, I)

        # Assign colors
        for node in cfg.sort_nodes("forward"):
            for I in exit[node.name]:
                if I not in color:
                    color[I] = free.pop(0)
                free.insert(0, color[I])

            for I in init[node.name]:
                color[I] = free.pop(0)

        return color

    @staticmethod
    def interval_to_elements(cfg: CFG, interval: Tuple[ID, str, str]) -> Set[str]:
        """Convert an interval to a set of node names."""
        res = set()
        running = False
        for node in cfg.sort_nodes("forward"):
            if node.name == interval[1]:
                running = True
            if node.name == interval[2]:
                break
            if running:
                res.add(node.name)

        if not res:
            res.add(interval[1])

        return res

    @staticmethod
    def print_interference_graph(live_ranges: Dict[ID, List[str]],
                                 interference_graph: Set[Tuple[ID, ID]]) -> None:
        """Print interference graph as a formatted table."""
        formatter = TableFormatter()

        # Prepare headers and rows
        headers = ["Variable"] + [str(var) for var in live_ranges]
        rows = []

        for x in live_ranges:
            row = [str(x)]
            for y in live_ranges:
                row.append("×" if (x, y) in interference_graph else "")
            rows.append(row)

        formatter.print_table(
            headers=headers,
            rows=rows,
            title="Interference Graph",
            min_width=8
        )

    @staticmethod
    def print_live_ranges(cfg: CFG, live_ranges: Dict[ID, List[str]],
                          color: Dict[Tuple[ID, str, str], int]) -> None:
        """Print live ranges as a formatted table."""
        formatter = TableFormatter()

        # Prepare headers and rows
        headers = ["Variable"] + \
            [node.name for node in cfg.sort_nodes("forward")]
        rows = []

        for var, live in sorted(live_ranges.items(), key=lambda x: x[0].name):
            row = [str(var)]
            for node in cfg.sort_nodes("forward"):
                if node.name in live:
                    col = None
                    for I, c in color.items():
                        if I[0] == var and node.name in Register_Allocation.interval_to_elements(cfg, I):
                            col = c
                            break
                    row.append(f"[{col}]" if col is not None else "●")
                else:
                    row.append("")
            rows.append(row)

        formatter.print_table(
            headers=headers,
            rows=rows,
            title="Live Ranges",
            min_width=6
        )

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:
        """Main transformation function that orchestrates the analysis and coloring process."""
        # Calculate live ranges
        live_ranges = self.calculate_live_ranges(
            cfg, analyses_results[self.LA])

        # Build and print interference graph
        interference_graph = self.build_interference_graph(live_ranges)
        self.print_interference_graph(live_ranges, interference_graph)

        # Calculate intervals and maximum colors needed
        intervals = self.calculate_intervals(cfg, live_ranges)
        k = self.calculate_max_colors(cfg, live_ranges)

        # Color the graph
        color = self.color_graph(cfg, intervals, k)

        # Print results
        self.print_live_ranges(cfg, live_ranges, color)

        def determine_color(var, node):
            for I, c in color.items():
                if I[0] == var and node.name in self.interval_to_elements(cfg, I):
                    return c
            return None

        def recolor(expr, node):
            expr = copy.deepcopy(expr)
            for var in variables_in_expression(expr):
                c = determine_color(var, node)
                if c is None:
                    print(f"Variable {var} not found in color graph")
                    c = -1
                expr.color(
                    var.name, Register_Allocation.colors[c % len(Register_Allocation.colors)])
                expr.rename(var.name, f"R_{c}")
            return expr

        for edge in cfg.edges:

            u = edge.source
            v = edge.dest
            if type(edge.command) == AssignmentCommand:
                edge.command.lvalue = recolor(edge.command.lvalue, v)
                edge.command.expr = recolor(edge.command.expr, u)
            elif type(edge.command) == ParallelAssigmentCommand:
                edge.command.assignments = [
                    (recolor(lvalue, v), recolor(expr, u)) for lvalue, expr in edge.command.assignments]
            elif type(edge.command) == PosCommand:
                edge.command.expr = recolor(edge.command.expr, u)
            elif type(edge.command) == NegCommand:
                edge.command.expr = recolor(edge.command.expr, u)
            elif type(edge.command) == LoadsCommand:
                edge.command.var = recolor(edge.command.var, v)
                edge.command.expr = recolor(edge.command.expr, u)
            elif type(edge.command) == StoresCommand:
                edge.command.lhs = recolor(edge.command.lhs, u)
                edge.command.rhs = recolor(edge.command.rhs, u)

        return cfg
