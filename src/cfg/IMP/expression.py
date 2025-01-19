from abc import ABC, abstractmethod
from ast import Set
from dataclasses import dataclass

from pycparser import c_ast


def string_to_html(s: str) -> str:
    return s.replace("&&", "&amp;&amp; ").replace("<", "&lt; ").replace(">", "&gt; ")


class Expression(ABC):

    @abstractmethod
    def to_short_string(self) -> str:
        pass

    @abstractmethod
    def is_worthwile_storing(self) -> bool:
        pass

    @abstractmethod
    def rename(self, old_name: str, new_name: str):
        pass

    @abstractmethod
    def color(self, old_name: str, new_name: str):
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
    elif op == "==":
        return "eq"
    elif op == "!=":
        return "neq"
    elif op == "<":
        return "lt"
    elif op == "<=":
        return "le"
    elif op == ">":
        return "gt"
    elif op == ">=":
        return "ge"

    return op


@dataclass
class Constant(Expression):
    value: int

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        if not isinstance(other, Constant):
            return False

        return self.value == other.value

    def to_short_string(self) -> str:
        return str(self.value)

    def is_worthwile_storing(self) -> bool:
        return False

    def __hash__(self):
        return hash(self.value)

    def rename(self, old_name: str, new_name: str):
        pass

    def color(self, old_name: str, new_name: str):
        pass


@dataclass
class ID(Expression):
    name: str
    col: str = "black"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        if not isinstance(other, ID):
            return False
        return self.name == other.name

    def to_short_string(self) -> str:
        return string_to_html(self.name)

    def is_worthwile_storing(self) -> bool:
        return False

    def __hash__(self):
        return hash(self.name)

    def rename(self, old_name: str, new_name: str):
        if self.name == old_name:
            self.name = new_name

    def color(self, old_name: str, new_name: str):
        if self.name == old_name:
            self.col = new_name


@dataclass
class UnaryExpression(Expression):
    op: str
    expr: Expression

    def __str__(self):
        return f"{self.op} {self.expr}"

    def __repr__(self):
        return f"{self.op} {self.expr}"

    def __eq__(self, other):
        if not isinstance(other, UnaryExpression):
            return False

        return self.op == other.op and self.expr == other.expr

    def to_short_string(self) -> str:
        return string_to_html(f"{op_to_shortstring(self.op)}{self.expr.to_short_string()}")

    def is_worthwile_storing(self) -> bool:
        return True

    def __hash__(self):
        return hash(self.op) + hash(self.expr)

    def rename(self, old_name: str, new_name: str):
        self.expr.rename(old_name, new_name)

    def color(self, old_name: str, new_name: str):
        self.expr.color(old_name, new_name)


@ dataclass
class BinExpression(Expression):
    left: Expression
    op: str
    right: Expression

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

        return op

        raise ValueError(f"Unknown operator: {op}")

    def __str__(self):
        return string_to_html(f"{self.left} {(self.op)} {self.right}")

    def __repr__(self):
        return f"{self.left} {self.op} {self.right}"

    def __hash__(self):
        return hash(self.left) + hash(self.op) + hash(self.right)

    def to_short_string(self) -> str:
        return string_to_html(f"{self.left.to_short_string()}{op_to_shortstring(self.op)}{self.right.to_short_string()}")

    def is_worthwile_storing(self) -> bool:
        return True

    def __eq__(self, other):
        if not isinstance(other, BinExpression):
            return False

        return self.left == other.left and self.op == other.op and self.right == other.right

    def rename(self, old_name: str, new_name: str):
        self.left.rename(old_name, new_name)
        self.right.rename(old_name, new_name)

    def color(self, old_name: str, new_name: str):
        self.left.color(old_name, new_name)
        self.right.color(old_name, new_name)


@dataclass
class MemoryExpression(Expression):
    array: c_ast.Node
    expr: c_ast.Node

    def __str__(self):
        return f"{self.array}[{self.expr}]"

    def __repr__(self):
        return f"{self.array}[{self.expr}]"

    def to_short_string(self) -> str:
        return string_to_html(f"{self.array.to_short_string()}_{self.expr.to_short_string()}")

    def __hash__(self):
        return hash(self.array) + hash(self.expr)

    def is_worthwile_storing(self) -> bool:
        return True

    def __eq__(self, other):
        if not isinstance(other, MemoryExpression):
            return False

        return self.array == other.array and self.expr == other.expr

    def rename(self, old_name: str, new_name: str):
        self.array.rename(old_name, new_name)
        self.expr.rename(old_name, new_name)

    def color(self, old_name: str, new_name: str):
        self.array.color(old_name, new_name)
        self.expr.color(old_name, new_name)


@dataclass
class FuncCall(Expression):
    name: str
    args: list[c_ast.Node]

    def __str__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

    def __repr__(self):
        return f"{self.name}({', '.join(map(str, self.args))})"

    def __eq__(self, other):
        return self.name == other.name and self.args == other.args

    def to_short_string(self) -> str:
        return string_to_html(f"{self.name}({', '.join(map(str, self.args))})")

    def is_worthwile_storing(self) -> bool:
        return True

    def __hash__(self):
        return hash(self.name) + hash(self.args)

    def rename(self, old_name: str, new_name: str):
        for arg in self.args:
            arg.rename(old_name, new_name)

    def color(self, old_name: str, new_name: str):
        for arg in self.args:
            arg.color(old_name, new_name)


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
    elif isinstance(expr, c_ast.FuncCall):
        if expr.args is None:
            return FuncCall(expr.name.name, [])
        else:
            return FuncCall(expr.name.name, expr.args)
    elif isinstance(expr, c_ast.ArrayRef):
        return MemoryExpression(convertToExpr(expr.name), convertToExpr(expr.subscript))

    raise ValueError(f"Unknown expression type: {expr}")


def variables_in_expression(expr: Expression) -> set[Expression]:
    if isinstance(expr, ID):
        return {expr}
    elif isinstance(expr, BinExpression):
        return variables_in_expression(expr.left) | variables_in_expression(expr.right)
    elif isinstance(expr, UnaryExpression):
        return variables_in_expression(expr.expr)
    elif isinstance(expr, Constant):
        return set()
    elif isinstance(expr, MemoryExpression):
        return variables_in_expression(expr.expr) | variables_in_expression(expr.array)

    raise ValueError(f"Unknown expression type: {expr}")
