
import pytest

from pylox.scanner import LoxScanner, LoxToken, UnterminatedLine
from pylox.scanner import TokenType, is_digit

def test_scans_empty():
    source = ""
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == []

def test_scans_plus():
    source = "+"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.PLUS, lexeme='+', literal=None, line=1)]

def test_scans_minus():
    source = "-"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.MINUS, lexeme='-', literal=None, line=1)]

def test_scans_left_paren():
    source = "("
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.LEFT_PAREN, lexeme='(', literal=None, line=1)]

def test_scans_right_paren():
    source = ")"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.RIGHT_PAREN, lexeme=')', literal=None, line=1)]

def test_scans_left_brace():
    source = "["
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.LEFT_BRACE, lexeme='[', literal=None, line=1)]

def test_scans_right_brace():
    source = "]"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.RIGHT_BRACE, lexeme=']', literal=None, line=1)]

def test_scans_comma():
    source = ","
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.COMMA, lexeme=',', literal=None, line=1)]

def test_scans_dot():
    source = "."
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.DOT, lexeme='.', literal=None, line=1)]

def test_scans_minus():
    source = "-"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.MINUS, lexeme='-', literal=None, line=1)]

def test_scans_plus():
    source = "+"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.PLUS, lexeme='+', literal=None, line=1)]

def test_scans_semicolon():
    source = ";"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.SEMICOLON, lexeme=';', literal=None, line=1)]

def test_scans_slash():
    source = "/"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.SLASH, lexeme='/', literal=None, line=1)]

def test_scans_star():
    source = "*"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.STAR, lexeme='*', literal=None, line=1)]

def test_scans_equal():
    source = "="
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.EQUAL, lexeme='=', literal=None, line=1)]

def test_scans_bang():
    source = "!"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.BANG, lexeme='!', literal=None, line=1)]

def test_scans_bang_equal():
    source = "!="
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.BANG_EQUAL, lexeme='!=', literal=None, line=1)]

def test_scans_equal_equal():
    source = "=="
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.EQUAL_EQUAL, lexeme='==', literal=None, line=1)]

def test_scans_less():
    source = "<"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.LESS, lexeme='<', literal=None, line=1)]

def test_scans_greater():
    source = ">"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.GREATER, lexeme='>', literal=None, line=1)]

def test_scans_less_equal():
    source = "<="
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.LESS_EQUAL, lexeme='<=', literal=None, line=1)]

def test_scans_greater_equal():
    source = ">="
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.GREATER_EQUAL, lexeme='>=', literal=None, line=1)]

def test_scans_whitespace():
    source = " "
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == []

def test_scans_comment():
    source = "// This is a comment\n<"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.LESS, lexeme='<', literal=None, line=2)]

def test_scans_grouping():
    source = "((()))[]"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [
        LoxToken(type_=TokenType.LEFT_PAREN, lexeme='(', literal=None, line=1),
        LoxToken(type_=TokenType.LEFT_PAREN, lexeme='(', literal=None, line=1),
        LoxToken(type_=TokenType.LEFT_PAREN, lexeme='(', literal=None, line=1),
        LoxToken(type_=TokenType.RIGHT_PAREN, lexeme=')', literal=None, line=1),
        LoxToken(type_=TokenType.RIGHT_PAREN, lexeme=')', literal=None, line=1),
        LoxToken(type_=TokenType.RIGHT_PAREN, lexeme=')', literal=None, line=1),
        LoxToken(type_=TokenType.LEFT_BRACE, lexeme='[', literal=None, line=1),
        LoxToken(type_=TokenType.RIGHT_BRACE, lexeme=']', literal=None, line=1)
    ]

def test_scans_operators():
    source = "+-=<>/*;"
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [
        LoxToken(type_=TokenType.PLUS, lexeme='+', literal=None, line=1),
        LoxToken(type_=TokenType.MINUS, lexeme='-', literal=None, line=1),
        LoxToken(type_=TokenType.EQUAL, lexeme='=', literal=None, line=1),
        LoxToken(type_=TokenType.LESS, lexeme='<', literal=None, line=1),
        LoxToken(type_=TokenType.GREATER, lexeme='>', literal=None, line=1),
        LoxToken(type_=TokenType.SLASH, lexeme='/', literal=None, line=1),
        LoxToken(type_=TokenType.STAR, lexeme='*', literal=None, line=1),
        LoxToken(type_=TokenType.SEMICOLON, lexeme=';', literal=None, line=1)
    ]

def test_scans_string():
    source = '"a"'
    scanner = LoxScanner(source=source)
    tokens = scanner.scan_tokens()
    assert tokens == [LoxToken(type_=TokenType.STRING, lexeme='"a"', literal='a', line=1)]


def test_raises_on_unterminated_string():
    source = '"a'
    scanner = LoxScanner(source=source)
    with pytest.raises(UnterminatedLine):
        scanner.scan_tokens()

class TestScannerNumbers:
    
    def test_scans_numbers(self):
        source = '5'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.NUMBER, lexeme='string', literal='string', line=1)]



class TestIsDigit:

    def test_is_digit(self):
        digits = list(range(10))
        for item in digits:
            assert is_digit(str(item))


# def test_scans_identifiers():
#     source = 'identifier'
#     scanner = LoxScanner(source=source)
#     tokens = scanner.scan_tokens()
#     assert tokens == [LoxToken(type_=TokenType.STRING, lexeme='string', literal='string', line=1)]

# def test_scans_keywords():
#     source = 'keywords'
#     scanner = LoxScanner(source=source)
#     tokens = scanner.scan_tokens()
#     assert tokens == [LoxToken(type_=TokenType.STRING, lexeme='string', literal='string', line=1)]
