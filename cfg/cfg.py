
import graphviz

from cfg.edge import Edge
from cfg.node import Node
from cfg.command import Command


class CFG:

    def __init__(self) -> None:
        self.edges: list[Edge] = []
        self.filename = None

        self.function_counter = 0
        self.assignment_counter = 0
        self.loads_counter = 0
        self.stores_counter = 0
        self.skip_counter = 0
        self.if_counter = 0

    def make_function_nodes(self, name: str):
        self.function_counter += 1
        entry = Node(f"{name}{self.function_counter}_entry")
        exit = Node(f"{name}{self.function_counter}_exit")

        return entry, exit

    def make_stmt_node(self):
        self.assignment_counter += 1
        return Node(f"stmt_{self.assignment_counter}")

    def make_loads_node(self):
        self.loads_counter += 1
        return Node(f"loads_{self.loads_counter}")

    def make_stores_node(self):
        self.stores_counter += 1
        return Node(f"stores_{self.stores_counter}")

    def make_skip_node(self):
        self.skip_counter += 1
        return Node(f"skip_{self.skip_counter}")

    def make_if_nodes(self):
        self.if_counter += 1
        true_entry = Node(f"if_true_{self.if_counter}")
        false_entry = Node(f"if_false_{self.if_counter}")

        return true_entry, false_entry

    def add_edge(self, source: Node, dest: Node, command: Command):
        edge = Edge(source, dest, command)

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
            src = str(edge.source)
            dest = str(edge.dest)
            # node1 = dot.node(src, label="")
            # node2 = dot.node(dest, label="")
            dot.edge(src, dest, label=str(edge.command))
        return dot

    def render(self, filename):
        self.to_dot().render(filename, format='png', cleanup=True)
