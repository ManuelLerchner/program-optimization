
import typing
from typing import Dict

from src.cfg.IMP.command import Command, SkipCommand, AssignmentCommand, LoadsCommand, StoresCommand, PosCommand, NegCommand, ParallelAssigmentCommand
from src.analyses.analysis import NodeInsensitiveAnalysis
from src.cfg.cfg import CFG
from src.cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                    MemoryExpression, UnaryExpression)
from src.lattices.combined_lattice import CombinedLattice
from src.lattices.powerset import FlippedPowerset, Powerset


class ExprStores(NodeInsensitiveAnalysis[Dict[Expression, FlippedPowerset[ID]]]):

    def __init__(self):
        super().__init__('forward', 'must')

    def create_lattice(self, cfg):
        expressions = cfg.get_all_expressions()
        exprs = list(expr for expr in expressions if not isinstance(
            expr, ID) and not isinstance(expr, Constant))
        ids = list(expr for expr in expressions if isinstance(expr, ID))

        return CombinedLattice[Expression, Powerset[ID]](
            {expr: FlippedPowerset[ID](set(ids)) for expr in exprs})

    def start_node(self, cfg: CFG):
        return self.lattice.top()

    @staticmethod
    def name():
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

        if isinstance(rhs, BinExpression) or isinstance(rhs, UnaryExpression) or isinstance(rhs, MemoryExpression):
            for expr in A:
                if expr == rhs:
                    A[expr] = typing.cast(Powerset[ID], {lhs})
                else:
                    A[expr].discard(lhs)

        return A

    def loads(self, lhs: Expression, rhs: Expression, A: Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:
        return self.assignment(lhs, MemoryExpression(ID("M"), rhs), A)

    def stores(self, lhs: Expression, rhs: Expression,  A: Dict[Expression, Powerset[ID]]) -> Dict[Expression, Powerset[ID]]:
        for expr in A:
            if type(expr) == MemoryExpression:
                A[expr] = typing.cast(Powerset[ID], set())

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

    def format_equation(self, A: CFG.Node, c: Command) -> str:
        return "Not implemented"
