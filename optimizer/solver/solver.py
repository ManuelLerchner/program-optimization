from abc import abstractmethod
from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from util.bcolors import BColors


class Solver:

    PRINT_TEMPLATE_FORWARDS = "                {:<20} {:^20}  --[ {:^30} ]--> {:>20} {:<20}"
    PRINT_TEMPLATE_BACKWARDS = "  {:<20} {:>20} <--[ {:^30} ]--  {:>20} {:>20}"

    @staticmethod
    def print_edge[T](analysis: Analysis[T], edge: CFG.Edge, source_state: T, dest_state: T, new_state: T):
        if (analysis.direction == 'forward'):
            print(Solver.PRINT_TEMPLATE_FORWARDS.format(
                BColors.okblue(str(edge.source.name)),
                BColors.okgreen(analysis.lattice.show(source_state)),
                BColors.okcyan(str(edge.command)),
                BColors.okblue(str(edge.dest.name)),
                # BColors.okgreen(analysis.lattice.show(dest_state)),
                BColors.okgreen(analysis.lattice.show(new_state))
            ))
        elif (analysis.direction == 'backward'):
            print(Solver.PRINT_TEMPLATE_BACKWARDS.format(
                BColors.okblue(edge.dest.name),
                BColors.okgreen(analysis.lattice.show(new_state)),
                # BColors.okgreen(analysis.lattice.show(dest_state)),
                BColors.okcyan(str(edge.command)),
                BColors.okgreen(edge.source.name),
                BColors.okblue(analysis.lattice.show(source_state))
            ))

    @ abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis, debug=False) -> dict[CFG.Node, dict[CFG.Node, Any]]:
        pass
