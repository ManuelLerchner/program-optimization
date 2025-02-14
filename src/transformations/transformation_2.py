

from typing import Any

from src.analyses.analysis import Analysis
from src.analyses.true_live_variables import TrueLiveVariables
from src.cfg.cfg import CFG
from src.cfg.IMP.command import AssignmentCommand, LoadsCommand, SkipCommand
from src.cfg.IMP.expression import Expression
from src.lattices.powerset import Powerset
from src.transformations.transformation import SingleStepTransformation


class Transformation_2(SingleStepTransformation):

    def __init__(self):
        self.LV = TrueLiveVariables()

    @staticmethod
    def name() -> str:
        return "T2"

    @staticmethod
    def description() -> str:
        return "Delete assignments to variables that are not (truly) live"

    def dependencies(self):
        return [self.LV]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:
        """
        Transformation 1.2
        x = e  --> NOP   if x not in L
        x = M[e] --> NOP if x not in L
        """

        L: dict[CFG.Node, Powerset[Expression]] = analyses_results[self.LV]

        edge_copy = cfg.edges.copy()

        for edge in edge_copy:

            if type(edge.command) == AssignmentCommand:
                V = edge.dest
                lval = edge.command.lvalue

                if lval not in L[V]:
                    edge.command = SkipCommand()

            elif type(edge.command) == LoadsCommand:
                V = edge.dest
                lval = edge.command.var

                if lval not in L[V]:
                    edge.command = SkipCommand()

        return cfg
