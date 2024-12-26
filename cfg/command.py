from abc import abstractmethod

from cfg.expression import Expression


class Command:
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class SkipCommand(Command):
    """
    ;
    """

    def __str__(self) -> str:
        return ";"


class AssignmentCommand(Command):
    """
    var = expr
    """

    def __init__(self, lvalue: Expression, expr: Expression):
        self.lvalue = lvalue
        self.expr = expr

    def __str__(self) -> str:
        return f"{self.lvalue} = {self.expr}"


class LoadsCommand(Command):
    """
    var = M[expr]
    """

    def __init__(self, lvalue: Expression, expr: Expression):
        self.var = lvalue
        self.expr = expr

    def __str__(self) -> str:
        return f"{self.var} = M[{self.expr}]"


class StoresCommand(Command):
    """
    M[lhs] = rhs
    """

    def __init__(self, lhs: Expression, rhs: Expression):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self) -> str:
        return f"M[{self.lhs}] = {self.rhs}"


class PosCommand(Command):
    """
    Pos(expr
    """

    def __init__(self, expr: Expression):
        self.expr = expr

    def __str__(self) -> str:
        return f"Pos({self.expr})"


class NegCommand(Command):
    """
    Neg(expr)
    """

    def __init__(self, expr: Expression):
        self.expr = expr

    def __str__(self) -> str:
        return f"Neg({self.expr})"
