

from typing import Any

from src.analyses.analysis import Analysis
from src.cfg.cfg import CFG
from src.cfg.IMP.command import SkipCommand
from src.transformations.transformation import SingleStepTransformation


class Transformation_0(SingleStepTransformation):

    def __init__(self, force=False) -> None:
        self.force = force

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

        def next(u: CFG.Node) -> CFG.Node:
            skip = list(filter(lambda x: isinstance(
                x.command, SkipCommand), cfg.get_outgoing(u)))
            if len(skip) == 0:
                return u
            else:
                n = skip.pop()
                if type(n.command) == SkipCommand and n.command.cfg_keep:
                    return u
                else:
                    return next(n.dest)

        for edge in edges:
            if not isinstance(edge.command, SkipCommand) or edge.command.cfg_keep:
                edge.dest = next(edge.dest)

        for edge in cfg.edges.copy():
            if isinstance(edge.command, SkipCommand) and (not edge.command.cfg_keep):
                u = edge.source
                v = edge.dest
                cfg.edges.remove(edge)

                if u.is_start:
                    v.is_start = True
                    v.name = u.name

                if v.is_end:
                    u.is_end = True
                    u.name = v.name

        return cfg
