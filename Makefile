default: help

help:
	@echo
	@echo "clean-pyc    Clean Python compiled files"
	@echo "flake8       Flake8 analysis"
	@echo

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

flake8:
	@echo "------Starting flake8 code analysis------"
	flake8 --benchmark
	@echo

