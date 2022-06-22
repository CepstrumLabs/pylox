
from pylox.expr_eval import Environment

class TestEnvironment:

    def test_correctly_stores_data(self):
        parent = Environment()
        parent.define('loop', 1)

        child = Environment(environment=parent)
        assert child.get('loop') == 1

        grandchild = Environment(environment=child)
        assert grandchild.get('loop') == 1

    def test_ancestor(self):
        parent = Environment()
        parent.define('loop', 1)

        child = Environment(environment=parent)
        grandchild = Environment(environment=child)
        great_grandchild = Environment(environment=grandchild)

        assert child.ancestor(depth=1) == parent
        assert grandchild.ancestor(depth=1) == child
        assert grandchild.ancestor(depth=2) == parent
        assert great_grandchild.ancestor(depth=3) == parent
        assert great_grandchild.ancestor(depth=2) == child
        assert great_grandchild.ancestor(depth=1) == grandchild
