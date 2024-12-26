
from abc import ABC, abstractmethod
from typing import Generic, Literal, TypeVar

from Lattices.completeLattice import CompleteLattice
from cfg.cfg import CFG
from cfg.command import Command, SkipCommand, AssignmentCommand, LoadsCommand, StoresCommand, PosCommand, NegCommand
from cfg.expression import Expression


T = TypeVar('T')


class Analysis(Generic[T], ABC):

    def __init__(self, lattice: CompleteLattice[T], type: Literal['forward', 'backward']):
        self.lattice = lattice
        self.type = type
        self.cfg: CFG | None = None

    def name(self) -> str:
        return self.__class__.__name__

    def prepare(self):
        pass

    def finish(self):
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
