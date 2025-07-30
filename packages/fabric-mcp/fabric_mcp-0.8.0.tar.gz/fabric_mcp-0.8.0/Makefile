# Makefile for
#

.PHONY: _default bootstrap build clean coverage coverage-html coverage-show format help lint merge tag test

COVERAGE_FAIL_UNDER := 90
PACKAGE_PATH := src/fabric_mcp

VERSION := $(shell uv run hatch version)

_default: help

bootstrap:
	uv sync --dev
	uv run pre-commit autoupdate
	uv run pre-commit install
	uv run pre-commit install --hook-type commit-msg

build:
	uv run hatch build

clean:
	rm -f ../.venv && rm -rf .venv && rm -rf dist

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

format:
	uv run ruff format .
	uv run isort .

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
	@echo "  merge         Merge develop into main branch (bypassing pre-commit hooks)"
	@echo "  tag           Tag the current git HEAD with the semantic versioning name."
	@echo "  test          Run tests"

lint:
	uv run ruff format --check .
	uv run ruff check .
	uv run pylint --fail-on=W0718 $(PACKAGE_PATH) tests
	uv run pyright $(PACKAGE_PATH) tests

merge:
	@echo "This will merge develop into main and push to origin."
	@git diff-index --quiet HEAD -- || { echo "Error: Working directory not clean. Please commit or stash your changes before proceeding."; exit 1; }
	@read -p "Are you sure? (y/N): " confirm && [ "$$confirm" = "y" ] || { echo "Merge aborted."; exit 1; }
	@echo "Merging develop into main..."
	@current_branch=$$(git rev-parse --abbrev-ref HEAD); \
	if [ "$$current_branch" != "develop" ]; then \
		echo "Error: You must be on the develop branch to run this command."; \
		echo "Current branch: $$current_branch"; \
		exit 1; \
	fi
	@echo "Ensuring develop is up to date..."
	git pull origin develop
	@echo "Switching to main..."
	git checkout main
	@echo "Pulling latest main..."
	git pull origin main
	@echo "Merging develop into main (bypassing pre-commit hooks)..."
	git merge develop --no-verify || { echo "Error: Merge failed. Please resolve conflicts and try again."; exit 1; }
	@echo "Pushing to main..."
	git push origin main
	@echo "Switching back to develop..."
	git checkout develop
	@echo "Merge completed successfully!"

tag:
	git tag v$(VERSION)

test: lint
	uv run pytest -v

