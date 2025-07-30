#!/bin/bash

# Get git tracked files
FILES=$(git ls-files)
PYFILES=$(echo "$FILES" | grep '\.py$')

# Format code with black (only git tracked Python files)
echo "$PYFILES" | xargs -r uv run black

# Fix linting issues with ruff (only git tracked Python files)
echo "$PYFILES" | xargs -r uv run ruff check --fix

# Type check with mypy (only git tracked Python files)
echo "$PYFILES" | xargs -r uv run mypy

# Format with prettier (only git tracked files)
echo "$FILES" | grep -E '\.(js|ts|json|md|yml|yaml)$' | xargs -r bunx prettier --write
