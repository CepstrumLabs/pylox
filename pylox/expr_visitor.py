
from typing import List


class ExprVisitor:
    
    def parenthesize(self, name: str, *exprs: List["Expr"]):
        block = ""
        block += "("
        block += name
        for expr in exprs:
            block += " "
            block += expr.accept(self)
        block += ")"
        return str(block)

    def visitLiteralExpr(self, expr: "Expr"):
        if not expr.value:
            return 'nil'
        return str(expr.value)

    def visitBinaryExpr(self, expr: "Expr"):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)
    
    def visitUnaryExpr(self, expr: "Expr"):
        return self.parenthesize(expr.operator.lexeme, expr.right)
    
    def visitGroupingExpr(self, expr: "Expr"):
        return self.parenthesize("group", expr)