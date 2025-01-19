
import typing

from src.cfg.IMP.command import Command, AssignmentCommand, LoadsCommand, ParallelAssigmentCommand, SkipCommand, StoresCommand, PosCommand, NegCommand
from src.analyses.analysis import NodeSensitiveAnalysis
from src.cfg.cfg import CFG
from src.cfg.IMP.expression import Expression
from src.lattices.powerset import FlippedPowerset, Powerset


class PredominatorAnalysis(NodeSensitiveAnalysis[Powerset[str]]):

    def __init__(self):
        super().__init__('forward', "must")

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

    def format_equation(self, A: CFG.Node, c: Command, B: CFG.Node) -> str:
        return f"{self.wrap_name(A)} ∪ {B.name}"
