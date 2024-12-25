from typing import Literal, Any


class Node:

    function_counter = 0
    assignment_counter = 0
    loads_counter = 0
    stores_counter = 0
    skip_counter = 0
    if_counter = 0

    def __init__(self, name: str):
        self.name = name
        self.annotations: dict[str, Any] = {}

    @staticmethod
    def make_function_nodes(name: str):
        Node.function_counter += 1
        entry = Node(f"{name}{Node.function_counter}_entry")
        exit = Node(f"{name}{Node.function_counter}_exit")

        return entry, exit

    @staticmethod
    def make_stmt_node():
        Node.assignment_counter += 1
        return Node(f"stmt_{Node.assignment_counter}")

    @staticmethod
    def make_loads_node():
        Node.loads_counter += 1
        return Node(f"loads_{Node.loads_counter}")

    @staticmethod
    def make_stores_node():
        Node.stores_counter += 1
        return Node(f"stores_{Node.stores_counter}")

    @staticmethod
    def make_skip_node():
        Node.skip_counter += 1
        return Node(f"skip_{Node.skip_counter}")

    @staticmethod
    def make_if_nodes():
        Node.if_counter += 1
        true_entry = Node(f"if_true_{Node.if_counter}")
        false_entry = Node(f"if_false_{Node.if_counter}")

        return true_entry, false_entry

    def __str__(self):

        values = [f"{key}={value}" for key, value in self.annotations.items()]

        return f"{self.name} {values}" if self.annotations else self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name
