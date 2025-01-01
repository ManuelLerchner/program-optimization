
from typing import Any, List

from analyses.analysis import Analysis
from cfg.cfg import CFG
from optimizer.solver.round_robin2 import RoundRobinSolver
from transformations.transformation import Transformation
from util.bcolors import BColors


class Optimizer:
    def __init__(self, cfg: CFG, transformations: List[Transformation]):
        self.cfg = cfg
        self.transformations = transformations

    def optimize(self, debug=False) -> CFG:

        analyses_results: dict[Analysis, dict[CFG.Node, Any]] = {}

        self.cfg.render(f"{self.cfg.path}/{self.cfg.filename}/initial")

        for i, trans in enumerate(self.transformations):

            print(f"{BColors.WARNING}Running transformation:{BColors.ENDC} {
                BColors.OKCYAN}{trans.name()}{BColors.ENDC}")

            for analyses in trans.dependencies():
                print(f"{BColors.WARNING}Running analysis:{BColors.ENDC} {
                    BColors.OKCYAN}{analyses.name()}{BColors.ENDC}")

                analyses.cfg = self.cfg

                A = RoundRobinSolver('always',  narrow_iterations=10, debug=debug).solve(
                    self.cfg, analyses,)

                analyses_results[analyses] = A

                for node, state in A.items():
                    node.annotations[analyses] = state

            self.cfg = trans.transform(self.cfg, analyses_results)

            self.cfg.render(
                f"{self.cfg.path}/{self.cfg.filename}/step_{i+1}_{trans.name()}")

            print()

        # clean all annotations
        for node in self.cfg.get_nodes():
            node.annotations = {}

        self.cfg.render(f"{self.cfg.path}/{self.cfg.filename}/result")

        return self.cfg
