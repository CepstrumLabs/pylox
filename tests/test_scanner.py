
import pytest

from pylox.scanner import LoxScanner, LoxToken, UnterminatedLine
from pylox.scanner import TokenType, is_digit, is_alpha

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

class TestScannerString:

    def test_scans_string(self):
        source = '"a"'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.STRING, lexeme='"a"', literal='a', line=1)]

    def test_scans_two_char_string(self):
        source = '"ab"'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.STRING, lexeme='"ab"', literal='ab', line=1)]

    def test_scans_three_char_string(self):
        source = '"abc"'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.STRING, lexeme='"abc"', literal='abc', line=1)]

    def test_scans_multichar_string(self):
        source = '"A string with multiple characters inside"'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.STRING, lexeme='"A string with multiple characters inside"', literal='A string with multiple characters inside', line=1)]

    def test_raises_on_unterminated_string(self):
        source = '"a'
        scanner = LoxScanner(source=source)
        with pytest.raises(UnterminatedLine):
            scanner.scan_tokens()

class TestScannerNumbers:
    
    def test_scans_single_digits(self):
        source = '5'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.NUMBER, lexeme='5', literal=5, line=1)]

    def test_scans_double_digits(self):
        source = '55'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.NUMBER, lexeme='55', literal=55, line=1)]
    
    def test_scans_triple_digits(self):
        source = '555'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.NUMBER, lexeme='555', literal=555, line=1)]
    
    def test_scans_multiple_digits(self):
        source = '1234567890'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.NUMBER, lexeme='1234567890', literal=1234567890, line=1)]

    def test_scans_fractions(self):
        source = '123.121'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [LoxToken(type_=TokenType.NUMBER, lexeme='123.121', literal=123.121, line=1)]

    def test_dot_without_decimal_part_not_allowed(self):
        source = '123.'
        scanner = LoxScanner(source=source)
        tokens = scanner.scan_tokens()
        assert tokens == [
            LoxToken(type_=TokenType.NUMBER, lexeme='123', literal=123, line=1),
            LoxToken(type_=TokenType.DOT, lexeme='.', literal=None, line=1)
        ]


class TestIsDigit:

    def test_is_digit(self):
        digits = map(str, list(range(10)))
        for item in digits:
            assert is_digit(str(item))


class TestIsAlpha:
    
    def test_is_alpha(self):
        ordering_lower = list(range(97, 123))
        ordering_higher = list(range(65, 91))
        chars = [chr(a) for a in ordering_lower + ordering_higher] + ['_']
        for item in chars:
            assert is_alpha(item)


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
