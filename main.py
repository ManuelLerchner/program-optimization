import argparse
from cfg.parser import Parser
from optimizer.optimizer import Optimizer
from transformations.transformation import Transformation
from transformations.transformation_0 import Transformation_0
from transformations.transformation_5 import Transformation_5
from transformations.transformation_4 import Transformation_4
from transformations.transformation_3 import Transformation_3
from transformations.transformation_2 import Transformation_2
from transformations.transformation_1_2 import Transformation_1_2
from transformations.transformation_1_1 import Transformation_1_1
from cfg.parser import Parser


def test():

    # Optimizer(Parser('examples/available_expr.c').parse(), [
    #     Transformation_1_1(),  Transformation_1_2(), Transformation_0()], debug=True).optimize()

    # Optimizer(Parser('examples/dead_variables.c').parse(), [
    #     Transformation_2(), Transformation_0()], debug=True).optimize()

    # Optimizer(Parser('examples/dead_variables2.c').parse(), [
    #     Transformation_2(), Transformation_0()], debug=True).optimize()

    # Optimizer(Parser('examples/true_liveness.c').parse(), [
    #     Transformation_2(), Transformation_0()], debug=True).optimize()

    # Optimizer(Parser('examples/superflous.c').parse(), [
    #     Transformation_1_1(), Transformation_3(), Transformation_2(), Transformation_0()], debug=True).optimize()

    # Optimizer(Parser('examples/decr.c').parse(), [
    #     Transformation_1_1(), Transformation_1_2(), Transformation_3(), Transformation_2(), Transformation_0()], debug=True).optimize()

    # Optimizer(Parser('examples/constant_propagation.c').parse(), [
    #     Transformation_4(), Transformation_0()], debug=True).optimize()

    # Optimizer(Parser('examples/interval_analysis.c').parse(), [
    #     Transformation_5(widen=True), Transformation_0()], widen_strategy="loop_separator", max_narrow_iterations=5, debug=True).optimize()

    # Optimizer(Parser('examples/available_expr.c').parse(), [
    #     Transformation_1_1(), Transformation_1_2(),
    #     Transformation_0()
    # ], debug=True).optimize()

    Optimizer(Parser('examples/memory.c').parse(), [

    ], debug=True).optimize()


if __name__ == "__main__":
    test()
