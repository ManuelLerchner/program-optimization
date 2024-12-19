from CFG import CFG
from analysis.available_expr import AvailableExpressions
from parser import Parser
from solver.Solver import Solver
from pycparser.c_generator import CGenerator


def main():
    p = Parser('examples/entry.c', only_func='main')

    cfg = p.parse()

    cfg.render('examples/entry_cfg')

    analysis = AvailableExpressions()
    solver = Solver(cfg, analysis)

    states = solver.solve()

    for node, state in states.items():
        print(node, state)


if __name__ == '__main__':
    main()
