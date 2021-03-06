from typing import List


class LoxCallable:
    def __init__(self, callee):
        self.callee = callee

    def call(self, interpreter: "ExpressionInterpreter", arguments: List[object]):
        raise NotImplementedError("Subclasses shlould implement this method")


class ReturnVal(Exception):
    def __init__(self, value):
        self.value = value
