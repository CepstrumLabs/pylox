from .context import pylox

from pylox.expr import Literal, Binary, Unary, Variable
from pylox.tokens import TokenType
from pylox.scanner import LoxToken
from pylox.parser import Parser
from pylox.stmt import Expression, Stmt, Print, Function, Var


def create_number_token(value, line=1, offset=0):
    assert isinstance(value, (int, float)), f'Can\'t create number token with value {value}'
    return LoxToken(type_=TokenType.NUMBER, lexeme=f'{value}', literal=value, line=line, offset=offset)

def create_string_token(value, line=1, offset=0):
    assert isinstance(value, str), f'Can\'t create string token with value {value}'
    return LoxToken(type_=TokenType.STRING, lexeme=f'{value}', literal=value, line=line, offset=offset)

def create_identifier(value, line=1, offset=0):
    return LoxToken(type_=TokenType.IDENTIFIER, lexeme=value, literal=None, line=line, offset=offset)

def create_token(type_, line=1, offset=0):
    lexeme = TokenType.TOKENS_TO_LEXEMES[type_]
    return LoxToken(type_=type_, lexeme=lexeme, literal=None, line=line, offset=offset)

def create_literal(value):
    return Literal(value=value)


class TestParser:

    """
    Tests for pylox.parser.LoxParser
    """

    def test_parses_expression(self):
        """
        Ensure that an expression is parsed as expected
        """
        value = 123
        tokens = [create_number_token(value=value, offset=0), create_token(type_=TokenType.SEMICOLON, offset=3)]
        expected = [Expression(expression=create_literal(value=value))]
        parser = pylox.Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

    def test_parses_equality(self):
        """
        Ensure that an equality is parsed as expected
        """
        tokens = [create_number_token(1), create_token(type_=TokenType.BANG_EQUAL), create_number_token(1), create_token(type_=TokenType.SEMICOLON)]
        expected = [Expression(expression=Binary(left=create_literal(value=1), operator=create_token(type_=TokenType.BANG_EQUAL), right=create_literal(value=1)))]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

    def test_parses_comparison(self):
        """
        Ensure that an comparison is parsed as expected
        """
        tokens = [create_number_token(1), create_token(type_=TokenType.GREATER_EQUAL), create_number_token(1), create_token(type_=TokenType.SEMICOLON)]
        expected = [Expression(expression=Binary(left=create_literal(value=1), operator=create_token(type_=TokenType.GREATER_EQUAL), right=create_literal(value=1)))]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

    def test_parses_term(self):
        """
        Ensure that a term is parsed as expected
        """
        tokens = [create_number_token(1), create_token(type_=TokenType.PLUS), create_number_token(1), create_token(type_=TokenType.SEMICOLON)]
        expected = [Expression(expression=Binary(left=create_literal(value=1), operator=create_token(type_=TokenType.PLUS), right=create_literal(value=1)))]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

    def test_parses_factor(self):
        """
        Ensure that an factor is parsed as expected
        """
        tokens = [create_number_token(1), create_token(type_=TokenType.STAR), create_number_token(1), create_token(type_=TokenType.SEMICOLON)]
        expected = [Expression(expression=Binary(left=create_literal(value=1), operator=create_token(type_=TokenType.STAR), right=create_literal(value=1)))]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

    def test_parses_unary(self):
        """
        Ensure that an unary is parsed as expected
        """
        tokens = [create_token(type_=TokenType.MINUS), create_number_token(value=123), create_token(type_=TokenType.SEMICOLON)]
        expected = [Expression(expression=Unary(operator=create_token(type_=TokenType.MINUS), right=create_literal(value=123)))]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

    def test_parses_primary(self):
        """
        Ensure that an primary is parsed as expected
        """
        tokens = [create_number_token(1), create_token(type_=TokenType.SEMICOLON)]
        expected = [Expression(expression=create_literal(value=1))]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

    def test_parses_primary_string(self):
        """
        Ensure that an primary is parsed as expected
        """
        tokens = [create_string_token(value="imastring"), create_token(type_=TokenType.SEMICOLON)]
        expected = [Expression(expression=create_literal(value="imastring"))]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected
    
    def test_parses_function(self):
        """
        Ensure that an primary is parsed as expected
        """
        tokens = [create_token(type_=TokenType.FUN), create_identifier(value="myFun"), create_token(type_=TokenType.LEFT_PAREN), create_token(type_=TokenType.RIGHT_PAREN), create_token(type_=TokenType.LEFT_BRACE), create_token(type_=TokenType.RIGHT_BRACE)]
        expected = [Function(name=Variable(name=LoxToken(type_=TokenType.IDENTIFIER, lexeme='myFun', literal=None, line=1, offset=0)), body=[], params=[])]
        parser = Parser(tokens=tokens)
        expr = parser.parse()
        assert expr == expected

