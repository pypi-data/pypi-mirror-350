include .env
PACKAGE := xync_script
VPYTHON := $(VENV)/bin/python

.PHONY: all cv install deps pre-commit clean build twine patch

all: install clean build

cv:
	python3 -m venv venv
install: deps pre-commit
	$(VPYTHON) -m pip install .[dev]; make pre-commit
deps: $(VENV)
	$(VPYTHON) -m pip install .[dev]
pre-commit: .pre-commit-config.yaml
	pre-commit install -t pre-commit -t post-commit -t pre-push

clean: dist $(PACKAGE).egg-info
	rm -rf dist/* $(PACKAGE).egg-info $(PACKAGE)/__pycache__ dist/__pycache__

build: $(VENV)
	$(VPYTHON) -m build
twine: build dist
	$(VPYTHON) -m twine upload dist/* --skip-existing

patch: $(VENV)
	git tag `$(VPYTHON) -m setuptools_scm --strip-dev`; git push --tags --prune -f