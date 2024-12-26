
from typing import Set
from Lattices.completeLattice import CompleteLattice


class Powerset[T](CompleteLattice[Set[T]]):
    def top(self) -> Set[T]:
        raise NotImplementedError

    def bot(self) -> Set[T]:
        return set()

    def bottom(self) -> Set[T]:
        return set()

    def join(self, a: Set[T], b: Set[T]) -> Set[T]:
        return a.union(b)

    def meet(self, a: Set[T], b: Set[T]) -> Set[T]:
        return a.intersection(b)

    def leq(self, a:  Set[T], b: Set[T]) -> bool:
        return a.issubset(b)

    def eq(self, a: Set[T], b: Set[T]) -> bool:
        return a == b

    def diff(self, a: Set[T], b: Set[T]) -> Set[T]:
        return a.difference(b)

    def copy(self, a):
        return a.copy()

    def __hash__(self) -> int:
        return hash(str(self))

    def show(self, a: Set[T]) -> str:
        return str(a)
