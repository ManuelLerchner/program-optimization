from typing import Callable, DefaultDict, Literal, Union

from src.cfg.IMP.expression import ID
from src.lattices.all_variable_lattice import AllVariableLattice
from src.lattices.complete_lattice import CompleteLattice

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
        if a == "⊤" or b == "⊤":
            return "⊤"
        if a == "⊥":
            return b
        if b == "⊥":
            return a
        return a if a == b else "⊤"

    @staticmethod
    def meet(a: IntegerLatticeElement, b: IntegerLatticeElement) -> IntegerLatticeElement:
        if a == "⊥" or b == "⊥":
            return "⊥"
        if a == "⊤":
            return b
        if b == "⊤":
            return a
        return a if a == b else "⊥"

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


class DLattice(AllVariableLattice[IntegerLatticeElement]):

    def __init__(self, vars: set[ID]):
        self.vars = vars
        self.lattice = IntegerLattice()


DLatticeElement = Union[DefaultDict[ID, IntegerLatticeElement], Literal["⊥"]]
