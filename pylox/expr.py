# This file was autogenerated by pylox
# on June 20, 2022 20:00:19
from pylox.scanner import LoxToken as Token


class Expr:
    def accept(self, visitor: "ExprVisitor"):
        raise NotImplementedError("Subclasses should implement this method")


class Binary(Expr):
    def __init__(self, left: "Expr", operator: "Token", right: "Expr"):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_binary_expr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(left={self.left}, operator={self.operator}, right={self.right})"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.left == other.left
            and self.operator == other.operator
            and self.right == other.right
        )

    def __hash__(self):
        return hash(
            (
                self.left,
                self.operator,
                self.right,
            )
        )


class Unary(Expr):
    def __init__(self, operator: "Token", right: "Expr"):
        self.operator = operator
        self.right = right

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_unary_expr(self)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(operator={self.operator}, right={self.right})"
        )

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.operator == other.operator
            and self.right == other.right
        )

    def __hash__(self):
        return hash(
            (
                self.operator,
                self.right,
            )
        )


class Literal(Expr):
    def __init__(self, value: "object"):
        self.value = value

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_literal_expr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value})"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.value == other.value

    def __hash__(self):
        return hash((self.value,))


class Logical(Expr):
    def __init__(self, operator: "Token", left: "Expr", right: "Expr"):
        self.operator = operator
        self.left = left
        self.right = right

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_logical_expr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(operator={self.operator}, left={self.left}, right={self.right})"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.operator == other.operator
            and self.left == other.left
            and self.right == other.right
        )

    def __hash__(self):
        return hash(
            (
                self.operator,
                self.left,
                self.right,
            )
        )


class Variable(Expr):
    def __init__(self, name: "Token"):
        self.name = name

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_variable_expr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"

    # def __eq__(self, other):
    #     return isinstance(other, self.__class__) and self.name == other.name

    # def __hash__(self):
    #     return hash((self.name,))


class Grouping(Expr):
    def __init__(self, expression: "Expr"):
        self.expression = expression

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_grouping_expr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(expression={self.expression})"

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.expression == other.expression

    def __hash__(self):
        return hash((self.expression,))


class Assign(Expr):
    def __init__(self, assign_to: "Token", to_assign: "Expr"):
        self.assign_to = assign_to
        self.to_assign = to_assign

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_assign_expr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(assign_to={self.assign_to}, to_assign={self.to_assign})"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.assign_to == other.assign_to
            and self.to_assign == other.to_assign
        )

    def __hash__(self):
        return hash(
            (
                self.assign_to,
                self.to_assign,
            )
        )


class Call(Expr):
    def __init__(self, callee: "Expr", arguments: "List[Expr]"):
        self.callee = callee
        self.arguments = arguments

    def accept(self, visitor: "ExprVisitor"):
        return visitor.visit_call_expr(self)

    def __repr__(self):
        return f"{self.__class__.__name__}(callee={self.callee}, arguments={self.arguments})"

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__)
            and self.callee == other.callee
            and self.arguments == other.arguments
        )

    def __hash__(self):
        return hash(
            (
                self.callee,
                self.arguments,
            )
        )
