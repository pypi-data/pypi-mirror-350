# Contributing to Arc Tracing SDK

Thank you for your interest in contributing to Arc Tracing SDK! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- Basic understanding of OpenTelemetry and AI frameworks

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/arc-tracing-sdk.git
   cd arc-tracing-sdk
   ```

2. **Set up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## 🛠️ Development Workflow

### Code Style

We use several tools to maintain code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking

Run all checks:
```bash
# Format code
black arc_tracing/ tests/ examples/
isort arc_tracing/ tests/ examples/

# Check linting
flake8 arc_tracing/ tests/ examples/

# Type checking
mypy arc_tracing/
```

### Testing

Run the test suite:
```bash
# All tests
pytest

# With coverage
pytest --cov=arc_tracing --cov-report=html

# Specific test file
pytest tests/test_trace.py

# Verbose output
pytest -v
```

### Integration Tests

Test with real frameworks:
```bash
# Install framework dependencies
pip install openai langchain llama-index

# Run integration tests
pytest tests/integration/
```

## 📦 Project Structure

```
arc-tracing-sdk/
├── arc_tracing/           # Main package
│   ├── integrations/      # Framework integrations
│   ├── exporters/         # Trace exporters
│   ├── frameworks/        # Legacy framework patches
│   ├── clients/           # Client wrappers
│   └── ...
├── tests/                 # Test suite
│   ├── integration/       # Integration tests
│   └── ...
├── examples/              # Example code
│   ├── integration_examples/
│   └── ...
└── docs/                  # Documentation
```

## 🔌 Adding Framework Support

### Integration Approach (Recommended)

For modern frameworks with built-in tracing:

1. **Create Integration Class**
   ```python
   # arc_tracing/integrations/new_framework.py
   from arc_tracing.integrations.base import BaseIntegration

   class NewFrameworkIntegration(BaseIntegration):
       def __init__(self):
           super().__init__("new_framework")
       
       def is_available(self) -> bool:
           # Check if framework is installed
           pass
       
       def _setup_integration(self) -> bool:
           # Hook into framework's tracing system
           pass
   ```

2. **Register Integration**
   ```python
   # arc_tracing/integrations/__init__.py
   from .new_framework import NewFrameworkIntegration
   
   new_framework = NewFrameworkIntegration()
   ```

3. **Add Tests**
   ```python
   # tests/test_new_framework_integration.py
   def test_new_framework_integration():
       # Test integration functionality
       pass
   ```

### Legacy Patching (Fallback)

For frameworks without built-in tracing:

1. **Create Framework Module**
   ```python
   # arc_tracing/frameworks/new_framework.py
   def patch() -> bool:
       # Monkey patch framework classes
       pass
   ```

2. **Add to Legacy Handler**
   ```python
   # arc_tracing/trace.py - _apply_legacy_instrumentation()
   elif framework == "new_framework":
       from arc_tracing.frameworks import new_framework
       if new_framework.patch():
           # ...
   ```

## 📝 Documentation

### Code Documentation

- Use clear, descriptive docstrings
- Include type hints for all functions
- Add examples in docstrings when helpful

```python
def enable_framework_integration(framework: str) -> bool:
    """
    Enable integration for a specific framework.
    
    Args:
        framework: Name of the framework to enable
        
    Returns:
        True if integration was successful, False otherwise
        
    Example:
        >>> enable_framework_integration("openai_agents")
        True
    """
```

### README Updates

When adding new features:
- Update the main README.md
- Add examples to demonstrate usage
- Update the supported frameworks table

## 🧪 Writing Tests

### Unit Tests

```python
import pytest
from arc_tracing.integrations import OpenAIAgentsIntegration

def test_openai_agents_integration():
    integration = OpenAIAgentsIntegration()
    assert integration.name == "openai_agents"
    
    # Mock framework availability
    with patch('importlib.util.find_spec') as mock_find_spec:
        mock_find_spec.return_value = True
        assert integration.is_available()
```

### Integration Tests

```python
@pytest.mark.integration
def test_real_framework_integration():
    """Test with actual framework if available."""
    try:
        import agents  # OpenAI Agents SDK
        
        # Test real integration
        integration = OpenAIAgentsIntegration()
        assert integration.enable()
        
    except ImportError:
        pytest.skip("OpenAI Agents SDK not available")
```

### Test Coverage

Maintain high test coverage:
- Aim for >90% coverage on new code
- Test both success and error paths
- Mock external dependencies appropriately

## 🔄 Pull Request Process

### Before Submitting

1. **Run All Checks**
   ```bash
   # Code quality
   black arc_tracing/ tests/ examples/
   flake8 arc_tracing/ tests/ examples/
   mypy arc_tracing/
   
   # Tests
   pytest --cov=arc_tracing
   ```

2. **Update Documentation**
   - Add/update docstrings
   - Update README if needed
   - Add examples for new features

3. **Write Clear Commit Messages**
   ```
   feat: add support for new framework
   
   - Implement NewFrameworkIntegration class
   - Add integration tests
   - Update documentation
   ```

### PR Guidelines

- **Title**: Clear, descriptive title
- **Description**: Explain what and why
- **Testing**: Describe how you tested the changes
- **Breaking Changes**: Call out any breaking changes
- **Related Issues**: Link to related issues

### Review Process

1. Automated checks must pass
2. At least one maintainer review required
3. All feedback addressed
4. Documentation updated if needed

## 🐛 Reporting Issues

### Bug Reports

Include:
- Python version
- Arc Tracing SDK version
- Framework versions
- Minimal reproduction case
- Expected vs actual behavior
- Full error traceback

### Feature Requests

Include:
- Use case description
- Proposed API design
- Alternative solutions considered
- Willingness to implement

## 🏷️ Versioning

We follow [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features, backward compatible
- **PATCH**: Bug fixes, backward compatible

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 💬 Community

- **Discussions**: Use GitHub Discussions for questions
- **Discord**: Join our Discord server for real-time chat
- **Issues**: Use GitHub Issues for bugs and feature requests

## 🙏 Recognition

Contributors are recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributor graph

Thank you for helping make Arc Tracing SDK better! 🎉