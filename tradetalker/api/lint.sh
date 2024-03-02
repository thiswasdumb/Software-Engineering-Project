#!/bin/bash

# Activate pipenv environment
PIPENV_CMD="pipenv run"
PIPENV_SHELL="pipenv shell"

# Check if Pipenv is installed
if ! command -v pipenv &> /dev/null; then
    echo "Pipenv is not installed. Please install it by running: pip install pipenv"
    exit 1
fi

# Check if virtual environment exists, if not create one
if ! command pipenv --venv &> /dev/null; then
    echo "Creating virtual environment with pipenv..."
    pipenv install --dev
fi

# Run linting
echo "Formatting Python code with black..."
$PIPENV_CMD black .
echo "Linting Python code with pylint..."
$PIPENV_CMD pylint . --fail-under=10
echo "Linting Python code with ruff..."
$PIPENV_CMD ruff --fix .
echo "Type checking Python code with mypy..."
$PIPENV_CMD mypy .

# Exit virtual environment
exit