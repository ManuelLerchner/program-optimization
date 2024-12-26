

from typing import Any
from analysis.available_expr import AvailableExpressions
from cfg.cfg import CFG
from cfg.command import AssignmentCommand, SkipCommand
from transformations.transformation import Transformation


class Transformation_1_2(Transformation):

    def name(self) -> str:
        return "Transformation 1.2"

    def transform(self, cfg: CFG, analyses_results: dict[str, Any]) -> CFG:
        """
        Transformation 1.2
        T_e = e  --> NOP   if e in A
        """

        A = analyses_results[AvailableExpressions().name()]

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
