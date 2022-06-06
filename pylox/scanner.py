from pylox.tokens import TokenType

def error(line: int, message: str):
    print(f"[line: {line}]: Error {message}")

class LoxToken:
    
    def __init__(self, type_: TokenType, lexeme: str, literal: str, line: int):
        self.type = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __eq__(self, other):
        return (self.type == other.type) and (self.lexeme == other.lexeme) and (self.literal == other.literal) and (self.line == other.line)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type}, lexeme='{self.lexeme}', literal={self.literal}, line={self.line})"


class LoxScanner:
    
    def __init__(self, source):
        self.source = source
        self.tokens = []
        
        self._start = 0
        self._current = 0;
        self._line = 1;

    def is_at_end(self):
        return self._current >= len(self.source)

    def scan_tokens(self):
        """
        Main interpreter loop
        """
        while not self.is_at_end():
            self._start = self._current;
            self.scan_token()
        return self.tokens

    def advance(self):
        char =  self.source[self._current]
        self._inc_current()
        return char
    
    def add_token(self, type_: str):
        self._add_token(type_=type_, literal=None)
    
    def _add_token(self, type_, literal):
        text = self.source[self._start: self._current]
        token = LoxToken(type_=type_, lexeme = text, literal=literal, line=self._line)
        self.tokens.append(token)

    def scan_token(self):
        """
        Identify the tokens we are seeing
        """
        char = self.advance()

        # 1 char tokens
        if char == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif char == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif char == "[":
            self.add_token(TokenType.LEFT_BRACE)
        elif char == "]":
            self.add_token(TokenType.RIGHT_BRACE)
        elif char == ",":
            self.add_token(TokenType.COMMA)
        elif char == ".":
            self.add_token(TokenType.DOT)
        elif char == "-":
            self.add_token(TokenType.MINUS)
        elif char == "+":
            self.add_token(TokenType.PLUS)
        elif char == ";":
            self.add_token(TokenType.SEMICOLON)
        elif char == "*":
            self.add_token(TokenType.STAR)
        elif char == "/":
            if self.match(expected="/"):
                # We matched a comment
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TokenType.SLASH)
        
        # 1-2 char tokens
        elif char == "!":
            self.add_token(TokenType.BANG_EQUAL if self.match(expected="=") else TokenType.BANG)
        elif char == "=":
            self.add_token(TokenType.EQUAL_EQUAL if self.match(expected="=") else TokenType.EQUAL)
        elif char == "<":
            self.add_token(TokenType.LESS_EQUAL if self.match(expected="=") else TokenType.LESS)    
        elif char == ">":
            self.add_token(TokenType.GREATER_EQUAL if self.match(expected="=") else TokenType.GREATER)
        else:
            error(self._line, f"Token at {self._current} not recognised")

    def peek(self):
        if self.is_at_end(): return '\0';
        return self.source[self._current]


    def match(self, expected):
        """Return true if the current character matches

        Args:
            expected (str): The character that we expect to match

        Returns:
            boolean: True if there is a match, False otherwise
        """
        if self.is_at_end(): return False
        if not (self.source[self._current] == expected): return False
        self._inc_current()
        return True

    def _inc_current(self):
        """
        Increments the current character offset in the scanner
        """
        self._current += 1
