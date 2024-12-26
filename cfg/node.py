from typing import Any


class Node:

    def __init__(self, name: str):
        self.name = name
        self.annotations: dict[str, Any] = {}

    def __str__(self):

        values = [f"{key}={value}" for key, value in self.annotations.items()]

        return f"{self.name} {values}" if self.annotations else self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name
