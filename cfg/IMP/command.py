from abc import abstractmethod

from cfg.IMP.expression import ID, Expression


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

    def __init__(self, cfg_keep: bool = False):
        self.cfg_keep = cfg_keep

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


class GotoCommand(Command):
    """
    goto label
    """

    def __init__(self, label: str):
        self.label = label

    def __str__(self) -> str:
        return f"goto {self.label}"


class AllocCommand(Command):
    """
    var = new()
    """

    def __init__(self, var: Expression):
        self.var = var

    def __str__(self) -> str:
        return f"{self.var} = new()"


class FreeCommand(Command):
    """
    free(var)
    """

    def __init__(self, var: Expression):
        self.var = var

    def __str__(self) -> str:
        return f"free({self.var})"


class BlockReadCommand(Command):
    """
    var = x[e]
    """

    def __init__(self, var: Expression, x: Expression, e: Expression):
        self.var = var
        self.x = x
        self.e = e

    def __str__(self) -> str:
        return f"{self.var} = {self.x}[{self.e}]"


class BlockWriteCommand(Command):
    """
    x[e] = var
    """

    def __init__(self, x: Expression, e: Expression, var: Expression):
        self.x = x
        self.e = e
        self.var = var

    def __str__(self) -> str:
        return f"{self.x}[{self.e}] = {self.var}"


class FunCallCommand(Command):
    """
    fun()
    """

    def __init__(self, fun: Expression):
        self.fun = fun

    def __str__(self) -> str:
        return f"{self.fun}()"


class ParallelAssigmentCommand(Command):
    """
    var1=expr1 || var2=expr2 || ... || varn=exprn
    """

    def __init__(self, assignments: list[tuple[ID, Expression]]):
        self.assignments = assignments

    def __str__(self) -> str:
        return " || ".join([f"{var}={expr}" for var, expr in self.assignments])
