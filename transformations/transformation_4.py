

from typing import Any
from Lattices.ZFlat import DLattice
from analysis.analysis import Analysis
from analysis.available_expr import AvailableExpressions
from analysis.constant_propagation import ConstantPropagation, abstract_eval
from analysis.live_variables import LiveVariables
from analysis.expression_stores import ExprStores
from analysis.true_live_variables import TrueLiveVariables
from cfg.cfg import CFG
from cfg.command import AssignmentCommand, LoadsCommand, NegCommand, PosCommand, SkipCommand, StoresCommand
from cfg.expression import BinExpression, Constant, UnaryExpression
from transformations.transformation import Transformation
from transformations.transformation_1_1 import Transformation_1_1


class Transformation_4(Transformation):

    def name(self) -> str:
        return "Transformation 4"

    def dependencies(self):
        self.CP = ConstantPropagation()
        return [self.CP]

    def transform(self, cfg: CFG, analyses_results: dict[Analysis, Any]) -> CFG:
        """
        Transformation 4
        bot -> delete[node]
        """

        lattice = self.CP.lattice
        D = analyses_results[self.CP]

        for node in cfg.get_nodes():
            if D[node] == '⊥':
                incoming_edges = cfg.get_incoming(node)
                outgoing_edges = cfg.get_outgoing(node)

                for edge in incoming_edges | outgoing_edges:
                    cfg.edges.remove(edge)

        edge_copy = cfg.edges.copy()
        for edge in edge_copy:
            U = edge.source

            if type(edge.command) == PosCommand:
                expr = edge.command.expr

                if not lattice.eq(D[U], '⊥') and not abstract_eval(expr, D[U]) in [0, '⊤']:

                    x = abstract_eval(expr, D[U])
                    edge.command = SkipCommand()

            elif type(edge.command) == NegCommand:
                expr = edge.command.expr

                if not lattice.eq(D[U], '⊥') and abstract_eval(expr, D[U]) == 0:
                    edge.command = SkipCommand()

            elif type(edge.command) == AssignmentCommand:
                rhs = edge.command.expr

                if not lattice.eq(D[U], '⊥'):
                    simplified_rhs = abstract_eval(rhs, D[U])

                    if simplified_rhs == '⊤' or simplified_rhs == '⊥':
                        continue

                    if simplified_rhs != '⊥':
                        edge.command = AssignmentCommand(
                            edge.command.lvalue, Constant(simplified_rhs))

        return cfg
