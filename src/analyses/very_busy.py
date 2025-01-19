
import typing

from src.cfg.IMP.command import Command, AssignmentCommand, LoadsCommand, StoresCommand, PosCommand, NegCommand, SkipCommand, ParallelAssigmentCommand
from src.analyses.analysis import NodeInsensitiveAnalysis
from src.analyses.live_variables import variables_in_expression
from src.cfg.cfg import CFG
from src.cfg.IMP.expression import ID, Expression
from src.lattices.complete_lattice import CompleteLattice
from src.lattices.powerset import FlippedPowerset


class VeryBusyAnalysis(NodeInsensitiveAnalysis[FlippedPowerset[Expression]]):

    def __init__(self):
        super().__init__('backward', 'must')

    @staticmethod
    def name():
        return "VeryBusy"

    def create_lattice(self, cfg: CFG) -> CompleteLattice[FlippedPowerset[Expression]]:
        return typing.cast(CompleteLattice[FlippedPowerset[Expression]],
                           FlippedPowerset[Expression](cfg.get_all_expressions()))

    def start_node(self, cfg: CFG) -> FlippedPowerset[Expression]:
        return self.lattice.top()

    def skip(self, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        return A

    def assignment(self, lhs: Expression, rhs: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        expr_with_lhs = {
            expr for expr in A if lhs in variables_in_expression(expr)}
        A.difference_update(expr_with_lhs)
        if not isinstance(rhs, ID):
            A.add(rhs)
        return A

    def loads(self, lhs: Expression, rhs: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        expr_with_lhs = {
            expr for expr in A if lhs in variables_in_expression(expr)}
        A.difference_update(expr_with_lhs)
        if not isinstance(rhs, ID):
            A.add(rhs)
        return A

    def stores(self, lhs: Expression, rhs: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        if not isinstance(lhs, ID):
            A.add(lhs)
        if not isinstance(rhs, ID):
            A.add(rhs)
        return A

    def Pos(self, expr: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        if not isinstance(expr, ID):
            A.add(expr)
        return A

    def Neg(self, expr: Expression, A: FlippedPowerset[Expression]) -> FlippedPowerset[Expression]:
        if not isinstance(expr, ID):
            A.add(expr)
        return A

    def format_equation(self, A: CFG.Node, c: Command) -> str:
        if type(c) == SkipCommand:
            return f"{self.wrap_name(A)}"
        elif type(c) == AssignmentCommand:
            return f"({self.wrap_name(A)} - ExprsWith({c.lvalue})) ∪ {c.expr}"
        elif type(c) == LoadsCommand:
            return f"({self.wrap_name(A)} - ExprsWith({c.var})) ∪ {c.expr}"
        elif type(c) == StoresCommand:
            return f"{self.wrap_name(A)} ∪ {c.lhs} ∪ {c.rhs}"
        elif type(c) == PosCommand:
            return f"{self.wrap_name(A)} ∪ {c.expr}"
        elif type(c) == NegCommand:
            return f"{self.wrap_name(A)} ∪ {c.expr}"
        elif type(c) == ParallelAssigmentCommand:
            return " || ".join([f"({self.wrap_name(A)} - ExprsWith({x[0]})) ∪ {x[1]}" for x in c.assignments])

        raise ValueError(f"Unknown command type: {c}")
