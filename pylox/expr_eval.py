from pylox.expr_visitor import Visitor, Expr
from pylox.tokens import TokenType

class ExpressionInterpreter(Visitor):
    
    def visitLiteralExpr(self, expr: "Expr"):
        return expr.value

    def visitBinaryExpr(self, expr: "Expr"):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)
        
        if expr.operator.type_ == TokenType.PLUS:
            return float(left) + float(right)
        if expr.operator.type_ == TokenType.MINUS:
            return float(left) - float(right)
        if expr.operator.type_ == TokenType.STAR:
            return float(left) * float(right)
        if expr.operator.type_ == TokenType.SLASH:
            return float(left) / float(right)

    
    def visitUnaryExpr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")
    
    def visitGroupingExpr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    def evaluate(self, expr: "Expr"):
        return expr.accept(self)
