
.PHONY: build, env

build_req:
	pip install -r dev-requirements.txt

build: build_req
	python3 setup.py sdist bdist_wheel

isort:
	isort --check pylox

black:
	black --check pylox -vvvv

lint: black isort

test: build_req
	pytest -svvvv

lang_test:
	python -mpylox examples/test_script.lox
	python -mpylox examples/fib.lox
	python -mpylox examples/fun.lox
	python -mpylox examples/counter.lox
	python -mpylox examples/scoping_error.lox
	python -mpylox examples/bad_return.lox
	python -mpylox examples/bad.lox
	python -mpylox examples/bad_assignment.lox

ci: test lang_test

clean:
	rm -rf *.pyc *.egg-info *.log build dist __pycache__

all: build lint test lang_test

