from typing import List

    
class LoxCallable:

    def __init__(self, callee):
        self.callee = callee

    def call(self, interpreter: 'ExpressionInterpreter', arguments: List[object]):
        return 1
