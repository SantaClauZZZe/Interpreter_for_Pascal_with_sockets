# Tokens.py

from enum import Enum, auto

class TokenType(Enum):
    VARIABLE = auto()
    INIT = auto()

    NUMBER = auto()

    PLUS = auto()
    MINUS = auto()
    DIV = auto()
    MUL = auto()

    BEGIN = auto()
    END = auto() # END;

    FINISH_PROGRAM = auto() # END.

    EOL = auto()

    LPAREN = auto()
    RPAREN = auto()

class Token:

    def __init__(self, type_ : TokenType, value : str):
        self.type = type_
        self.value = value

    def __str__(self) -> str:
        return f"Token ({self.type}, {self.value})"