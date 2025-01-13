
from typing import Set

from src.lattices.complete_lattice import CompleteLattice


class Powerset[T](CompleteLattice[Set[T]], Set[T]):

    def __init__(self, elements: set[T]):
        self.elements = elements

    def top(self) -> Set[T]:
        return self.elements

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


class FlippedPowerset[T](Powerset[T]):

    def top(self) -> Set[T]:
        return set()

    def bot(self) -> Set[T]:
        return self.elements

    def join(self, a: Set[T], b: Set[T]) -> Set[T]:
        return a.intersection(b)

    def meet(self, a: Set[T], b: Set[T]) -> Set[T]:
        return a.union(b)

    def diff(self, a: Set[T], b: Set[T]) -> Set[T]:
        return a.union(b)

    def leq(self, a:  Set[T], b: Set[T]) -> bool:
        return b.issubset(a)
