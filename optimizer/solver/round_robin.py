from collections import defaultdict
from typing import Callable, Literal

from analyses.analysis import Analysis
from cfg.cfg import CFG
from optimizer.solver.solver import Solver
from util.bcolors import BColors


def topo_sort_edges(cfg: CFG) -> list[CFG.Edge]:
    visited_edges = set()
    edge_order = []

    def dfs_edge(current_edge: CFG.Edge):
        if current_edge in visited_edges:
            return

        visited_edges.add(current_edge)

        outgoing_edges = cfg.get_outgoing(current_edge.dest)

        for dep_edge in outgoing_edges:
            dfs_edge(dep_edge)

        edge_order.append(current_edge)

    start_nodes = []
    for node in cfg.get_nodes():
        if len(cfg.get_incoming(node)) == 0:
            start_nodes.append(node)

    for node in start_nodes:
        for edge in cfg.get_outgoing(node):
            dfs_edge(edge)

    return edge_order


def sort_edges(type: Literal['forward', 'backward'], cfg: CFG):
    sorted_edges = topo_sort_edges(cfg)

    if type == 'backward':
        return sorted_edges
    elif type == 'forward':
        return sorted_edges[::-1]


class RoundRobinSolver(Solver):

    def __init__(self, widen_strategy: Literal['none', 'loop_separator', 'always'] = 'none', narrowing: bool = False) -> None:
        self.widen_strategy = widen_strategy
        self.narrowing = narrowing

    def solve[T](self, cfg: CFG, analysis: Analysis[T], debug=False) -> dict[CFG.Node, T]:
        edges = sort_edges(analysis.direction, cfg)
        analysis.lattice = analysis.create_lattice(cfg)
        lattice = analysis.lattice

        def base() -> T:
            return lattice.bot() if analysis.start == 'bot' else lattice.top()

        states: defaultdict[CFG.Node, T] = defaultdict(base)
        narrowing_active = False

        changed = True
        iterations = 1
        while changed:
            changed = False
            if debug:
                print(f"{BColors.WARNING}Iteration {iterations}{BColors.ENDC} {BColors.OKCYAN}{
                      "(narrowing)" if narrowing_active else ""}{BColors.ENDC}")

            for edge in edges:
                src, dest = (edge.source, edge.dest) if analysis.direction == 'forward' else (
                    edge.dest, edge.source)

                source_state = states[src]

                updated_dest = analysis.transfer(source_state, edge.command)

                op = "="
                if dest in states:
                    comb: Callable[[T, T], T]

                    if not narrowing_active and analysis.widen and ((self.widen_strategy == 'loop_separator' and dest.is_loop_separator) or self.widen_strategy == 'always'):
                        comb, op = lattice.widen, "⩏"
                    else:
                        comb, op = lattice.join, "⊔"

                    new_state = comb(states[dest], updated_dest)

                    if not lattice.eq(new_state, states[dest]):
                        changed = True
                else:
                    new_state = updated_dest

                if debug:
                    if not dest in states or not lattice.eq(states[dest], new_state):
                        Solver.print_edge(
                            analysis, edge, source_state, states[dest] if dest in states else lattice.bot(), op, new_state)

                states[dest] = new_state

            iterations += 1

            if self.narrowing and not narrowing_active and not changed:
                changed = True
                narrowing_active = True

        if debug:
            print()
            print(f"{BColors.WARNING}Analysis results{BColors.ENDC}")

            for node, state in states.items():
                print(f"{node.name:>15} {
                    BColors.OKGREEN}{
                    lattice.show(state):<20}{BColors.ENDC}")

        return states
