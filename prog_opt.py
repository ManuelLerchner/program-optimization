import argparse

import argcomplete

from analyses.analysis import Analysis
from cfg.parser import Parser
from optimizer.optimizer import Optimizer
from transformations import SingleStepTransformation, Transformation_Blank

available_transformations: dict[str, SingleStepTransformation] = {
    x.name(): x for x in SingleStepTransformation.__subclasses__()}

available_analyses: dict[str, SingleStepTransformation] = {
    x.name(): x for x in Analysis.__subclasses__()}


parser = argparse.ArgumentParser(
    prog="Program Optimization",
    description="Optimize IMP programs using various transformations",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)


parser.add_argument(
    "--file",
    type=str,
    required=True,
    help="Input file to optimize",
)
parser.add_argument(
    "--output",
    type=str,
    required=False,
    help="Output folder to store the optimized files",
)

parser.add_argument(
    "--debug",
    default=True,
    action="store_true",
    help="Enable debug mode",
)
parser.add_argument(
    "--widen_strategy",
    type=str,
    default="none",
    choices=["none", "loop_separator", "always"],
    help="Widening strategy to use",
)
parser.add_argument(
    "--max_narrow_iterations",
    type=int,
    default=5,
    help="Maximum number of narrow iterations",
)

parser.add_argument(
    "--t",
    type=str,
    nargs="+",
    choices=[name for name in sorted(
        available_transformations.keys() | available_analyses.keys())],
    help="Transformations or analyses to run",
)


argcomplete.autocomplete(parser)

if __name__ == '__main__':
    args = parser.parse_args()

    trs: list[SingleStepTransformation] = [
        available_transformations[name]() if name in available_transformations
        else Transformation_Blank(available_analyses[name]()) for name in args.t
    ]

    cfg = Parser(args.file).parse()

    Optimizer(cfg, trs, args.output, args.widen_strategy,
              args.max_narrow_iterations, args.debug).optimize()
