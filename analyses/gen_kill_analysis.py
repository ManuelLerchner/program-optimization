
from abc import abstractmethod
from typing import Literal, Set, final


from analyses.analysis import Analysis
from cfg.IMP.expression import Expression
from lattices.powerset import FlippedPowerset, Powerset


class GenKill[T](Analysis[Set[T]]):

    def __init__(self,  direction: Literal['forward', 'backward'],
                 type: Literal["may", "must"]):
        super().__init__(direction, type)
        self.lattice: Powerset[T]

    @staticmethod
    def name() -> str:
        return "GenKill"

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
