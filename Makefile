
.PHONY: build


build_req:
	pip install -r dev-requirements.txt

build: build_req
	python3 setup.py sdist bdist_wheel


test: build_req
	pytest -svvvv