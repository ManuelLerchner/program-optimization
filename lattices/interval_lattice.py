from typing import Callable, DefaultDict, Literal, Tuple, Union

from cfg.IMP.expression import ID
from lattices.all_variable_lattice import AllVariableLattice
from lattices.complete_lattice import CompleteLattice


Interval = Union[Tuple[float, float], Literal["⊥"]]


class IntervalLattice(CompleteLattice[Interval]):

    @ staticmethod
    def top() -> Interval:
        return (float("-inf"), float("inf"))

    @ staticmethod
    def bot() -> Interval:
        return "⊥"

    @ staticmethod
    def join(a: Interval, b: Interval) -> Interval:
        if a == "⊥":
            return b
        if b == "⊥":
            return a

        return (min(a[0], b[0]), max(a[1], b[1]))

    @ staticmethod
    def widen(a: Interval, b: Interval) -> Interval:
        if a == "⊥":
            return b
        if b == "⊥":
            return a

        l1, u1 = a
        l2, u2 = b

        l = l1 if l1 <= l2 else float("-inf")
        u = u1 if u1 >= u2 else float("inf")

        return (l, u)

    @ staticmethod
    def meet(a: Interval, b: Interval) -> Interval:
        if a == "⊥":
            return a
        if b == "⊥":
            return b
        return (max(a[0], b[0]), min(a[1], b[1]))

    @staticmethod
    def narrow(a: Interval, b: Interval) -> Interval:
        if a == "⊥":
            return a
        if b == "⊥":
            return b

        l1, u1 = a
        l2, u2 = b

        l = l2 if l1 == float("-inf") else l1
        u = u2 if u1 == float("inf") else u1

        return (l, u)

    @ staticmethod
    def leq(a: Interval, b: Interval) -> bool:
        if a == "⊥":
            return True
        if b == "⊥":
            return False

        return a[0] >= b[0] and a[1] <= b[1]

    @ staticmethod
    def eq(a: Interval, b: Interval) -> bool:
        return a == b

    @ staticmethod
    def copy(a: Interval) -> Interval:
        return a

    @ staticmethod
    def show(a: Interval) -> str:
        if a == "⊥":
            return "⊥"
        if a == (float("-inf"), float("inf")):
            return "⊤"

        return f"[{a[0]}, {a[1]}]"


DIntervalLatticeElement = Union[DefaultDict[ID, Interval], Literal["⊥"]]


class DIntervalLattice(AllVariableLattice[Interval]):

    def __init__(self, vars: set[ID]):
        self.vars = vars
        self.lattice = IntervalLattice()
