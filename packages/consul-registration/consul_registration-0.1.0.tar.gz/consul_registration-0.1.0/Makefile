.PHONY: help test test-unit test-integration test-ci test-example format lint type-check all install-hooks

help:
	@echo "Available commands:"
	@echo "  make test            - Run all tests (unit + integration)"
	@echo "  make test-unit       - Run unit tests only"
	@echo "  make test-integration - Run integration tests with Docker Consul"
	@echo "  make test-ci         - Run CI integration tests (requires Consul on localhost:8500)"
	@echo "  make test-example-server - Run example application tests"
	@echo "  make format          - Format code with black"
	@echo "  make lint            - Run linting checks"
	@echo "  make type-check      - Run mypy type checking"
	@echo "  make install-hooks   - Install pre-commit hooks"
	@echo "  make all             - Run format, lint, type-check, and test"

test: test-unit test-integration test-example-server

test-unit:
	pytest tests/ -v -k "not integration"

test-integration:
	./scripts/run_integration_tests.sh

test-ci:
	pytest tests/test_integration_ci.py -v

test-example-server:
	cd example && pytest tests -v

format:
	black src/ tests/ example/

lint:
	ruff check src/ tests/ example/

type-check:
	mypy src/ --ignore-missing-imports

install-hooks:
	pre-commit install

all: format lint type-check test