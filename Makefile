.PHONY: clean-pyc clean-build black lint build

VENV_NAME ?= venv
PYTHON = ${VENV_NAME}/bin/python3


clean-pyc:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force  {} +

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean: clean-pyc clean-build
	rm --force --recursive $(VENV_NAME)

black:
	black archive-repo/

lint:
	black --check archive-repo/

build:
	python3 -m build

venv: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.py
	test -d $(VENV_NAME) || virtualenv -p python3 $(VENV_NAME)
	${PYTHON} -m pip install -U pip
	${PYTHON} -m pip install -e .
	touch $(VENV_NAME)/bin/activate

test: venv
	${PYTHON} -m pip install -U behave
	. $(VENV_NAME)/bin/activate
	behave tests/features

upload: build venv
	${PYTHON} -m pip install -U build twine
	. $(VENV_NAME)/bin/activate
	python3 -m twine upload dist/*
