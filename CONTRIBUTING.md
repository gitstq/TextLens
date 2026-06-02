# Contributing to TextPulse

Thank you for your interest in contributing to TextPulse!

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a virtual environment: `python -m venv venv`
4. Activate it: `source venv/bin/activate` (Linux/macOS) or `venv\Scripts\activate` (Windows)
5. Install in development mode: `pip install -e .`

## Development

TextPulse has zero external dependencies. All you need is Python 3.8+.

### Running Tests

```bash
python -m unittest textpulse.tests.test_all
```

### Code Style

- Follow PEP 8 conventions
- Use relative imports within the package
- Keep functions focused and well-documented

## Submitting Changes

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass
4. Submit a pull request with a clear description

## Reporting Issues

Please use the [GitHub issue tracker](https://github.com/gitstq/TextPulse/issues) to report bugs or request features.
