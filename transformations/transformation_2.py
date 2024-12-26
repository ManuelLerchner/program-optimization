

from typing import Any
from analysis.available_expr import AvailableExpressions
from analysis.live_variables import LiveVariables
from analysis.true_live_variables import TrueLiveVariables
from cfg.cfg import CFG
from cfg.command import AssignmentCommand, LoadsCommand, SkipCommand
from transformations.transformation import Transformation


class Transformation_2(Transformation):

    def name(self) -> str:
        return "Transformation 2"

    def transform(self, cfg: CFG, analyses_results: dict[str, Any]) -> CFG:
        """
        Transformation 1.2
        x = e  --> NOP   if x not in L
        x = M[e] --> NOP if x not in L
        """

        source = LiveVariables().name() if LiveVariables(
        ).name() in analyses_results else TrueLiveVariables().name()

        L = analyses_results[source]

        edge_copy = cfg.edges.copy()

        for edge in edge_copy:

            if type(edge.command) == AssignmentCommand:
                U = edge.source
                V = edge.dest
                lval = edge.command.lvalue

                if lval not in L[V]:
                    edge.command = SkipCommand()

            elif type(edge.command) == LoadsCommand:
                U = edge.source
                V = edge.dest
                lval = edge.command.var

                if lval not in L[V]:
                    edge.command = SkipCommand()

        return cfg
