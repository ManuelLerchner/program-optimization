from analysis.available_expr import AvailableExpressions
from optimizer.optimizer import Optimizer
from cfg.parser import Parser

from transformations.transformation_1 import RemoveSKIP
from transformations.transformation_1_1 import Transformation_1_1
from transformations.transformation_1_2 import Transformation_1_2


def main():
    p = Parser('examples/entry.c', only_func='main')

    cfg = p.parse()

    opt = Optimizer(cfg, [
                    Transformation_1_1(), AvailableExpressions(), Transformation_1_2(), RemoveSKIP()])

    opt.optimize()


if __name__ == '__main__':
    main()
