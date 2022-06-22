from pylox.tokens import TokenType


def error(line: int, message: str):
    print(f"[line: {line}]: Error {message}")


def is_digit(char):
    return "0" <= char <= "9"


def is_alpha(char):
    return ("a" <= char <= "z") or ("A" <= char <= "Z") or (char == "_")


def is_alphanumeric(char):
    return is_digit(char) or is_alpha(char)


class TokenNotRecognised(Exception):
    pass


class UnterminatedLine(Exception):
    pass


class LoxToken:
    def __init__(
        self, type_: TokenType, lexeme: str, literal: str, line: int, offset: int
    ):
        self.type_ = type_
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
        self.offset = offset

    def __eq__(self, other):
        return (
            (self.type_ == other.type_)
            and (self.lexeme == other.lexeme)
            and (self.literal == other.literal)
            and (self.line == other.line)
            and (self.offset == other.offset)
        )

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type_}, lexeme='{self.lexeme}', literal={self.literal}, line={self.line}, offset={self.offset})"

    def __hash__(self):
        return hash((self.type_, self.lexeme, self.literal, self.line, self.offset))


class LoxScanner:
    def __init__(self, source):
        self.source = source
        self.tokens = []

        self._start = 0
        self._current = 0
        self._line = 1

    def scan_tokens(self):
        """
        Main interpreter loop
        """
        while not self.is_at_end():
            self._start = self._current
            self.scan_token()
        return self.tokens

    def advance(self):
        char = self.source[self._current]
        self._inc_current()
        return char

    def add_token(self, type_: str):
        self._add_token(type_=type_, literal=None)

    def _add_token(self, type_, literal):
        text = self.source[self._start : self._current]
        token = LoxToken(
            type_=type_,
            lexeme=text,
            literal=literal,
            line=self._line,
            offset=self._start,
        )
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
        elif char == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif char == "}":
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
            self.add_token(
                TokenType.BANG_EQUAL if self.match(expected="=") else TokenType.BANG
            )
        elif char == "=":
            self.add_token(
                TokenType.EQUAL_EQUAL if self.match(expected="=") else TokenType.EQUAL
            )
        elif char == "<":
            self.add_token(
                TokenType.LESS_EQUAL if self.match(expected="=") else TokenType.LESS
            )
        elif char == ">":
            self.add_token(
                TokenType.GREATER_EQUAL
                if self.match(expected="=")
                else TokenType.GREATER
            )
        elif char in {" ", "\t", "\r"}:
            pass
        elif char == "\n":
            self._line += 1
        elif char == '"':
            self.string()
        elif is_digit(char):
            self.number()
        elif is_alpha(char):
            self.identifier()
        else:
            error(self._line, f"Token at {self._current} not recognised")
            raise TokenNotRecognised(
                "Line %s offset %s token  not recognised: %s"
                % (self._line, self._current, self.source[self._current - 1])
            )

    def identifier(self):
        while is_alphanumeric(self.peek()):
            self.advance()
        value = self.source[self._start : self._current]
        token_type = TokenType.KEYWORDS.get(value)
        if not token_type:
            token_type = TokenType.IDENTIFIER
        self.add_token(token_type)

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self._line += 1
            self.advance()

        if self.is_at_end():
            error(line=self._line, message="No matching '\"' found ")
            raise UnterminatedLine()

        self.advance()

        value = self.source[self._start + 1 : self._current - 1]

        self._add_token(type_=TokenType.STRING, literal=value)

    def number(self):
        _is_float = False
        while is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and is_digit(self.peek_next()):
            _is_float = True
            self.advance()
            # Fractional part
            while is_digit(self.peek()):
                self.advance()
        if _is_float:
            value = float(self.source[self._start : self._current])
        else:
            value = int(self.source[self._start : self._current])

        self._add_token(type_=TokenType.NUMBER, literal=value)

    def is_at_end(self):
        return self._current >= len(self.source)

    def peek(self):
        if self.is_at_end():
            return "\0"
        return self.source[self._current]

    def peek_next(self):
        if self._current + 1 >= len(self.source):
            return "\0"
        return self.source[self._current + 1]

    def match(self, expected):
        """Return true if the current character matches

        Args:
            expected (str): The character that we expect to match

        Returns:
            boolean: True if there is a match, False otherwise
        """
        if self.is_at_end():
            return False
        if not (self.source[self._current] == expected):
            return False
        self._inc_current()
        return True

    def _inc_current(self):
        """
        Increments the current character offset in the scanner
        """
        self._current += 1
