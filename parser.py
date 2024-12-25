from typing import Optional
from pycparser import c_parser, c_ast

from cfg.CFG import CFG, Command, Node
from cfg.Command import AssignmentCommand, NegCommand, SkipCommand, PosCommand
from cfg.Expression import ID, convertToExpr


class Parser:
    def __init__(self, filename, only_func=None):
        self.filename = filename
        self.cfg = CFG()
        self.node_counter = 0
        self.only_func = only_func

    def parse(self):
        with open(self.filename) as f:
            content = f.read()

        parser = c_parser.CParser()
        ast = parser.parse(content)

        self.cfg = CFG()

        assert isinstance(ast, c_ast.FileAST)

        for decl in ast.ext:
            self.visit(decl, None)

        return self.cfg

    def visit(self, ast_node: c_ast.Node, entry_node: Node, exit_node: Optional[Node] = None) -> Node | None:

        if isinstance(ast_node, c_ast.FuncDef):
            name = ast_node.decl.name

            entry_node, exit_node = Node.make_function_nodes(name)
            out = self.visit(ast_node.body, entry_node, exit_node)

            return out

        elif isinstance(ast_node, c_ast.Compound):
            current: Node = entry_node
            for stmt in ast_node.block_items or []:
                out = self.visit(stmt, current, exit_node)
                if out is not None:
                    current = out

            # self.cfg.add_edge(current, exit_node, SkipCommand())

            return current

        elif isinstance(ast_node, c_ast.If):
            true_entry, false_entry = Node.make_if_nodes()

            cond_expr = convertToExpr(ast_node.cond)

            self.cfg.add_edge(entry_node, true_entry,
                              PosCommand(cond_expr))
            self.cfg.add_edge(entry_node, false_entry,
                              NegCommand(cond_expr))

            out_true = self.visit(ast_node.iftrue, true_entry, exit_node)
            out_false = self.visit(ast_node.iffalse, false_entry, exit_node)

            if exit_node is None:
                exit_node = Node.make_skip_node()

            self.cfg.add_edge(out_true, exit_node, SkipCommand())
            self.cfg.add_edge(out_false, exit_node, SkipCommand())

            return exit_node

        elif isinstance(ast_node, c_ast.Assignment):
            node = Node.make_stmt_node()

            self.cfg.add_edge(entry_node, node, AssignmentCommand(
                convertToExpr(ast_node.lvalue), convertToExpr(ast_node.rvalue)))

            return node

        elif isinstance(ast_node, c_ast.Decl):
            if ast_node.init is None:
                return None

            node = Node.make_stmt_node()

            self.cfg.add_edge(entry_node, node, AssignmentCommand(ID(
                ast_node.name), convertToExpr(ast_node.init)))

            return node

        raise NotImplementedError(ast_node)
