from abc import ABC, abstractmethod
from dataclasses import dataclass

from pycparser import c_ast


class Expression(ABC):

    @abstractmethod
    def to_short_string(self) -> str:
        pass


def op_to_shortstring(op: str):
    if op == "+":
        return "p"
    elif op == "-":
        return "m"
    elif op == "*":
        return "t"
    elif op == "/":
        return "d"
    elif op == "%":
        return "mod"

    return op


@dataclass
class Constant(Expression):
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

    def to_short_string(self) -> str:
        return str(self.value)

    def __hash__(self):
        return hash(self.value)


@dataclass
class ID(Expression):
    name: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, ID):
            return False
        return self.name == other.name

    def to_short_string(self) -> str:
        return self.name

    def __hash__(self):
        return hash(self.name)


@dataclass
class UnaryExpression(Expression):
    op: str
    expr: c_ast.Node

    def __str__(self):
        return f"{self.op} {self.expr}"

    def __repr__(self):
        return f"{self.op} {self.expr}"

    def __eq__(self, other):
        return self.op == other.op and self.expr == other.expr

    def to_short_string(self) -> str:
        return f"{op_to_shortstring(self.op)}{self.expr.to_short_string()}"

    def __hash__(self):
        return hash(self.op) + hash(self.expr)


@ dataclass
class BinExpression(Expression):
    left: c_ast.Node
    op: str
    right: c_ast.Node

    @staticmethod
    def flip_op(op: str) -> str:
        if op == "<":
            return ">"
        if op == "<=":
            return ">="
        if op == ">":
            return "<"
        if op == ">=":
            return "<="

        raise ValueError(f"Unknown operator: {op}")

    def __str__(self):
        return f"{self.left} {self.op} {self.right}"

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

    def __hash__(self):
        return hash(self.left) + hash(self.op) + hash(self.right)

    def to_short_string(self) -> str:
        return f"{self.left.to_short_string()}{op_to_shortstring(self.op)}{self.right.to_short_string()}"

    def __eq__(self, other):
        return self.left == other.left and self.op == other.op and self.right == other.right


def normalize_bin_expr(left: Expression, op: str, right: Expression) -> Expression:
    if op == ">" or op == ">=":
        return BinExpression(right, "<" if op == ">" else "<=", left)
    return BinExpression(left, op, right)


def convertToExpr(expr: c_ast.Node) -> Expression:
    if isinstance(expr, c_ast.ID):
        return ID(expr.name)
    elif isinstance(expr, c_ast.BinaryOp):
        return normalize_bin_expr(convertToExpr(expr.left), expr.op, convertToExpr(expr.right))
    elif isinstance(expr, c_ast.UnaryOp):
        return UnaryExpression(expr.op, convertToExpr(expr.expr))
    elif isinstance(expr, c_ast.Decl):
        pass
    elif isinstance(expr, c_ast.Constant):
        return Constant(expr.value)

    raise ValueError(f"Unknown expression type: {expr}")
