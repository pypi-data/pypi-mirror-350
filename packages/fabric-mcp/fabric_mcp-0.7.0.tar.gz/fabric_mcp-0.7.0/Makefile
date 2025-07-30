# Makefile for
#

.PHONY: help bootstrap test coverage coverage-html coverage-show lint format build clean tag

COVERAGE_FAIL_UNDER := 90
PACKAGE_PATH := src/fabric_mcp

VERSION := $(shell uv run hatch version)

help:
	@echo "Makefile for fabric_mcp (Version $(VERSION))"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  bootstrap     Bootstrap the project"
	@echo "  build         Build the project"
	@echo "  clean         Clean up the project"
	@echo "  coverage      Run test coverage"
	@echo "  coverage-html Run tests and generate an HTML coverage report."
	@echo "  coverage-show Show the coverage report in the browser."
	@echo "  format        Format the codebase"
	@echo "  help          Show this help message"
	@echo "  lint          Run linters"
	@echo "  tag           Tag the current git HEAD with the semantic versioning name."
	@echo "  test          Run tests"

bootstrap:
	uv sync --dev

test: lint
	uv run pytest -v

coverage:
	uv run pytest --cov=$(PACKAGE_PATH) \
		-ra -q \
		--cov-report=term-missing \
		--cov-fail-under=$(COVERAGE_FAIL_UNDER)

coverage-html:
	# This will generate an HTML coverage report.
	uv run pytest --cov=$(PACKAGE_PATH) \
		--cov-report=html:coverage_html \
		--cov-fail-under=$(COVERAGE_FAIL_UNDER)

coverage-show:
	# This will open the HTML coverage report in the default web browser.
	@echo "Opening coverage report in the browser..."
	@open coverage_html/index.html || xdg-open coverage_html/index.html || start coverage_html/index.html
	@echo "Done."


lint:
	uv run ruff format --check .
	uv run ruff check .
	uv run pylint --fail-on=W0718 $(PACKAGE_PATH) tests
	uv run pyright $(PACKAGE_PATH) tests

format:
	uv run ruff format .
	uv run isort .

# Target to build the application's source distribution and wheel
build:
	uv run hatch build

clean:
	rm -f ../.venv && rm -rf .venv && rm -rf dist

tag:
	git tag v$(VERSION)
