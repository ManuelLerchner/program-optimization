

from typing import Any, Set

from src.analyses.analysis import Analysis
from src.analyses.available_expr import AvailableExpressions
from src.analyses.very_busy import VeryBusyAnalysis
from src.cfg.cfg import CFG
from src.cfg.IMP.command import AssignmentCommand, Command, SkipCommand
from src.cfg.IMP.expression import Expression
from src.transformations.transformation import SingleStepTransformation
from src.transformations.transformation_1_1 import Transformation_1_1


class Transformation_5_1(SingleStepTransformation):
    def __init__(self) -> None:
        self.VB = VeryBusyAnalysis()
        self.AA = AvailableExpressions()

    @staticmethod
    def name() -> str:
        return "T5_1"

    @staticmethod
    def description() -> str:
        return "Partial Redundancy Elimination, using very busy analysis"

    def dependencies(self):
        return [self.VB, self.AA]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:

        A: dict[CFG.Node, Set[Expression]] = analyses_results[self.AA]
        B: dict[CFG.Node, Set[Expression]] = analyses_results[self.VB]

        edge_copy = cfg.edges.copy()
        nodes = cfg.get_nodes()

        to_insert: list[Command]
        for node in nodes:
            if node.is_end:
                to_insert = sorted([AssignmentCommand(Transformation_1_1.introduce_register(
                    expr), expr) for expr in B[node]], key=lambda x: str(x))

                source = node
                new_target = cfg.make_opt_node()
                for command in to_insert:
                    cfg.add_edge(source, new_target, command)
                    source = new_target
                    new_target = cfg.make_opt_node()

        for edge in edge_copy:
            u = edge.source
            v = edge.dest

            save = A[u] | B[u]

            not_available = B[v] - \
                self.AA.transfer(save, edge.source, edge.command, edge.dest)

            if len(not_available) == 0:
                continue

            to_insert = sorted([AssignmentCommand(Transformation_1_1.introduce_register(
                expr), expr) for expr in not_available], key=lambda x: str(x))

            cfg.edges.remove(edge)

            source = u
            new_target = cfg.make_opt_node()
            for command in [edge.command] + to_insert:
                cfg.add_edge(source, new_target, command)
                source = new_target
                new_target = cfg.make_opt_node()

            cfg.add_edge(source, v, SkipCommand())
        return cfg
