# Contributing to AHI Module 2

Thank you for your interest in contributing!

## Development Setup

```bash
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

- Black for formatting: `black .`
- Ruff for linting: `ruff check .`

## Pull Requests

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass with ≥90% coverage
5. Submit a pull request

## Coding Standards

- Python 3.12+
- Full type hints on all public APIs
- Pydantic v2 for data models
- SOLID principles
