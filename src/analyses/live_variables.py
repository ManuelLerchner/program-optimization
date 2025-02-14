
from typing import Set

from src.cfg.IMP.command import SkipCommand, AssignmentCommand, LoadsCommand, StoresCommand, PosCommand, NegCommand, ParallelAssigmentCommand, Command
from src.analyses.gen_kill_analysis import GenKill
from src.cfg.cfg import CFG
from src.cfg.IMP.expression import ID, Expression, variables_in_expression
from src.lattices.powerset import Powerset


class LiveVariables(GenKill[Expression]):

    def __init__(self):
        super().__init__('backward', 'may')

    @staticmethod
    def name():
        return "LiveVar"

    def create_lattice(self, cfg):
        expr = cfg.get_all_expressions()
        filtered = set([x for x in expr if type(x) == ID])
        return Powerset[Expression](filtered)

    def start_node(self, cfg: CFG):
        expr = cfg.get_all_expressions()
        if any([type(x) == ID and x.name == "result" for x in expr]):
            return {(ID("result"))}
        else:
            return set()

    def gen_kill_skip(self, A) -> tuple[Set[Expression], Set[Expression]]:
        return set(), set()

    def gen_kill_assignment(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        gen: Set[Expression] = variables_in_expression(rhs)

        return gen, d

    def gen_kill_loads(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        gen: Set[Expression] = variables_in_expression(rhs)
        return gen, d

    def gen_kill_stores(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(rhs) | variables_in_expression(lhs), set()

    def gen_kill_Pos(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(expr), set()

    def gen_kill_Neg(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(expr), set()

    def gen_string(self,  A: CFG.Node, c: Command) -> str:
        if type(c) == SkipCommand:
            return "{}"
        elif type(c) == AssignmentCommand:
            return f"VARS({c.expr})"
        elif type(c) == LoadsCommand:
            return f"VARS({c.expr})"
        elif type(c) == StoresCommand:
            return f"VARS({c.rhs})"
        elif type(c) == PosCommand:
            return f"VARS({c.expr})"
        elif type(c) == NegCommand:
            return f"VARS({c.expr})"
        elif type(c) == ParallelAssigmentCommand:
            return "||".join([f"VARS({x[1]})" for x in c.assignments])

        raise ValueError(f"Unknown command type: {c}")

    def kill_string(self,  A: CFG.Node, c: Command) -> str:
        if type(c) == SkipCommand:
            return "{}"
        elif type(c) == AssignmentCommand:
            return f"VARS({c.lvalue})"
        elif type(c) == LoadsCommand:
            return f"VARS({c.var})"
        elif type(c) == StoresCommand:
            return f"VARS({c.lhs})"
        elif type(c) == PosCommand:
            return f"VARS({c.expr})"
        elif type(c) == NegCommand:
            return f"VARS({c.expr})"
        elif type(c) == ParallelAssigmentCommand:
            return "||".join([f"VARS({x[0]})" for x in c.assignments])

        raise ValueError(f"Unknown command type: {c}")
