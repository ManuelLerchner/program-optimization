
from typing import TYPE_CHECKING, Any, Set

import graphviz

from cfg.IMP.command import (AssignmentCommand, Command, LoadsCommand,
                             NegCommand, PosCommand, SkipCommand,
                             StoresCommand)
from cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                UnaryExpression)

if TYPE_CHECKING:
    from analyses.analysis import Analysis


def get_vars(expression: Expression) -> Set[ID]:
    if isinstance(expression, ID):
        return {expression}
    if isinstance(expression, Constant):
        return set()
    if isinstance(expression, BinExpression):
        return get_vars(expression.left) | get_vars(expression.right)
    if isinstance(expression, UnaryExpression):
        return get_vars(expression.expr)

    raise Exception("Unknown expression")


def get_expressions_command(expr: Command) -> Set[Expression]:
    if isinstance(expr, SkipCommand):
        return set()
    elif isinstance(expr, AssignmentCommand):
        return {expr.expr}
    elif isinstance(expr, LoadsCommand):
        return {expr.expr}
    elif isinstance(expr, StoresCommand):
        return {expr.lhs, expr.rhs}
    elif isinstance(expr, PosCommand):
        return {expr.expr}
    elif isinstance(expr, NegCommand):
        return {expr.expr}
    else:
        raise Exception("Unknown command")


class CFG:

    class Node:
        def __init__(self, name: str):
            self.name = name
            self.annotations: dict[Analysis, dict[CFG.Node, Any]] = {}

        def __str__(self):

            values = "\n".join(
                [f"{key.name()}={key.lattice.show(value)}" for key, value in self.annotations.items()])

            return f"{self.name}\n{values}" if self.annotations else self.name

        def __hash__(self):
            return hash(self.name)

        def __eq__(self, other):
            return self.name == other.name

    class Edge:
        def __init__(self, source, dest, command: Command):
            self.source: CFG.Node = source
            self.command = command
            self.dest: CFG.Node = dest

        def __repr__(self):
            return f"Edge({self.source} -> {self.dest} [{self.command}])"

    def __init__(self) -> None:
        self.edges: list[CFG.Edge] = []
        self.path: str
        self.filename: str

        self.function_counter = 0
        self.assignment_counter = 0
        self.loads_counter = 0
        self.stores_counter = 0
        self.skip_counter = 0
        self.if_counter = 0
        self.loop_counter = 0

    def make_function_nodes(self, name: str):
        self.function_counter += 1
        entry = CFG.Node(f"{name}{self.function_counter}_entry")
        exit = CFG.Node(f"{name}{self.function_counter}_exit")

        return entry, exit

    def make_stmt_node(self):
        self.assignment_counter += 1
        return CFG.Node(f"stmt_{self.assignment_counter}")

    def make_loads_node(self):
        self.loads_counter += 1
        return CFG.Node(f"loads_{self.loads_counter}")

    def make_stores_node(self):
        self.stores_counter += 1
        return CFG.Node(f"stores_{self.stores_counter}")

    def make_skip_node(self):
        self.skip_counter += 1
        return CFG.Node(f"skip_{self.skip_counter}")

    def make_if_nodes(self):
        self.if_counter += 1
        true_entry = CFG.Node(f"if_true_{self.if_counter}")
        false_entry = CFG.Node(f"if_false_{self.if_counter}")

        return true_entry, false_entry

    def make_loop_nodes(self):
        self.loop_counter += 1
        loop_entry = CFG.Node(f"loop_{self.loop_counter}_entry")
        loop_exit = CFG.Node(f"loop_{self.loop_counter}_exit")

        return loop_entry, loop_exit

    def add_edge(self, source: Node, dest: Node, command: Command):
        edge = CFG.Edge(source, dest, command)

        self.edges.append(edge)

    def get_nodes(self):
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.source)
            nodes.add(edge.dest)

        return nodes

    def get_incoming(self, node: Node) -> set[Edge]:
        incoming = set()
        for edge in self.edges:
            if edge.dest == node:
                incoming.add(edge)
        return incoming

    def get_outgoing(self, node: Node) -> set[Edge]:
        outgoing = set()
        for edge in self.edges:
            if edge.source == node:
                outgoing.add(edge)
        return outgoing

    def to_dot(self):
        dot = graphviz.Digraph()
        for edge in self.edges:
            # set label to empty string
            src = edge.source
            dest = edge.dest
            dot.node(src.name, label=str(src))
            dot.node(dest.name, label=str(dest))

            dot.edge(src.name, dest.name, label=str(edge.command))

        return dot

    def get_all_vars(self) -> Set[ID]:
        all_vars = set()
        for expr in self.get_all_expressions():
            all_vars |= get_vars(expr)

        return all_vars

    def get_all_expressions(self) -> Set[Expression]:
        expressions = set()
        for edge in self.edges:
            expressions |= get_expressions_command(edge.command)

        return expressions

    def render(self, filename):
        self.to_dot().render(filename, format='png', cleanup=True)
