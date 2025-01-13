
from collections import defaultdict
from typing import Callable, DefaultDict, Dict, Literal, Union

from src.cfg.IMP.expression import ID
from src.lattices.complete_lattice import CompleteLattice


class AllVariableLattice[T](CompleteLattice[Union[DefaultDict[ID, T], Literal["⊥"]]]):

    def __init__(self, vars: set[ID], lattice: CompleteLattice[T]):
        self.vars = vars
        self.lattice = lattice

    def top(self) -> Union[DefaultDict[ID, T], Literal["⊥"]]:
        return defaultdict(lambda: self.lattice.top(), {k: self.lattice.top() for k in self.vars})

    def bot(self) -> Union[DefaultDict[ID, T], Literal["⊥"]]:
        return "⊥"  # Bottom element

    def join(self, a: Union[DefaultDict[ID, T], Literal["⊥"]], b: Union[DefaultDict[ID, T], Literal["⊥"]]) -> Union[DefaultDict[ID, T], Literal["⊥"]]:
        if a == "⊥":
            return b
        if b == "⊥":
            return a

        return defaultdict(lambda: self.lattice.bot(), {k: self.lattice.join(a[k], b[k]) for k in self.vars | a.keys() | b.keys()})

    def widen(self, a: Union[DefaultDict[ID, T], Literal["⊥"]], b: Union[DefaultDict[ID, T], Literal["⊥"]]) -> Union[DefaultDict[ID, T], Literal["⊥"]]:
        if a == "⊥":
            return b
        if b == "⊥":
            return a

        return defaultdict(lambda: self.lattice.bot(), {k: self.lattice.widen(a[k], b[k]) for k in self.vars | a.keys() | b.keys()})

    def meet(self, a: Union[DefaultDict[ID, T], Literal["⊥"]], b: Union[DefaultDict[ID, T], Literal["⊥"]]) -> Union[DefaultDict[ID, T], Literal["⊥"]]:
        if a == "⊥" or b == "⊥":
            return "⊥"
        return defaultdict(lambda: self.lattice.bot(), {k: self.lattice.meet(a[k], b[k]) for k in self.vars | a.keys() | b.keys()})

    def narrow(self, a: Union[DefaultDict[ID, T], Literal["⊥"]], b: Union[DefaultDict[ID, T], Literal["⊥"]]) -> Union[DefaultDict[ID, T], Literal["⊥"]]:
        if a == "⊥" or b == "⊥":
            return "⊥"
        return defaultdict(lambda: self.lattice.bot(), {k: self.lattice.narrow(a[k], b[k]) for k in self.vars | a.keys() | b.keys()})

    def leq(self, a: Union[DefaultDict[ID, T], Literal["⊥"]], b: Union[DefaultDict[ID, T], Literal["⊥"]]) -> bool:
        if a == "⊥":
            return True
        if b == "⊥":
            return False
        return all(self.lattice.leq(a[k], b[k]) for k in self.vars)

    def eq(self, a: Union[DefaultDict[ID, T], Literal["⊥"]], b: Union[DefaultDict[ID, T], Literal["⊥"]]) -> bool:
        if a == "⊥" and b == "⊥":
            return True
        if a == "⊥" or b == "⊥":
            return False
        return all(self.lattice.eq(a[k], b[k]) for k in self.vars | a.keys() | b.keys())

    def copy(self, a: Union[DefaultDict[ID, T], Literal["⊥"]]) -> Union[DefaultDict[ID, T], Literal["⊥"]]:
        if a == "⊥":
            return "⊥"

        return defaultdict(lambda: self.lattice.top(), {k: self.lattice.copy(a[k]) for k in self.vars | a.keys()})

    def show(self, a: Union[DefaultDict[ID, T], Literal["⊥"]]) -> str:
        if a == "⊥":
            return "⊥"

        return f"({', '.join([f'{k}={self.lattice.show(v)}' for k, v in sorted(a.items(), key=lambda x: str(x[0]))])})"
