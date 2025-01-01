
import typing
from typing import Dict

from analyses.analysis import Analysis
from cfg.IMP.expression import (ID, BinExpression, Constant, Expression,
                                UnaryExpression)
from lattices.combined_lattice import CombinedLattice
from lattices.powerset import Powerset


class ExprStores(Analysis[Dict[Expression, Powerset[ID]]]):

    def __init__(self):
        super().__init__('forward', 'bot')

    def create_lattice(self, cfg):
        expressions = cfg.get_all_expressions()
        expressions = {
            expr for expr in expressions if not isinstance(expr, ID)}

        return CombinedLattice[Expression, Powerset[ID]](
            {expr: Powerset[ID]() for expr in expressions})

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
