
from typing import Set
from Lattices.powerset import Powerset
from analysis.gen_kill import GenKill
from cfg.expression import ID, BinExpression, Constant, Expression, UnaryExpression
from analysis.analysis import Analysis


def vars(expr: Expression) -> Set[Expression]:
    if isinstance(expr, ID):
        return {expr}
    elif isinstance(expr, BinExpression):
        return vars(expr.left) | vars(expr.right)
    elif isinstance(expr, UnaryExpression):
        return vars(expr.expr)
    else:
        return set()


class LiveVariables(GenKill[Expression]):

    def __init__(self):
        super().__init__(Powerset[Expression](), 'backward', 'may')

    def name(self):
        return "LiveVar"

    def gen_kill_skip(self, A) -> tuple[Set[Expression], Set[Expression]]:
        return set(), set()

    def gen_kill_assignment(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        return vars(rhs), d

    def gen_kill_loads(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        return vars(rhs), d

    def gen_kill_stores(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return vars(rhs) | vars(lhs), set()

    def gen_kill_Pos(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return vars(expr), set()

    def gen_kill_Neg(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return vars(expr), set()
