
from typing import Generic, Set, TypeVar
from Lattices.completeLattice import CompleteLattice

A = TypeVar('A')
T = TypeVar('T', bound=CompleteLattice)


class NamedTupleLattice(Generic[A, T], CompleteLattice[dict[A, T]]):

    def __init__(self, entries: dict[A, T]):
        self.entries = entries

    def top(self) -> dict[A, T]:
        return {k: v.top() for k, v in self.entries.items()}

    def bot(self) -> dict[A, T]:
        return {k: v.bot() for k, v in self.entries.items()}

    def join(self, a: dict[A, T], b: dict[A, T]) -> dict[A, T]:
        return {k: self.entries[k].join(a[k], b[k]) for k in self.entries.keys()}

    def meet(self, a: dict[A, T], b: dict[A, T]) -> dict[A, T]:
        return {k: self.entries[k].meet(a[k], b[k]) for k in self.entries.keys()}

    def leq(self, a: dict[A, T], b: dict[A, T]) -> bool:
        return all(self.entries[k].leq(a[k], b[k]) for k in self.entries.keys())

    def eq(self, a:  dict[A, T], b:  dict[A, T]) -> bool:
        return all(self.entries[k].eq(a[k], b[k]) for k in self.entries.keys())

    def copy(self, a: dict[A, T]) -> dict[A, T]:
        return {k: self.entries[k].copy(a[k]) for k in self.entries.keys()}

    def show(self,  a: dict[A, T]) -> str:
        ret = ""
        for k, v in a.items():
            ret += f"{str(k)}: {self.entries[k].show(v)}\n"
        return ret
