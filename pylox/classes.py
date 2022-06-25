from pylox.callable import LoxCallable


class LoxInstace:
    def __init__(self, klass):
        self.klass = klass

    def __repr__(self):
        return f"{self.klass.name} instance"

    def __str__(self):
        return self.__repr__()


class LoxClass(LoxCallable):
    def __init__(self, name):
        self.name = name

    def arity(self):
        return 0

    def call(self, interpreter, arguments):
        instance = LoxInstace(self)
        return instance

    def __repr__(self):
        return f"<class {self.name}>"

    def __str__(self):
        return self.__repr__()
