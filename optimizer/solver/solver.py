from abc import abstractmethod
from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from util.bcolors import BColors


class Solver:

    @ abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis, debug=False) -> dict[CFG.Node, dict[CFG.Node, Any]]:
        pass
