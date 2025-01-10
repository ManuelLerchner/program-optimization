
from typing import Set
import typing

from analyses.analysis import Analysis, NodeSensitiveAnalysis
from analyses.live_variables import variables_in_expression
from cfg.IMP.expression import ID, BinExpression, Constant, Expression, UnaryExpression
from analyses.gen_kill_analysis import GenKill
from cfg.cfg import CFG
from lattices.complete_lattice import CompleteLattice
from lattices.powerset import FlippedPowerset, Powerset


class PredominatorAnalysis(NodeSensitiveAnalysis[Powerset[str]]):

    def __init__(self):
        super().__init__('forward', "may")

    @staticmethod
    def name():
        return "Predominator"

    def create_lattice(self, cfg: CFG):
        return FlippedPowerset[str](set(x.name for x in cfg.get_nodes()))

    def start_node(self, cfg: CFG) -> Powerset[str]:
        start = [x for x in cfg.get_nodes() if x.is_start]

        return typing.cast(Powerset[str], {start[0].name})

    def skip(self, A: Powerset[str], u: CFG.Node, v: CFG.Node) -> Powerset[str]:
        A.add(v.name)
        return A

    def assignment(self, lhs: Expression, rhs: Expression, A: Powerset[str], u: CFG.Node, v: CFG.Node) -> Powerset[str]:
        A.add(v.name)
        return A

    def loads(self, lhs: Expression, rhs: Expression, A: Powerset[str], u: CFG.Node, v: CFG.Node) -> Powerset[str]:
        A.add(v.name)
        return A

    def stores(self, lhs: Expression, rhs: Expression, A: Powerset[str], u: CFG.Node, v: CFG.Node) -> Powerset[str]:

        A.add(v.name)
        return A

    def Pos(self, expr: Expression, A: Powerset[str], u: CFG.Node, v: CFG.Node) -> Powerset[str]:
        A.add(v.name)

        return A

    def Neg(self, expr, A, u, v):
        A.add(v.name)

        return A
