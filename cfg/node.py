from typing import TYPE_CHECKING, Any
from collections import defaultdict

if TYPE_CHECKING:
    from analysis.analysis import Analysis


class Node:

    def __init__(self, name: str):
        self.name = name
        self.annotations: defaultdict[Analysis, dict[Node, Any]] = defaultdict(
            lambda: (defaultdict(lambda: "TOP")))

    def __str__(self):

        values = "\n".join(
            [f"{key.name()}={key.lattice.show(value)}" for key, value in self.annotations.items()])

        return f"{self.name}\n{values}" if self.annotations else self.name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        return self.name == other.name
