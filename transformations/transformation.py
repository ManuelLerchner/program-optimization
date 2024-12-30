from abc import ABC, abstractmethod

from analyses.analysis import Analysis
from cfg.cfg import CFG


class Transformation(ABC):

    def __init__(self):
        pass

    def dependencies(self) -> list[Analysis]:
        return []

    @abstractmethod
    def transform[T](self, cfg: CFG, analyses_results: dict[Analysis[T], dict[CFG.Node, T]]) -> CFG:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
