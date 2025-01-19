
import inspect
from abc import ABC, abstractmethod
from typing import Literal

from src.cfg.cfg import CFG
from src.cfg.IMP.command import (AssignmentCommand, Command, LoadsCommand,
                                 NegCommand, ParallelAssigmentCommand,
                                 PosCommand, SkipCommand, StoresCommand)
from src.cfg.IMP.expression import ID, Expression
from src.lattices.complete_lattice import CompleteLattice
from src.util.bcolors import BColors


class Analysis[T](ABC):

    def __init__(self, direction: Literal['forward', 'backward'], type: Literal['may', 'must'], use_widen: bool = False, use_narrow: bool = False) -> None:
        self.direction = direction
        self.type = type
        self.cfg: CFG
        self.lattice: CompleteLattice[T]
        self.use_widen = use_widen
        self.use_narrow = use_narrow

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @abstractmethod
    def create_lattice(self, cfg: CFG) -> CompleteLattice[T]:
        pass

    @abstractmethod
    def start_node(self, cfg: CFG) -> T:
        pass

    @abstractmethod
    def transfer(self, X: T, u: CFG.Node, command: Command, v: CFG.Node) -> T:
        pass

    @abstractmethod
    def get_equation(self, u: CFG.Node, incoming: list[CFG.Edge]) -> str:
        pass

    def wrap_name(self, x: CFG.Node) -> str:
        return f"{BColors.BOLD}{self.name()}({BColors.ENDC}{x.name}{BColors.BOLD}){BColors.ENDC}"


class NodeInsensitiveAnalysis[T](Analysis[T], ABC):

    @abstractmethod
    def skip(self, x: T) -> T:
        """
        ;
        """
        pass

    @abstractmethod
    def assignment(self, lhs: Expression, rhs: Expression, A: T) -> T:
        """
        lhs = rhs
        """
        pass

    @abstractmethod
    def loads(self, lhs: Expression, rhs: Expression, A: T) -> T:
        """
        lhs = M[rhs]
        """
        pass

    @abstractmethod
    def stores(self, lhs: Expression, rhs: Expression, A: T) -> T:
        """
        M[lhs] = rhs
        """
        pass

    @abstractmethod
    def Pos(self, expr: Expression, A: T) -> T:
        """
        Pos(expr)
        """
        pass

    @abstractmethod
    def Neg(self, expr: Expression, A: T) -> T:
        """
        Neg(expr)
        """
        pass

    def ParallelAssigment(self, ass: list[tuple[ID, Expression]], A: T) -> T:
        """
        var1=expr1 || var2=expr2 || ... || varn=exprn
        """
        raise NotImplementedError

    def transfer(self, X: T, u: CFG.Node, command: Command, v: CFG.Node) -> T:
        A = self.lattice.copy(X)

        if type(command) == SkipCommand:
            return self.skip(A)
        elif type(command) == AssignmentCommand:
            return self.assignment(command.lvalue, command.expr, A)
        elif type(command) == LoadsCommand:
            return self.loads(command.var, command.expr, A)
        elif type(command) == StoresCommand:
            return self.stores(command.lhs, command.rhs, A)
        elif type(command) == PosCommand:
            return self.Pos(command.expr, A)
        elif type(command) == NegCommand:
            return self.Neg(command.expr, A)
        elif type(command) == ParallelAssigmentCommand:
            return self.ParallelAssigment(command.assignments, A)

        raise ValueError(f"Unknown command type: {command}")

    @abstractmethod
    def format_equation(self, A: CFG.Node, c: Command) -> str:
        pass

    def get_equation(self, u: CFG.Node, incoming: list[CFG.Edge]) -> str:
        if (self.direction == 'forward' and u.is_start) or (self.direction == 'backward' and u.is_end):
            eq = [self.lattice.show(self.start_node(self.cfg))]
        else:
            eq = ["("+self.format_equation(e.source, e.command)+")" for e in incoming]

        src = self.wrap_name(u)

        s = f"{src} {self.lattice.geq_symbol()} {
            f" {self.lattice.join_symbol()} ".join(eq)}"

        return s


class NodeSensitiveAnalysis[T](Analysis[T], ABC):

    def __init__(self, direction: Literal['forward', 'backward'], type: Literal['may', 'must'], use_widen: bool = False, use_narrow: bool = False) -> None:
        self.direction = direction
        self.type = type
        self.cfg: CFG
        self.lattice: CompleteLattice[T]
        self.use_widen = use_widen
        self.use_narrow = use_narrow

    @ abstractmethod
    def skip(self, x: T, u: CFG.Node, v: CFG.Node) -> T:
        """
        ;
        """
        pass

    @ abstractmethod
    def assignment(self, lhs: Expression, rhs: Expression, A: T, u: CFG.Node, v: CFG.Node) -> T:
        """
        lhs = rhs
        """
        pass

    @ abstractmethod
    def loads(self, lhs: Expression, rhs: Expression, A: T, u: CFG.Node, v: CFG.Node) -> T:
        """
        lhs = M[rhs]
        """
        pass

    @ abstractmethod
    def stores(self, lhs: Expression, rhs: Expression, A: T, u: CFG.Node, v: CFG.Node) -> T:
        """
        M[lhs] = rhs
        """
        pass

    @ abstractmethod
    def Pos(self, expr: Expression, A: T, u: CFG.Node, v: CFG.Node) -> T:
        """
        Pos(expr)
        """
        pass

    @ abstractmethod
    def Neg(self, expr: Expression, A: T, u: CFG.Node, v: CFG.Node) -> T:
        """
        Neg(expr)
        """
        pass

    def ParallelAssigment(self, ass: list[tuple[ID, Expression]], A: T, u: CFG.Node, v: CFG.Node) -> T:
        """
        var1=expr1 || var2=expr2 || ... || varn=exprn
        """
        raise NotImplementedError

    def transfer(self, X: T,  u: CFG.Node, command: Command, v: CFG.Node) -> T:
        A = self.lattice.copy(X)

        if type(command) == SkipCommand:
            return self.skip(A, u, v)
        elif type(command) == AssignmentCommand:
            return self.assignment(command.lvalue, command.expr, A, u, v)
        elif type(command) == LoadsCommand:
            return self.loads(command.var, command.expr, A, u, v)
        elif type(command) == StoresCommand:
            return self.stores(command.lhs, command.rhs, A, u, v)
        elif type(command) == PosCommand:
            return self.Pos(command.expr, A, u, v)
        elif type(command) == NegCommand:
            return self.Neg(command.expr, A, u, v)
        elif type(command) == ParallelAssigmentCommand:
            return self.ParallelAssigment(command.assignments, A, u, v)

        raise ValueError(f"Unknown command type: {command}")

    @ abstractmethod
    def format_equation(self, A: CFG.Node, c: Command, B: CFG.Node) -> str:
        pass

    def get_equation(self, u: CFG.Node, incoming: list[CFG.Edge]) -> str:
        if (self.direction == 'forward' and u.is_start) or (self.direction == 'backward' and u.is_end):
            eq = [self.lattice.show(self.start_node(self.cfg))]
        else:
            eq = ["("+self.format_equation(e.source, e.command, u)+")"
                  for e in incoming]

        src = self.wrap_name(u)

        s = f"{src} {self.lattice.geq_symbol()} {
            f" {self.lattice.join_symbol()} ".join(eq)}"

        return s
