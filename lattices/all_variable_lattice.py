
from typing import Callable, Literal, Union

from cfg.IMP.expression import ID
from lattices.complete_lattice import CompleteLattice


class AllVariableLattice[T](CompleteLattice[Union[Callable[[ID],  T], Literal["⊥"]]]):

    def __init__(self, vars: set[ID], lattice: CompleteLattice[T]):
        self.vars = vars
        self.lattice = lattice

    def top(self) -> Union[Callable[[ID],  T], Literal["⊥"]]:
        return lambda _: self.lattice.top()

    def bot(self) -> Union[Callable[[ID],  T], Literal["⊥"]]:
        return "⊥"  # Bottom element

    def join(self, a: Union[Callable[[ID],  T], Literal["⊥"]], b: Union[Callable[[ID],  T], Literal["⊥"]]) -> Union[Callable[[ID],  T], Literal["⊥"]]:
        if a == "⊥":
            return b
        if b == "⊥":
            return a

        return lambda x: self.lattice.join(a(x), b(x))

    def meet(self, a: Union[Callable[[ID],  T], Literal["⊥"]], b: Union[Callable[[ID],  T], Literal["⊥"]]) -> Union[Callable[[ID],  T], Literal["⊥"]]:
        if a == "⊥" or b == "⊥":
            return "⊥"
        return lambda x: self.lattice.meet(a(x), b(x))

    def leq(self, a: Union[Callable[[ID],  T], Literal["⊥"]], b: Union[Callable[[ID],  T], Literal["⊥"]]) -> bool:
        if a == "⊥":
            return True
        if b == "⊥":
            return False
        return all(self.lattice.leq(a(k), b(k)) for k in self.vars)

    def eq(self, a: Union[Callable[[ID],  T], Literal["⊥"]], b: Union[Callable[[ID],  T], Literal["⊥"]]) -> bool:
        if a == "⊥" and b == "⊥":
            return True
        if a == "⊥" or b == "⊥":
            return False
        return all(self.lattice.eq(a(k), b(k)) for k in self.vars)

    def copy(self, a: Union[Callable[[ID],  T], Literal["⊥"]]) -> Union[Callable[[ID],  T], Literal["⊥"]]:
        if a == "⊥":
            return "⊥"

        def result(x): return a(x)
        return result

    def show(self, a: Union[Callable[[ID],  T], Literal["⊥"]]) -> str:
        if a == "⊥":
            return "⊥"
        return f"({', '.join([f'{k} -> {self.lattice.show(a(k))}' for k in self.vars])})"
