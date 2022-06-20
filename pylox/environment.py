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

    def get_at(self, depth: int, key):
        return self.ancestor(depth)[key]

    def assign_at(self, distance, key, value):
        self.ancestor(distance)[key] = value

    def ancestor(self, depth):
        i = 0
        ancestor = self
        while i < depth:
            ancestor = ancestor.parent
            i += 1
        return ancestor

    def define(self, key, value):
        self[key] = value

    def assign(self, key, value):

        if key in self.keys():
            self[key] = value
            return

        raise RuntimeError(f"Variable '{key}' is accessed but it was never defined")
