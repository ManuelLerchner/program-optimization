
from typing import Any, List, Literal

from analyses.analysis import Analysis
from cfg.cfg import CFG
from optimizer.solver.round_robin import RoundRobinSolver
from optimizer.solver.worklist import WorklistSolver
from transformations.transformation import Transformation
from util.bcolors import BColors


class Optimizer:
    def __init__(self, cfg: CFG, transformations: List[Transformation], output_path: str = 'output/',
                 widen_strategy: Literal['none', 'loop_separator', 'always'] = 'none', max_narrow_iterations: int = 5, debug: bool = False) -> None:
        self.cfg = cfg
        self.transformations = transformations
        self.output_path = output_path
        self.widen_strategy = widen_strategy
        self.max_narrow_iterations = max_narrow_iterations
        self.debug = debug

    def optimize(self) -> CFG:

        analyses_results: dict[Analysis, dict[CFG.Node, Any]] = {}

        self.cfg.render(f"{self.output_path}{self.cfg.filename}/initial")

        total_iter = 0
        for i, trans in enumerate(self.transformations):

            print(f"{BColors.WARNING}Running transformation:{BColors.ENDC} {
                BColors.OKCYAN}{trans.name()}{BColors.ENDC}")

            for analyses in trans.dependencies():
                print(f"{BColors.WARNING}Running analysis:{BColors.ENDC} {
                    BColors.OKCYAN}{analyses.name()} ({analyses.use_widen=}, {analyses.use_narrow=}){BColors.ENDC}")

                analyses.cfg = self.cfg

                A, it = WorklistSolver(self.widen_strategy,  self.max_narrow_iterations, self.debug).solve(
                    self.cfg, analyses,)

                analyses_results[analyses] = A
                total_iter += it

                for node, state in A.items():
                    node.annotations[analyses] = state

            self.cfg = trans.transform(self.cfg, analyses_results)

            self.cfg.render(
                f"{self.output_path}/{self.cfg.filename}/step_{i+1}_{trans.name()}")

            print()

        print(f"{BColors.OKGREEN}Total iterations:{BColors.ENDC} {total_iter}")

        # clean all annotations
        for node in self.cfg.get_nodes():
            node.annotations = {}

        self.cfg.render(f"{self.output_path}/{self.cfg.filename}/result")

        return self.cfg
