
from typing import Set, Tuple
from Lattices.completeLattice import CompleteLattice
from Lattices.powerset import Powerset
from Lattices.tupleLattice import NamedTupleLattice
from cfg.command import AssignmentCommand, Command, SkipCommand, LoadsCommand, StoresCommand, PosCommand, NegCommand
from cfg.expression import ID, BinExpression, Constant, Expression, UnaryExpression
from analysis.analysis import Analysis


def get_exprs(expr: Command) -> Set[Expression]:
    if isinstance(expr, SkipCommand):
        return set()
    elif isinstance(expr, AssignmentCommand):
        return {expr.expr}
    elif isinstance(expr, LoadsCommand):
        return {expr.expr}
    elif isinstance(expr, StoresCommand):
        return {expr.lhs, expr.rhs}
    elif isinstance(expr, PosCommand):
        return {expr.expr}
    elif isinstance(expr, NegCommand):
        return {expr.expr}
    else:
        raise Exception("Unknown command")


class Superfluous(Analysis[Tuple[Set[ID]]]):

    def __init__(self, entries: dict[Expression, Powerset[ID]] = {}):
        lattice: CompleteLattice = NamedTupleLattice[Expression, Powerset[ID]](
            entries)
        super().__init__(lattice, 'forward')

    def prepare(self):
        expressions = set()
        for edge in self.cfg.edges:
            expressions |= get_exprs(edge.command)

        # filter out IDs
        expressions = {
            expr for expr in expressions if not isinstance(expr, ID)}

        entries = {expr: Powerset[ID]() for expr in expressions}
        self.lattice = NamedTupleLattice[Expression, Powerset[ID]](entries)

    def name(self):
        return "SM"

    def skip(self, x: Tuple[Set[ID]]) -> Tuple[Set[ID]]:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, A: Tuple[Set[ID]]) -> Tuple[Set[ID]]:

        if isinstance(rhs, ID):
            for expr in A:
                A[expr].discard(lhs)

                if rhs in A[expr]:
                    A[expr].add(lhs)

        if isinstance(rhs, Constant):
            for expr in A:
                if expr == rhs:
                    A[rhs].add(lhs)
                else:
                    A[rhs].discard(lhs)

        if isinstance(rhs, BinExpression) or isinstance(rhs, UnaryExpression):
            for expr in A:
                if expr == rhs:
                    A[rhs] = {lhs}
                else:
                    A[rhs].discard(lhs)

        return A

    def loads(self, lhs: Expression, rhs: Expression, A: Tuple[Set[ID]]) -> Tuple[Set[ID]]:
        for expr in A:

            if isinstance(rhs, Constant):
                A[expr].discard(lhs)

            if isinstance(rhs, BinExpression) or isinstance(rhs, UnaryExpression):
                if expr == rhs:
                    A[rhs] = {}
                else:
                    A[rhs].discard(lhs)

        return A

    def stores(self, lhs: Expression, rhs: Expression, A: Tuple[Set[ID]]) -> Tuple[Set[ID]]:
        for expr in A:

            if isinstance(rhs, BinExpression) or isinstance(rhs, UnaryExpression):
                if expr == rhs or expr == lhs:
                    A[rhs] = {}

        return A

    def Pos(self, expr: Expression, A: Tuple[Set[ID]]) -> Tuple[Set[ID]]:
        for e in A:
            if e == expr:
                A[e] = {}

        return A

    def Neg(self, expr: Expression, A: Tuple[Set[ID]]) -> Tuple[Set[ID]]:
        for e in A:
            if e == expr:
                A[e] = {}

        return A
