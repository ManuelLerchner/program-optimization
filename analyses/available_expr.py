from typing import Set

from analyses.analysis import Analysis
from cfg.IMP.expression import (ID, BinExpression, Constant, Expression, MemoryExpression,
                                UnaryExpression)
from lattices.powerset import Powerset


def check_occurence(expr: Expression, lvalue: Expression):
    if isinstance(expr, Constant):
        return False
    if isinstance(expr, ID):
        return expr == lvalue
    elif isinstance(expr, BinExpression):
        return check_occurence(expr.left, lvalue) or check_occurence(expr.right, lvalue)
    elif isinstance(expr, UnaryExpression):
        return check_occurence(expr.expr, lvalue)
    elif isinstance(expr, MemoryExpression):
        return check_occurence(expr.expr, lvalue) or check_occurence(expr.array, lvalue)

    raise Exception("Unknown expression" + str(expr) + str(type(expr)))


class AvailableExpressions(Analysis[Set[Expression]]):

    def __init__(self):
        super().__init__('forward', 'bot')

    @staticmethod
    def name():
        return "AvailExpr"

    def create_lattice(self, cfg):
        return Powerset[Expression]()

    @staticmethod
    def is_worthwile_storing(expr: Expression) -> bool:
        if isinstance(expr, ID) or isinstance(expr, Constant):
            return False

        return True

    def skip(self, x: Set[Expression]) -> Set[Expression]:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, A: Set[Expression]) -> Set[Expression]:

        if self.is_worthwile_storing(rhs):
            A.add(rhs)

        filtered = set([x for x in A if not check_occurence(x, lhs)])

        return filtered

    def loads(self, lhs: Expression, rhs: Expression, A: Set[Expression]) -> Set[Expression]:

        if self.is_worthwile_storing(rhs):
            A.add(rhs)

        A.add(MemoryExpression(ID("M"), rhs))

        filtered = set([x for x in A if not check_occurence(x, lhs)])

        return filtered

    def stores(self, lhs: Expression, rhs: Expression, A: Set[Expression]) -> Set[Expression]:
        e1 = lhs
        e2 = rhs

        if self.is_worthwile_storing(e1):
            A.add(e1)
        if self.is_worthwile_storing(e2):
            A.add(e2)

        # remove all MemoryExpressions that are not in the store
        filtered = set([x for x in A if not isinstance(x, MemoryExpression)])

        return filtered

    def Pos(self, expr: Expression, A: Set[Expression]) -> Set[Expression]:

        if self.is_worthwile_storing(expr):
            A.add(expr)

        return A

    def Neg(self, expr: Expression, A: Set[Expression]) -> Set[Expression]:
        if self.is_worthwile_storing(expr):
            A.add(expr)

        return A
