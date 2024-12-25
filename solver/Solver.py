from abc import abstractmethod
from analysis.Analysis import Analysis
from cfg.CFG import CFG
from cfg.Node import Node


class Solver[T]:

    @abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis[T]) -> dict[Node, T]:
        pass
