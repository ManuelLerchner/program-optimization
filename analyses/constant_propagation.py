
from typing import DefaultDict, Dict

from analyses.analysis import Analysis
from cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                MemoryExpression, UnaryExpression)
from lattices.combined_lattice import CombinedLattice
from lattices.d_lattice import (DLattice, DLatticeElement, IntegerLattice,
                                IntegerLatticeElement)


def abstract_eval_expr(expr: Expression, A: DefaultDict[ID, IntegerLatticeElement], M: DefaultDict[ID, IntegerLatticeElement]) -> IntegerLatticeElement:
    if isinstance(expr, ID):
        return A[expr]

    if isinstance(expr, Constant):
        return int(expr.value)

    if isinstance(expr, BinExpression):
        left = abstract_eval_expr(expr.left, A, M)
        right = abstract_eval_expr(expr.right, A, M)

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
        e = abstract_eval_expr(expr.expr, A, M)

        if e == "⊥":
            return "⊥"

        if e == "⊤":
            return "⊤"

        if expr.op == '-':
            return -e
        if expr.op == '!':
            return 1 if e == 0 else 0

    if isinstance(expr, MemoryExpression):
        return M[ID(str(abstract_eval_expr(expr.expr, A, M)))]

    raise Exception("Unknown expression")


class ConstantPropagation(Analysis[Dict[str, DLatticeElement]]):
    def __init__(self):
        super().__init__('forward', "top")

    def create_lattice(self, cfg):
        return CombinedLattice({"D": DLattice(cfg.get_all_vars()), "M": DLattice({})})

    @staticmethod
    def name():
        return "ConstantPropagation"

    def skip(self, x: Dict[str, DLatticeElement]) -> Dict[str, DLatticeElement]:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, P: Dict[str, DLatticeElement]) -> Dict[str, DLatticeElement]:
        A = P["D"]
        M = P["M"]

        if A != "⊥" and M != "⊥" and isinstance(lhs, ID):
            A.update({lhs: abstract_eval_expr(rhs, A, M)})

        return {"D": A, "M": M}

    def loads(self, lhs: Expression, rhs: Expression, P: Dict[str, DLatticeElement]) -> Dict[str, DLatticeElement]:
        A = P["D"]
        M = P["M"]

        if A != "⊥" and M != "⊥" and isinstance(lhs, ID):
            M.update({lhs: abstract_eval_expr(rhs, A, M)})

        return {"D": A, "M": M}

    def stores(self, lhs: Expression, rhs: Expression, P: Dict[str, DLatticeElement]) -> Dict[str, DLatticeElement]:
        A = P["D"]
        M = P["M"]
        if A == "⊥" or M == "⊥":
            return {"D": A, "M": M}

        if abstract_eval_expr(lhs, A, M) == "⊤":
            M = DLattice(set()).top()
        else:
            M.update({ID(str(abstract_eval_expr(lhs, A, M)))
                     : abstract_eval_expr(rhs, A, M)})

        return {"D": A, "M": M}

    def Pos(self, expr: Expression, P: Dict[str, DLatticeElement]) -> Dict[str, DLatticeElement]:
        A = P["D"]
        M = P["M"]

        if A == "⊥" or M == "⊥":
            return {"D": A, "M": M}

        v = abstract_eval_expr(expr, A, M)

        if v == 0:
            return {"D": "⊥", "M": "⊥"}
        elif v == 1:
            return {"D": A, "M": M}
        else:
            if type(expr) == BinExpression and expr.op == '==':
                A.update({expr.left: IntegerLattice.meet(
                    A[expr.left], abstract_eval_expr(expr.right, A, M))})

            return {"D": A, "M": M}

    def Neg(self, expr: Expression, P: Dict[str, DLatticeElement]) -> Dict[str, DLatticeElement]:
        A = P["D"]
        M = P["M"]

        if A == "⊥" or M == "⊥":
            return {"D": A, "M": M}

        v = abstract_eval_expr(expr, A, M)

        if v == 0:
            return {"D": A, "M": M}
        elif v == 1:
            return {"D": "⊥", "M": M}
        else:
            if type(expr) == BinExpression and expr.op == '!=':
                A.update({expr.left: IntegerLattice.meet(
                    A[expr.left], abstract_eval_expr(expr.right, A, M))})

            return {"D": A, "M": M}
