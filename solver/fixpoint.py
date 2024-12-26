from typing import Literal
from analysis.analysis import Analysis
from cfg.cfg import CFG
from cfg.edge import Edge
from cfg.node import Node
from solver.solver import Solver
from util.bcolors import BColors


def topo_sort_edges(cfg: CFG) -> list[Edge]:
    visited_edges = set()
    edge_order = []

    def dfs_edge(current_edge: Edge):
        if current_edge in visited_edges:
            return

        visited_edges.add(current_edge)

        outgoing_edges = cfg.get_outgoing(current_edge.dest)

        for dep_edge in outgoing_edges:
            dfs_edge(dep_edge)

        edge_order.append(current_edge)

    start_nodes = []
    for node in cfg.get_nodes():
        if len(cfg.get_incoming(node)) == 0:
            start_nodes.append(node)

    for node in start_nodes:
        for edge in cfg.get_outgoing(node):
            dfs_edge(edge)

    return edge_order


def sort_edges(type: Literal['forward', 'backward'], cfg: CFG):
    sorted_edges = topo_sort_edges(cfg)

    if type == 'backward':
        return sorted_edges
    elif type == 'forward':
        return sorted_edges[::-1]


class FixpointSolver(Solver):

    @staticmethod
    def solve[T](cfg: CFG, analysis: Analysis[T], debug=False):
        states: dict[Node, T] = {}

        lattice = analysis.lattice

        edges = sort_edges(analysis.type, cfg)

        for edge in edges:
            states[edge.source] = analysis.lattice.bot()
            states[edge.dest] = analysis.lattice.bot()

        changed = True
        iterations = 1
        while changed:
            changed = False
            if debug:
                print(f"{BColors.WARNING}Iteration {iterations}{BColors.ENDC}")

            for edge in edges:
                src, dest = (edge.source, edge.dest) if analysis.type == 'forward' else (
                    edge.dest, edge.source)
                dest_state, source_state = states[dest], states[src]

                new_state = lattice.join(
                    dest_state, analysis.transfer(source_state, edge.command))

                if debug:
                    Solver.print_edge(
                        analysis, edge, source_state, dest_state, new_state)

                if not lattice.eq(new_state, dest_state):
                    changed = True

                states[dest] = new_state

            iterations += 1

        if debug:
            print()

        return states
