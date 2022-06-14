
.PHONY: build


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
	python -mpylox test_script.lox

all: build lint test lang_test
