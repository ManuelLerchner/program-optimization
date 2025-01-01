

from typing import Any

from analyses.analysis import Analysis
from analyses.interval import IntervalAnalysis, abstract_eval, DIntervalLatticeElement
from cfg.cfg import CFG
from cfg.IMP.command import (AssignmentCommand, NegCommand,
                             PosCommand, SkipCommand)
from cfg.IMP.expression import Constant
from lattices.d_lattice import DLatticeElement
from lattices.interval_lattice import IntervalLattice
from transformations.transformation import Transformation


class Transformation_5(Transformation):
    def __init__(self, widen: bool) -> None:
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

                if not IntervalLattice.leq((0, 0), abstract_eval(expr, abstact_state)):
                    edge.command = SkipCommand()

                if IntervalLattice.eq((0, 0), abstract_eval(expr, abstact_state)):
                    cfg.edges.remove(edge)

            elif type(edge.command) == NegCommand:
                expr = edge.command.expr

                if IntervalLattice.eq((0, 0), abstract_eval(expr, abstact_state)):
                    edge.command = SkipCommand()

                if not IntervalLattice.leq((0, 0), abstract_eval(expr, abstact_state)):
                    cfg.edges.remove(edge)

        return cfg
