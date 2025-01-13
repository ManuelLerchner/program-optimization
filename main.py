
from cfg.parser import Parser
from optimizer.optimizer import Optimizer
from transformations.transformation_0 import Transformation_0
from transformations.transformation_1_1 import Transformation_1_1
from transformations.transformation_1_2 import Transformation_1_2
from transformations.transformation_2 import Transformation_2
from transformations.transformation_3 import Transformation_3
from transformations.transformation_4 import Transformation_4
from transformations.transformation_5_0 import Transformation_5_0
from transformations.transformation_5_1 import Transformation_5_1
from transformations.transformation_5_2 import Transformation_5_2
from transformations.transformation_6 import Transformation_6
from transformations.transformation_9 import Transformation_9
from transformations.transformation_11 import Transformation_11
from transformations.transformation_SSA_1_Prep import Transformation_SSA_Prep
from transformations.transformation_SSA_2_Calc import Transformation_SSA
from transformations.transformation_SSA_3_Rename import \
    Transformation_SSA_Rename
from transformations.transformation_SSA_4_register_allocation import \
    Register_Allocation

fullPipeline = [
    Transformation_4(), Transformation_5_0(), Transformation_6(), Transformation_1_1(), Transformation_1_2(
    ), Transformation_3(), Transformation_2(), Transformation_5_1(), Transformation_5_2(), Transformation_3(), Transformation_2(),
    Transformation_0()
]


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
        Transformation_5_1(), Transformation_5_2(), Transformation_0(force=True)], debug=True).optimize()

    Optimizer(Parser('examples/very_busy_loop_invariant.c').parse(), [
        Transformation_5_1(), Transformation_5_2(), Transformation_0(force=True)], debug=True).optimize()

    Optimizer(Parser('examples/loop_rotation.c').parse(), [
        Transformation_6(),
    ], debug=True).optimize()

    Optimizer(Parser('examples/big_program.c').parse(),
              fullPipeline, debug=True).optimize()

    Optimizer(Parser('examples/factorial.c').parse(),
              fullPipeline, debug=True).optimize()

    Optimizer(Parser('examples/inline.c').parse(),
              [Transformation_9()], debug=True).optimize()

    Optimizer(Parser('examples/tail_recursive.c').parse(),
              [Transformation_11()], debug=True).optimize()

    Optimizer(Parser('examples/static_single_assigment_form.c').parse(),
              [Transformation_SSA_Prep(), Transformation_SSA(), Transformation_SSA_Rename(), Register_Allocation()], debug=True).optimize()

    Optimizer(Parser('examples/static_single_assigment_form_factorial.c').parse(),
              [Transformation_SSA_Prep(), Transformation_SSA(), Transformation_SSA_Rename(), Register_Allocation()], debug=True).optimize()


if __name__ == "__main__":
    test()
