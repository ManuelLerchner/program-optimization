

from typing import Any

from analyses.expression_stores import ExprStores
from analyses.analysis import Analysis
from cfg.cfg import CFG
from cfg.IMP.command import (AssignmentCommand, LoadsCommand, PosCommand,
                             StoresCommand)
from cfg.IMP.expression import ID, Expression, UnaryExpression
from lattices.powerset import Powerset
from transformations.transformation import Transformation
from transformations.transformation_1_1 import Transformation_1_1


class Transformation_3(Transformation):
    def __init__(self):
        self.ES = ExprStores()

    @staticmethod
    def name() -> str:
        return "T3"

    @staticmethod
    def description() -> str:
        return "Substitute expressions with temporary variables if they are available"

    def dependencies(self):
        return [self.ES]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:
        """
        Transformation 3
        e -> sigma(e)
        """

        V: dict[CFG.Node, dict[Expression, Powerset[ID]]
                ] = analyses_results[self.ES]

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
