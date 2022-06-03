import pytest

import pylox


def test_can_run_with_file():
    pylox.run_file(file="test_script.lox")

def test_raises_on_non_existent_file():
    with pytest.raises(pylox.LoxException):
        pylox.run_file(file="non_existent.lox")
