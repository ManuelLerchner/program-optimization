from abc import abstractmethod
from analysis.analysis import Analysis
from cfg.cfg import CFG
from cfg.edge import Edge
from cfg.node import Node
from util.bcolors import BColors


class Solver[T]:

    PRINT_TEMPLATE_FORWARDS = "                {:<20} {:^20}  --[ {:^30} ]--> {:>20} {:>20} ====> {:<20}"
    PRINT_TEMPLATE_BACKWARDS = "  {:<20} {:>20} <==== {:<20} <--[ {:^30} ]--  {:>20} {:>20}"

    @staticmethod
    def print_edge(analysis: Analysis[T], edge: Edge, source_state: T, dest_state: T, new_state: T):
        if (analysis.direction == 'forward'):
            print(Solver.PRINT_TEMPLATE_FORWARDS.format(
                BColors.okblue(str(edge.source.name)),
                BColors.okgreen(str(source_state)),
                BColors.okcyan(str(edge.command)),
                BColors.okblue(str(edge.dest.name)),
                BColors.okgreen(str(dest_state)),
                BColors.okgreen(str(new_state)))
            )
        elif (analysis.direction == 'backward'):
            print(Solver.PRINT_TEMPLATE_BACKWARDS.format(
                BColors.okblue(edge.dest.name),
                BColors.okgreen(str(new_state)),
                BColors.okgreen(str(dest_state)),
                BColors.okcyan(str(edge.command)),
                BColors.okgreen(edge.source.name),
                BColors.okblue(str(source_state)))
            )

    @ abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis[T], debug=False) -> dict[Node, T]:
        pass
