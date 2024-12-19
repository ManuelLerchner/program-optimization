from CFG import CFG


class Solver:
    def __init__(self, cfg: CFG, analysis):
        self.cfg = cfg
        self.analysis = analysis

    def solve(self):
        self.states = {node: self.analysis.init() for node in self.cfg.get_nodes()}

        changed = True
        while changed:
            changed = False
            for edge in self.cfg.edges:
                source_state = self.states[edge.source]
                dest_state = self.states[edge.dest]

                new_state = self.analysis.transfer(edge.command, source_state)

                if new_state != dest_state:
                    self.states[edge.dest] = new_state
                    changed = True

        return self.states
