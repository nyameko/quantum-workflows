PYTHON ?= python3
VENV ?= .venv
RESULTS ?= results

.PHONY: help install install-all lint test check hello-local trotter sqd container

help:
	@$(PYTHON) -c 'print("Targets: install install-all lint test check hello-local trotter sqd container")'

$(VENV)/bin/python:
	$(PYTHON) -m venv $(VENV)
	$(VENV)/bin/python -m pip install --upgrade pip

install: $(VENV)/bin/python
	$(VENV)/bin/python -m pip install -e '.[dev]'

install-all: $(VENV)/bin/python
	$(VENV)/bin/python -m pip install -e '.[ibm,sqd,notebooks,dev]'

lint:
	$(VENV)/bin/ruff check src tests
	$(VENV)/bin/ruff format --check src tests

test:
	$(VENV)/bin/pytest -m 'not hardware'

check: lint test

hello-local:
	$(VENV)/bin/qw hello --executor aer --output $(RESULTS)

trotter:
	$(VENV)/bin/qw trotter --executor aer --output $(RESULTS)

sqd:
	$(VENV)/bin/qw sqd --executor statevector --output $(RESULTS)

container:
	docker build -f runners/qiskit-cpu/Dockerfile -t quantum-workflows:qiskit-cpu .
