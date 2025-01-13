
import typing
from typing import Tuple

from analyses.analysis import NodeSensitiveAnalysis
from cfg.cfg import CFG
from cfg.IMP.expression import (ID, Expression)
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
