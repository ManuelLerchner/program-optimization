

from typing import Any, Dict

from src.analyses.analysis import Analysis
from src.analyses.constant_propagation import (ConstantPropagation,
                                               abstract_eval_expr)
from src.cfg.cfg import CFG
from src.cfg.IMP.command import (AssignmentCommand, LoadsCommand, NegCommand,
                                 PosCommand, SkipCommand, StoresCommand)
from src.cfg.IMP.expression import Constant
from src.lattices.d_lattice import DLatticeElement, IntegerLattice
from src.transformations.transformation import SingleStepTransformation


class Transformation_4(SingleStepTransformation):
    def __init__(self):
        self.CP = ConstantPropagation()

    @staticmethod
    def name() -> str:
        return "T4"

    @staticmethod
    def description() -> str:
        return "Perform constant propagation and delete unreachable nodes"

    def dependencies(self):
        return [self.CP]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, dict[CFG.Node, Any]]) -> CFG:
        """
        Transformation 4
        bot -> delete[node]
        """

        P: dict[CFG.Node,
                Dict[str, DLatticeElement]] = analyses_results[self.CP]

        for node in cfg.get_nodes():
            if P[node]["D"] == '⊥':
                incoming_edges = cfg.get_incoming(node)
                outgoing_edges = cfg.get_outgoing(node)

                for edge in incoming_edges | outgoing_edges:
                    cfg.edges.remove(edge)

        edge_copy = cfg.edges.copy()
        for edge in edge_copy:
            U = edge.source

            D, M = P[U]["D"], P[U]["M"]

            if D == '⊥' or M == '⊥':
                continue

            if type(edge.command) == PosCommand:
                expr = edge.command.expr

                if not IntegerLattice.leq(0, abstract_eval_expr(expr, D, M)):
                    edge.command = SkipCommand()

                if IntegerLattice.eq(0, abstract_eval_expr(expr, D, M)):
                    cfg.edges.remove(edge)

            elif type(edge.command) == NegCommand:
                expr = edge.command.expr

                if IntegerLattice.eq(0, abstract_eval_expr(expr, D, M)):
                    edge.command = SkipCommand()

                if not IntegerLattice.leq(0, abstract_eval_expr(expr, D, M)):
                    cfg.edges.remove(edge)

            elif type(edge.command) == AssignmentCommand:
                rhs = edge.command.expr

                simplified_rhs = abstract_eval_expr(rhs, D, M)

                if simplified_rhs == '⊤' or simplified_rhs == '⊥':
                    continue

                edge.command = AssignmentCommand(
                    edge.command.lvalue, Constant(simplified_rhs))

            elif type(edge.command) == LoadsCommand:
                lhs = edge.command.var
                rhs = edge.command.expr

                simplified_rhs = abstract_eval_expr(rhs, D, M)

                if simplified_rhs != '⊤' and simplified_rhs != '⊥':
                    edge.command = AssignmentCommand(
                        lhs, Constant(simplified_rhs))

            elif type(edge.command) == StoresCommand:
                lhs = edge.command.lhs
                rhs = edge.command.rhs

                simplified_rhs = abstract_eval_expr(rhs, D, M)
                simplified_lhs = abstract_eval_expr(lhs, D, M)

                if simplified_lhs != '⊤' and simplified_lhs != '⊥':
                    edge.command.lhs = Constant(simplified_lhs)

                if simplified_rhs != '⊤' and simplified_rhs != '⊥':
                    edge.command.rhs = Constant(simplified_rhs)

        return cfg
