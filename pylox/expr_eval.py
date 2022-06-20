from typing import List

from pylox.callable import ReturnVal
from pylox.environment import Environment
from pylox.function import LoxFunction
from pylox.tokens import TokenType
from pylox.visitor import Expr, Visitor


class LoxRuntimeError(Exception):
    def __init__(self, token=None, msg=None):
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


class ExpressionInterpreter(Visitor):
    def __init__(self):
        self.environ = Environment()
        self.locals = {}

    @property
    def globals(self):
        return self.environ

    def resolve(self, expr: "Expr", depth: int):
        self.locals[expr] = depth

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

        distance = self.locals.get(expr)

        if distance is not None:
            self.environment.assign_at(distance, name, value)
        self.environ.assign(name, value)
        return value

    def visit_print_stmt(self, stmt: "Stmt"):
        expr = self.evaluate(stmt.expression)
        print(expr)
        return None

    def visit_function_stmt(self, stmt: "Function"):
        function = LoxFunction(stmt=stmt, closure=self.environ)
        self.environ.define(stmt.name.name.lexeme, function)

    def visit_variable_expr(self, expr: "Expr"):
        value = None
        try:
            value = self._look_up_variable(expr.name, expr)
        except KeyError:
            raise LoxRuntimeError(
                token=expr.name, msg=f"Token {expr.name.lexeme} is not defined"
            )
        return value

    def _look_up_variable(self, name, expression):
        distance = self.locals.get(expression)
        if distance is not None:
            value = self.environ.get_at(distance, name.lexeme)
            return value

        return self.environ.get(name.lexeme)

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

    def visit_call_expr(self, expr: "Expr"):
        try:
            callee = self.evaluate(expr.callee)
        except KeyError:
            callee = None
        arguments = []

        for argument in expr.arguments:
            arguments.append(self.evaluate(argument))
        if not isinstance(callee, LoxFunction):
            raise LoxRuntimeError(msg="you can only call functions")
        return callee.call(self, arguments)

    def visit_return_stmt(self, stmt: "Stmt"):
        value = None

        if stmt.value is not None:
            value = self.evaluate(stmt.value)
            raise ReturnVal(value=value)

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

    def execute_block(self, statements, env=None):
        previous_env = self.environ
        self.environ = env if env else self.environ
        try:
            for statement in statements:
                self._execute(statement)
        except LoxRuntimeError as error:
            _runtime_error(error.msg, error.token.line)
        finally:
            self.environ = previous_env
