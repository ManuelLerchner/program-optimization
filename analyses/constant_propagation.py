
from typing import Callable, DefaultDict

from analyses.analysis import Analysis
from cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                UnaryExpression)
from lattices.d_lattice import (DLattice, DLatticeElement, IntegerLattice,
                                IntegerLatticeElement)


def abstract_eval(expr: Expression, A: DefaultDict[ID, IntegerLatticeElement]) -> IntegerLatticeElement:
    if isinstance(expr, ID):
        return A[expr]

    if isinstance(expr, Constant):
        return int(expr.value)

    if isinstance(expr, BinExpression):
        left = abstract_eval(expr.left, A)
        right = abstract_eval(expr.right, A)

        if left == "⊥" or right == "⊥":
            return "⊥"

        if left == "⊤" or right == "⊤":
            return "⊤"

        if expr.op == '+':
            return left + right
        if expr.op == '-':
            return left - right
        if expr.op == '*':
            return left * right
        if expr.op == '/':
            return left // right

        if expr.op == '<':
            return 1 if left < right else 0
        if expr.op == '<=':
            return 1 if left <= right else 0
        if expr.op == '>':
            return 1 if left > right else 0
        if expr.op == '>=':
            return 1 if left >= right else 0
        if expr.op == '==':
            return 1 if left == right else 0
        if expr.op == '!=':
            return 1 if left != right else 0

    if isinstance(expr, UnaryExpression):
        e = abstract_eval(expr.expr, A)

        if e == "⊥":
            return "⊥"

        if e == "⊤":
            return "⊤"

        if expr.op == '-':
            return -e
        if expr.op == '!':
            return 1 if e == 0 else 0

    raise Exception("Unknown expression")


class ConstantPropagation(Analysis[DLatticeElement]):

    def __init__(self):
        super().__init__('forward', "top")

    def create_lattice(self, cfg):
        self.lattice = DLattice(cfg.get_all_vars())

    def name(self):
        return "ConstantPropagation"

    def skip(self, x: DLatticeElement) -> DLatticeElement:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        if not isinstance(lhs, ID):
            return A

        A.update({lhs: abstract_eval(rhs, A)})

        return A

    def loads(self, lhs: Expression, rhs: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        if not isinstance(lhs, ID):
            return A

        A.update({lhs: "⊤"})

        return A

    def stores(self, lhs: Expression, rhs: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        return A

    def Pos(self, expr: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        v = abstract_eval(expr, A)

        if v == 0:
            return "⊥"
        elif v == 1:
            return A
        else:
            if type(expr) == BinExpression and expr.op == '==':
                A.update({expr.left: IntegerLattice.meet(
                    A[expr.left], abstract_eval(expr.right, A))})

            return A

    def Neg(self, expr: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        v = abstract_eval(expr, A)

        if v == 0:
            return A
        elif v == 1:
            return "⊥"
        else:
            if type(expr) == BinExpression and expr.op == '!=':
                A.update({expr.left: IntegerLattice.meet(
                    A[expr.left], abstract_eval(expr.right, A))})

            return A
