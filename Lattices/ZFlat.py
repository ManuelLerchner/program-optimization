from typing import Dict, Tuple, Literal, Union, Callable
from abc import ABC, abstractmethod

from Lattices.completeLattice import CompleteLattice
from cfg.expression import ID

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


DLatticeElement = Union[Dict[ID,
                             IntegerLatticeElement], Literal["⊥"]]


class DLattice(CompleteLattice[DLatticeElement]):
    @staticmethod
    def top() -> DLatticeElement:
        return {}  # Empty dict represents top (all undefined)

    @staticmethod
    def bot() -> DLatticeElement:
        return "⊥"  # Bottom element

    @staticmethod
    def join(a: DLatticeElement, b: DLatticeElement) -> DLatticeElement:
        if a == "⊥":
            return b
        if b == "⊥":
            return a

        result = {}
        # Get all keys from both dictionaries
        all_keys = set(a.keys()) | set(b.keys())

        for k in all_keys:
            # If key only in one dict, use ⊤ for other
            a_val = a.get(k, "⊤")
            b_val = b.get(k, "⊤")
            # Use integer lattice join for the values
            result[k] = IntegerLattice.join(a_val, b_val)

        return result

    @staticmethod
    def meet(a: DLatticeElement, b: DLatticeElement) -> DLatticeElement:
        if a == "⊥" or b == "⊥":
            return "⊥"

        result = {}
        # Get all keys from both dictionaries
        all_keys = set(a.keys()) | set(b.keys())

        for k in all_keys:
            # If key only in one dict, use ⊤ for other
            a_val = a.get(k, "⊤")
            b_val = b.get(k, "⊤")
            # Use integer lattice meet for the values
            result[k] = IntegerLattice.meet(a_val, b_val)

        return result

    @staticmethod
    def leq(a: DLatticeElement, b: DLatticeElement) -> bool:
        if a == "⊥":
            return True
        if b == "⊥":
            return False

        # Check that all values in a are less than or equal to corresponding values in b
        for k, a_val in a.items():
            b_val = b.get(k, "⊤")
            if not IntegerLattice.leq(a_val, b_val):
                return False
        return True

    @staticmethod
    def eq(a: DLatticeElement, b: DLatticeElement) -> bool:
        if a == "⊥" or b == "⊥":
            return a == b

        if set(a.keys()) != set(b.keys()):
            return False

        # Both are dicts, compare each value
        for k in a.keys():
            if not a[k] == b[k]:  # Use direct comparison since values are immutable
                return False
        return True

    @staticmethod
    def copy(a: DLatticeElement) -> DLatticeElement:
        if a == "⊥":
            return "⊥"
        return {k: IntegerLattice.copy(v) for k, v in a.items()}

    @staticmethod
    def show(a: DLatticeElement) -> str:
        if a == "⊥":
            return "⊥"
        items = [f"{k}: {IntegerLattice.show(v)}" for k, v in a.items()]
        return "{" + ", ".join(items) + "}"
