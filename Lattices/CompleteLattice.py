from abc import ABC, abstractmethod


class CompleteLattice[T](ABC):

    @abstractmethod
    def top(self) -> T:
        pass

    @abstractmethod
    def bot(self) -> T:
        pass

    @abstractmethod
    def join(self, a: T, b: T) -> T:
        pass

    @abstractmethod
    def meet(self, a: T, b: T) -> T:
        pass

    @abstractmethod
    def leq(self, a: T, b: T) -> bool:
        pass

    @abstractmethod
    def eq(self, a: T, b: T) -> bool:
        pass

    @abstractmethod
    def copy(self, a: T) -> T:
        pass

    @abstractmethod
    def show(self, a: T) -> str:
        pass

    @abstractmethod
    def __hash__(self) -> int:
        pass
