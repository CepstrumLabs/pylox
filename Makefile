
.PHONY: build

build:
	python3 setup.py sdist bdist_wheel

test:
	pytest -svvvv