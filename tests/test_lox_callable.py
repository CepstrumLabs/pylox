from pylox.callable import LoxCallable


class TestLoxCallable:
    """
    Tests for the LoxCallable interface
    """

    def test_can_call(self):
        lox_callable = LoxCallable(None)
        assert lox_callable.call(interpreter=None, arguments=[])

