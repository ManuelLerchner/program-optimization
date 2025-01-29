

from typing import Any

from src.analyses.analysis import Analysis
from src.analyses.interval import (DIntervalLatticeElement, IntervalAnalysis,
                                   abstract_eval_interval)
from src.cfg.cfg import CFG
from src.cfg.IMP.command import NegCommand, PosCommand, SkipCommand
from src.lattices.interval_lattice import IntervalLattice
from src.transformations.transformation import SingleStepTransformation


class Transformation_5_0(SingleStepTransformation):
    def __init__(self, widen: bool = True) -> None:
        self.IA = IntervalAnalysis(widen)

    @staticmethod
    def name() -> str:
        return "T5"

    @staticmethod
    def description() -> str:
        return "Perform interval analysis and delete unreachable nodes"

    def dependencies(self):
        return [self.IA]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:
        """
        Transformation 4
        bot -> delete[node]
        """

        D: dict[CFG.Node, DIntervalLatticeElement] = analyses_results[self.IA]

        for node in cfg.get_nodes():
            if D[node] == '⊥':
                incoming_edges = cfg.get_incoming(node)
                outgoing_edges = cfg.get_outgoing(node)

                for edge in incoming_edges | outgoing_edges:
                    cfg.edges.remove(edge)

        edge_copy = cfg.edges.copy()
        for edge in edge_copy:
            U = edge.source

            abstact_state = D[U]

            if abstact_state == '⊥':
                continue

            if type(edge.command) == PosCommand:
                expr = edge.command.expr

                if not IntervalLattice.leq((0, 0), abstract_eval_interval(expr, abstact_state)):
                    edge.command = SkipCommand()

                if IntervalLattice.eq((0, 0), abstract_eval_interval(expr, abstact_state)):
                    cfg.edges.remove(edge)

            elif type(edge.command) == NegCommand:
                expr = edge.command.expr

                if IntervalLattice.eq((0, 0), abstract_eval_interval(expr, abstact_state)):
                    edge.command = SkipCommand()

                if not IntervalLattice.leq((0, 0), abstract_eval_interval(expr, abstact_state)):
                    cfg.edges.remove(edge)

        return cfg
