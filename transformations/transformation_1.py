

from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from cfg.IMP.command import SkipCommand
from transformations.transformation import Transformation


class RemoveSKIP(Transformation):

    def name(self) -> str:
        return "RemoveSKIP"

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, Any]) -> CFG:
        """
        Transformation 1.1
        ;  -->  [delete]

        """

        edge_copy = cfg.edges.copy()

        for edge in edge_copy:

            if type(edge.command) == SkipCommand:
                U = edge.source
                V = edge.dest

                cfg.edges.remove(edge)

                for incoming in cfg.get_incoming(U):
                    incoming.dest = V

        return cfg
