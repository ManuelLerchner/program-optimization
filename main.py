from cfg.CFG import CFG
from analysis.available_expr import AvailableExpressions
from parser import Parser
from solver.Fixpoint import FixpointSolver
from solver.Solver import Solver
from pycparser.c_generator import CGenerator


def main():
    p = Parser('examples/entry.c', only_func='main')

    cfg = p.parse()
    cfg.render('examples/entry_cfg')

    analysis = AvailableExpressions()

    states = FixpointSolver.solve(cfg, analysis)

    for node, state in states.items():
        node.annotations[analysis.name()] = state
        print(node)

    cfg.render('examples/entry_cfg_annotated')


if __name__ == '__main__':
    main()
