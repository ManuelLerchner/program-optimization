from typing import Callable, Literal, Union

from cfg.IMP.expression import ID
from lattices.complete_lattice import CompleteLattice

IntegerLatticeElement = Union[int, Literal["⊥"], Literal["⊤"]]


class IntegerLattice(CompleteLattice[IntegerLatticeElement]):

    @staticmethod
    def top() -> IntegerLatticeElement:
        return "⊤"

    @staticmethod
    def bot() -> IntegerLatticeElement:
        return "⊥"

    @staticmethod
    def join(a: IntegerLatticeElement, b: IntegerLatticeElement) -> IntegerLatticeElement:
        if a == "⊥":
            return b
        if b == "⊥":
            return a
        if a == "⊤" or b == "⊤":
            return "⊤"
        return max(a, b)

    @staticmethod
    def meet(a: IntegerLatticeElement, b: IntegerLatticeElement) -> IntegerLatticeElement:
        if a == "⊥" or b == "⊥":
            return "⊥"
        if a == "⊤":
            return b
        if b == "⊤":
            return a
        return min(a, b)

    @staticmethod
    def leq(a: IntegerLatticeElement, b: IntegerLatticeElement) -> bool:
        return a == b or b == "⊤"

    @staticmethod
    def eq(a: IntegerLatticeElement, b: IntegerLatticeElement) -> bool:
        return a == b

    @staticmethod
    def copy(a: IntegerLatticeElement) -> IntegerLatticeElement:
        return a  # Since all values are immutable, we can just return them

    @staticmethod
    def show(a: IntegerLatticeElement) -> str:
        return str(a)

    @staticmethod
    def of_bool(b: bool) -> IntegerLatticeElement:
        return 1 if b else 0


DLatticeElement = Union[Callable[[ID],
                                 IntegerLatticeElement], Literal["⊥"]]


class DLattice(CompleteLattice[DLatticeElement]):

    def __init__(self, vars: set[ID]):
        self.vars = vars

    def top(self) -> DLatticeElement:
        return lambda _: "⊤"

    def bot(self) -> DLatticeElement:
        return "⊥"  # Bottom element

    def join(self, a: DLatticeElement, b: DLatticeElement) -> DLatticeElement:
        if a == "⊥":
            return b
        if b == "⊥":
            return a

        # return new function that returns the join of the two functions

        return lambda x: IntegerLattice.join(a(x), b(x))

    def meet(self, a: DLatticeElement, b: DLatticeElement) -> DLatticeElement:

        if a == "⊥" or b == "⊥":
            return "⊥"

        # return new function that returns the meet of the two functions
        return lambda x: IntegerLattice.meet(a(x), b(x))

    def leq(self, a: DLatticeElement, b: DLatticeElement) -> bool:
        if a == "⊥":
            return True
        if b == "⊥":
            return False

        return all(IntegerLattice.leq(a(k), b(k)) for k in self.vars)

    def eq(self, a: DLatticeElement, b: DLatticeElement) -> bool:
        if a == "⊥" or b == "⊥":
            return a == b

        return all(IntegerLattice.eq(a(k), b(k)) for k in self.vars)

    def copy(self, a: DLatticeElement) -> DLatticeElement:
        if a == "⊥":
            return "⊥"

        def result(x): return a(x)

        return result

    def show(self, a: DLatticeElement) -> str:
        if a == "⊥":
            return "⊥"

        return "{" + ", ".join(f"{k.name} ⟶ {IntegerLattice.show(a(k))}" for k in self.vars) + "}"
