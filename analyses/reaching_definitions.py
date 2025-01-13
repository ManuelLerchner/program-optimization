
import typing
from typing import Tuple

from analyses.analysis import NodeSensitiveAnalysis
from cfg.cfg import CFG
from cfg.IMP.expression import ID, Expression
from lattices.powerset import Powerset


class ReachingDefinitionsAnalysis(NodeSensitiveAnalysis[Powerset[Tuple[ID, str]]]):

    def __init__(self):
        super().__init__('forward', "may")

    @staticmethod
    def name():
        return "ReachingDefinitions"

    def create_lattice(self, cfg: CFG):
        variables = cfg.get_all_expressions()
        variables = set([x for x in variables if isinstance(x, ID)])

        return Powerset[Tuple[Expression, str]](set((x, y.name) for x in variables for y in cfg.get_nodes()))

    def start_node(self, cfg: CFG) -> Powerset[Tuple[ID, str]]:
        variables = cfg.get_all_expressions()
        variables = set([x for x in variables if isinstance(x, ID)])

        start = [x for x in cfg.get_nodes() if x.is_start]

        return typing.cast(Powerset[Tuple[ID, str]], {(x, start[0].name) for x in variables})

    def skip(self, A: Powerset[Tuple[ID, str]], u: CFG.Node, v: CFG.Node) -> Powerset[Tuple[ID, str]]:
        return A

    def assignment(self, lhs: Expression, rhs: Expression, A: Powerset[Tuple[ID, str]], u: CFG.Node, v: CFG.Node) -> Powerset[Tuple[ID, str]]:
        expr_with_lhs = {
            expr for expr in A if lhs == expr[0]}
        A.difference_update(expr_with_lhs)

        if isinstance(lhs, ID):
            A.add((lhs, v.name))

        return A

    def loads(self, lhs: Expression, rhs: Expression, A: Powerset[Tuple[ID, str]], u: CFG.Node, v: CFG.Node) -> Powerset[Tuple[ID, str]]:
        expr_with_lhs = {
            expr for expr in A if lhs == expr[0]}
        A.difference_update(expr_with_lhs)

        if isinstance(lhs, ID):
            A.add((lhs, v.name))

        return A

    def stores(self, lhs: Expression, rhs: Expression, A: Powerset[Tuple[ID, str]], u: CFG.Node, v: CFG.Node) -> Powerset[Tuple[ID, str]]:

        return A

    def Pos(self, expr: Expression, A: Powerset[Tuple[ID, str]], u: CFG.Node, v: CFG.Node) -> Powerset[Tuple[ID, str]]:

        return A

    def Neg(self, expr, A, u, v):

        return A

    def ParallelAssigment(self, ass: list[tuple[ID, Expression]], A:  Powerset[Tuple[ID, str]], u: CFG.Node, v: CFG.Node) -> Powerset[Tuple[ID, str]]:

        expr_with_lhs = set()
        for expr in ass:
            for r in A:
                if r[0] == expr[0]:
                    expr_with_lhs.add(r)

        A.difference_update(expr_with_lhs)

        for expr in ass:
            lh = expr[0]
            if isinstance(lh, ID):
                A.add((lh, v.name))

        return A
