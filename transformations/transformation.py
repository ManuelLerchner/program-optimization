from abc import ABC, abstractmethod
from typing import Any
from analysis.analysis import Analysis
from cfg.cfg import CFG


class Transformation(ABC):

    def __init__(self):
        pass

    def dependencies(self) -> list[Analysis]:
        return []

    @abstractmethod
    def transform(self, cfg: CFG, analyses_results: dict[str, Any]) -> CFG:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
