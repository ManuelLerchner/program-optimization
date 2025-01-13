

from typing import Any

from src.analyses.analysis import Analysis
from src.cfg.cfg import CFG
from src.transformations.transformation import SingleStepTransformation


class Transformation_Blank(SingleStepTransformation):

    def __init__(self, analysis: Analysis):
        self.analysis = analysis

    @staticmethod
    def name() -> str:
        return "Blank"

    @staticmethod
    def description() -> str:
        return "Run the analysis"

    def dependencies(self):
        return [self.analysis]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, Any]) -> CFG:
        return cfg
