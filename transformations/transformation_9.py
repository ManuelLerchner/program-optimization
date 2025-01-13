

from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from cfg.IMP.command import AssignmentCommand, FunCallCommand, SkipCommand
from cfg.IMP.expression import ID, Constant
from transformations.transformation import SingleStepTransformation


class Transformation_9(SingleStepTransformation):
    def __init__(self, max_depth=2) -> None:
        self.max_depth = max_depth

    @staticmethod
    def name() -> str:
        return "T9"

    @staticmethod
    def description() -> str:
        return "Inline function calls"

    def dependencies(self):
        return []

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:

        for i in range(self.max_depth):

            for edge in cfg.edges.copy():
                if isinstance(edge.command, FunCallCommand):
                    u = edge.source
                    v = edge.dest

                    fun_name = edge.command.fun
                    fun_cfg_entry = cfg.find_node(f"{fun_name}_entry")
                    fun_cfg_exit = cfg.find_node(f"{fun_name}_exit")

                    if fun_cfg_entry is None or fun_cfg_exit is None:
                        raise Exception(f"Function {fun_name} not found")

                    start, end = cfg.duplicate_subgraph(
                        fun_cfg_entry, fun_cfg_exit)

                    temp = u
                    for local in fun_cfg_entry.locals:
                        next = cfg.make_stmt_node()
                        cfg.add_edge(temp, next, AssignmentCommand(
                            ID(local[1]), Constant(0)))
                        temp = next

                    cfg.edges.remove(edge)
                    cfg.add_edge(temp, start, SkipCommand())
                    cfg.add_edge(end, v, SkipCommand())

        return cfg
