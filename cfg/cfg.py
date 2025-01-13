
from typing import TYPE_CHECKING, Any, Literal, Set

import graphviz

from cfg.IMP.command import (AssignmentCommand, Command, LoadsCommand,
                             NegCommand, ParallelAssigmentCommand, PosCommand,
                             SkipCommand, StoresCommand)
from cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                MemoryExpression, UnaryExpression)
from util.bcolors import BColors

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
    if isinstance(expression, MemoryExpression):
        return get_vars(expression.expr) | get_vars(expression.array)

    raise Exception("Unknown expression")


def get_expressions_command(expr: Command) -> Set[Expression]:
    if isinstance(expr, SkipCommand):
        return set()
    elif isinstance(expr, AssignmentCommand):
        return {expr.expr, expr.lvalue}
    elif isinstance(expr, LoadsCommand):
        return {expr.expr, expr.var, MemoryExpression(ID("M"), expr.expr)}
    elif isinstance(expr, StoresCommand):
        return {expr.lhs, expr.rhs}
    elif isinstance(expr, PosCommand):
        return {expr.expr}
    elif isinstance(expr, NegCommand):
        return {expr.expr}
    elif isinstance(expr, ParallelAssigmentCommand):
        xs, ys = [], []
        for l, r in expr.assignments:
            xs.append(l)
            ys.append(r)
        return set(xs + ys)
    else:
        raise Exception("Unknown command")


class CFG:

    class Node:
        def __init__(self, name: str):
            self.name = name
            self.annotations: dict[Analysis, dict[CFG.Node, Any]] = {}
            self.is_start = False
            self.is_end = False
            self.is_loop_separator = False
            self.age = 0
            self.temperature = float('inf')
            self.locals: set[str] = set()
            self.globals: set[str] = set()

        def __str__(self):
            values = "<br/>".join(
                [f"{key.name()}={key.lattice.show(value)}" for key, value in sorted(self.annotations.items(), key=lambda x: str(x[0]))])

            if self.locals:
                values += f"<br/>locals=[{', '.join(sorted(self.locals, key=lambda x: str(x)))}]"
            if self.globals:
                values += f"<br/>globals=[{', '.join(sorted(self.globals, key=lambda x: str(x)))}]"

            return f"{self.name}<br/>{values}" if self.annotations or self.locals else f"{self.name}"

        def __repr__(self):
            values = "\n".join(
                [f"{key.name()}={key.lattice.show(value)}" for key, value in sorted(self.annotations.items(), key=lambda x: str(x[0]))])

            if self.locals:
                values += f"\nlocals=[{', '.join(map(str, self.locals))}]"
            if self.globals:
                values += f"\nglobals=[{', '.join(map(str, self.globals))}]"

            return f"{BColors.OKGREEN}{self.name}{BColors.ENDC}\n{BColors.OKBLUE}{values}{BColors.ENDC}" if self.annotations or self.locals else f"{BColors.OKGREEN}{self.name}{BColors.ENDC}"

        def __hash__(self):
            return hash(self.name) + hash(self.is_start) + hash(self.is_end) + hash(self.is_loop_separator) + hash(self.age) + hash(self.temperature) + hash(str(self.locals))

        def __eq__(self, other):
            return self.name == other.name and self.is_start == other.is_start and self.is_end == other.is_end and self.is_loop_separator == other.is_loop_separator and self.age == other.age and self.temperature == other.temperature and self.locals == other.locals

    class Edge:
        def __init__(self, source, dest, command: Command):
            self.source: CFG.Node = source
            self.command = command
            self.dest: CFG.Node = dest
            self.age = 0

        def __repr__(self):
            return f"Edge({repr(self.source)} -> {repr(self.dest)} [{(self.command)} : {type(self.command).__name__}])"

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
        self.alloc_counter = 0
        self.block_read_counter = 0
        self.block_write_counter = 0
        self.optimization_counter = 0
        self.copy_counter = 0

    def make_function_nodes(self, name: str):
        self.function_counter += 1
        entry = CFG.Node(f"{name}_entry_{self.function_counter}")

        entry.is_start = True
        exit = CFG.Node(f"{name}_exit_{self.function_counter}")

        exit.is_end = True

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

    def make_alloc_node(self):
        self.alloc_counter += 1
        return CFG.Node(f"alloc_{self.alloc_counter}")

    def make_block_read_node(self):
        self.block_read_counter += 1
        return CFG.Node(f"block_read_{self.block_read_counter}")

    def make_block_write_node(self):
        self.block_write_counter += 1
        return CFG.Node(f"block_write_{self.block_write_counter}")

    def make_opt_node(self):
        self.optimization_counter += 1
        return CFG.Node(f"opt_{self.optimization_counter}")

    def make_copy_node(self):
        self.copy_counter += 1
        return CFG.Node(f"copy_{self.copy_counter}")

    def add_edge(self, source: Node, dest: Node, command: Command):
        edge = CFG.Edge(source, dest, command)

        self.edges.append(edge)

    def get_nodes(self) -> set[Node]:
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

    def topo_sort_nodes(self) -> list[Node]:
        visited_nodes = set()

        sorted_nodes = []

        def dfs_node(current_node: CFG.Node):
            if current_node in visited_nodes:
                return

            visited_nodes.add(current_node)

            sorted_nodes.append(current_node)

            for e in sorted(self.get_outgoing(current_node), key=lambda x: str(x)):
                dfs_node(e.dest)

        for node in self.get_nodes():
            if node.is_start:
                dfs_node(node)

        return sorted_nodes

    def topo_sort_edges(self) -> list[Edge]:
        visited_nodes = set()

        sorted_edges = []

        def dfs_node(current_node: CFG.Node):
            if current_node in visited_nodes:
                return

            visited_nodes.add(current_node)

            for e in sorted(self.get_outgoing(current_node), key=lambda x: str(x)):
                dfs_node(e.dest)
                sorted_edges.append(e)

        for node in sorted(self.get_nodes(), key=lambda x: str(x)):
            if node.is_start:
                dfs_node(node)

        return sorted_edges[::-1]

    def sort_nodes(self, type: Literal['forward', 'backward']):
        sorted_nodes = self.topo_sort_nodes()

        if type == 'backward':
            rev = sorted_nodes[::-1]
            return rev
        elif type == 'forward':
            return sorted_nodes

    def to_dot(self):
        dot = graphviz.Digraph()

        nodes = self.sort_nodes('forward')

        for node in sorted(nodes, key=lambda x: str(x)):

            if node.is_start:
                dot.node(node.name, label="<"+str(node) + ">",
                         shape='box', style="filled", fillcolor='green')
                continue
            elif node.is_end:
                dot.node(node.name, label="<"+str(node) + ">",
                         shape='box', style="filled", fillcolor='green')
                continue

            if len(self.get_outgoing(node)) >= 2:
                dot.node(node.name, label="<"+str(node) + ">",
                         shape='diamond', style="filled", fillcolor='yellow')
                continue

            fillcolor = 'orange' if node.age == 0 else 'white'
            dot.node(node.name, label="<"+str(node) + ">",
                     style="filled", fillcolor=fillcolor)

        for edge in sorted(self.edges, key=lambda x: str(x)):
            # set label to empty string
            src = edge.source
            dest = edge.dest

            linecolor = 'red' if edge.age == 0 else 'black'

            dot.edge(src.name, dest.name, label="<"+str(edge.command) + ">",
                     color=linecolor, fontcolor=linecolor)

        for node in nodes:
            node.age += 1
        for edge in self.edges:
            edge.age += 1

        return dot

    def __str__(self):
        edge_str = self.topo_sort_edges()

        s = ""
        s += "Filename: "+(self.filename) + "\n"
        for edge in edge_str:
            s += "\t"+repr(edge) + "\n"

        return s

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

    def find_node(self, name: str) -> Node | None:
        for node in self.get_nodes():
            if name in node.name:
                return node

        return None

    def duplicate_subgraph(self, start: Node, end: Node) -> tuple[Node, Node]:

        visited = set()

        node_mappping = {}

        start_copy = self.make_copy_node()
        end_copy = self.make_copy_node()

        node_mappping[start] = start_copy
        node_mappping[end] = end_copy

        def dfs(node: CFG.Node):

            for edge in self.get_outgoing(node):
                if edge in visited:
                    continue

                visited.add(edge)

                if edge.source not in node_mappping:
                    node_mappping[edge.source] = self.make_copy_node()
                if edge.dest not in node_mappping:
                    node_mappping[edge.dest] = self.make_copy_node()

                self.add_edge(node_mappping[edge.source],
                              node_mappping[edge.dest], edge.command)

                dfs(edge.dest)

        dfs(start)

        return start_copy, end_copy
