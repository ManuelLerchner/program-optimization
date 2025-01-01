from cfg.parser import Parser
from optimizer.optimizer import Optimizer
from transformations.transformation_0 import RemoveSKIP
from transformations.transformation_5 import Transformation_5
from transformations.transformation_4 import Transformation_4
from transformations.transformation_3 import Transformation_3
from transformations.transformation_2 import Transformation_2
from transformations.transformation_1_2 import Transformation_1_2
from transformations.transformation_1_1 import Transformation_1_1
from cfg.parser import Parser


def main():

    Optimizer(Parser('examples/available_expr.c').parse(), [
        Transformation_1_1(),  Transformation_1_2(), RemoveSKIP()], debug=True).optimize()

    Optimizer(Parser('examples/dead_variables.c').parse(), [
        Transformation_2(), RemoveSKIP()], debug=True).optimize()

    Optimizer(Parser('examples/dead_variables2.c').parse(), [
        Transformation_2(), RemoveSKIP()], debug=True).optimize()

    Optimizer(Parser('examples/true_liveness.c').parse(), [
        Transformation_2(), RemoveSKIP()], debug=True).optimize()

    Optimizer(Parser('examples/superflous.c').parse(), [
        Transformation_1_1(), Transformation_3(), Transformation_2(), RemoveSKIP()], debug=True).optimize()

    Optimizer(Parser('examples/decr.c').parse(), [
        Transformation_1_1(), Transformation_1_2(), Transformation_3(), Transformation_2(), RemoveSKIP()], debug=True).optimize()

    Optimizer(Parser('examples/constant_propagation.c').parse(), [
        Transformation_4(), RemoveSKIP()], debug=True).optimize()

    Optimizer(Parser('examples/interval_analysis.c').parse(), [
        Transformation_5(widen=True), RemoveSKIP()], widen_strategy="loop_separator", max_narrow_iterations=5, debug=True).optimize()


if __name__ == '__main__':
    main()
