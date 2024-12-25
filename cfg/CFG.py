
import graphviz

from cfg.Edge import Edge
from cfg.Node import Node
from cfg.Command import Command


class CFG:
    def __init__(self) -> None:
        self.edges: list[Edge] = []

    def add_edge(self, source: Node, dest: Node, command: Command):
        edge = Edge(source, dest, command)

        self.edges.append(edge)

    def get_nodes(self):
        nodes = set()
        for edge in self.edges:
            nodes.add(edge.source)
            nodes.add(edge.dest)

        return nodes

    def get_incoming(self, node: Node):
        incoming = set()
        for edge in self.edges:
            if edge.dest == node:
                incoming.add(edge.source)
        return incoming

    def get_outgoing(self, node: Node):
        outgoing = set()
        for edge in self.edges:
            if edge.source == node:
                outgoing.add(edge.dest)
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
