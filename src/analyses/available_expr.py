from typing import Set

from src.analyses.analysis import NodeInsensitiveAnalysis
from src.cfg.cfg import CFG
from src.cfg.IMP.command import (AssignmentCommand, Command, LoadsCommand,
                                 NegCommand, ParallelAssigmentCommand,
                                 PosCommand, SkipCommand, StoresCommand)
from src.cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                    MemoryExpression, UnaryExpression)
from src.lattices.powerset import FlippedPowerset, Powerset
from src.util.bcolors import BColors


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


class AvailableExpressions(NodeInsensitiveAnalysis[Set[Expression]]):

    def __init__(self):
        super().__init__('forward', 'must')

    @staticmethod
    def name():
        return "AvailExpr"

    def create_lattice(self, cfg):
        expr = cfg.get_all_expressions()
        filtered = set([x for x in expr if x.is_worthwile_storing()])
        return FlippedPowerset[Expression](filtered)

    def start_node(self, cfg: CFG):
        return set()

    def skip(self, x: Set[Expression]) -> Set[Expression]:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, A: Set[Expression]) -> Set[Expression]:

        if rhs.is_worthwile_storing():
            A.add(rhs)

        filtered = set([x for x in A if not check_occurence(x, lhs)])

        return filtered

    def loads(self, lhs: Expression, rhs: Expression, A: Set[Expression]) -> Set[Expression]:

        if rhs.is_worthwile_storing():
            A.add(rhs)

        A.add(MemoryExpression(ID("M"), rhs))

        filtered = set([x for x in A if not check_occurence(x, lhs)])

        return filtered

    def stores(self, lhs: Expression, rhs: Expression, A: Set[Expression]) -> Set[Expression]:
        e1 = lhs
        e2 = rhs

        if e1.is_worthwile_storing():
            A.add(e1)
        if e2.is_worthwile_storing():
            A.add(e2)

        # remove all MemoryExpressions that are not in the store
        filtered = set([x for x in A if not isinstance(x, MemoryExpression)])

        return filtered

    def Pos(self, expr: Expression, A: Set[Expression]) -> Set[Expression]:

        if expr.is_worthwile_storing():
            A.add(expr)

        return A

    def Neg(self, expr: Expression, A: Set[Expression]) -> Set[Expression]:
        if expr.is_worthwile_storing():
            A.add(expr)

        return A

    # string versions of the transfer functions

    def format_equation(self, A: CFG.Node, c: Command) -> str:
        if type(c) == SkipCommand:
            return f"{self.wrap_name(A)}"
        elif type(c) == AssignmentCommand:
            return f"({self.wrap_name(A)} - Occ({c.lvalue})) ∪ ({str(c)})"
        elif type(c) == LoadsCommand:
            return f"({self.wrap_name(A)} - Occ({c.var})) ∪ ({str(c)})"
        elif type(c) == StoresCommand:
            return f"({self.wrap_name(A)} - Occ({c.lhs})) ∪ ({str(c)})"
        elif type(c) == PosCommand:
            return f"{self.wrap_name(A)} ∪ ({str(c)})"
        elif type(c) == NegCommand:
            return f"{self.wrap_name(A)} ∪ ({str(c)})"
        elif type(c) == ParallelAssigmentCommand:
            raise NotImplementedError
        else:
            raise ValueError(f"Unknown command type: {c}")
