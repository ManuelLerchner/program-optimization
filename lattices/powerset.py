
from typing import Set

from lattices.complete_lattice import CompleteLattice


class Powerset[T](CompleteLattice[Set[T]], Set[T]):
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

    def show(self, a: Set[T]) -> str:
        return f"{{{', '.join([str(x) for x in sorted(a, key=str)])}}}"
