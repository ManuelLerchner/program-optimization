from dataclasses import dataclass
from pycparser.c_generator import CGenerator
import graphviz
from typing import Optional
from pycparser import c_parser, c_ast
import typing


class Node:
    def __init__(self, counter, name: str):
        self.counter = counter
        self.name = name

    def __repr__(self):
        return (f"Node({self.counter}, {self.name})")

    def __str__(self):
        return f"{self.counter}"

    def __hash__(self):
        return hash(self.name) + hash(self.counter)

    def __eq__(self, other):
        return self.name == other.name and self.counter == other.counter


@dataclass
class Constant:
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __hash__(self):
        return hash(self.value)


@dataclass
class ID:
    name: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(self.name)


@dataclass
class UnaryExpression:
    op: str
    expr: c_ast.Node

    def __str__(self):
        return f"{self.op} {self.expr}"

    def __repr__(self):
        return f"{self.op} {self.expr}"

    def __hash__(self):
        return hash(self.op) + hash(self.expr)


@dataclass
class BinExpression:
    left: c_ast.Node
    op: str
    right: c_ast.Node

    def __str__(self):
        return f"{self.left} {self.op} {self.right}"

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

    def __hash__(self):
        return hash(self.left) + hash(self.op) + hash(self.right)

    def __eq__(self, other):
        return self.left == other.left and self.op == other.op and self.right == other.right


@dataclass
class Assignment:
    lhs: str
    rhs: c_ast.Node

    def __str__(self):
        return f"{self.lhs} = {self.rhs}"

    def __repr__(self):
        return f"{self.lhs} = {self.rhs}"


def parseExpression(expr: c_ast.Node):
    if isinstance(expr, c_ast.ID):
        return ID(expr.name)
    elif isinstance(expr, c_ast.BinaryOp):
        return BinExpression(parseExpression(expr.left), expr.op, parseExpression(expr.right))
    elif isinstance(expr, c_ast.UnaryOp):
        return UnaryExpression(expr.op, parseExpression(expr.expr))
    elif isinstance(expr, c_ast.Decl):
        return Assignment(expr.name, parseExpression(expr.init))
    elif isinstance(expr, c_ast.Constant):
        return Constant(expr.value)
    else:
        return expr


class Command:
    def __init__(self, type: typing.Literal["skip", "function_entry", "assignment", "loads", "stores"], expr: Optional[c_ast.Node] = None):
        self.type = type

        self.expr = parseExpression(expr)

    def __str__(self):
        if self.expr:
            return f"{self.type} {self.expr}"
        return self.type


class Edge:
    def __init__(self, source: Node, dest: Node, command: Command):
        self.source = source
        self.dest = dest
        self.command = command

    def __repr__(self):
        return f"Edge({self.source} -> {self.dest} [{self.command}])"


class CFG:
    def __init__(self):
        self.edges: list[Edge] = []
        self.finalized = False

    def add_edge(self, source: Node, dest: Node, command: Command):
        if self.finalized:
            return
        edge = Edge(source, dest, command)
        self.edges.append(edge)

    def get_nodes(self):
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.source)
            nodes.add(edge.dest)
        return nodes

    def to_dot(self):
        dot = graphviz.Digraph()
        for edge in self.edges:
            # set label to empty string
            src = str(edge.source)
            dest = str(edge.dest)
            # node1 = dot.node(src, label="")
            # node2 = dot.node(dest, label="")
            dot.edge(src, dest, label=str(edge.command))
        return dot

    def render(self, filename):
        self.to_dot().render(filename, format='png', cleanup=True)

    def finalize(self):
        self.finalized = True
