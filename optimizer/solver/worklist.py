from collections import defaultdict
from typing import Callable, Literal, Tuple

from analyses.analysis import Analysis
from cfg.cfg import CFG
from optimizer.solver.solver import Solver, sort_nodes
from util.bcolors import BColors


class WorklistSolver(Solver):

    def __init__(self, widen_strategy: Literal['none', 'loop_separator', 'always'] = 'none', max_narrow_iterations: int = 0, debug: bool = False) -> None:
        self.widen_strategy = widen_strategy
        self.max_narrow_iterations = max_narrow_iterations
        self.debug = debug

    def perform_step[T](self, analysis: Analysis[T], states: dict[CFG.Node, T], op:  Callable[[CFG.Node], Tuple[str, Callable[[T, T], T]]], worklist: dict[CFG.Node, None]
                        ):
        lattice = analysis.lattice

        node = next(iter(worklist))
        del worklist[node]

        if (analysis.direction == 'forward' and node.is_start) or (
                analysis.direction == 'backward' and node.is_end):
            return

        if analysis.direction == 'forward':
            edges = analysis.cfg.get_incoming(node)
        else:
            edges = set(map(lambda e: CFG.Edge(e.dest, e.source,
                                               e.command), analysis.cfg.get_outgoing(node)))

        fxs = [analysis.transfer(states[edge.source], edge.command)
               for edge in edges]
        incoming = lattice.bot()
        [incoming := lattice.join(fx, incoming) for fx in fxs]

        comb_name, sq = op(node)

        new_state = sq(states[node], incoming)

        if not lattice.eq(new_state, states[node]):
            if self.debug:
                print(f"  {BColors.BOLD}{node.name}{BColors.ENDC} {BColors.OKGREEN}{
                    lattice.show(states[node]):<50}{BColors.ENDC}")
                for edge, fx in zip(edges, fxs):
                    print(f"    {BColors.HEADER}⟵{BColors.ENDC}     {BColors.OKGREEN}{lattice.show(fx):<40}{BColors.ENDC} <--[ {BColors.OKCYAN}{
                        str(edge.command):^15}{BColors.ENDC} ]-- {BColors.OKGREEN}{
                        lattice.show(states[edge.source]):<40}{BColors.ENDC}  {BColors.OKBLUE}{edge.source.name}{BColors.ENDC} ")

                print(f"    {BColors.HEADER}⟶ {'⊔'} f([{BColors.ENDC}{BColors.ENDC}{BColors.OKBLUE}{', '.join([e.source.name for e in edges])}{BColors.ENDC}{BColors.HEADER}]){BColors.ENDC} = {BColors.OKGREEN}{
                    lattice.show(incoming):<40}")

                print(f"    {BColors.FAIL}{comb_name} ⇒ {BColors.ENDC}{BColors.OKGREEN}{
                    lattice.show(new_state):<50}{BColors.ENDC}")

            states[node] = new_state

            new = {e.dest: None for e in analysis.cfg.get_outgoing(node)} if analysis.direction == 'forward' else {
                e.source: None for e in analysis.cfg.get_incoming(node)}

            old = {**worklist}
            worklist.clear()
            worklist.update({**new, **old})

    def find_fixpoint[T](self, phase: str, states: dict[CFG.Node, T], analysis: Analysis[T], comb: Callable[[CFG.Node], Tuple[str, Callable[[T, T], T]]], max_iter=float("inf")) -> int:
        iterations = 0

        worklist = dict.fromkeys(states)

        while worklist and iterations < max_iter:

            if self.debug:
                print(f"\n{BColors.WARNING}{phase} Iteration {
                      iterations+1}{BColors.ENDC}")

            self.perform_step(analysis, states, comb, worklist)
            iterations += 1

        if self.debug and iterations > 0:
            print(f"\n{BColors.WARNING}Analysis results after {
                  iterations} iterations of {phase}{BColors.ENDC}")

            for node in states:
                print(f"{node.name:>15} {
                    BColors.OKGREEN}{
                    analysis.lattice.show(states[node]):<20}{BColors.ENDC}")

        return iterations

    def solve[T](self, cfg: CFG, analysis: Analysis[T]) -> Tuple[dict[CFG.Node, T], int]:
        analysis.lattice = analysis.create_lattice(cfg)

        states: defaultdict[CFG.Node, T] = defaultdict(
            lambda: analysis.lattice.bot(), {n: analysis.lattice.bot() for n in sort_nodes(analysis.direction, cfg)})

        for n in states:
            start = analysis.lattice.top() if analysis.start == 'top' else analysis.lattice.bot()
            if analysis.direction == 'forward' and n.is_start:
                states[n] = start
            elif analysis.direction == 'backward' and n.is_end:
                states[n] = start

        iter = 0

        # forward
        def comb(node: CFG.Node):
            if analysis.use_widen and ((self.widen_strategy == 'loop_separator' and node.is_loop_separator) or self.widen_strategy == 'always'):
                return ("⩏", analysis.lattice.widen,)
            else:
                return ("⊔", analysis.lattice.join)

        iter += self.find_fixpoint("Widening", states, analysis, comb)

        if analysis.use_narrow:
            # backward
            def comb(node: CFG.Node):
                if analysis.use_narrow and ((self.widen_strategy == 'loop_separator' and node.is_loop_separator) or self.widen_strategy == 'always'):
                    return ("⩎", analysis.lattice.narrow)
                else:
                    return ("⊔", analysis.lattice.join)

            iter += self.find_fixpoint("Narrowing", states,
                                       analysis, comb, self.max_narrow_iterations)

        return states, iter
