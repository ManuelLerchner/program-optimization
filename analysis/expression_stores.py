
from typing import Dict, Set, Tuple
import typing
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


class ExprStores(Analysis[Dict[Expression, Powerset[ID]]]):

    def __init__(self, entries: Dict[Expression, Powerset[ID]] = {}):
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
        return "ExprStores"

    def skip(self, x: Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:
        return x

    def assignment(self, lhs: Expression, rhs: Expression, A: Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:

        if not isinstance(lhs, ID):
            return A

        if isinstance(rhs, ID):
            for expr in A:
                rhs_isin = rhs in A[expr]

                A[expr].discard(lhs)

                if rhs_isin:
                    A[expr].add(lhs)

        if isinstance(rhs, Constant):
            for expr in A:
                if expr == rhs:
                    A[expr].add(lhs)
                else:
                    A[expr].discard(lhs)

        if isinstance(rhs, BinExpression) or isinstance(rhs, UnaryExpression):
            for expr in A:
                if expr == rhs:
                    A[expr] = typing.cast(Powerset[ID], {lhs})
                else:
                    A[expr].discard(lhs)

        return A

    def loads(self, lhs: Expression, rhs: Expression, A: Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:
        if not isinstance(lhs, ID):
            return A

        for expr in A:

            if isinstance(rhs, Constant):
                A[expr].discard(lhs)

            if isinstance(rhs, BinExpression) or isinstance(rhs, UnaryExpression):
                if expr == rhs:
                    A[expr] = typing.cast(Powerset[ID], {})
                else:
                    A[expr].discard(lhs)

        return A

    def stores(self, lhs: Expression, rhs: Expression,  A: Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:
        for expr in A:

            if isinstance(rhs, BinExpression) or isinstance(rhs, UnaryExpression):
                if expr == rhs or expr == lhs:
                    A[expr] = typing.cast(Powerset[ID], {})

        return A

    def Pos(self, expr: Expression, A:  Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:
        for e in A:
            if e == expr:
                A[e] = typing.cast(Powerset[ID], {})

        return A

    def Neg(self, expr: Expression, A:  Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:
        for e in A:
            if e == expr:
                A[e] = typing.cast(Powerset[ID], {})

        return A
