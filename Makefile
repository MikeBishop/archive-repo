.PHONY: clean-pyc clean-build black lint build venv test upload

VENV_NAME ?= venv


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

venv: Pipfile Pipfile.lock setup.py
	pipenv install --dev

build: venv
	pipenv run python3 setup.py build

test: venv
	pipenv run behave tests/features

upload: build venv
	pipenv run python3 -m twine upload dist/*
