
from analyses.pre_dominator import PredominatorAnalysis
from cfg.parser import Parser
from optimizer.optimizer import Optimizer
from transformations.transformation_0 import Transformation_0
from transformations.transformation_1_1 import Transformation_1_1
from transformations.transformation_5_0 import Transformation_5_0
from transformations.transformation_5_1 import Transformation_5_1
from transformations.transformation_5_2 import Transformation_5_2
from transformations.transformation_1_2 import Transformation_1_2
from transformations.transformation_2 import Transformation_2
from transformations.transformation_3 import Transformation_3

from transformations.transformation_4 import Transformation_4
from transformations.transformation_6 import Transformation_6
from transformations.transformation_blank import Transformation_Blank


def test():

    Optimizer(Parser('examples/available_expr.c').parse(), [
        Transformation_1_1(),  Transformation_1_2(), Transformation_0()], debug=True).optimize()

    Optimizer(Parser('examples/dead_variables.c').parse(), [
        Transformation_2(), Transformation_0()], debug=True).optimize()

    Optimizer(Parser('examples/dead_variables2.c').parse(), [
        Transformation_2(), Transformation_0()], debug=True).optimize()

    Optimizer(Parser('examples/true_liveness.c').parse(), [
        Transformation_2(), Transformation_0()], debug=True).optimize()

    Optimizer(Parser('examples/superflous.c').parse(), [
        Transformation_1_1(), Transformation_3(), Transformation_2(), Transformation_0()], debug=True).optimize()

    Optimizer(Parser('examples/decr.c').parse(), [
        Transformation_1_1(), Transformation_1_2(), Transformation_3(), Transformation_2(), Transformation_0()], debug=True).optimize()

    Optimizer(Parser('examples/constant_propagation.c').parse(), [
        Transformation_4(), Transformation_0()], debug=True).optimize()

    Optimizer(Parser('examples/interval_analysis.c').parse(), [
        Transformation_5_0(widen=True), Transformation_0()], widen_strategy="loop_separator", max_narrow_iterations=5, debug=True).optimize()

    Optimizer(Parser('examples/available_expr.c').parse(), [
        Transformation_1_1(), Transformation_1_2(),
        Transformation_0()
    ], debug=True).optimize()

    Optimizer(Parser('examples/very_busy.c').parse(), [
        Transformation_5_1(widen=False), Transformation_5_2(), Transformation_0(force=True)], debug=True).optimize()

    Optimizer(Parser('examples/very_busy_loop_invariant.c').parse(), [
        Transformation_5_1(widen=False), Transformation_5_2(), Transformation_0(force=True)], debug=True).optimize()

    Optimizer(Parser('examples/loop_rotation.c').parse(), [
        Transformation_6(),
    ], debug=True).optimize()


if __name__ == "__main__":
    test()
