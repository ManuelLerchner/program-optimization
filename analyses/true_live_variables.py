
from typing import Set

from analyses.live_variables import variables_in_expression
from cfg.IMP.expression import ID, Expression
from analyses.gen_kill_analysis import GenKill
from lattices.powerset import FlippedPowerset, Powerset


class TrueLiveVariables(GenKill[Expression]):

    def __init__(self):
        super().__init__('backward', 'bot')

    @staticmethod
    def name():
        return "TrueLiveVar"

    def create_lattice(self, cfg):
        expr = cfg.get_all_expressions()
        filtered = set([x for x in expr if type(x) == ID])
        return Powerset[Expression](filtered)

    def start_node(self):
        return self.lattice.bot()

    def gen_kill_skip(self, A) -> tuple[Set[Expression], Set[Expression]]:
        return set(), set()

    def gen_kill_assignment(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        gen: Set[Expression] = variables_in_expression(
            rhs) if lhs in A else set()

        return gen, d

    def gen_kill_loads(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        d: Set[Expression] = {lhs} if isinstance(lhs, ID) else set()
        gen: Set[Expression] = variables_in_expression(
            rhs) if lhs in A else set()
        return gen, d

    def gen_kill_stores(self, lhs: Expression, rhs: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(rhs) | variables_in_expression(lhs), set()

    def gen_kill_Pos(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(expr), set()

    def gen_kill_Neg(self, expr: Expression, A) -> tuple[Set[Expression], Set[Expression]]:
        return variables_in_expression(expr), set()
