from typing import Callable, Literal, Tuple, Union

from cfg.IMP.expression import ID
from lattices.all_variable_lattice import AllVariableLattice
from lattices.complete_lattice import CompleteLattice

IntervalElement = Union[float]
Interval = Tuple[IntervalElement, IntervalElement]


class IntervalLattice(CompleteLattice[Interval]):

    @ staticmethod
    def top() -> Interval:
        return (float("-inf"), float("inf"))

    @ staticmethod
    def bot() -> Interval:
        return (float("inf"), float("-inf"))

    @ staticmethod
    def join(a: Interval, b: Interval) -> Interval:
        return (min(a[0], b[0]), max(a[1], b[1]))

    @ staticmethod
    def meet(a: Interval, b: Interval) -> Interval:
        return (max(a[0], b[0]), min(a[1], b[1]))

    @ staticmethod
    def leq(a: Interval, b: Interval) -> bool:
        return a[0] >= b[0] and a[1] <= b[1]

    @ staticmethod
    def eq(a: Interval, b: Interval) -> bool:
        return a == b

    @ staticmethod
    def copy(a: Interval) -> Interval:
        return a

    @ staticmethod
    def show(a: Interval) -> str:
        return f"[{a[0]}, {a[1]}]"


class DIntervalLattice(AllVariableLattice[Interval]):

    def __init__(self, vars: set[ID]):
        self.vars = vars
        self.lattice = IntervalLattice()


DIntervalLatticeElement = Union[Callable[[ID], Interval], Literal["⊥"]]
