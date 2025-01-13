

from typing import Any

from src.analyses.analysis import Analysis
from src.analyses.available_expr import AvailableExpressions
from src.cfg.cfg import CFG
from src.cfg.IMP.command import AssignmentCommand, LoadsCommand, SkipCommand
from src.cfg.IMP.expression import ID, Expression, MemoryExpression
from src.lattices.powerset import Powerset
from src.transformations.transformation import SingleStepTransformation


class Transformation_1_2(SingleStepTransformation):

    def __init__(self):
        self.AE = AvailableExpressions()

    @staticmethod
    def name() -> str:
        return "T1.2"

    @staticmethod
    def description() -> str:
        return "Delete assignments to temporary variables if the expression is already available"

    def dependencies(self) -> list[Analysis]:
        return [self.AE]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:
        """
        Transformation 1.2
        T_e = e  --> NOP   if e in A
        """

        A: dict[CFG.Node, Powerset[Expression]] = analyses_results[self.AE]

        edge_copy = cfg.edges.copy()

        for edge in edge_copy:

            if type(edge.command) == AssignmentCommand:
                U = edge.source
                expr = edge.command.expr

                if expr in A[U]:
                    edge.command = SkipCommand()

            if type(edge.command) == LoadsCommand:
                U = edge.source
                expr = edge.command.expr

                if MemoryExpression(ID("M"), expr) in A[U]:
                    edge.command = SkipCommand()

        return cfg
