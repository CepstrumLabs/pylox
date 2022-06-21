
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
	echo "Running the test_script.lox source code..."
	python -mpylox test_script.lox
	echo "Running the fib.lox source code..."
	python -mpylox fib.lox
	# echo "Running the counter.lox source code..."
	# python -mpylox counter.lox

ci: test lang_test

all: build lint test lang_test
