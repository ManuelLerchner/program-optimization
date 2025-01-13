

from typing import Any

from src.analyses.analysis import Analysis
from src.cfg.cfg import CFG
from src.cfg.IMP.command import (AssignmentCommand, LoadsCommand, NegCommand,
                                 PosCommand, StoresCommand)
from src.cfg.IMP.expression import (ID, Expression)
from src.transformations.transformation import SingleStepTransformation
from src.transformations.transformation_1_1 import Transformation_1_1


class Transformation_5_2(SingleStepTransformation):
    def __init__(self) -> None:
        pass

    @staticmethod
    def name() -> str:
        return "T5_2"

    @staticmethod
    def description() -> str:
        return "Canonize all uses of expressions"

    def dependencies(self):
        return []

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:
        """
        Transformation 4
        bot -> delete[node]
        """

        def should_canonize(expr: Expression) -> bool:
            return expr.is_worthwile_storing()

        for edge in cfg.edges:
            command = edge.command

            if type(command) == AssignmentCommand:
                lval = command.lvalue
                expr = command.expr

                if isinstance(lval, ID) and hasattr(lval, "is_register") and lval.is_register:
                    continue

                if should_canonize(lval):
                    command.lvalue = Transformation_1_1.introduce_register(
                        lval)

                if should_canonize(expr):
                    command.expr = Transformation_1_1.introduce_register(expr)

            elif type(command) == LoadsCommand:
                var = command.var
                expr = command.expr

                if isinstance(var, ID) and hasattr(var, "is_register") and var.is_register:
                    continue

                if should_canonize(var):
                    command.var = Transformation_1_1.introduce_register(var)

                if should_canonize(expr):
                    command.expr = Transformation_1_1.introduce_register(expr)

            elif type(command) == StoresCommand:
                lhs = command.lhs
                rhs = command.rhs

                if isinstance(lhs, ID) and hasattr(lhs, "is_register") and lhs.is_register:
                    continue

                if should_canonize(lhs):
                    command.lhs = Transformation_1_1.introduce_register(lhs)

                if should_canonize(rhs):
                    command.rhs = Transformation_1_1.introduce_register(rhs)

            elif type(command) == NegCommand or type(command) == PosCommand:
                expr = command.expr

                if should_canonize(expr):
                    command.expr = Transformation_1_1.introduce_register(expr)

        return cfg
