

from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from cfg.IMP.command import SkipCommand
from transformations.transformation import SingleStepTransformation


class Transformation_SSA_Prep(SingleStepTransformation):
    def __init__(self) -> None:
        pass

    @staticmethod
    def name() -> str:
        return "SSA Prep"

    @staticmethod
    def description() -> str:
        return "Prepares Transforms the CFG to SSA form"

    def dependencies(self):
        return []

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:

        for node in sorted(cfg.get_nodes().copy(), key=lambda x: x.name):
            if node.is_start:
                new_node = cfg.make_opt_node()
                n_name = new_node.name
                new_node.is_start = True
                new_node.name = node.name
                new_node.locals = node.locals
                new_node.globals = node.globals

                node.is_start = False
                node.name = n_name
                node.locals = set()
                node.globals = set()

                cfg.add_edge(new_node, node, SkipCommand())

        for node in sorted(cfg.get_nodes().copy(), key=lambda x: x.name):

            incoming_edges = cfg.get_incoming(node)
            if len(incoming_edges) > 1:
                for edge in sorted(incoming_edges, key=lambda x: x.source.name):
                    if type(edge.command) == SkipCommand:
                        continue

                    new_node = cfg.make_opt_node()
                    edge.dest = new_node
                    cfg.add_edge(new_node, node, SkipCommand())

        return cfg
