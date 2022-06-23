import pytest

from .context import pylox

@pytest.fixture(name="interpreter")
def _interpreter():
    yield pylox.LoxIntepreter()

def test_can_run_with_file(interpreter):
    interpreter.run_file(file="examples/test_script.lox")

def test_raises_on_non_existent_file(interpreter):
    with pytest.raises(pylox.LoxException):
        interpreter.run_file(file="non_existent.lox")

def test_run_simple_expression(interpreter):
    source = "1 + 1;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_simple_divide(interpreter):
    source = "1 / 1;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_multiply(interpreter):
    source = "1 * 5;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_string_addition(interpreter):
    source = '"a" + "a";'
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_arithmetic_expression(interpreter):
    source = '(3 + 2)/5;'
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_comparison_less(interpreter):
    source = "1 < 2;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_comparison_equal(interpreter):
    source = "1 == 2;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_comparison_not_equal(interpreter):
    source = "1 != 2;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_comparison_less_equal(interpreter):
    source = "1 <= 2;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_run_comparison_greater(interpreter):
    source = "5 > 2;"
    interpreter.run(source=source)
    assert not interpreter.had_error


def test_run_comparison_greater_equal(interpreter):
    source = "3 >= 2;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_print_statement(interpreter):
    source = "print 1;"
    interpreter.run(source=source)
    assert not interpreter.had_error


def test_print_statements(interpreter):
    source = "print 1;\nprint 2;"
    interpreter.run(source=source)
    assert not interpreter.had_error

def test_class_decl(interpreter):
    source = "class MyClass {};"
    interpreter.run(source=source)
    assert not interpreter.had_error
