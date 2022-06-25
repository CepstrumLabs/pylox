from pylox.callable import LoxCallable, ReturnVal
from pylox.environment import Environment
from pylox.stmt import Function


class LoxFunction(LoxCallable):
    def __init__(self, stmt: Function, closure: Environment):
        self.declaration = stmt
        self.closure = closure

    def arity(self):
        return len(self.declaration.params)

    def call(self, interpreter, arguments):
        environment = Environment(self.closure)
        for index, _ in enumerate(self.declaration.params):
            name = self.declaration.params[index].name.lexeme
            value = arguments[index]
            environment.define(name, value)
        try:
            interpreter.execute_block(self.declaration.body, env=environment)
        except ReturnVal as rv:
            return rv.value
        return None
