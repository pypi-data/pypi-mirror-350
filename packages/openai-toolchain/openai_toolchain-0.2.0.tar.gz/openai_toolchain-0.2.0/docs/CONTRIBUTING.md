# Contributing

We welcome contributions! Here's how you can help:

1. Report bugs
2. Develop new features
3. Improve documentation
4. Submit fixes

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/bemade/openai-toolchain.git
   cd openai-toolchain
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
5. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

## Running Tests

Run all tests with coverage:

```bash
pytest --cov=openai_toolchain --cov-report=term-missing
```

Run a specific test file:

```bash
pytest tests/test_module.py -v
```

## Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for all function signatures
- Include Google-style docstrings for all public functions and classes
- Keep lines under 88 characters (Black's default)
- The project uses pre-commit hooks to enforce code style:
  - `ruff` for linting and formatting
  - `black` for code formatting
  - `mypy` for static type checking
  - `prettier` for Markdown formatting

To run all linters manually:

```bash
pre-commit run --all-files
```

## Documentation

We use MkDocs with Material for documentation. To build the docs locally:

```bash
# Install docs dependencies
pip install -e ".[docs]"

# Build and serve the docs
mkdocs serve
```

Then open `http://127.0.0.1:8000` in your browser.

## Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add/update tests
4. Update documentation if needed
5. Run tests and linters
6. Submit a pull request with a clear description of changes

## Pre-commit Hooks

This project uses pre-commit to ensure code quality. The pre-commit hooks will
run automatically on each commit. To manually run the hooks:

```bash
pre-commit run --all-files
```

To skip the pre-commit checks (not recommended):

```bash
git commit --no-verify -m "Your commit message"
```

## Code of Conduct

This project adheres to the
[Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

## Reporting Issues

When reporting issues, please include:

- A clear description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Any relevant error messages
- If possible, include a minimal reproducible example

## License

By contributing, you agree that your contributions will be licensed under the
[MIT License](LICENSE).
