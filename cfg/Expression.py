from dataclasses import dataclass
from pycparser import c_ast


class Expression:
    pass


@dataclass
class Constant(Expression):
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other.value

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
        return self.name == other.name

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

    def __hash__(self):
        return hash(self.op) + hash(self.expr)


@dataclass
class BinExpression(Expression):
    left: c_ast.Node
    op: str
    right: c_ast.Node

    def __str__(self):
        return f"{self.left} {self.op} {self.right}"

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

    def __hash__(self):
        return hash(self.left) + hash(self.op) + hash(self.right)

    def __eq__(self, other):
        return self.left == other.left and self.op == other.op and self.right == other.right


def convertToExpr(expr: c_ast.Node) -> Expression:
    if isinstance(expr, c_ast.ID):
        return ID(expr.name)
    elif isinstance(expr, c_ast.BinaryOp):
        return BinExpression(convertToExpr(expr.left), expr.op, convertToExpr(expr.right))
    elif isinstance(expr, c_ast.UnaryOp):
        return UnaryExpression(expr.op, convertToExpr(expr.expr))
    elif isinstance(expr, c_ast.Decl):
        pass
    elif isinstance(expr, c_ast.Constant):
        return Constant(expr.value)

    raise ValueError(f"Unknown expression type: {expr}")