from pycparser import c_parser, c_ast

from CFG import CFG, Command, Node


class Parser:
    def __init__(self, filename, only_func=None):
        self.filename = filename
        self.cfg = CFG()
        self.node_counter = 0
        self.only_func = only_func

    def get_new_node(self, prefix="node"):
        self.node_counter += 1
        return Node(self.node_counter, prefix)

    def parse(self):
        with open(self.filename) as f:
            content = f.read()

        parser = c_parser.CParser()
        ast = parser.parse(content)

        start_node = self.get_new_node("START")
        end_node = self.get_new_node("END")

        self.cfg = CFG()
        self.visit(ast, start_node, end_node)

        return self.cfg

    def visit(self, node, entry_node, exit_node):
        if node is None:
            return entry_node, exit_node

        if isinstance(node, c_ast.FileAST):
            current_entry = entry_node
            for decl in node.ext:
                current_exit = self.get_new_node("decl")
                self.visit(decl, current_entry, current_exit)
                current_entry = current_exit
            self.cfg.add_edge(current_entry, exit_node, Command("skip"))

        elif isinstance(node, c_ast.FuncDef):

            func_entry = self.get_new_node("func_entry")
            func_exit = self.get_new_node("func_exit")

            self.cfg.add_edge(entry_node, func_entry,
                              Command("function_entry", node.decl))

            if self.only_func and node.decl.name == self.only_func:
                # reset the cfg
                self.cfg = CFG()

            self.visit(node.body, func_entry, func_exit)
            self.cfg.add_edge(func_exit, exit_node, Command("skip"))

            self.cfg.finalize()

        elif isinstance(node, c_ast.Compound):
            current_entry = entry_node
            for stmt in node.block_items or []:
                current_exit = self.get_new_node("stmt")
                self.visit(stmt, current_entry, current_exit)
                current_entry = current_exit
            self.cfg.add_edge(current_entry, exit_node, Command("skip"))

        elif isinstance(node, c_ast.If):
            true_entry = self.get_new_node("if_true")
            false_entry = self.get_new_node("if_false")

            self.cfg.add_edge(entry_node, true_entry,
                              Command("Pos", node.cond))
            self.cfg.add_edge(entry_node, false_entry,
                              Command("Neg", node.cond))

            self.visit(node.iftrue, true_entry, exit_node)

            if node.iffalse:
                self.visit(node.iffalse, false_entry, exit_node)
            else:
                self.cfg.add_edge(false_entry, exit_node,
                                  Command("empty_else"))

        elif isinstance(node, c_ast.Assignment) or isinstance(node, c_ast.Decl):
            stmt_node = self.get_new_node("assign")
            self.cfg.add_edge(entry_node, stmt_node,
                              Command("assignment", node))
            self.cfg.add_edge(stmt_node, exit_node, Command("skip"))

        elif isinstance(node, c_ast.Return):
            stmt_node = self.get_new_node("return")
            self.cfg.add_edge(entry_node, stmt_node,
                              Command("return", node.expr))
            self.cfg.add_edge(stmt_node, exit_node, Command("skip"))

        else:
            self.cfg.add_edge(entry_node, exit_node,
                              Command("", node))
