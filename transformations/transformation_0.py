

from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from cfg.IMP.command import SkipCommand
from transformations.transformation import Transformation


class Transformation_0(Transformation):

    @staticmethod
    def name() -> str:
        return "T0"

    @staticmethod
    def description() -> str:
        return "Delete all skip commands"

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, Any]) -> CFG:
        """
        Transformation 1.1
        ;  -->  [delete]

        """

        edges = cfg.edges.copy()

        for edge in edges:
            U = edge.source
            V = edge.dest

            if isinstance(edge.command, SkipCommand):
                incoming_edges = cfg.get_incoming(U)

                if not len(incoming_edges) == 1:
                    continue

                for incoming_edge in incoming_edges:

                    incoming_edge.dest = V

                    for out2 in cfg.get_outgoing(U):
                        out2.source = V

                    cfg.edges.remove(edge)

        edges = cfg.edges.copy()
        for edge in edges:
            U = edge.source
            V = edge.dest

            if isinstance(edge.command, SkipCommand):
                outgoing_edges = cfg.get_outgoing(V)

                if not len(outgoing_edges) == 1:
                    continue

                for outgoing_edge in outgoing_edges:

                    outgoing_edge.source = U
                    for inc2 in cfg.get_incoming(V):
                        inc2.dest = U

                    cfg.edges.remove(edge)

        return cfg
