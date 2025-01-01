
from abc import ABC, abstractmethod
from typing import Literal

from cfg.cfg import CFG
from cfg.IMP.command import (AssignmentCommand, Command, LoadsCommand,
                             NegCommand, PosCommand, SkipCommand,
                             StoresCommand)
from cfg.IMP.expression import Expression
from lattices.complete_lattice import CompleteLattice


class Analysis[T](ABC):

    def __init__(self, direction: Literal['forward', 'backward'], start: Literal['top', 'bot'], use_widen: bool = False, use_narrow: bool = False) -> None:
        self.direction = direction
        self.start = start
        self.cfg: CFG
        self.lattice: CompleteLattice[T]
        self.use_widen = use_widen
        self.use_narrow = use_narrow

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def create_lattice(self, cfg: CFG) -> CompleteLattice[T]:
        pass

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

    def transfer(self, X: T, command: Command) -> T:
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

        raise ValueError(f"Unknown command type: {command}")
