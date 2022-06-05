import pytest

from pylox import LoxIntepreter, LoxException


@pytest.fixture(name="interpreter")
def _interpreter():
    yield LoxIntepreter()

def test_can_run_with_file(interpreter):
    interpreter.run_file(file="test_script.lox")

def test_raises_on_non_existent_file(interpreter):
    with pytest.raises(LoxException):
        interpreter.run_file(file="non_existent.lox")
