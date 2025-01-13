from collections import defaultdict
from typing import Callable, DefaultDict, Literal, Tuple, Union

from src.cfg.IMP.expression import ID
from src.lattices.all_variable_lattice import AllVariableLattice
from src.lattices.complete_lattice import CompleteLattice
from src.lattices.powerset import Powerset

Addr = Tuple[int, int]
Val = Powerset[Addr]
Store = Tuple[DefaultDict[Addr, Val], int]
State = Tuple[DefaultDict[ID, Addr], Store]

IntegerLatticeElement = Union[int, Literal["⊥"], Literal["⊤"]]


class MemoryLattice(CompleteLattice[State]):

    @staticmethod
    def top() -> State:
        return (defaultdict(lambda: "⊤"), defaultdict(lambda: "⊤"))

    @staticmethod
    def bot() -> State:
        return (defaultdict(lambda: "⊥"), defaultdict(lambda: "⊥"))

    @staticmethod
    def join(a: State, b: State) -> State:
        D1, M1 = a
        D2, M2 = b

        D = defaultdict(lambda: "⊥")
        M = defaultdict(lambda: "⊥")

        for x in D1:
            D[x] = D1[x].union(D2[x])

        for x in M1:
            M[x] = M1[x].union(M2[x])

        return (D, M)

    @staticmethod
    def meet(a: State, b: State) -> State:
        D1, M1 = a
        D2, M2 = b

        D = defaultdict(lambda: "⊥⊤")
        M = defaultdict(lambda: "⊥")

        for x in D1:
            D[x] = D1[x].intersection(D2[x])

        for x in M1:
            M[x] = M1[x].intersection(M2[x])

        return

    @staticmethod
    def leq(a: State, b: State) -> bool:
        D1, M1 = a
        D2, M2 = b

        return all(D1[x].issubset(D2[x]) for x in D1) and all(M1[x].issubset(M2[x]) for x in M1)

    @staticmethod
    def eq(a: State, b: State) -> bool:
        D1, M1 = a
        D2, M2 = b

        return all(D1[x] == D2[x] for x in D1) and all(M1[x] == M2[x] for x in M1)

    @staticmethod
    def copy(a: State) -> State:
        D, M = a
        return (defaultdict(lambda: "⊥", {k: v.copy() for k, v in D.items()}),
                defaultdict(lambda: "⊥", {k: v.copy() for k, v in M.items()}))

    @staticmethod
    def show(a: State) -> str:
        D, M = a
        return f"D: {D}, M: {M}"
