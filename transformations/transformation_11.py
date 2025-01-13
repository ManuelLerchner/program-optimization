

from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from cfg.IMP.command import AssignmentCommand, FunCallCommand, SkipCommand
from cfg.IMP.expression import ID, Constant
from transformations.transformation import SingleStepTransformation


class Transformation_11(SingleStepTransformation):
    def __init__(self, max_depth=2) -> None:
        self.max_depth = max_depth

    @staticmethod
    def name() -> str:
        return "T11"

    @staticmethod
    def description() -> str:
        return "Jump to tailecursive functions"

    def dependencies(self):
        return []

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:

        for i in range(self.max_depth):

            for edge in cfg.edges.copy():
                if isinstance(edge.command, FunCallCommand):
                    u = edge.source
                    v = edge.dest

                    if v.is_end:
                        fun_name = edge.command.fun
                        fun_cfg_entry = cfg.find_node(f"{fun_name}_entry")
                        if not fun_cfg_entry:
                            raise Exception(
                                f"Function {fun_name} not found in CFG")

                        cfg.edges.remove(edge)

                        temp = u
                        for local in fun_cfg_entry.locals:
                            next = cfg.make_stmt_node()
                            cfg.add_edge(temp, next, AssignmentCommand(
                                ID(local[1]), Constant(0)))
                            temp = next

                        cfg.add_edge(temp, fun_cfg_entry, SkipCommand())

        return cfg
