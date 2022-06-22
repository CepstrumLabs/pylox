
.PHONY: build, env

build_req:
	pip install -r dev-requirements.txt

build: build_req
	python3 setup.py sdist bdist_wheel

isort:
	isort --check pylox

black:
	black --check pylox

lint: black isort

test: build_req
	pytest -svvvv

lang_test:
	echo "Running Generic language test script..."
	python -mpylox examples/test_script.lox && echo ✅
	echo "Testing fibonnaci implementation..."
	python -mpylox examples/fib.lox && echo ✅
	echo "Testing functions..."
	python -mpylox examples/fun.lox && echo ✅
	echo "Testing function closures..."
	python -mpylox examples/counter.lox && echo ✅
	python -mpylox examples/scoping_error.lox && echo ✅

ci: test lang_test

all: build lint test lang_test
	echo ✅✅✅
