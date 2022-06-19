from pylox.callable import LoxCallable
from pylox.environment import Environment
from pylox.stmt import Function


class LoxFunction(LoxCallable):
    def __init__(self, stmt: Function):
        self.declaration = stmt

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.globals)
        for index, _ in enumerate(self.declaration.params):
            name = self.declaration.params[index].name.lexeme
            value = arguments[index]
            environment.define(name, value)

        interpreter.execute_block(self.declaration.body, env=environment)
        return None
