from analysis.Analysis import Analysis
from cfg.CFG import CFG
from cfg.Node import Node
from solver.Solver import Solver


class FixpointSolver(Solver):

    @staticmethod
    def solve[T](cfg: CFG, analysis: Analysis[T]):
        states: dict[Node, T] = {}

        lattice = analysis.lattice

        for node in cfg.get_nodes():
            states[node] = analysis.lattice.bot()

        changed = True
        while changed:
            changed = False
            for edge in cfg.edges:

                dest_state = states[edge.dest]
                source_state = states[edge.source]

                new_state = lattice.join(
                    dest_state, analysis.transfer(source_state, edge.command))

                if not lattice.eq(new_state, dest_state):
                    changed = True
                    states[edge.dest] = new_state

        return states
