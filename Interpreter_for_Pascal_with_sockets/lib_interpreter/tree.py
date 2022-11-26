from abc import ABC
from .tokens import Token

class Node(ABC):
    ...

class Variable(Node):
    def __init__(self, value : Token) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"Variable ({self.value})"

class Number(Node):

    def __init__(self, value: Token) -> None:
        self.value = value

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.value})"

class AssignOp(Node):
    def __init__(self, left_variable : Variable, right : Node) -> None:
        self.left = left_variable
        self.right = right

    def __str__(self) -> str:
        return f"AssignOp ({self.left} := {self.right})"

class BinOp(Node):
    def __init__(self, left: Node, op: Token, right: Node) -> None:
        self.left = left
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"BinOp ({self.op.value}, {self.left}, {self.right})"

class UnOp(Node):
    def __init__(self, op: Token, right: Node) -> None:
        self.op = op
        self.right = right

    def __str__(self) -> str:
        return f"UnOp ({self.op.value}, {self.right})"

class NodeVisitor:
    def visit(self, node: Node) -> float:
        raise NotImplementedError