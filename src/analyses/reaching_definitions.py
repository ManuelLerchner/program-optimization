
import typing
from typing import Tuple

from src.cfg.IMP.command import Command, ParallelAssigmentCommand, SkipCommand, AssignmentCommand, LoadsCommand, StoresCommand, PosCommand, NegCommand
from src.analyses.analysis import NodeSensitiveAnalysis
from src.cfg.cfg import CFG
from src.cfg.IMP.expression import ID, Expression
from src.lattices.powerset import Powerset


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

    @staticmethod
    def hd(a: tuple):
        x, y = a
        return x

    def format_equation(self, A: CFG.Node, c: Command, B: CFG.Node) -> str:
        if type(c) == SkipCommand:
            return f"{self.wrap_name(A)}"
        elif type(c) == AssignmentCommand:
            return f"({self.wrap_name(A)} - DEFS({c.lvalue}) ∪ ({{({c.lvalue},{B.name})}})"
        elif type(c) == LoadsCommand:
            return f"({self.wrap_name(A)} - DEFS({c.var}) ∪ ({{({c.expr},{B.name})}})"
        elif type(c) == LoadsCommand:
            return f"{self.wrap_name(A)}"
        elif type(c) == StoresCommand:
            return f"{self.wrap_name(A)}"
        elif type(c) == PosCommand:
            return f"{self.wrap_name(A)}"
        elif type(c) == NegCommand:
            return f"{self.wrap_name(A)}"
        elif type(c) == ParallelAssigmentCommand:
            return f"({self.wrap_name(A)} - DEFS({''.join(map(str, map(self.hd, c.assignments)))} ∪ {''.join(map(lambda a: f"({self.hd(a)},{B.name})", c.assignments))})"

        raise ValueError(f"Unknown command type: {c}")
