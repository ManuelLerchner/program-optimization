

from typing import Any, List

from analyses.analysis import Analysis
from analyses.pre_dominator import PredominatorAnalysis
from cfg.cfg import CFG
from cfg.IMP.command import (NegCommand,
                             PosCommand)
from transformations.transformation import SingleStepTransformation


class Transformation_6(SingleStepTransformation):
    def __init__(self) -> None:
        self.PD = PredominatorAnalysis()

    @staticmethod
    def name() -> str:
        return "T6"

    @staticmethod
    def description() -> str:
        return "Loop Rotation"

    def dependencies(self):
        return [self.PD]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:

        P: dict[CFG.Node, set[str]] = analyses_results[self.PD]

        def is_loop_head(node: CFG.Node) -> tuple[CFG.Node, List[CFG.Edge], List[CFG.Edge]]:
            neg = [x for x in cfg.get_outgoing(
                node) if type(x.command) == NegCommand]
            pos = [x for x in cfg.get_outgoing(
                node) if type(x.command) == PosCommand]

            return node, neg, pos

        for node in cfg.get_nodes():
            incoming_edges = cfg.get_incoming(node)

            v, neg, pos = is_loop_head(node)

            if len(neg) == 1 and len(pos) == 1:
                neg_edge = neg[0]
                pos_edge = pos[0]
                u1 = neg_edge.dest
                u2 = pos_edge.dest
                for inc in incoming_edges:
                    u = inc.source

                    if u2.name in P[u] and v.name in P[u]:
                        print(f"Rotating loop at {node.name}")

                        cfg.edges.remove(inc)

                        new_node = cfg.make_opt_node()

                        cfg.add_edge(u, new_node, inc.command)
                        cfg.add_edge(new_node, u1, neg_edge.command)
                        cfg.add_edge(new_node, u2, pos_edge.command)

        return cfg
