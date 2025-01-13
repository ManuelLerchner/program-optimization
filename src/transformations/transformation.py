from abc import ABC, abstractmethod

from src.analyses.analysis import Analysis
from src.cfg.cfg import CFG


class TransformationFixpoint(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def transform_until_stable[T](self, cfg: CFG, analyses_results: dict[Analysis[T], dict[CFG.Node, T]]) -> tuple[CFG, bool]:
        """
        :param cfg: The CFG to transform
        :param analyses_results: The results of the analyses
        :return: The transformed CFG and a boolean indicating if the transformation needs to be applied again
        """
        pass

    def dependencies(self) -> list[Analysis]:
        return []

    @staticmethod
    @abstractmethod
    def name() -> str:
        pass

    @staticmethod
    @abstractmethod
    def description() -> str:
        pass


class SingleStepTransformation(TransformationFixpoint):

    def __init__(self):
        pass

    def transform_until_stable[T](self, cfg: CFG, analyses_results: dict[Analysis[T], dict[CFG.Node, T]]) -> tuple[CFG, bool]:
        return self.transform(cfg, analyses_results), False

    @abstractmethod
    def transform[T](self, cfg: CFG, analyses_results: dict[Analysis[T], dict[CFG.Node, T]]) -> CFG:
        pass
