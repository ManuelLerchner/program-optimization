
import sys
from typing import Any, List, Literal

from analyses.analysis import Analysis
from cfg.cfg import CFG
from optimizer.solver.worklist import WorklistSolver
from transformations.transformation import TransformationFixpoint
from util.bcolors import BColors


class Optimizer:
    def __init__(self, cfg: CFG, transformations: List[TransformationFixpoint], output_path: str = 'output/',
                 widen_strategy: Literal['none', 'loop_separator', 'always'] = 'loop_separator', max_narrow_iterations: int = 5, debug: bool = False) -> None:
        self.cfg = cfg
        self.transformations = transformations
        self.output_path = output_path
        self.widen_strategy = widen_strategy
        self.max_narrow_iterations = max_narrow_iterations
        self.debug = debug

    def summarize(self):
        print(f"{BColors.OKGREEN}Optimizer configuration:{BColors.ENDC}")

        print(f"{BColors.OKGREEN}CFG:{BColors.ENDC}")
        print(self.cfg)
        print(f"{BColors.OKGREEN}Transformations:{BColors.ENDC}")
        for t in self.transformations:
            print(f"\t{BColors.OKCYAN}{t.name()}{
                  BColors.ENDC}:\t {t.description()}")
        print(f"{BColors.OKGREEN}Widen strategy:{
              BColors.ENDC} {self.widen_strategy}")
        print(f"{BColors.OKGREEN}Max narrow iterations:{
              BColors.ENDC} {self.max_narrow_iterations}")
        print(f"{BColors.OKGREEN}Debug:{BColors.ENDC} {self.debug}")

        print()

    def optimize(self) -> CFG:
        folder = f"{self.output_path}{self.cfg.filename}/{
            "_".join([t.name() for t in self.transformations])}"

        sys.stdout = open(f"{folder}/log.txt", "w")

        self.summarize()

        analyses_results: dict[Analysis, dict[CFG.Node, Any]] = {}

        self.cfg.render(f"{folder}/initial")

        total_iter = 0
        for i, trans in enumerate(self.transformations):
            changes = True

            fixpoint_counter = 0
            while (changes):

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

                self.cfg, changes = trans.transform_until_stable(
                    self.cfg, analyses_results)
                self.cfg.render(
                    f"{folder}/step_{i+1}_{str(fixpoint_counter)+'_' if changes or fixpoint_counter > 0 else ''}{trans.name()}")
                fixpoint_counter += 1

                # clean all annotations
                for node in self.cfg.get_nodes():
                    node.annotations = {}
                print()

        print(f"{BColors.OKGREEN}Total iterations:{BColors.ENDC} {total_iter}")

        self.cfg.render(f"{folder}/result")

        return self.cfg
