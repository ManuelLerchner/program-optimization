from analysis.available_expr import AvailableExpressions
from analysis.live_variables import LiveVariables
from analysis.superfluous import Superfluous
from analysis.true_live_variables import TrueLiveVariables
from optimizer.optimizer import Optimizer
from cfg.parser import Parser

from transformations.transformation_1 import RemoveSKIP
from transformations.transformation_1_1 import Transformation_1_1
from transformations.transformation_1_2 import Transformation_1_2
from transformations.transformation_2 import Transformation_2
from transformations.transformation_3 import Transformation_3


def available_expr():
    p = Parser('examples/available_expr.c', only_func='main')

    cfg = p.parse()

    opt = Optimizer(cfg, [
                    Transformation_1_1(), AvailableExpressions(), Transformation_1_2(), RemoveSKIP()])

    opt.optimize(debug=True)


def dead_variables1():
    p = Parser('examples/dead_variables.c', only_func='main')

    cfg = p.parse()

    opt = Optimizer(cfg, [LiveVariables(), Transformation_2(), RemoveSKIP()])

    opt.optimize(debug=True)


def dead_variables2():
    p = Parser('examples/dead_variables2.c', only_func='main')

    cfg = p.parse()

    opt = Optimizer(cfg, [LiveVariables(), Transformation_2(), RemoveSKIP()])

    opt.optimize(debug=True)


def true_liveness():
    p = Parser('examples/true_liveness.c', only_func='main')

    cfg = p.parse()

    opt = Optimizer(cfg, [TrueLiveVariables(),
                    Transformation_2(), RemoveSKIP()])

    opt.optimize(debug=True)


def superflous():
    p = Parser('examples/superflous.c', only_func='main')

    cfg = p.parse()

    opt = Optimizer(cfg, [Transformation_1_1(),Superfluous(),Transformation_3()])

    opt.optimize(debug=True)


def main():
    # available_expr()
    # dead_variables1()
    # dead_variables2()
    # true_liveness()
    superflous()


if __name__ == '__main__':
    main()
