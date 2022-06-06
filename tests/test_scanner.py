from tokenize import Token
from pylox.scanner import LoxScanner, LoxToken
from pylox.scanner import TokenType

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
