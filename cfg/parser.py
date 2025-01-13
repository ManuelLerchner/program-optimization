from collections import defaultdict
from typing import Optional

from pycparser import c_ast, c_parser

from cfg.cfg import CFG
from cfg.IMP.command import (AllocCommand, AssignmentCommand, BlockReadCommand,
                             BlockWriteCommand, FunCallCommand, LoadsCommand,
                             NegCommand, PosCommand, SkipCommand,
                             StoresCommand)
from cfg.IMP.expression import convertToExpr
from transformations.transformation_0 import Transformation_0


class Parser:
    def __init__(self, filename):
        self.filename = filename
        self.cfg = CFG()
        self.node_counter = 0
        self.current_function = None
        self.curr_continue = None
        self.curr_break = None
        self.locals = defaultdict(set)
        self.globals = defaultdict(None)

    def parse(self) -> CFG:
        with open(self.filename) as f:
            content = f.read()

        parser = c_parser.CParser()
        ast = parser.parse(content)

        self.cfg = CFG()

        assert isinstance(ast, c_ast.FileAST)

        for decl in ast.ext:
            self.visit(decl, entry_node=None, exit_node=None)

        self.cfg.path = "/".join(self.filename.split("/")[:-1])
        self.cfg.filename = self.filename.split("/")[-1]

        for node in self.cfg.get_nodes():
            node.age += 1
        for edge in self.cfg.edges:
            edge.age += 1

        return Transformation_0().transform(self.cfg, {})

    def visit(self, ast_node: c_ast.Node, entry_node: CFG.Node | None, exit_node: Optional[CFG.Node] = None) -> CFG.Node | None:

        if isinstance(ast_node, c_ast.FuncDef):
            name = ast_node.decl.name

            previous_function = self.current_function
            self.current_function = name

            entry_node, exit_node = self.cfg.make_function_nodes(name)
            assert entry_node is not None
            out = self.visit(ast_node.body, entry_node, exit_node)

            self.cfg.add_edge(out, exit_node, SkipCommand())

            entry_node.locals = sorted(self.locals[name], key=lambda x: str(x)) if self.locals.get(
                name) is not None else set()
            entry_node.globals = sorted(self.globals, key=lambda x: str(x))
            self.current_function = previous_function

            return exit_node

        elif isinstance(ast_node, c_ast.Compound):
            current = entry_node
            for stmt in ast_node.block_items or []:
                out = self.visit(stmt, current, exit_node)
                current = out

            # self.cfg.add_edge(current, exit_node, SkipCommand())

            return current

        elif isinstance(ast_node, c_ast.If):
            true_entry, false_entry = self.cfg.make_if_nodes()

            combine_node = self.cfg.make_skip_node()

            cond_expr = convertToExpr(ast_node.cond)

            self.cfg.add_edge(entry_node, true_entry,
                              PosCommand(cond_expr))
            self.cfg.add_edge(entry_node, false_entry,
                              NegCommand(cond_expr))

            out_true = self.visit(ast_node.iftrue, true_entry, combine_node)

            if ast_node.iffalse is not None:
                out_false = self.visit(
                    ast_node.iffalse, false_entry, combine_node)

                self.cfg.add_edge(out_false, combine_node, SkipCommand())
            else:
                self.cfg.add_edge(false_entry, combine_node, SkipCommand())

            if out_true is not None:
                self.cfg.add_edge(out_true, combine_node, SkipCommand())

            return combine_node

        elif isinstance(ast_node, c_ast.Assignment):
            command: AssignmentCommand | LoadsCommand | StoresCommand | BlockReadCommand | BlockWriteCommand | AllocCommand
            if (type(ast_node.lvalue) == c_ast.ArrayRef):
                if ast_node.lvalue.name.name == "M":
                    command = StoresCommand(convertToExpr(
                        ast_node.lvalue.subscript), convertToExpr(ast_node.rvalue))
                    node = self.cfg.make_stores_node()
                else:
                    command = BlockWriteCommand(convertToExpr(
                        ast_node.lvalue.name), convertToExpr(ast_node.lvalue.subscript), convertToExpr(ast_node.rvalue))
                    node = self.cfg.make_block_write_node()
            elif (type(ast_node.rvalue) == c_ast.ArrayRef):
                if ast_node.rvalue.name.name == "M":
                    command = LoadsCommand(convertToExpr(
                        ast_node.lvalue), convertToExpr(ast_node.rvalue.subscript))
                    node = self.cfg.make_loads_node()
                else:
                    command = BlockReadCommand(convertToExpr(
                        ast_node.lvalue), convertToExpr(ast_node.rvalue.name), convertToExpr(ast_node.rvalue.subscript))
                    node = self.cfg.make_block_read_node()

            else:
                command = AssignmentCommand(convertToExpr(
                    ast_node.lvalue), convertToExpr(ast_node.rvalue))
                node = self.cfg.make_stmt_node()

            self.cfg.add_edge(entry_node, node, command)

            return node

        elif isinstance(ast_node, c_ast.Decl):
            if ast_node.init is None:
                self.globals[ast_node.name] = None
                return None

            self.locals[self.current_function].add(ast_node.name)

            if (type(ast_node.init) == c_ast.ArrayRef):
                if ast_node.init.name.name == "M":
                    command = LoadsCommand(convertToExpr(
                        c_ast.ID(ast_node.name)), convertToExpr(ast_node.init.subscript))
                    node = self.cfg.make_stores_node()
                else:
                    command = BlockReadCommand(convertToExpr(
                        c_ast.ID(ast_node.name)), convertToExpr(ast_node.init.name), convertToExpr(ast_node.init.subscript))
                    node = self.cfg.make_block_read_node()
            elif (type(ast_node.init) == c_ast.ArrayRef):
                if ast_node.init.name.name == "M":
                    command = StoresCommand(convertToExpr(
                        c_ast.ID(ast_node.name)), convertToExpr(ast_node.init.subscript))
                    node = self.cfg.make_loads_node()
                else:
                    command = BlockWriteCommand(convertToExpr(
                        c_ast.ID(ast_node.name)), convertToExpr(ast_node.init.name), convertToExpr(ast_node.init.field))
                    node = self.cfg.make_block_write_node()
            elif (type(ast_node.init) == c_ast.FuncCall) and ast_node.init.name.name == "new":
                command = AllocCommand(convertToExpr(c_ast.ID(ast_node.name)))
                node = self.cfg.make_alloc_node()
            else:
                command = AssignmentCommand(convertToExpr(
                    c_ast.ID(ast_node.name)), convertToExpr(ast_node.init))
                node = self.cfg.make_stmt_node()

            self.cfg.add_edge(entry_node, node, command)

            return node

        elif isinstance(ast_node, c_ast.While):
            loop_entry, loop_exit = self.cfg.make_loop_nodes()

            cond_expr = convertToExpr(ast_node.cond)

            old_continue = self.curr_continue
            old_break = self.curr_break

            self.curr_continue = loop_entry
            self.curr_break = loop_exit

            out = self.visit(ast_node.stmt, loop_entry, loop_exit)

            self.curr_continue = old_continue
            self.curr_break = old_break

            if entry_node is not None:
                entry_node.is_loop_separator = True

            self.cfg.add_edge(entry_node, loop_entry,
                              PosCommand(cond_expr))
            self.cfg.add_edge(entry_node, loop_exit,
                              NegCommand(cond_expr))

            self.cfg.add_edge(out, entry_node, SkipCommand())

            return loop_exit

        elif isinstance(ast_node, c_ast.DoWhile):
            loop_entry, loop_exit = self.cfg.make_loop_nodes()

            old_continue = self.curr_continue
            old_break = self.curr_break

            self.curr_continue = loop_entry
            self.curr_break = loop_exit

            out = self.visit(ast_node.stmt, loop_entry, loop_exit)

            self.curr_continue = old_continue
            self.curr_break = old_break

            if entry_node is not None:
                entry_node.is_loop_separator = True

            self.cfg.add_edge(entry_node, loop_entry, SkipCommand())

            cond_expr = convertToExpr(ast_node.cond)
            self.cfg.add_edge(out, entry_node, PosCommand(cond_expr))
            self.cfg.add_edge(out, loop_exit, NegCommand(cond_expr))

            return loop_exit

        elif isinstance(ast_node, c_ast.EmptyStatement):
            skip_node = self.cfg.make_skip_node()

            self.cfg.add_edge(entry_node, skip_node,
                              SkipCommand(cfg_keep=True))

            return skip_node

        elif isinstance(ast_node, c_ast.FuncCall):
            node = self.cfg.make_stmt_node()
            self.cfg.add_edge(entry_node, node,
                              FunCallCommand(ast_node.name.name))
            return node

        elif isinstance(ast_node, c_ast.Break):
            self.cfg.add_edge(entry_node, self.curr_break, SkipCommand())
            return None

        elif isinstance(ast_node, c_ast.Continue):
            self.cfg.add_edge(entry_node, self.curr_continue, SkipCommand())
            return None

        raise NotImplementedError(ast_node)
