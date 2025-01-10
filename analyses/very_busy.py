
from typing import Set
import typing

from analyses.analysis import Analysis, NodeInsensitiveAnalysis
from analyses.live_variables import variables_in_expression
from cfg.IMP.expression import ID, BinExpression, Constant, Expression, UnaryExpression
from analyses.gen_kill_analysis import GenKill
from cfg.cfg import CFG
from lattices.complete_lattice import CompleteLattice
from lattices.powerset import FlippedPowerset, Powerset


class VeryBusyAnalysis(NodeInsensitiveAnalysis[FlippedPowerset[Expression]]):

    def __init__(self):
        super().__init__('backward', 'bot')

    @staticmethod
    def name():
        return "VeryBusy"

    def create_lattice(self, cfg: CFG) -> CompleteLattice[FlippedPowerset[Expression]]:
        return typing.cast(CompleteLattice[FlippedPowerset[Expression]],
                           FlippedPowerset[Expression](cfg.get_all_expressions()))

    def start_node(self, cfg: CFG) -> FlippedPowerset[Expression]:
        return self.lattice.top()

    def skip(self, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        return A

    def assignment(self, lhs: Expression, rhs: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        expr_with_lhs = {
            expr for expr in A if lhs in variables_in_expression(expr)}
        A.difference_update(expr_with_lhs)
        if not isinstance(rhs, ID):
            A.add(rhs)
        return A

    def loads(self, lhs: Expression, rhs: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        expr_with_lhs = {
            expr for expr in A if lhs in variables_in_expression(expr)}
        A.difference_update(expr_with_lhs)
        if not isinstance(rhs, ID):
            A.add(rhs)
        return A

    def stores(self, lhs: Expression, rhs: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        if not isinstance(lhs, ID):
            A.add(lhs)
        if not isinstance(rhs, ID):
            A.add(rhs)
        return A

    def Pos(self, expr: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        if not isinstance(expr, ID):
            A.add(expr)
        return A

    def Neg(self, expr: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        if not isinstance(expr, ID):
            A.add(expr)
        return A
