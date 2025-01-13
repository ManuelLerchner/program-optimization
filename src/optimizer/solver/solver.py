from abc import abstractmethod
from typing import Any, Tuple

from src.analyses.analysis import Analysis
from src.cfg.cfg import CFG


class Solver:

    @ abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis) -> Tuple[dict[CFG.Node, dict[CFG.Node, Any]], int]:
        pass
