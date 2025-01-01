from collections import defaultdict
from typing import Callable, Literal, Tuple

from analyses.analysis import Analysis
from cfg.cfg import CFG
from lattices.complete_lattice import CompleteLattice
from optimizer.solver.solver import Solver
from util.bcolors import BColors


def topo_sort_nodes(cfg: CFG) -> list[CFG.Node]:
    visited_nodes = set()

    sorted_nodes = []

    def dfs_node(current_node: CFG.Node):
        if current_node in visited_nodes:
            return

        visited_nodes.add(current_node)

        sorted_nodes.append(current_node)

        for e in cfg.get_outgoing(current_node):
            dfs_node(e.dest)

    for node in cfg.get_nodes():
        if node.is_start:
            dfs_node(node)

    return sorted_nodes


def sort_nodes(type: Literal['forward', 'backward'], cfg: CFG):
    sorted_nodes = topo_sort_nodes(cfg)

    if type == 'backward':
        return sorted_nodes[::-1]
    elif type == 'forward':
        return sorted_nodes


class RoundRobinSolver(Solver):

    def __init__(self, widen_strategy: Literal['none', 'loop_separator', 'always'] = 'none', narrow_iterations: int = 0, debug: bool = False) -> None:
        self.widen_strategy = widen_strategy
        self.narrow_iterations = narrow_iterations
        self.debug = debug

    def perform_round[T](self, analysis: Analysis[T], states: dict[CFG.Node, T], op:  Callable[[CFG.Node], Tuple[str, Callable[[T, T], T]]]) -> bool:
        lattice = analysis.lattice

        changed = False
        for node in states:
            if node.is_start:
                continue

            incoming_edges = analysis.cfg.get_incoming(node)

            fxs = [analysis.transfer(states[edge.source], edge.command)
                   for edge in incoming_edges]

            incoming = lattice.bot()
            [incoming := lattice.join(fx, incoming) for fx in fxs]

            comb_name, sq = op(node)

            new_state = sq(states[node], incoming)

            if not lattice.eq(new_state, states[node]):
                if self.debug:
                    print(f"  {BColors.OKBLUE}{node.name}{BColors.ENDC} {BColors.OKGREEN}{
                        lattice.show(states[node])}{BColors.ENDC}")
                    for edge, fx in zip(incoming_edges, fxs):
                        print(f"    ⟵     {BColors.OKGREEN}{lattice.show(fx):<40}{BColors.ENDC} <--[ {BColors.OKCYAN}{
                            str(edge.command):^15}{BColors.ENDC} ]-- {BColors.OKGREEN}{
                            lattice.show(states[edge.source]):<40}{BColors.ENDC}  {BColors.OKBLUE}{edge.source.name}{BColors.ENDC} ")

                print(f"    {BColors.HEADER}⟶ {'⊔'} = {BColors.ENDC}{BColors.OKGREEN}{
                    lattice.show(incoming)}{BColors.ENDC}")

                changed = True
                states[node] = new_state

                print(f"    {BColors.FAIL}⟶ {comb_name} = {BColors.ENDC}{BColors.OKGREEN}{
                      lattice.show(states[node])}{BColors.ENDC}")

        return changed

    def find_fixpoint[T](self,  states: dict[CFG.Node, T], analysis: Analysis[T], comb: Callable[[CFG.Node], Tuple[str, Callable[[T, T], T]]]) -> dict[CFG.Node, T]:
        iterations = 1
        while True:
            if self.debug:
                print(f"\n{BColors.WARNING}Iteration {
                      iterations}{BColors.ENDC}")

            changed = self.perform_round(analysis, states, comb)
            iterations += 1

            if not changed:
                break

        if self.debug:
            print(f"\n{BColors.WARNING}Analysis results{BColors.ENDC}")

            for node in states:
                print(f"{node.name:>15} {
                    BColors.OKGREEN}{
                    analysis.lattice.show(states[node]):<20}{BColors.ENDC}")

    def solve[T](self, cfg: CFG, analysis: Analysis[T]) -> dict[CFG.Node, T]:
        analysis.lattice = analysis.create_lattice(cfg)

        states: defaultdict[CFG.Node, T] = defaultdict(
            lambda: analysis.lattice.bot(), {n: analysis.lattice.bot() if not n.is_start else analysis.lattice.top()
                                             for n in sort_nodes(analysis.direction, cfg)})

        # forward
        def comb(node: CFG.Node):
            if analysis.widen and ((self.widen_strategy == 'loop_separator' and node.is_loop_separator) or self.widen_strategy == 'always'):
                return ("⩏", analysis.lattice.widen,)
            else:
                return ("⊔", analysis.lattice.join)

        self.find_fixpoint(states, analysis, comb)

        # backward
        def comb(_: CFG.Node):
            return ("⩎", analysis.lattice.narrow)

        self.find_fixpoint(states, analysis, comb)

        return states
