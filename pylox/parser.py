
from typing import List

from pylox.scanner import LoxToken, error
from pylox.tokens import TokenType
from pylox.Expr import Binary, Grouping, Literal, Unary

"""
Grammar:
====
"""

class ParserError(Exception):
    """
    Exception class for Parser
    """

class Parser:
    """

    Implements a parser for the Grammar

    Grammar
    ========

    expression -> equality;
    equality -> comparison ( ("!=" | "==") comparison)* ;
    comparison -> term ( (">" | ">=" | "<" | "<=") term)* ;
    term -> factor ( ("-" | "+") factor)* ;
    factor -> unary ( ("*" | "/") unary)* ;
    unary ->("!" | "-") unary | primary ;
    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ; 
    """
    def __init__(self, tokens: List[LoxToken]):
        self._tokens = tokens
        self.current = 0
        self.line = 0

    def parse(self):
        try:
            return self.expression()
        except ParserError:
            return None

    def expression(self):
        return self.equality()
    
    def equality(self):
        
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self.comparison()
            expr = Binary(left=expr, operator=operator, right=right)
        
        return expr

    def comparison(self):

        expr = self.term()

        while self.match(TokenType.LESS, TokenType.LESS_EQUAL, TokenType.GREATER, TokenType.GREATER_EQUAL):
            operator = self._previous()
            right = self.term()
            expr = Binary(left=expr, operator=operator, right=right)
        
        return expr

    def term(self):

        expr = self.factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self._previous()
            right = self.factor()
            expr = Binary(left=expr, operator=operator, right=right)
        
        return expr

    def factor(self):
    
        expr = self.unary()

        while self.match(TokenType.STAR, TokenType.SLASH):
            operator = self._previous()
            right = self.unary()
            expr = Binary(left=expr, operator=operator, right=right)
        
        return expr

    def unary(self):
        
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self._previous()
            right = self.unary()
            return Unary(operator=operator, right=right)
        
        primary = self.primary()
        return primary

    def primary(self):
        if self.match(TokenType.TRUE):
            return Literal(value=True)
        if self.match(TokenType.FALSE):
            return Literal(value=False)
        if self.match(TokenType.NIL):
            return Literal(value=None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(value=self._previous().lexeme)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(type_=TokenType.RIGHT_PAREN, msg="Expect ')' after left parenthesis");
            return Grouping(expression=expr)
        else:
            self.error(self.peek(), msg="Expected expression")

    def _previous(self):
        return self._tokens[self.current - 1]

    def match(self, *types):
        for type_ in types:
            if self._check(type_=type_):
                self.advance()
                return True
        return False
    
    def _check(self, type_):
        if self.is_at_end():
            return False
        return self.peek().type_ == type_
    
    def is_at_end(self):
        return self.peek().type_ == TokenType.EOF

    def peek(self):
        try:
            return self._tokens[self.current]
        except IndexError:
            return LoxToken(type_=TokenType.EOF, lexeme="\0", literal=None, line=self.line)

    def advance(self):
        if not self.is_at_end():
            self.current += 1
            self.line = self.peek().line
        return self._previous()

    def consume(self, type_, msg):
        if self._check(type_):
            return self.advance()
        self.error(token=self.peek(), msg=msg)

    def error(self, token, msg):
        if token.type_ == TokenType.EOF:
            raise ParserError(error(token.line, message=" at end" + msg))
        else:
            raise ParserError(error(token.line, message=f"at token {token.lexeme} " + msg))
