
from typing import List, Any
from analysis.analysis import Analysis
from cfg.cfg import CFG
from solver.fixpoint import FixpointSolver
from transformations.transformation import Transformation


class Optimizer:
    def __init__(self, cfg: CFG, steps: List[Analysis | Transformation]):
        self.cfg = cfg
        self.steps = steps

    def optimize(self) -> CFG:

        analyses_results: dict[str, Any] = {}

        for i, step in enumerate(self.steps):
            if isinstance(step, Analysis):
                print(f"Running analysis: {step.name()}")

                A = FixpointSolver.solve(self.cfg, step)
                analyses_results[step.name()] = A

                for node, state in A.items():
                    node.annotations[step.name()] = state

            elif isinstance(step, Transformation):
                print(f"Running transformation: {step.name()}")

                self.cfg = step.transform(self.cfg, analyses_results)

            self.cfg.render(f"{self.cfg.filename}_step_{i}")

        # clean all annotations
        for node in self.cfg.get_nodes():
            node.annotations = {}

        self.cfg.render(f"{self.cfg.filename}_step_final")

        return self.cfg
