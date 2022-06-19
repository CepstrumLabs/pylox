
from pylox.expr_eval import Environment

class TestEnvironment:

    def test_correctly_stores_data(self):
        parent = Environment()
        parent.define('loop', 1)

        child = Environment(environment=parent)
        assert child.get('loop') == 1

        grandchild = Environment(environment=child)
        assert grandchild.get('loop') == 1

