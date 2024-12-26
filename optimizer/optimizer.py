
from typing import List, Any
from analysis.analysis import Analysis
from cfg.cfg import CFG
from solver.fixpoint import FixpointSolver
from transformations.transformation import Transformation
from util.bcolors import BColors


class Optimizer:
    def __init__(self, cfg: CFG, steps: List[Analysis | Transformation]):
        self.cfg = cfg
        self.steps = steps

    def optimize(self, debug=False) -> CFG:

        analyses_results: dict[str, Any] = {}

        self.cfg.render(f"{self.cfg.path}/{self.cfg.filename}/initial")

        for i, step in enumerate(self.steps):

            if isinstance(step, Analysis):
                print(f"{BColors.WARNING}Running analysis:{BColors.ENDC} {
                    BColors.OKCYAN}{step.name()}{BColors.ENDC}")

                A = FixpointSolver.solve(self.cfg, step, debug=debug)
                analyses_results[step.name()] = A

                if debug:
                    print(f"{BColors.WARNING}Analysis results for {
                          step.name()}{BColors.ENDC}")

                for node, state in A.items():

                    if debug:
                        print(f"{node.name:>15} {BColors.OKBLUE}{str(
                            node.annotations[step.name()][node]):^20}{BColors.ENDC} ===> {BColors.OKGREEN}{str(state):^20}{BColors.ENDC}")

                    node.annotations[step.name()] = state

            elif isinstance(step, Transformation):
                print(f"{BColors.WARNING}Running transformation:{BColors.ENDC} {
                    BColors.OKCYAN}{step.name()}{BColors.ENDC}")

                self.cfg = step.transform(self.cfg, analyses_results)

            self.cfg.render(
                f"{self.cfg.path}/{self.cfg.filename}/step_{i+1}_{step.name()}")

            print()

        # clean all annotations
        for node in self.cfg.get_nodes():
            node.annotations = {}

        self.cfg.render(f"{self.cfg.path}/{self.cfg.filename}/result")

        return self.cfg
