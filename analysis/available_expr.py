
from CFG import Assignment, Command, Node
from pycparser import c_ast


def check_occurence(expr: c_ast.Node, lvalue):
    if isinstance(expr, c_ast.ID):
        return expr.name == lvalue
    elif isinstance(expr, c_ast.BinaryOp):
        return check_occurence(expr.left, lvalue) or check_occurence(expr.right, lvalue)
    elif isinstance(expr, c_ast.UnaryOp):
        return check_occurence(expr.expr, lvalue)
    else:
        return False


class AvailableExpressions:

    def __init__(self):
        pass

    def init(self):
        return set()

    def skip(self, x: tuple):
        return x

    def assignment(self, expr: Assignment, A: set):
        Acpy = A.copy()

        lhs = expr.lhs
        rhs = expr.rhs

        Acpy.add(rhs)

        filtered = set([x for x in Acpy if not check_occurence(x, lhs)])

        return filtered

    def loads(self, expr: c_ast.Node, A: set):
        Acpy = A.copy()

        lhs = expr.lhs
        rhs = expr.rhs

        Acpy.add(rhs)

        filtered = set([x for x in Acpy if not check_occurence(x, lhs)])

        return filtered

    def stores(self, expr: c_ast.Node, A: set):
        e1 = expr.expr1
        e2 = expr.expr2

        new_A = A.copy().add(e1).add(e2)

        return new_A

    def Pos(self, expr: c_ast.Node, A: set):
        return A.copy().add(expr)

    def Neg(self, expr: c_ast.Node, A: set):
        return A.copy().add(expr)

    def transfer(self, command: Command, A: set):
        if command.type == 'skip':
            return self.skip(A)
        elif command.type == 'assignment':
            return self.assignment(command.expr, A)
        elif command.type == 'load':
            return self.loads(command.expr, A)
        elif command.type == 'store':
            return self.stores(command.expr, A)
        elif command.type == 'Pos':
            return self.Pos(command.expr, A)
        elif command.type == 'Neg':
            return self.Neg(command.expr, A)
        else:
            raise ValueError(f"Unknown command type: {command.type}")
