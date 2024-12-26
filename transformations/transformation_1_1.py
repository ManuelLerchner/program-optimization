

from typing import Any
from analysis.available_expr import AvailableExpressions
from cfg.cfg import CFG
from cfg.command import AssignmentCommand, LoadsCommand, NegCommand, PosCommand, StoresCommand
from cfg.expression import ID, Expression
from transformations.transformation import Transformation


class Transformation_1_1(Transformation):

    @staticmethod
    def introduce_register(expr: Expression) -> ID:
        reg = ID(f"T_{expr.to_short_string()}")
        reg.is_register = True
        return reg

    def name(self) -> str:
        return "Transformation 1.1"

    def transform(self, cfg: CFG, analyses_results: dict[str, Any]) -> CFG:
        """
        Transformation 1.1
        x = e  -->  T_e=e; x = T_e

        branch(expr) --> T_e = expr; branch(T_e)

        """

        edge_copy = cfg.edges.copy()

        for edge in edge_copy:

            ass1: Any = None
            ass2: Any = None

            if type(edge.command) == AssignmentCommand:
                U = edge.source
                V = edge.dest
                lval = edge.command.lvalue
                expr = edge.command.expr

                if not AvailableExpressions.is_worthwile_storing(expr):
                    continue
                T_e = Transformation_1_1.introduce_register(expr)

                ass1 = AssignmentCommand(T_e, expr)
                ass2 = AssignmentCommand(lval, T_e)

                edge.dest = cfg.make_stmt_node()
                edge.command = ass1

                cfg.add_edge(edge.dest, V, ass2)

            elif type(edge.command) == PosCommand:
                U = edge.source
                V = edge.dest
                expr = edge.command.expr
                T_e = Transformation_1_1.introduce_register(expr)

                if not AvailableExpressions.is_worthwile_storing(expr):
                    continue

                ass1 = AssignmentCommand(T_e, expr)

                M = cfg.make_stmt_node()

                pos_edge = None
                neg_edge = None
                for edge in cfg.get_outgoing(U):
                    if type(edge.command) == PosCommand:
                        pos_edge = edge
                    if type(edge.command) == NegCommand:
                        neg_edge = edge

                if pos_edge:
                    pos_edge.command = ass1
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

                if not AvailableExpressions.is_worthwile_storing(expr):
                    continue

                T_e = Transformation_1_1.introduce_register(expr)

                ass1 = AssignmentCommand(T_e, expr)
                ass2 = LoadsCommand(lval, T_e)

                edge.dest = cfg.make_stmt_node()
                edge.command = ass1

                cfg.add_edge(edge.dest, V, ass2)

            elif type(edge.command) == StoresCommand:
                U = edge.source
                V = edge.dest
                lhs = edge.command.lhs
                rhs = edge.command.rhs

                if not AvailableExpressions.is_worthwile_storing(lhs) or not AvailableExpressions.is_worthwile_storing(rhs):
                    continue

                T_lhs = Transformation_1_1.introduce_register(lhs)
                T_rhs = Transformation_1_1.introduce_register(rhs)

                ass1 = AssignmentCommand(T_lhs, lhs)
                ass2 = AssignmentCommand(T_rhs, rhs)
                ass3 = StoresCommand(T_lhs, T_rhs)

                edge.dest = cfg.make_stmt_node()
                edge.command = ass1

                cfg.add_edge(edge.dest, cfg.make_stmt_node(), ass2)
                cfg.add_edge(cfg.make_stmt_node(), V, ass3)

        return cfg
