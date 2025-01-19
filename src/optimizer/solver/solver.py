from abc import abstractmethod
from typing import Any, Tuple

from src.analyses.analysis import Analysis
from src.cfg.cfg import CFG


class Solver:

    @ abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis) -> Tuple[dict[CFG.Node, dict[CFG.Node, Any]], int]:
        pass

    def printEquationSystem(self, cfg: CFG, analysis: Analysis):
   
        for node in cfg.sort_nodes(analysis.direction):

            if analysis.direction == 'forward':
                edges = list(cfg.get_incoming(node))
            else:
                edges = list(map(lambda e: CFG.Edge(e.dest, e.source,
                                                   e.command), cfg.get_outgoing(node)))

            print(analysis.get_equation(node, edges))
