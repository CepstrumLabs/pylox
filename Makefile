
.PHONY: build


build_req:
	pip install -r dev-requirements.txt

build: build_req
	python3 setup.py sdist bdist_wheel

isort:
	isort --check --verbose pylox

black:
	black --check --verbose pylox

lint: black isort

test: build_req
	pytest -svvvv