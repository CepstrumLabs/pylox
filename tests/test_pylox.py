import pytest

from .context import pylox

@pytest.fixture(name="interpreter")
def _interpreter():
    yield pylox.LoxIntepreter()

def test_can_run_with_file(interpreter):
    interpreter.run_file(file="test_script.lox")

def test_raises_on_non_existent_file(interpreter):
    with pytest.raises(pylox.LoxException):
        interpreter.run_file(file="non_existent.lox")

def test_run_simple_expression(interpreter):
    source = "1 + 1"
    result = interpreter.run(source=source)
    assert result == 2

def test_run_simple_divide(interpreter):
    source = "1 / 1"
    result = interpreter.run(source=source)
    assert result == 1

def test_run_multiply(interpreter):
    source = "1 * 5"
    result = interpreter.run(source=source)
    assert result == 5

def test_run_string_addition(interpreter):
    source = '"a" + "a"'
    result = interpreter.run(source=source)
    assert result == 'aa'

def test_run_arithmetic_expression(interpreter):
    source = '(3 + 2)/5'
    result = interpreter.run(source=source)
    assert result == 1

def test_run_comparison_less(interpreter):
    source = "1 < 2"
    result = interpreter.run(source=source)
    assert result == True

def test_run_comparison_equal(interpreter):
    source = "1 == 2"
    result = interpreter.run(source=source)
    assert result == False

def test_run_comparison_not_equal(interpreter):
    source = "1 != 2"
    result = interpreter.run(source=source)
    assert result == True

def test_run_comparison_less_equal(interpreter):
    source = "1 <= 2"
    result = interpreter.run(source=source)
    assert result == True

def test_run_comparison_greater(interpreter):
    source = "5 > 2"
    result = interpreter.run(source=source)
    assert result == True


def test_run_comparison_greater_equal(interpreter):
    source = "3 >= 2"
    result = interpreter.run(source=source)
    assert result == True
