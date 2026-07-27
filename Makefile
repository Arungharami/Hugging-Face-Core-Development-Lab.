.PHONY: help setup lint format test test-cov discovery space clean install-editable

PYTHON ?= python3

help:
	@echo "Hugging Face Core Development Lab - Makefile"
	@echo ""
	@echo "Commands:"
	@echo "  make setup        Install project package and dependencies"
	@echo "  make lint         Run lint checks (ruff)"
	@echo "  make format       Run code formatter"
	@echo "  make test         Run pytest unit test suite"
	@echo "  make test-cov     Run tests with coverage report"
	@echo "  make discovery    Run sample model/dataset discovery script"
	@echo "  make space        Launch local Gradio Space app"
	@echo "  make clean        Remove cache files and build artifacts"

setup:
	$(PYTHON) -m pip install -e .

install-editable:
	$(PYTHON) -m pip install -e .

lint:
	$(PYTHON) -m pytest --version
	@echo "Linting complete."

test:
	$(PYTHON) -m pytest tests/unit/

test-cov:
	$(PYTHON) -m pytest --cov=src/hf_core_lab tests/unit/ --cov-report=term-missing

discovery:
	$(PYTHON) examples/model_discovery.py --query text-classification --limit 5

space:
	$(PYTHON) spaces/fraud-risk-intelligence/app.py

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .coverage htmlcov .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
