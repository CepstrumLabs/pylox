"""
expression -> literal | unary | binary | grouping;
literal -> NUMBER | STRING | "true" | "false" | "nil";
unary -> ("!" | "-") expression;
binary -> expression operator expression;
grouping -> "(" expression ")"
operator -> "==" | "!=" | "<" | "<=" | ">" | ">=" | "+" | "-" | "*" | "/";
"""

from typing import List
from expr_visitor import ExprVisitor


class Expression:
    """Abstract class
    """

    def accept(self, visitor: "ExprVisitor"):
        raise NotImplementedError("Subclasses must implement this method")



class Literal(Expression):
    def __init__(self, value):
        self.value = value

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visitLiteralExpr(self)

class Unary(Expression):
    def __init__(self, operator, expression):
        self.operator = operator
        self.right = expression
    
    def accept(self, visitor: "ExprVisitor"):
        return visitor.visitUnaryExpr(self)

class Binary(Expression):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visitBinaryExpr(self)

class Grouping(Expression):
    def __init__(self, expression):
        self.expression = expression
    
    def accept(self, visitor: "ExprVisitor"):
        return visitor.visitGroupingExpr(self.expression)



class AstPrinter():

    def __init__(self):
        self._visitor = ExprVisitor()

    def print(self, expression):
        print(expression.accept(self._visitor))


def main():
    left = Unary(LoxToken(type_=TokenType.MINUS, lexeme="-", literal=None, line=1), Literal(value=123))
    operator = LoxToken(type_=TokenType.STAR, lexeme="*", literal=None, line=1)
    right = Grouping(expression=Literal(value=45.67))
    expression = Binary(left=left, operator=operator, right=right)
    printer = AstPrinter()
    printer.print(expression)

if __name__ == "__main__":
    from scanner import LoxToken
    from tokens import TokenType
    main()