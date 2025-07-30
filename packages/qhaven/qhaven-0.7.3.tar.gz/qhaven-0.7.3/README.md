QHaven – PQC remediation lib for security devs.

install, then run:
  pip install qhaven
  qhaven scan (.) / (path-to)
  qhaven fix  --repo path/to/repo --owner you --name repo --token $GITHUB_TOKEN


Makefile
--------
install:
	pip install -e .[dev]
lint:
	pycodestyle qhaven
test:
	pytest -q
build:
	python -m build