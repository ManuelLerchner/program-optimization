
from typing import DefaultDict

from analyses.analysis import NodeInsensitiveAnalysis
from cfg.cfg import CFG
from cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                UnaryExpression)
from lattices.interval_lattice import (DIntervalLattice,
                                       DIntervalLatticeElement, Interval,
                                       IntervalLattice)


def binary_interval_arithmetic(op: str, a: Interval, b: Interval) -> Interval:
    if a == "⊥" or b == "⊥":
        return "⊥"

    l1, u1 = (a)
    l2, u2 = (b)

    if op == '+':
        return (l1 + l2, u1 + u2)
    if op == '-':
        return (l1 - u2, u1 - l2)
    if op == '*':
        return (min(l1 * l2, l1 * u2, u1 * l2, u1 * u2), max(l1 * l2, l1 * u2, u1 * l2, u1 * u2))
    if op == '/':
        if l2 <= 0 <= u2:
            return (IntervalLattice.top())
        return (min(l1 / l2, l1 / u2, u1 / l2, u1 / u2), max(l1 / l2, l1 / u2, u1 / l2, u1 / u2))
    if op == '==':
        if l1 == l2 and u1 == u2:
            return (1, 1)
        elif u1 < l2 or u2 < l1:
            return (0, 0)
        else:
            return (0, 1)
    if op == '!=':
        if l1 == l2 and u1 == u2:
            return (0, 0)
        elif u1 < l2 or u2 < l1:
            return (1, 1)
        else:
            return (0, 1)
    if op == '<':
        if u1 < l2:
            return (1, 1)
        elif u2 <= l1:
            return (0, 0)
        else:
            return (0, 1)
    if op == '<=':
        if u1 <= l2:
            return (1, 1)
        elif u2 < l1:
            return (0, 0)
        else:
            return (0, 1)
    if op == '>':
        if u2 < l1:
            return (1, 1)
        elif u1 <= l2:
            return (0, 0)
        else:
            return (0, 1)
    if op == '>=':
        if u2 <= l1:
            return (1, 1)
        elif u1 < l2:
            return (0, 0)
        else:
            return (0, 1)

    if op == '&&':
        if l1 == 0 and u1 == 0:
            return (0, 0)
        if l2 == 0 and u2 == 0:
            return (0, 0)
        return (1, 1)

    if op == '||':
        if l1 == 0 and u1 == 0 and l2 == 0 and u2 == 0:
            return (0, 0)
        return (1, 1)

    if op == '%':
        if l2 == 0 and u2 == 0:
            return (IntervalLattice.top())
        if (l1 == u1) and (l2 == u2):
            res = l1 % l2
            return (res, res)
        else:
            return (0, max(abs(l2 - 1), abs(u2 - 1)))

    raise Exception("Unknown operator" + op)


def unary_interval_arithmetic(op: str, a: Interval) -> Interval:
    if a == "⊥":
        return "⊥"

    l, u = (a)

    if op == '-':
        return (-u, -l)
    if op == '!':
        if l == 0 and u == 0:
            return (1, 1)
        else:
            return (0, 0)

    raise Exception("Unknown operator")


def abstract_eval_interval(expr: Expression, A: DefaultDict[ID, Interval]) -> Interval:
    if isinstance(expr, ID):
        return A[expr]

    if isinstance(expr, Constant):
        return (int(expr.value), int(expr.value))

    if isinstance(expr, BinExpression):
        left = abstract_eval_interval(expr.left, A)
        right = abstract_eval_interval(expr.right, A)

        return binary_interval_arithmetic(expr.op, left, right)

    if isinstance(expr, UnaryExpression):
        e = abstract_eval_interval(expr.expr, A)
        return unary_interval_arithmetic(expr.op, e)

    raise Exception("Unknown expression")


class IntervalAnalysis(NodeInsensitiveAnalysis[DIntervalLatticeElement]):

    def __init__(self, widen: bool) -> None:
        super().__init__('forward', "may", use_widen=True, use_narrow=True)
        self.widen = widen

    def create_lattice(self, cfg):
        return DIntervalLattice(cfg.get_all_vars())

    def start_node(self, cfg: CFG):
        return self.lattice.top()

    @staticmethod
    def name():
        return "IntervalAnalysis"

    def skip(self, x: DIntervalLatticeElement) -> DIntervalLatticeElement:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, A: DIntervalLatticeElement) -> DIntervalLatticeElement:
        if A == "⊥":
            return A

        if not isinstance(lhs, ID):
            return A

        A.update({lhs: abstract_eval_interval(rhs, A)})
        return A

    def loads(self, lhs: Expression, rhs: Expression, A: DIntervalLatticeElement) -> DIntervalLatticeElement:
        if A == "⊥":
            return A

        if not isinstance(lhs, ID):
            return A

        A.update({lhs: IntervalLattice.top()})
        return A

    def stores(self, lhs: Expression, rhs: Expression, A: DIntervalLatticeElement) -> DIntervalLatticeElement:
        return A

    def Pos(self, expr: Expression, A: DIntervalLatticeElement) -> DIntervalLatticeElement:
        if A == "⊥":
            return A

        v = abstract_eval_interval(expr, A)

        if v == (0, 0):
            return "⊥"
        else:
            if type(expr) == BinExpression:
                var, new_op, subexpr = (expr.left, expr.op, expr.right) if isinstance(
                    expr.left, ID) else (expr.right, BinExpression.flip_op(expr.op), expr.left)

                sub_expr_interval = abstract_eval_interval(subexpr, A)

                assert sub_expr_interval != "⊥"

                if new_op == '==':
                    A.update({var: IntervalLattice.meet(
                        A[var], sub_expr_interval)})
                elif new_op == '<=':
                    A.update({var: IntervalLattice.meet(
                        A[var], (float("-inf"), sub_expr_interval[1]))})
                elif new_op == '<':
                    A.update({var: IntervalLattice.meet(
                        A[var], (float("-inf"), sub_expr_interval[1] - 1))})
                elif new_op == '>=':
                    A.update({var: IntervalLattice.meet(
                        A[var], (sub_expr_interval[0], float("inf")))})
                elif new_op == '>':
                    A.update({var: IntervalLattice.meet(
                        A[var], (sub_expr_interval[0], float("inf") - 1))})

            return A

    def Neg(self, expr: Expression, A: DIntervalLatticeElement) -> DIntervalLatticeElement:
        if A == "⊥":
            return A

        v = abstract_eval_interval(expr, A)

        if not IntervalLattice.leq((0, 0), v):
            return "⊥"
        else:
            if type(expr) == BinExpression:
                var, new_op, subexpr = (expr.left, expr.op, expr.right) if isinstance(
                    expr.left, ID) else (expr.right, BinExpression.flip_op(expr.op), expr.left)

                sub_expr_interval = abstract_eval_interval(subexpr, A)

                assert sub_expr_interval != "⊥"

                if new_op == '!=':
                    A.update({var: IntervalLattice.meet(
                        A[var], sub_expr_interval)})
                elif new_op == '>=':
                    A.update({var: IntervalLattice.meet(
                        A[var], (float("-inf"), sub_expr_interval[1]-1))})
                elif new_op == '>':
                    A.update({var: IntervalLattice.meet(
                        A[var], (float("-inf"), sub_expr_interval[1]))})
                elif new_op == '<=':
                    A.update({var: IntervalLattice.meet(
                        A[var], (sub_expr_interval[1]-1, float("inf")))})
                elif new_op == '<':
                    A.update({var: IntervalLattice.meet(
                        A[var], (sub_expr_interval[0], float("inf")))})

            return A
