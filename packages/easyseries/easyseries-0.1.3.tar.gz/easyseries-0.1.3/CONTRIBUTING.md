# Contributing to EasySeries

Thank you for your interest in contributing to EasySeries! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) (recommended package manager)
- Git

### Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/ScienisTmiaoT/easyseries.git
   cd easyseries
2. **Set up Development Environment**
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Run setup script
   chmod +x scripts/setup-dev.sh
   ./scripts/setup-dev.sh
   ```

3. **Verify Setup**
   ```bash
   uv run pytest
   uv run easyseries --help
   ```

### 🔄 Development Workflow
3. **Run Quality Checks**
   ```bash
   # Run all pre-commit hooks
   uv run pre-commit run --all-files

   # Or run individual checks
   uv run ruff check .           # Linting
   uv run ruff format .          # Code formatting
   uv run mypy src/easyseries    # Type checking
   uv run pytest                # Tests

4. **Submit Pull Request**

- Push your branch to your fork
- Create a Pull Request with:

  - Clear title and description
  - Reference to related issues
  - Screenshots/examples if applicable



### 📝 Code Style Guidelines
**Python Code Style**
We use modern Python practices with these tools:

- Ruff: For linting and formatting
- MyPy: For type checking
- Black: Code formatting (integrated with Ruff)

**Key Principles**

- Type Hints: Always use type hints for function parameters and return values
- Async/Await: Use modern async patterns
- Error Handling: Provide meaningful error messages and custom exceptions
- Documentation: Write clear docstrings and comments

**Example Code Style**
```python
from typing import Optional, Dict, Any
import asyncio
from easyseries.core.exceptions import EasySeriesError

async def process_data(
    data: Dict[str, Any],
    timeout: float = 30.0,
    retries: Optional[int] = None
) -> Dict[str, Any]:
    """Process data with optional timeout and retries.

    Args:
        data: Input data to process
        timeout: Processing timeout in seconds
        retries: Number of retry attempts

    Returns:
        Processed data dictionary

    Raises:
        EasySeriesError: If processing fails
    """
    try:
        # Implementation here
        return processed_data
    except Exception as e:
        raise EasySeriesError(
            "Data processing failed",
            details={"original_error": str(e)},
            original_error=e
        )
```

### 🧪 Testing Guidelines
**Test Structure**
```txt
tests/
├── test_http/          # HTTP client tests
├── test_cli/           # CLI tests
├── test_core/          # Core functionality tests
└── conftest.py         # Shared fixtures
```

**Writing Tests**

- Use pytest fixtures for common setup
- Test both success and failure cases
- Use meaningful test names
- Mock external dependencies

**Example Test**
```python
import pytest
from unittest.mock import AsyncMock
from easyseries.http.client import HTTPClient

class TestHTTPClient:
    @pytest.mark.asyncio
    async def test_successful_get_request(self, respx_mock):
        """Test successful GET request returns expected data."""
        respx_mock.get("https://api.test.com/users").mock(
            return_value=httpx.Response(200, json={"users": []})
        )

        async with HTTPClient(base_url="https://api.test.com") as client:
            response = await client.get("/users")

            assert response.status_code == 200
            assert response.json() == {"users": []}
```

**Running Tests**
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=easyseries --cov-report=html

# Run specific test file
uv run pytest tests/test_http/test_client.py

# Run tests matching pattern
uv run pytest -k "test_client"

# Run tests with specific markers
uv run pytest -m "not slow"
```

### 📚 Documentation
**Writing Documentation**

- Docstrings: Use Google-style docstrings
- Type Information: Include parameter and return types
- Examples: Provide usage examples where helpful
- Updates: Update relevant documentation when changing functionality

**Building Documentation**
```bash
# Build documentation locally
./scripts/build-docs.sh

# Or manually
cd docs
uv run sphinx-build -b html source _build/html
```

**Documentation Structure**

- docs/source/index.rst - Main documentation page
- docs/source/api.rst - API reference
- docs/source/quickstart.rst - Getting started guide
- docs/source/modules/ - Module-specific documentation

**🐛 Bug Reports**
When reporting bugs, please include:

- Environment Information

  - Python version
  - EasySeries version
  - Operating system


- Reproduction Steps

  - Minimal code example
  - Expected vs actual behavior
  - Error messages/tracebacks


- Additional Context

  - Related issues
  - Possible solutions you've tried



### ✨ Feature Requests
For new features:

- Check existing issues to avoid duplicates
- Describe the use case clearly
- Provide examples of the desired API
- Consider backwards compatibility

### 🔄 Release Process
**Version Numbering**
We follow Semantic Versioning:

- MAJOR.MINOR.PATCH
- Major: Breaking changes
- Minor: New features (backwards compatible)
- Patch: Bug fixes

**Release Steps**

- Update version in src/easyseries/__init__.py
- Update CHANGELOG.md
- Create and push tag: git tag v1.0.0 && git push origin v1.0.0
- GitHub Actions will automatically publish to PyPI

### 💬 Communication

- GitHub Issues: Bug reports and feature requests
- GitHub Discussions: General questions and ideas
- Pull Requests: Code contributions and reviews

### 📋 Checklist for Contributors
Before submitting a PR, ensure:

 - Code follows style guidelines
 - Tests pass locally
 - New functionality includes tests
 - Documentation is updated
 - Pre-commit hooks pass
 - PR description is clear and complete

### 🎯 Areas for Contribution
We especially welcome contributions in these areas:

- Performance optimizations
- Additional HTTP utilities
- CLI enhancements
- Documentation improvements
- Test coverage expansion
- Bug fixes

### 🙏 Recognition
Contributors are recognized in:

- CHANGELOG.md for each release
- GitHub contributors list
- Special mentions for significant contributions

Thank you for contributing to EasySeries! 🚀
