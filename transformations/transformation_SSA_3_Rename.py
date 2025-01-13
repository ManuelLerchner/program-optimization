

from ast import Tuple
from typing import Any

from analyses.analysis import Analysis
from analyses.reaching_definitions import ReachingDefinitionsAnalysis
from cfg.IMP.expression import ID, Expression
from cfg.cfg import CFG
from cfg.IMP.command import AssignmentCommand, Command, SkipCommand, PosCommand, NegCommand, StoresCommand, LoadsCommand, ParallelAssigmentCommand
from lattices.powerset import Powerset
from transformations.transformation import SingleStepTransformation
from copy import deepcopy


class Transformation_SSA_Rename(SingleStepTransformation):
    def __init__(self) -> None:
        self.RA = ReachingDefinitionsAnalysis()

    @staticmethod
    def name() -> str:
        return "SSA Rename"

    @staticmethod
    def description() -> str:
        return "Renames variables to SSA form"

    def dependencies(self):
        return [self.RA]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:

        R: dict[CFG.Node, Powerset[tuple[ID, str]]] = analyses_results[self.RA]

        def T(v, phi, command: Command):
            if type(command) == SkipCommand:
                return SkipCommand()
            elif type(command) == AssignmentCommand:
                if not isinstance(command.lvalue, ID):
                    raise Exception("Lvalue of assignment command is not ID")
                return AssignmentCommand(ID(command.lvalue.name+"_"+v.name), phi(command.expr))
            elif type(command) == PosCommand:
                return PosCommand(phi(command.expr))
            elif type(command) == NegCommand:
                return NegCommand(phi(command.expr))
            elif type(command) == StoresCommand:
                return StoresCommand(phi(command.lhs), phi(command.rhs))
            elif type(command) == LoadsCommand:
                if not isinstance(command.var, ID):
                    raise Exception("Var of loads command is not ID")
                return LoadsCommand(ID(command.var.name+"_"+v.name), phi(command.expr))
            elif type(command) == ParallelAssigmentCommand:

                return ParallelAssigmentCommand([(ID(l.name+"_"+v.name), phi(r)) for l, r in command.assignments])
            else:
                raise Exception("Unknown command type")

        for edge in cfg.edges.copy():
            u = edge.source
            v = edge.dest

            def phi(expr: Expression):
                expr = deepcopy(expr)
                for (x_r, u_r) in R[u]:
                    expr.rename(x_r.name, (x_r.name+"_"+u_r))
                return expr

            edge.command = T(v, phi, edge.command)

        return cfg
