from typing import List

from pylox.expr import Assign, Binary, Grouping, Literal, Logical, Unary, Variable
from pylox.scanner import LoxToken, error
from pylox.stmt import Block, Expression, If, Print, Var, While
from pylox.tokens import TokenType


class ParserError(Exception):
    """
    Exception class for Parser
    """

    def __init__(self, message):
        self.message = message


class Parser:
    """

    Implements a parser for the Grammar

    Grammar
    ========

    program -> declaration* EOF ;
    declaration -> varDeclaration | statement ;
    statement -> expressionStmt | printStatement | block | if_stmt | while_stmt;
    if_stmt -> "if" + "(" expression ")" statement ("else" statement)? ;
    while_stmt -> "while" + "(" expression ")" statement;
    block -> "{" declaration* "}" ;
    expressionStmt -> expression ";" ;
    printStatement -> print expression ;

    expression -> assignment ;
    assignment -> IDENTIFIER "=" assignment | logic_or ;

    logic_or -> logic_and ( "or" logic_and )* ;
    logic_and -> equality ( "and" logic_and )* ;

    equality -> comparison ( ("!=" | "==") comparison)* ;
    comparison -> term ( (">" | ">=" | "<" | "<=") term)* ;
    term -> factor ( ("-" | "+") factor)* ;
    factor -> unary ( ("*" | "/") unary)* ;
    unary ->("!" | "-") unary | primary ;

    primary -> NUMBER | STRING | "true" | "false" | "nil" | "(" expression ")" ;
    '''
    A parser has two responsibilities:
    a) Given a valid sequence of tokens, produce a corresponding syntaxt tree
    b) Given an invalid sequence of tokens, detect any errors and tell the user about it
    '''
    """

    def __init__(self, tokens: List[LoxToken]):
        self._tokens = tokens
        self.current = 0
        self.line = 0

    def parse(self):
        statements = []
        try:
            while not (self.is_at_end()):
                statements.append(self.declaration())
            return statements
        except ParserError as e:
            error(self.line, message="Encountered parse error")
            raise e

    def declaration(self):
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParserError as e:
            error(line=self.line, message=e.message)
            raise e

    def var_declaration(self):
        name = self.consume(
            type_=TokenType.IDENTIFIER, msg="Expected identifier"
        ).lexeme

        initialiser = None
        if self.match(TokenType.EQUAL):
            initialiser = self.expression()

        self.consume(
            type_=TokenType.SEMICOLON, msg="Expected ';' after variable declaration"
        )
        return Var(name=name, initialiser=initialiser)

    def statement(self):
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        return self.expression_statement()

    def while_statement(self):
        """ "(" expression ")" statement; """
        self.consume(TokenType.LEFT_PAREN, msg="parenthesis required for the condition of a while statement")
        condition = self.expression();
        self.consume(TokenType.RIGHT_PAREN, msg="parenthesis required for the condition of a while statement")
        statement = self.statement()
        return While(condition=condition, statement=statement)

    def if_statement(self):
        self.consume(TokenType.LEFT_PAREN, "Expected ( after if keyword")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expected ) after if keyword")
        then_branch = self.statement()
        else_branch = None
        if self.match(TokenType.ELSE):
            else_branch = self.statement()
        return If(condition=condition, then_branch=then_branch, else_branch=else_branch)

    def block(self):
        """Match a block"""
        statements = []
        while not self._check(TokenType.RIGHT_BRACE) and (not self.is_at_end()):
            statements.append(self.declaration())

        self.consume(
            TokenType.RIGHT_BRACE, msg="Expected '}' to terminate block expression"
        )
        return statements

    def print_statement(self):
        expr = self.expression()
        self.consume(type_=TokenType.SEMICOLON, msg="Expected ';' after value")

        return Print(expression=expr)

    def expression_statement(self):
        expr = self.expression()
        self.consume(type_=TokenType.SEMICOLON, msg="Expected ';' after expression")

        return Expression(expression=expr)

    def expression(self):
        return self.assignment()

    def assignment(self):
        expr = self.logic_or()

        assign_to = self._previous()

        if self.match(TokenType.EQUAL):
            to_assign = self.assignment()
            return Assign(assign_to=assign_to, to_assign=to_assign)

        return expr

    def logic_or(self):
        expr = self.logic_and()

        while self.match(TokenType.OR):
            right = self.logic_and()
            expr = Logical(operator=TokenType.OR, left=expr, right=right)

        return expr

    def logic_and(self):
        expr = self.equality()

        while self.match(TokenType.AND):
            right = self.logic_and()
            expr = Logical(operator=TokenType.AND, left=expr, right=right)
        return expr

    def equality(self):

        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self._previous()
            right = self.comparison()
            expr = Binary(left=expr, operator=operator, right=right)

        return expr

    def comparison(self):

        expr = self.term()

        while self.match(
            TokenType.LESS,
            TokenType.LESS_EQUAL,
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
        ):
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
            return Literal(value="true")
        if self.match(TokenType.FALSE):
            return Literal(value="false")
        if self.match(TokenType.NIL):
            return Literal(value=None)
        if self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(value=self._previous().literal)
        if self.match(TokenType.IDENTIFIER):
            return Variable(name=self._previous().lexeme)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(
                type_=TokenType.RIGHT_PAREN, msg="Expected ')' after left parenthesis"
            )
            return Grouping(expression=expr)
        else:
            self.error(self.peek(), msg="Expected expression")

    def _previous(self):
        return self._tokens[self.current - 1]

    def match(self, *types, with_advance=True):
        for type_ in types:
            if self._check(type_=type_):
                if with_advance:
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
            return LoxToken(
                type_=TokenType.EOF, lexeme="\0", literal=None, line=self.line
            )

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
            raise ParserError(error(token.line, message=" at end " + msg))
        else:
            raise ParserError(
                error(token.line, message=f"at token {token.lexeme} " + msg)
            )
