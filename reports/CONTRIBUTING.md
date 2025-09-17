# Contributing to Football Pool Domination System

Thank you for your interest in contributing to the Football Pool Domination System! This document provides guidelines for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd football-pool-domination
   ```

2. **Install development dependencies**
   ```bash
   pip install -r requirements.txt -r requirements-dev.txt
   ```

3. **Run tests to ensure everything works**
   ```bash
   make test
   ```

## Code Style

We use several tools to maintain code quality:

- **ruff**: For linting and formatting
- **mypy**: For type checking
- **pytest**: For testing

### Running Quality Checks

```bash
# Format code
make format

# Run linting
make lint

# Run type checking
make type-check

# Run all tests
make test

# Run tests with coverage
make test-cov
```

## Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run quality checks**
   ```bash
   make lint
   make type-check
   make test
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add feature: brief description"
   ```

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Testing

We require comprehensive test coverage for all new functionality:

- **Unit tests**: Test individual functions and methods
- **Integration tests**: Test component interactions
- **CLI tests**: Test command-line interface functionality

### Writing Tests

- Place tests in the `tests/` directory
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies when appropriate

Example test structure:
```python
def test_feature_success_case():
    """Test feature works correctly."""
    # Arrange
    input_data = "test input"

    # Act
    result = feature_function(input_data)

    # Assert
    assert result == expected_output
```

## Documentation

- Update docstrings for new functions and classes
- Add examples to the README if adding new features
- Update the CHANGELOG for significant changes

## Pull Request Process

1. **Ensure all checks pass**
   - All tests pass
   - Code is properly formatted
   - Type checking passes
   - No linting errors

2. **Write a clear description**
   - What changes were made
   - Why the changes were necessary
   - How to test the changes

3. **Request review**
   - Assign appropriate reviewers
   - Respond to feedback promptly
   - Make requested changes

## Reporting Issues

When reporting issues, please include:

- **Description**: Clear description of the problem
- **Steps to reproduce**: Detailed steps to reproduce the issue
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens
- **Environment**: Python version, OS, etc.

## Feature Requests

When requesting features, please include:

- **Use case**: Why this feature would be useful
- **Proposed solution**: How you think it should work
- **Alternatives**: Other approaches you've considered
- **Additional context**: Any other relevant information

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the golden rule

## Questions?

If you have questions about contributing, please:

- Check existing issues and discussions
- Create a new issue with the "question" label
- Reach out to maintainers directly

Thank you for contributing to the Football Pool Domination System!
