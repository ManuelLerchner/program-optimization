

from ast import Tuple
from typing import Any

from analyses.analysis import Analysis
from analyses.live_variables import LiveVariables
from analyses.reaching_definitions import ReachingDefinitionsAnalysis
from analyses.true_live_variables import TrueLiveVariables
from cfg.cfg import CFG
from cfg.IMP.command import ParallelAssigmentCommand
from cfg.IMP.expression import ID, Expression
from lattices.powerset import Powerset
from transformations.transformation import (TransformationFixpoint)


class Transformation_SSA(TransformationFixpoint):
    def __init__(self) -> None:
        self.LA = LiveVariables()
        self.RA = ReachingDefinitionsAnalysis()

    @staticmethod
    def name() -> str:
        return "SSA"

    @staticmethod
    def description() -> str:
        return "Transforms the CFG to SSA form"

    def dependencies(self):
        return [self.RA, self.LA]

    def transform_until_stable(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> tuple[CFG, bool]:
        R: dict[CFG.Node, Powerset[tuple[ID, str]]] = analyses_results[self.RA]
        L: dict[CFG.Node, Powerset[Expression]] = analyses_results[self.LA]

        changes = False

        for v in cfg.get_nodes().copy():

            incoming_edges = cfg.get_incoming(v)

            start_prev = False
            for edge in incoming_edges:
                if edge.source.is_start:
                    start_prev = True
                    break

            if len(incoming_edges) > 1 or start_prev:
                ass: list[tuple[ID, Expression]] = []

                for l in sorted(L[v], key=lambda x: str(x)):
                    curr = None
                    for edge in incoming_edges:
                        x = set(u for u in R[edge.source] if u[0] == l)

                        if curr is None:
                            curr = x
                        else:
                            if curr != x:
                                ass.append((l, l))
                                break

                for edge in incoming_edges:
                    changes = True

                    if type(edge.command) == ParallelAssigmentCommand and edge.command.assignments == ass:
                        changes = False
                    else:
                        edge.command = ParallelAssigmentCommand(ass)

        return cfg, changes
