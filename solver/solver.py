from abc import abstractmethod
from analysis.analysis import Analysis
from cfg.cfg import CFG
from cfg.node import Node


class Solver[T]:

    @abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis[T]) -> dict[Node, T]:
        pass
