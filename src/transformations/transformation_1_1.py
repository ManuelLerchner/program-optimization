

import typing
from typing import Any

from src.analyses.analysis import Analysis
from src.cfg.cfg import CFG
from src.cfg.IMP.command import (AssignmentCommand, LoadsCommand, NegCommand,
                                 PosCommand, StoresCommand)
from src.cfg.IMP.expression import ID, Expression, MemoryExpression
from src.transformations.transformation import SingleStepTransformation


class Transformation_1_1(SingleStepTransformation):

    @staticmethod
    def introduce_register(expr: Expression) -> ID:
        reg = ID(f"T_{expr.to_short_string()}")

        typing.cast(Any, reg).is_register = True
        return reg

    @staticmethod
    def name() -> str:
        return "T1.1"

    @staticmethod
    def description() -> str:
        return "Introduce temporary variables for expressions"

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, Any]) -> CFG:
        """
        Transformation 1.1
        x = e  -->  T_e=e; x = T_e
        x = M[e]  -->  T_e=e; x = M[T_e]

        branch(expr) --> T_e = expr; branch(T_e)

        """

        edge_copy = cfg.edges.copy()

        for edge in edge_copy:

            ass: Any = None
            ass2: Any = None

            if type(edge.command) == AssignmentCommand:
                U = edge.source
                V = edge.dest
                lval = edge.command.lvalue
                expr = edge.command.expr

                if not expr.is_worthwile_storing():
                    continue
                T_e = Transformation_1_1.introduce_register(expr)

                ass = AssignmentCommand(T_e, expr)
                ass2 = AssignmentCommand(lval, T_e)

                edge.dest = cfg.make_opt_node()
                edge.command = ass

                cfg.add_edge(edge.dest, V, ass2)

            elif type(edge.command) == PosCommand:
                U = edge.source
                V = edge.dest
                expr = edge.command.expr
                T_e = Transformation_1_1.introduce_register(expr)

                if not expr.is_worthwile_storing():
                    continue

                ass = AssignmentCommand(T_e, expr)

                M = cfg.make_opt_node()

                pos_edge = None
                neg_edge = None
                for edge in cfg.get_outgoing(U):
                    if type(edge.command) == PosCommand:
                        pos_edge = edge
                    if type(edge.command) == NegCommand:
                        neg_edge = edge

                if pos_edge:
                    pos_edge.command = ass
                    pos_edge.dest = M
                    cfg.add_edge(M, V, PosCommand(T_e))

                if neg_edge:
                    cfg.edges.remove(neg_edge)
                    cfg.add_edge(M, neg_edge.dest, NegCommand(T_e))

            elif type(edge.command) == LoadsCommand:
                U = edge.source
                V = edge.dest
                lval = edge.command.var
                expr = edge.command.expr

                possible_expressions = [
                    expr, MemoryExpression(ID("M"), expr)]

                # filter out expressions that are not worth storing
                possible_expressions = [
                    e for e in possible_expressions if e.is_worthwile_storing()]

                cfg.edges.remove(edge)

                source = U
                target = cfg.make_opt_node()
                for expr in possible_expressions:
                    T_e = Transformation_1_1.introduce_register(expr)

                    ass = LoadsCommand(T_e, expr.expr) if type(
                        expr) == MemoryExpression else AssignmentCommand(T_e, expr)

                    cfg.add_edge(source, target, ass)
                    source = target
                    target = cfg.make_opt_node()

                cfg.add_edge(source, V,
                             AssignmentCommand(lval, T_e))

            elif type(edge.command) == StoresCommand:
                U = edge.source
                V = edge.dest
                lhs = edge.command.lhs
                rhs = edge.command.rhs

                if not lhs.is_worthwile_storing() or not rhs.is_worthwile_storing():
                    continue

                T_lhs = Transformation_1_1.introduce_register(lhs)
                T_rhs = Transformation_1_1.introduce_register(rhs)

                ass1 = AssignmentCommand(T_lhs, lhs)
                ass2 = AssignmentCommand(T_rhs, rhs)
                ass3 = StoresCommand(T_lhs, T_rhs)

                edge.dest = cfg.make_opt_node()
                edge.command = ass1

                cfg.add_edge(edge.dest, cfg.make_opt_node(), ass2)
                cfg.add_edge(cfg.make_opt_node(), V, ass3)

        return cfg
