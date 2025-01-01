from abc import abstractmethod
from typing import Any, Tuple

from analyses.analysis import Analysis
from cfg.cfg import CFG
from util.bcolors import BColors


class Solver:

    @ abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis) -> Tuple[dict[CFG.Node, dict[CFG.Node, Any]], int]:
        pass
