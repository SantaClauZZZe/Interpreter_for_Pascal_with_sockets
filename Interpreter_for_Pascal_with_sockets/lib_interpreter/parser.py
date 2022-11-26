from .lexer import *
from .tree import *
from .tokens import Token, TokenType

class ParserException(Exception):
    ...

class Parser:

    def __init__(self):
        self.current_token: Token | None = None
        self.nesting = -1    # вложенность
        self.lexer = Lexer()

    def init_parser(self, text: str) -> None:
        self.lexer.init_lexer(text)
        if self.lexer.is_empty():
            self.current_token = None
        else:
            self.current_token = self.lexer.next()

    def check_type(self, type_: TokenType):
        if self.current_token is None:
            raise ParserException("Current token is not defined")

        if self.current_token.type == type_:
            self.current_token = self.lexer.next()
            return

        raise ParserException(
            f"invalid token order. Expected {type_}, Received {self.current_token.type}")

    def complex_statement(self) -> Node | None:
        if self.current_token == None:
            return None
        elif self.current_token.type == TokenType.BEGIN:
            self.nesting += 1
        elif self.current_token.type == TokenType.END:
            self.nesting -= 1
        elif self.current_token.type == TokenType.FINISH_PROGRAM:
            self.nesting -= 1
            if self.nesting != -1:
                raise ParserException("Error with Begin or End operators!")
        elif self.nesting >= 0:
            return self.statement()
        else:
            raise ParserException("The begin operator was expected")

    def statement(self) -> Node | None:
        if self.current_token is None:
            raise ParserException("Current token is not defined")
            
        if self.current_token.type == TokenType.VARIABLE:
            return self.assignment()
        else:
            return self.expr()

    def assignment(self) -> Node:
        token_var = self.current_token
        self.check_type(TokenType.VARIABLE)

        if self.current_token.type == TokenType.EOL:
            return Variable(token_var)

        self.check_type(TokenType.INIT)
        result = self.expr()
        return AssignOp(Variable(token_var), result)

    def expr(self) -> Node:
        ops = [TokenType.MINUS, TokenType.PLUS]
        result = self.term()

        while self.current_token.type in ops:
            token = self.current_token
            match token.type:
                case TokenType.PLUS:
                    self.check_type(TokenType.PLUS)
                case TokenType.MINUS:
                    self.check_type(TokenType.MINUS)

            result = BinOp(result, token, self.term())

        return result

    def term(self) -> Node:
        ops = [TokenType.MUL, TokenType.DIV]
        result = self.factor()

        while self.current_token.type in ops:
            token = self.current_token
            match token.type:
                case TokenType.DIV:
                    self.check_type(TokenType.DIV)
                case TokenType.MUL:
                    self.check_type(TokenType.MUL)

            result = BinOp(result, token, self.factor())

        return result

    def factor(self) -> Node:
        if (self.current_token is None):
            raise ParserException("Current token is not defined")

        token = self.current_token

        if token.type == TokenType.NUMBER:
            self.check_type(TokenType.NUMBER)
            return Number(token)
        elif token.type == TokenType.MINUS:
            self.check_type(TokenType.MINUS)
            result = self.factor()
            return UnOp(token, result)
        elif token.type == TokenType.PLUS:
            self.check_type(TokenType.PLUS)
            result = self.factor()
            return result
        elif token.type == TokenType.LPAREN:
            self.check_type(TokenType.LPAREN)
            result = self.expr()
            self.check_type(TokenType.RPAREN)
            return result
        elif token.type == TokenType.VARIABLE:
            self.check_type(TokenType.VARIABLE)
            return Variable(token)

        raise ParserException("Invalid factor")