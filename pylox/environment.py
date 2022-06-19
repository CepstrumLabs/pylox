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

        else:
            raise KeyError(f"{key} is not defined")

    def define(self, key, value):
        self[key] = value

    def assign(self, key, value):

        if key in self.keys():
            self[key] = value
            return

        if self.parent is not None:
            return self.parent.assign(key, value)

        raise RuntimeError(f"Variable '{key}' is accessed but it was never defined")
