from typing import List

from pylox.expr import Expr


class Visitor:
    """
    Abstract Visitor class
    """

    def visitLiteralExpr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    def visitBinaryExpr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    def visitUnaryExpr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    def visitGroupingExpr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")


class AstPrinter:
    def __init__(self):
        self._visitor = ExprVisitor()

    def print(self, expression):
        if expression:
            print(expression.accept(self._visitor))


class ExprVisitor(Visitor):
    def parenthesize(self, name: str, *exprs: List["Expr"]):
        block = ""
        block += "("
        block += name
        for expr in exprs:
            block += " "
            block += expr.accept(self)
        block += ")"
        return block

    def visitLiteralExpr(self, expr: "Expr"):
        if not expr.value:
            return "nil"
        return str(expr.value)

    def visitBinaryExpr(self, expr: "Expr"):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visitUnaryExpr(self, expr: "Expr"):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visitGroupingExpr(self, expr: "Expr"):
        return self.parenthesize("group", expr.expression)
