from abc import ABC, abstractmethod
from typing import Any
from cfg.cfg import CFG


class Transformation(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def transform(self, cfg: CFG, analyses_results: dict[str, Any]) -> CFG:
        pass

    @abstractmethod
    def name(self) -> str:
        pass
