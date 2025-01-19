
from abc import abstractmethod
from typing import Literal, Set

from src.cfg.IMP.command import Command
from src.cfg.cfg import CFG
from src.analyses.analysis import NodeInsensitiveAnalysis
from src.cfg.IMP.expression import Expression
from src.lattices.powerset import Powerset


class GenKill[T](NodeInsensitiveAnalysis[Set[T]]):

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

    def ParallelAssigment(self, ass, A):
        g, k = set(), set()
        for l, r in ass:
            g_n, k_n = self.gen_kill_assignment(l, r, A)
            g = g | g_n
            k = k | k_n

        return self.lattice.join(self.lattice.diff(A, k), g)

    @abstractmethod
    def gen_string(self,  A: CFG.Node, c: Command) -> str:
        pass

    @abstractmethod
    def kill_string(self, A: CFG.Node, c: Command) -> str:
        pass

    def format_equation(self, A: CFG.Node, c: Command) -> str:
        return f"({self.wrap_name(A)} - {self.kill_string(A, c)}) ∪ {self.gen_string(A, c)}"
