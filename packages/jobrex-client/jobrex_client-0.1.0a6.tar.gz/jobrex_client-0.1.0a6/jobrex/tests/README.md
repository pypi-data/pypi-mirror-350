# Jobrex Client Tests

This directory contains tests for the Jobrex client library.

## Running Tests

To run the tests, you need to have pytest installed. If you don't have it yet, you can install it with:

```bash
pip install pytest pytest-cov
```

Then, from the root directory of the project, run:

```bash
pytest jobrex/tests
```

To run tests with coverage report:

```bash
pytest --cov=jobrex jobrex/tests
```

## Test Structure

The tests are organized as follows:

- `test_utils.py`: Tests for utility functions in the `utils.py` module
- `test_models.py`: Tests for data models in the `models.py` module
- `test_client.py`: Tests for API clients in the `client.py` module
- `conftest.py`: Shared fixtures for tests

## Mocking

The tests use the `unittest.mock` module to mock API calls, ensuring that tests don't make actual HTTP requests. This makes the tests faster and more reliable, as they don't depend on external services.

## Adding New Tests

When adding new tests:

1. Follow the existing pattern of test organization
2. Use appropriate fixtures from `conftest.py`
3. Mock external dependencies
4. Test both success and error cases
5. Ensure test names are descriptive

## Continuous Integration

These tests are designed to be run in a CI/CD pipeline. They should be fast and reliable, and should not depend on external services or specific environment configurations. 