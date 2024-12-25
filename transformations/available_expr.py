
from cfg.CFG import Assignment, Command, Node, CFG
from pycparser import c_ast


def transformation1_1(cfg: CFG):
    """
    Transformation 1.1
    Assignemnt x = e  -->  T_e=e; x = T_e
    """

    for edge in cfg.edges:
        A = edge.source
        B = edge.dest

        if edge.command.type == "assignment":
            pass