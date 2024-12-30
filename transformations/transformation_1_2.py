

from typing import Any
from analysis.analysis import Analysis
from analysis.available_expr import AvailableExpressions
from cfg.cfg import CFG
from cfg.command import AssignmentCommand, SkipCommand
from transformations.transformation import Transformation


class Transformation_1_2(Transformation):

    def name(self) -> str:
        return "Transformation 1.2"

    def dependencies(self) -> list[Analysis]:
        self.AE = AvailableExpressions()
        return [self.AE]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, Any]) -> CFG:
        """
        Transformation 1.2
        T_e = e  --> NOP   if e in A
        """

        A = analyses_results[self.AE]

        edge_copy = cfg.edges.copy()

        for edge in edge_copy:

            if type(edge.command) == AssignmentCommand:
                U = edge.source
                V = edge.dest
                lval = edge.command.lvalue
                expr = edge.command.expr

                if expr in A[U]:
                    edge.command = SkipCommand()

        return cfg
