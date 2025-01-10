from abc import abstractmethod
from typing import Any, Literal, Tuple

from analyses.analysis import Analysis
from cfg.cfg import CFG
from util.bcolors import BColors


def topo_sort_nodes(cfg: CFG) -> list[CFG.Node]:
    visited_nodes = set()

    sorted_nodes = []

    def dfs_node(current_node: CFG.Node):
        if current_node in visited_nodes:
            return

        visited_nodes.add(current_node)

        sorted_nodes.append(current_node)

        for e in cfg.get_outgoing(current_node):
            dfs_node(e.dest)

    for node in cfg.get_nodes():
        if node.is_start:
            dfs_node(node)

    return sorted_nodes


def sort_nodes(type: Literal['forward', 'backward'], cfg: CFG):
    sorted_nodes = topo_sort_nodes(cfg)

    if type == 'backward':
        rev = sorted_nodes[::-1]
        return rev
    elif type == 'forward':
        return sorted_nodes


class Solver:

    @ abstractmethod
    def solve(self, cfg: CFG, analysis: Analysis) -> Tuple[dict[CFG.Node, dict[CFG.Node, Any]], int]:
        pass
