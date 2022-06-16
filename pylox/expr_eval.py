from typing import List

from pylox.expr_visitor import Expr, Visitor
from pylox.tokens import TokenType


class LoxRuntimeError(Exception):
    def __init__(self, token, msg):
        self.token = token
        self.msg = msg


def _is_number(value):
    return isinstance(value, (int, float))


def _checkNumberOperands(operator, left, right):
    if _is_number(left) and _is_number(right):
        return
    raise LoxRuntimeError(
        f"Operands for {operator.lexeme} should be int or float not {type(left)}"
    )


def _checkNumberOperand(operator, operand):
    if _is_number(operand):
        return
    raise LoxRuntimeError(f"Operand for {operator.lexeme} should be int or float")


def _isTruthy(object_):
    if object_ in ("false", "nil", None):
        return False
    if isinstance(object_, bool):
        return bool(object_)
    return True


def _isEqual(left, right):
    return left == right


def _runtime_error(msg, line):
    print(msg + " @ [line " + str(line) + "]")


class Environment(dict):
    """
    Key-value pair holder that has a reference to its parent
    """

    def __init__(self, environment=None):
        self.parent = environment

    def get(self, key):
        if key in self.keys():
            return self[key]

        if self.parent is not None:
            return self.parent.get(key)

    def define(self, key, value):
        self[key] = value

    def assign(self, key, value):

        if key in self.keys():
            self[key] = value
            return

        if self.parent is not None:
            return self.parent.assign(key, value)

        raise RuntimeError(f"Variable '{key}' is accessed but it was never defined")

    def __getitem__(self, lexeme):
        """
        If the key exists, return it from the current object
        If it doesnt, search the parent.
        If parent doesn't exist
        """
        if self.parent is None or lexeme in self.keys():  # reached the parent
            return super().__getitem__(lexeme)
        return self.parent[lexeme]


class ExpressionInterpreter(Visitor):
    def __init__(self):
        self.environ = Environment()

    def visit_literal_expr(self, expr: "Expr"):
        return expr.value

    def visit_logical_expr(self, expr: "Expr"):
        left = self.evaluate(expr.left)
        if expr.operator == TokenType.OR:
            if _isTruthy(left):
                return left
        elif expr.operator == TokenType.AND:
            if not _isTruthy(left):
                return left

        return self.evaluate(expr.right)

    def visit_binary_expr(self, expr: "Expr"):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        operator = expr.operator

        if operator.type_ == TokenType.PLUS:
            if isinstance(left, str):
                return left + str(right)
            _checkNumberOperands(operator=operator, left=left, right=right)
            return left + right
        if operator.type_ == TokenType.MINUS:
            _checkNumberOperands(operator=operator, left=left, right=right)
            return float(left) - float(right)
        if operator.type_ == TokenType.STAR:
            _checkNumberOperands(operator=operator, left=left, right=right)
            return float(left) * float(right)
        if operator.type_ == TokenType.SLASH:
            _checkNumberOperands(operator=operator, left=left, right=right)
            try:
                rv = float(left) / float(right)
            except ZeroDivisionError:
                raise LoxRuntimeError(operator, msg="ZeroDivisionError")
            return rv
        if operator.type_ == TokenType.BANG_EQUAL:
            return not _isEqual(left, right)
        if operator.type_ == TokenType.EQUAL_EQUAL:
            return _isEqual(left, right)
        if operator.type_ == TokenType.GREATER:
            return left > right
        if operator.type_ == TokenType.GREATER_EQUAL:
            return left >= right
        if operator.type_ == TokenType.LESS:
            return left < right
        if operator.type_ == TokenType.LESS_EQUAL:
            return left <= right

    def visit_unary_expr(self, expr: "Expr"):
        operator = expr.operator
        right = self.evaluate(expr.right)

        if operator.type_ == TokenType.BANG:
            return not _isTruthy(right)

        if operator.type_ == TokenType.MINUS:
            _checkNumberOperand(operator=operator, operand=right)
            return -(float(right))

    def visit_grouping_expr(self, expr: "Expr"):
        return self.evaluate(expr.expression)

    def visit_assign_expr(self, expr: "Expr"):
        value = self.evaluate(expr.to_assign)
        name = expr.assign_to.lexeme

        self.environ.assign(name, value)
        return value

    def visit_print_stmt(self, stmt: "Stmt"):
        expr = self.evaluate(stmt.expression)
        print(expr)
        return None

    def visit_variable_expr(self, expr: "Expr"):
        return self.environ.get(expr.name)

    def visit_expression_stmt(self, stmt: "Stmt"):
        self.evaluate(stmt.expression)

    def visit_var_stmt(self, stmt: "Stmt"):
        value = self.evaluate(stmt.initialiser)
        self.environ.define(stmt.name, value)
        return None

    def visit_block_stmt(self, block: "Stmt"):
        self.execute_block(statements=block.statements)

    def visit_if_stmt(self, if_stmt: "Stmt"):
        condition = if_stmt.condition
        then_branch = if_stmt.then_branch
        else_branch = if_stmt.else_branch

        if _isTruthy(self.evaluate(condition)):
            self._execute(then_branch)
        elif else_branch:
            self._execute(else_branch)
        return None

    def visit_while_stmt(self, stmt: "Stmt"):
        while _isTruthy(self.evaluate(stmt.condition)):
            self._execute(stmt.statement)
        return None

    def evaluate(self, expr: "Expr"):
        return expr.accept(self)

    def interpret(self, statements: List["Stmt"]):
        try:
            for statement in statements:
                self._execute(statement)
        except LoxRuntimeError as error:
            _runtime_error(error.msg, error.token.line)

    def _execute(self, statement):
        return statement.accept(self)

    def execute_block(self, statements):
        previous_env = self.environ
        self.environ = Environment(environment=previous_env)
        # breakpoint()
        try:
            for statement in statements:
                self._execute(statement)
        except LoxRuntimeError as error:
            _runtime_error(error.msg, error.token.line)
        finally:
            self.environ = previous_env
