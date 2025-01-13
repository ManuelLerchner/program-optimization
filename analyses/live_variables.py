
from typing import Set

from cfg.IMP.expression import ID, BinExpression, Constant, Expression, UnaryExpression, MemoryExpression, variables_in_expression
from analyses.gen_kill_analysis import GenKill
from cfg.cfg import CFG
from lattices.powerset import FlippedPowerset, Powerset


class LiveVariables(GenKill[Expression]):

    def __init__(self):
        super().__init__('backward', 'bot')

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
