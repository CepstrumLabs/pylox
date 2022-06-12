# This file was autogenerated by pylox
# on June 12, 2022 13:31:26
from pylox.scanner import LoxToken as Token

class Expr:
	pass

	def accept(self, visitor: 'ExprVisitor'):
		raise NotImplementedError('Subclasses should implement this method')

class Binary(Expr):

	def __init__(self, left: Expr, operator: Token, right: Expr):
		self.left = left
		self.operator = operator
		self.right = right

	def accept(self, visitor: 'ExprVisitor'):
		return visitor.visitBinaryExpr(self)

	def __repr__(self):
		return f'{self.__class__.__name__}(left={self.left}, operator={self.operator}, right={self.right})'

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.left==other.left and self.operator==other.operator and self.right==other.right


class Unary(Expr):

	def __init__(self, operator: Token, right: Expr):
		self.operator = operator
		self.right = right

	def accept(self, visitor: 'ExprVisitor'):
		return visitor.visitUnaryExpr(self)

	def __repr__(self):
		return f'{self.__class__.__name__}(operator={self.operator}, right={self.right})'

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.operator==other.operator and self.right==other.right


class Literal(Expr):

	def __init__(self, value: object):
		self.value = value

	def accept(self, visitor: 'ExprVisitor'):
		return visitor.visitLiteralExpr(self)

	def __repr__(self):
		return f'{self.__class__.__name__}(value={self.value})'

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.value==other.value


class Grouping(Expr):

	def __init__(self, expression: Expr):
		self.expression = expression

	def accept(self, visitor: 'ExprVisitor'):
		return visitor.visitGroupingExpr(self)

	def __repr__(self):
		return f'{self.__class__.__name__}(expression={self.expression})'

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.expression==other.expression


