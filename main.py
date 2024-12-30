from cfg.parser import Parser
from optimizer.optimizer import Optimizer
from transformations.transformation_1 import RemoveSKIP

from transformations.transformation_4 import Transformation_4


def main():

    # from transformations.transformation_1_1 import Transformation_1_1
    # from transformations.transformation_1_2 import Transformation_1_2
    # from transformations.transformation_2 import Transformation_2
    # from transformations.transformation_3 import Transformation_3
    # Optimizer(Parser('examples/available_expr.c', only_func='main').parse(), [
    #     Transformation_1_1(),  Transformation_1_2(), RemoveSKIP()]).optimize(debug=True)

    # Optimizer(Parser('examples/dead_variables.c', only_func='main').parse(), [
    #     Transformation_2(), RemoveSKIP()]).optimize(debug=True)

    # Optimizer(Parser('examples/dead_variables2.c', only_func='main').parse(), [
    #     Transformation_2(), RemoveSKIP()]).optimize(debug=True)

    # Optimizer(Parser('examples/true_liveness.c', only_func='main').parse(), [
    #     Transformation_2(), RemoveSKIP()]).optimize(debug=True)

    # Optimizer(Parser('examples/superflous.c', only_func='main').parse(), [
    #     Transformation_1_1(), Transformation_3(), Transformation_2(), RemoveSKIP()]).optimize(debug=True)

    # Optimizer(Parser('examples/decr.c', only_func='main').parse(), [
    #     Transformation_1_1(), Transformation_1_2(), Transformation_3(), Transformation_2(),          RemoveSKIP()]).optimize(debug=True)

    Optimizer(Parser('examples/constant_propagation.c', only_func='main').parse(), [
        Transformation_4(), RemoveSKIP()]).optimize(debug=True)


if __name__ == '__main__':
    main()
