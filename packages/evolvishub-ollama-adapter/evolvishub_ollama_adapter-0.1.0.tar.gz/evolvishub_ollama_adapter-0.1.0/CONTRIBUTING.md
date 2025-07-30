# Contributing to Evolvishub Ollama Adapter

Thank you for your interest in contributing to the Evolvishub Ollama Adapter! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please read it before contributing.

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/evolvishub-ollama-adapter.git
   cd evolvishub-ollama-adapter
   ```
3. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes
3. Run tests:
   ```bash
   pytest
   ```
4. Run linting:
   ```bash
   ruff check .
   black .
   isort .
   mypy .
   ```
5. Commit your changes with a descriptive commit message
6. Push to your fork
7. Create a pull request

## Code Style

We use the following tools to maintain code quality:

- Black for code formatting
- isort for import sorting
- ruff for linting
- mypy for type checking

Please ensure your code passes all checks before submitting a pull request.

## Testing

We use pytest for testing. Please write tests for all new features and bug fixes. Run tests with:

```bash
pytest
```

For test coverage:

```bash
pytest --cov=evolvishub_ollama_adapter
```

## Documentation

- Update docstrings for all new functions, classes, and methods
- Follow the Google style guide for docstrings
- Update the README.md if necessary
- Add examples for new features

## Pull Request Process

1. Update the README.md with details of changes if needed
2. Update the documentation if needed
3. The PR will be merged once you have the sign-off of at least one other developer
4. Make sure all tests pass and there are no linting errors

## Versioning

We use semantic versioning. Update the version in `pyproject.toml` when making changes.

## Questions?

Feel free to open an issue if you have any questions about contributing. 