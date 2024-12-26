from cfg.node import Node
from cfg.command import Command


class Edge:
    def __init__(self, source: Node, dest: Node, command: Command):
        self.source = source
        self.command = command
        self.dest = dest

    def __repr__(self):
        return f"Edge({self.source} -> {self.dest} [{self.command}])"
