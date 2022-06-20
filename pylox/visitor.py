from abc import ABC, abstractmethod

from pylox.expr import Expr


class Visitor(ABC):
    """
    Abstract Visitor class
    """

    @abstractmethod
    def visit_literal_expr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def visit_binary_expr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def visit_unary_expr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def visit_grouping_expr(self, expr: "Expr"):
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def visit_print_stmt(self, stmt: "Stmt"):
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def visit_expression_stmt(self, stmt: "Stmt"):
        raise NotImplementedError("Subclasses should implement this method")

    @abstractmethod
    def visit_block_stmt(self, stmt: "Stmt"):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_logical_expr(self, expr: 'Expr'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_assign_expr(self, expr: 'Expr'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_function_stmt(self, stmt: 'Stmt'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_variable_expr(self, expr: 'Expr'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_var_stmt(self, stmt: 'Stmt'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_if_stmt(self, stmt: 'Stmt'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_while_stmt(self, stmt: 'Stmt'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_call_expr(self, expr: 'Expr'):
        raise NotImplementedError("Subclasses should implement this method")
    
    @abstractmethod
    def visit_return_stmt(self, stmt: 'Stmt'):
        raise NotImplementedError("Subclasses should implement this method")
