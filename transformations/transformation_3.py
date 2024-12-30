

from typing import Any
from analysis.analysis import Analysis
from analysis.available_expr import AvailableExpressions
from analysis.live_variables import LiveVariables
from analysis.expression_stores import ExprStores
from analysis.true_live_variables import TrueLiveVariables
from cfg.cfg import CFG
from cfg.command import AssignmentCommand, LoadsCommand, PosCommand, SkipCommand, StoresCommand
from cfg.expression import BinExpression, UnaryExpression
from transformations.transformation import Transformation
from transformations.transformation_1_1 import Transformation_1_1


class Transformation_3(Transformation):

    def name(self) -> str:
        return "Transformation 3"

    def dependencies(self):
        self.ES = ExprStores()
        return [self.ES]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, Any]) -> CFG:
        """
        Transformation 3
        e -> sigma(e)
        """

        V = analyses_results[self.ES]

        edge_copy = cfg.edges.copy()

        def substitute(node, var):
            if hasattr(var, 'is_register'):
                return var
            for expr in V[node]:
                if var in V[node][expr]:
                    # check if attribute is a register

                    return Transformation_1_1.introduce_register(expr)
            return var

        for edge in edge_copy:
            U = edge.source

            if type(edge.command) == AssignmentCommand:
                edge.command.expr = substitute(U, edge.command.expr)

            elif type(edge.command) == LoadsCommand:
                edge.command.expr = substitute(U, edge.command.expr)

            elif type(edge.command) == StoresCommand:
                edge.command.lhs = substitute(U, edge.command.lhs)
                edge.command.rhs = substitute(U, edge.command.rhs)

            elif type(edge.command) == PosCommand:
                edge.command.expr = substitute(U, edge.command.expr)

            elif type(edge.command) == UnaryExpression:
                edge.command.expr = substitute(U, edge.command.expr)

        return cfg
