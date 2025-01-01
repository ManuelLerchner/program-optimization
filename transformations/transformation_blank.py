

from typing import Any

from analyses.analysis import Analysis
from cfg.cfg import CFG
from cfg.IMP.command import SkipCommand
from transformations.transformation import Transformation


class Transformation_Blank(Transformation):

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
