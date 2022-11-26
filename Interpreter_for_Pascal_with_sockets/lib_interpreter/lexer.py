from .tokens import Token, TokenType

class LexerException(Exception):
    ...

class Lexer:
    def __init__(self):
        self.pos = -1
        self.text = ""
        self.current_char = ""

    def init_lexer(self, text: str):
        self.pos = -1
        self.text = text

    def is_empty(self) -> bool:
        if self.text == "":
            return True

        return False not in [elem.isspace() for elem in self.text]

    def forward(self):
        self.pos += 1
        if self.pos >= len(self.text):
            self.current_char = ""
        else:
            self.current_char = self.text[self.pos]

        return self.current_char

    def back(self):
        self.pos -= 1
        self.current_char = self.text[self.pos]

        return self.current_char

    def next(self) -> Token:
        while self.forward() != "":
            if self.current_char.isspace():
                self.skip()
                continue
            if self.current_char.isdigit():
                return Token(TokenType.NUMBER, self.number())
            if self.current_char == "+":
                return Token(TokenType.PLUS, self.current_char)
            if self.current_char == "-":
                return Token(TokenType.MINUS, self.current_char)
            if self.current_char == "*":
                return Token(TokenType.MUL, self.current_char)
            if self.current_char == "/":
                return Token(TokenType.DIV, self.current_char)
            if self.current_char == "(":
                return Token(TokenType.LPAREN, self.current_char)
            if self.current_char == ")":
                return Token(TokenType.RPAREN, self.current_char)
            if self.current_char.isalpha():
                word = self.word()

                next_char = self.forward()
                self.back()

                if word == "BEGIN":
                    return Token(TokenType.BEGIN, "")
                elif word == "END" and next_char == ';':
                    return Token(TokenType.END, "")
                elif word == "END" and next_char == '.':
                    return Token(TokenType.FINISH_PROGRAM, "")
                else:
                    return Token(TokenType.VARIABLE, word)
            if self.current_char == ':':
                next_char = self.forward()

                if next_char == '=':
                    return Token(TokenType.INIT, "")
                
                self.back()
            if self.current_char == ';':
                return Token(TokenType.EOL, "")
            raise LexerException("bad token")
        raise LexerException("Expected ;")    #return Token(TokenType.EOL, "")

    def skip(self):
        while self.current_char != "" and self.current_char.isspace():
            self.forward()
        
        self.back()

    def word(self) -> str:
        res = ""

        while self.current_char != "" and (self.current_char.isalpha() or self.current_char.isdigit()):
            res += self.current_char
            self.forward()

        self.back()

        return res

    def number(self) -> str:
        result = []

        while self.current_char != "" and \
                (self.current_char.isdigit() or 
                self.current_char == '.'):
            result.append(self.current_char)
            self.forward()

        self.back()

        return "".join(result)