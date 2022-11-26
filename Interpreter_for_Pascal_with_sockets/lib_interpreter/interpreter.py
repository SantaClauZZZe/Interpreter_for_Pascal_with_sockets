from .parser import *
from .tree import *
from .tokens import *

class InterpreterException(Exception):
    ...

class Interpreter(NodeVisitor):
    def __init__(self):
        self.variables : dict[str, float] = {}
        self.parser = Parser()

    def visit(self, node: Node) -> float:
        if isinstance(node, Variable):
            return self.visit_variable(node)
        if isinstance(node, Number):
            return self.visit_number(node)
        elif isinstance(node, AssignOp):
            return self.visit_assign_op(node)
        elif isinstance(node, BinOp):
            return self.visit_bin_op(node)
        elif isinstance(node, UnOp):
            return self.visit_un_op(node)

        # raise IndentationError("Invalid Node")

    def visit_variable(self, var : Variable) -> float:
        try:
            return self.variables[var.value.value]
        except:
            raise InterpreterException("Undefined variable")

    def visit_number(self, node: Number) -> float:
        return float(node.value.value)

    def visit_assign_op(self, node: AssignOp) -> float:
        self.variables[node.left.value.value] = self.visit(node.right)
        return self.variables[node.left.value.value]

    def visit_bin_op(self, node: BinOp) -> float:
        match node.op.type:
            case TokenType.PLUS:
                return self.visit(node.left) + self.visit(node.right)
            case TokenType.MINUS:
                return self.visit(node.left) - self.visit(node.right)
            case TokenType.MUL:
                return self.visit(node.left) * self.visit(node.right)
            case TokenType.DIV:
                return self.visit(node.left) / self.visit(node.right)

        # raise InterpreterException("Invalid operator")

    def visit_un_op(self, node: UnOp) -> float:
        match node.op.type:
            case TokenType.MINUS:
                return -float(self.visit(node.right))

        # raise InterpreterException("Invalid unary operator")

    def eval(self, text: str, return_variables = False, return_tree = False) -> float | tuple | None:
        self.parser.init_parser(text)
        tree = self.parser.complex_statement()

        # print(tree)

        res = (None,)

        if tree is not None:
            res = (self.visit(tree),)

        if (return_variables):
            res = (*res, self.variables)

        if return_tree:
            res = (*res, tree.__str__())

        return res