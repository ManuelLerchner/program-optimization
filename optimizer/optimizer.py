
from typing import List, Any
from analysis.analysis import Analysis
from cfg.cfg import CFG
from solver.fixpoint import FixpointSolver
from transformations.transformation import Transformation
from util.bcolors import BColors


class Optimizer:
    def __init__(self, cfg: CFG, transformations: List[Transformation]):
        self.cfg = cfg
        self.transformations = transformations

    def optimize(self, debug=False) -> CFG:

        analyses_results: dict[Analysis, Any] = {}

        self.cfg.render(f"{self.cfg.path}/{self.cfg.filename}/initial")

        for i, trans in enumerate(self.transformations):

            print(f"{BColors.WARNING}Running transformation:{BColors.ENDC} {
                BColors.OKCYAN}{trans.name()}{BColors.ENDC}")

            for analyses in trans.dependencies():
                print(f"{BColors.WARNING}Running analysis:{BColors.ENDC} {
                    BColors.OKCYAN}{trans.name()}{BColors.ENDC}")

                analyses.cfg = self.cfg

                analyses.prepare()
                A = FixpointSolver.solve(self.cfg, analyses, debug=debug)
                analyses.finish()

                analyses_results[analyses] = A

                if debug:
                    print(f"{BColors.WARNING}Analysis results for {
                        analyses.name()}{BColors.ENDC}")

                for node, state in A.items():

                    if debug:
                        print(f"{node.name:>15} {
                            BColors.OKGREEN}{
                            analyses.lattice.show(state):^20}{BColors.ENDC}")

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
