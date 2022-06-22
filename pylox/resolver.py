from typing import List, Union

from pylox.logging import logger
from pylox.visitor import Visitor


class CompilerError(Exception):
    """
    Represents all errors that can occur in the Resolver
    """
    


class FunctionType:
    NONE = "NONE"
    FUNCTION = "FUNCTION"

class Resolver(Visitor):
    """
    Resolve variables in the tokens
    """

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.current_function = FunctionType.NONE
        self.scopes = []

    def resolve_all(self, statements: List[Union["Stmt", "Expr"]]):
        for statement in statements:
            self.resolve(statement=statement)

    def resolve(self, statement: Union["Stmt", "Expr"]):
        logger.debug(f"Resolving {statement}")
        statement.accept(self)

    def begin_scope(self):
        logger.debug("begin_scope")
        self.scopes.append({})

    def end_scope(self):
        logger.debug("end_scope")
        self.scopes.pop()

    def visit_literal_expr(self, expr: "Expr"):
        pass

    def visit_binary_expr(self, expr: "Expr"):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_unary_expr(self, expr: "Expr"):
        self.resolve(expr.right)

    def visit_grouping_expr(self, expr: "Expr"):
        self.resolve(expr.expression)

    def visit_print_stmt(self, stmt: "Stmt"):
        self.resolve(stmt.expression)

    def visit_expression_stmt(self, stmt: "Stmt"):
        self.resolve(stmt.expression)

    def visit_block_stmt(self, stmt: "Stmt"):
        self.begin_scope()
        self.resolve_all(stmt.statements)
        self.end_scope()

    def visit_logical_expr(self, expr: "Expr"):
        self.resolve(expr.left)
        self.resolve(expr.right)

    def visit_assign_expr(self, expr: "Expr"):
        self.resolve(expr.to_assign)
        self.resolve_local(expr, expr.assign_to)

    def visit_function_stmt(self, stmt: "Stmt"):
        self.declare(stmt.name.name.lexeme)
        self.define(stmt.name.name.lexeme)
        self._resolve_function(statement=stmt, function_type=FunctionType.FUNCTION)

    def _resolve_function(self, statement, function_type):
        self.begin_scope()
        
        enclosing_function = self.current_function
        self.current_function = function_type
        
        for param in statement.params:
            self.declare(param.name.lexeme)
            self.define(param.name.lexeme)

        self.resolve_all(statement.body)
        self.end_scope()
        self.current_function = enclosing_function

    def visit_variable_expr(self, expr: "Expr"):
        if self.scopes and self.scopes[-1].get(expr.name.lexeme) is False:
            raise CompilerError("Can't read local variable in its own initializer")
        self.resolve_local(expr, expr.name)
        return None

    def resolve_local(self, expr: "Expr", name: "Token"):
        logger.debug(f"resolve_local: expr={expr}, token={name}")
        for i in range(len(self.scopes) - 1, -1, -1):

            if name.lexeme in self.scopes[i].keys():
                logger.debug(
                    f"resolve_local: resolve {name} at {len(self.scopes) - 1 - i} "
                )
                self.interpreter.resolve(expr, len(self.scopes) - 1 - i)
                return

    def visit_var_stmt(self, stmt: "Stmt"):
        self.declare(stmt.name)
        if stmt.initialiser is not None:
            self.resolve(stmt.initialiser)
        self.define(stmt.name)
        return None

    def declare(self, name):
        if not self.scopes:
            return

        # Get the last scope
        scope = self.scopes[-1]
        if name in scope:
            raise CompilerError(f"Already a variable called '{name}' defined in scope")
        scope[name] = False
        logger.debug(f"declare: scope={scope}")

    def define(self, name):
        if not self.scopes:
            return

        # Get the last scope
        scope = self.scopes[-1]
        scope[name] = True
        logger.debug(f"define: scope={scope}")

    def visit_if_stmt(self, stmt: "Stmt"):
        self.resolve(stmt.condition)
        self.resolve(stmt.then_branch)
        if stmt.else_branch:
            self.resolve(stmt.else_branch)

    def visit_while_stmt(self, stmt: "Stmt"):
        self.resolve(stmt.condition)
        self.resolve(stmt.statement)

    def visit_call_expr(self, expr: "Expr"):
        self.resolve(expr.callee)
        for argument in expr.arguments:
            self.resolve(argument)

    def visit_return_stmt(self, stmt: "Stmt"):
        if self.current_function is FunctionType.NONE:
            raise CompilerError("Cannot return outside of a function")
        if stmt.value != None:
            self.resolve(stmt.value)
