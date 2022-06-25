from typing import List
import abc


class LoxCallable(abc.ABC):
    def __init__(self, callee):
        self.callee = callee

    @abc.abstractmethod
    def arity():
        raise NotImplementedError("Subclasses shlould implement this method")

    @abc.abstractmethod
    def call(self, interpreter: "ExpressionInterpreter", arguments: List[object]):
        raise NotImplementedError("Subclasses shlould implement this method")


class ReturnVal(Exception):
    def __init__(self, value):
        self.value = value
