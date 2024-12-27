
from typing import Dict, Literal, Set
from Lattices.powerset import Powerset
from cfg.command import Command, AssignmentCommand, LoadsCommand, StoresCommand, PosCommand, NegCommand, SkipCommand
from cfg.expression import ID, BinExpression, Constant, Expression, UnaryExpression
from analysis.analysis import Analysis
from Lattices.ZFlat import DLattice, DLatticeElement, IntegerLattice


def abstract_eval(expr: Expression, A: Dict[ID, int | Literal['⊥', '⊤']]) -> DLatticeElement:
    if isinstance(expr, ID):
        if expr in A:
            return A[expr]
        else:
            return "⊤"

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
            return left / right

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
        operand = abstract_eval(expr.operand, A)

        if operand == "⊥":
            return "⊥"

        if operand == "⊤":
            return "⊤"

        if expr.op == '-':
            return -operand

    return "⊤"


def get_vars(expression: Expression) -> Set[ID]:
    if isinstance(expression, ID):
        return {expression}
    if isinstance(expression, Constant):
        return set()
    if isinstance(expression, BinExpression):
        return get_vars(expression.left) | get_vars(expression.right)
    if isinstance(expression, UnaryExpression):
        return get_vars(expression.expr)

    raise Exception("Unknown expression")


def get_vars_command(command: Command) -> Set[Expression]:
    if isinstance(command, SkipCommand):
        return set()
    if isinstance(command, AssignmentCommand):
        return get_vars(command.lvalue) | get_vars(command.expr)
    if isinstance(command, LoadsCommand):
        return get_vars(command.expr) | get_vars(command.rvalue)
    if isinstance(command, StoresCommand):
        return get_vars(command.lhs) | get_vars(command.rhs)
    if isinstance(command, PosCommand):
        return get_vars(command.expr)
    if isinstance(command, NegCommand):
        return get_vars(command.expr)


class ConstantPropagation(Analysis[DLatticeElement]):

    def __init__(self):
        super().__init__(DLattice(), 'forward', "top")

    def name(self):
        return "ConstantPropagation"

    def skip(self, x: DLatticeElement) -> DLatticeElement:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        if not isinstance(lhs, ID):
            return A

        A[lhs] = abstract_eval(rhs, A)

        return A

    def loads(self, lhs: Expression, rhs: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        if not isinstance(lhs, ID):
            return A

        A[lhs] = "⊤"

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
        else:
            return A

    def Neg(self, expr: Expression, A: DLatticeElement) -> DLatticeElement:
        if A == "⊥":
            return A

        v = abstract_eval(expr, A)

        if IntegerLattice.leq(0, v):
            return A
        else:
            return "⊥"
