
from abc import ABC, abstractmethod
from typing import Generic, Literal, Set, TypeVar

from Lattices.completeLattice import CompleteLattice
from Lattices.powerset import Powerset
from analysis.analysis import Analysis
from cfg.expression import Expression


class GenKill[T](Analysis[Set[T]]):

    def __init__(self, lattice: Powerset[T], type: Literal['forward', 'backward']):
        self.lattice: Powerset[T] = lattice
        self.type = type

    def name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def gen_kill_skip(self, A:  set[T]) -> tuple[set[T],  set[T]]:
        pass

    @abstractmethod
    def gen_kill_assignment(self, lhs: Expression, rhs: Expression, A:  set[T]) -> tuple[set[T],  set[T]]:
        pass

    @abstractmethod
    def gen_kill_loads(self, lhs: Expression, rhs: Expression, A:  set[T]) -> tuple[set[T],  set[T]]:
        pass

    @abstractmethod
    def gen_kill_stores(self, lhs: Expression, rhs: Expression, A:  set[T]) -> tuple[set[T],  set[T]]:
        pass

    @abstractmethod
    def gen_kill_Pos(self, expr: Expression, A:  set[T]) -> tuple[set[T],  set[T]]:
        pass

    @abstractmethod
    def gen_kill_Neg(self, expr: Expression, A:  set[T]) -> tuple[set[T],  set[T]]:
        pass

    def skip(self, A: set[T]) -> set[T]:
        gen, kill = self.gen_kill_skip(A)
        return self.lattice.join(self.lattice.diff(A, kill), gen)

    def assignment(self, lhs: Expression, rhs: Expression, A:  set[T]) -> set[T]:
        gen, kill = self.gen_kill_assignment(lhs, rhs, A)
        return self.lattice.join(self.lattice.diff(A, kill), gen)

    def loads(self, lhs: Expression, rhs: Expression, A:  set[T]) -> set[T]:
        gen, kill = self.gen_kill_loads(lhs, rhs, A)
        return self.lattice.join(self.lattice.diff(A, kill), gen)

    def stores(self, lhs: Expression, rhs: Expression, A:  set[T]) -> set[T]:
        gen, kill = self.gen_kill_stores(lhs, rhs, A)
        return self.lattice.join(self.lattice.diff(A, kill), gen)

    def Pos(self, expr: Expression, A:  set[T]) -> set[T]:
        gen, kill = self.gen_kill_Pos(expr, A)
        return self.lattice.join(self.lattice.diff(A, kill), gen)

    def Neg(self, expr: Expression, A:  set[T]) -> set[T]:
        gen, kill = self.gen_kill_Neg(expr, A)
        return self.lattice.join(self.lattice.diff(A, kill), gen)
