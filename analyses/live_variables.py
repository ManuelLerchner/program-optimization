
from typing import Set

from cfg.IMP.expression import ID, BinExpression, Constant, Expression, UnaryExpression, MemoryExpression
from analyses.gen_kill_analysis import GenKill
from lattices.powerset import FlippedPowerset


def variables_in_expression(expr: Expression) -> Set[Expression]:
    if isinstance(expr, ID):
        return {expr}
    elif isinstance(expr, BinExpression):
        return variables_in_expression(expr.left) | variables_in_expression(expr.right)
    elif isinstance(expr, UnaryExpression):
        return variables_in_expression(expr.expr)
    elif isinstance(expr, Constant):
        return set()
    elif isinstance(expr, MemoryExpression):
        return variables_in_expression(expr.expr) | variables_in_expression(expr.array)

    raise ValueError(f"Unknown expression type: {expr}")


class LiveVariables(GenKill[Expression]):

    def __init__(self):
        super().__init__('backward', 'bot')

    @staticmethod
    def name():
        return "LiveVar"

    def create_lattice(self, cfg):
        return FlippedPowerset[Expression](cfg.get_all_expressions())

    def gen_kill_skip(self, A) -> tuple[Set[Expression], Set[Expression]]:
        return set(), set()

    def gen_kill_assignment(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        return variables_in_expression(rhs), d

    def gen_kill_loads(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        return variables_in_expression(rhs), d

    def gen_kill_stores(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(rhs) | variables_in_expression(lhs), set()

    def gen_kill_Pos(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(expr), set()

    def gen_kill_Neg(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(expr), set()
