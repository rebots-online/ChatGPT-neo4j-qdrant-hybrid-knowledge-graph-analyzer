# Contributing to ChatGPT Neo4j-Qdrant Hybrid Knowledge Graph Analyzer

We're excited that you're interested in contributing! This document outlines the process and guidelines for contributing to the project.

## Development Process

### Setting Up Development Environment

1. Fork and clone the repository:
```bash
git clone https://github.com/yourusername/ChatGPT-neo4j-qdrant-hybrid-knowledge-graph-analyzer.git
cd ChatGPT-neo4j-qdrant-hybrid-knowledge-graph-analyzer
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev]"
```

4. Set up pre-commit hooks:
```bash
pre-commit install
```

### Development Workflow

1. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

2. Make your changes following our coding standards
3. Write/update tests
4. Run the test suite:
```bash
pytest tests/
```

5. Submit a pull request

## Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for formatting
- Maximum line length: 100 characters
- Use type hints for all function parameters and return values

### Documentation Style

Use Google-style docstrings:

```python
def analyze_conversation(
    conversation_id: str,
    metrics: List[str]
) -> Dict[str, Any]:
    """Analyzes a conversation using specified metrics.

    Args:
        conversation_id: The ID of the conversation to analyze.
        metrics: List of metric names to calculate.

    Returns:
        Dictionary containing the calculated metrics.

    Raises:
        ValueError: If an invalid metric is specified.
        ConversationNotFound: If the conversation doesn't exist.
    """
```

### Commit Messages

Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Code style changes
- refactor: Code refactoring
- test: Adding or modifying tests
- chore: Maintenance tasks

## Project Structure

```
.
├── chat_analyzer/           # Main package
│   ├── core/               # Core functionality
│   ├── importers/          # Data import modules
│   ├── analysis/           # Analysis components
│   └── utils/              # Utility functions
├── docs/                   # Documentation
├── tests/                  # Test suite
└── scripts/                # Utility scripts
```

## Testing Guidelines

### Writing Tests

- Write unit tests for all new functionality
- Use pytest fixtures for common setup
- Mock external dependencies
- Include both positive and negative test cases
- Test edge cases and error conditions

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_analyzer.py

# Run with coverage
pytest --cov=chat_analyzer tests/
```

## Component Guidelines

### Vector Operations

When working with vector embeddings:
- Use batch processing for efficiency
- Handle out-of-memory scenarios
- Implement proper error handling
- Document vector dimensions and requirements

### Graph Operations

When modifying the knowledge graph:
- Use transactions for atomic operations
- Implement proper indexing
- Document graph patterns and queries
- Consider performance implications

### Analysis Components

When adding new analysis features:
- Document the analysis methodology
- Include performance considerations
- Provide usage examples
- Add relevant metrics

## Pull Request Process

1. Update documentation for new features
2. Add or update tests
3. Update the CHANGELOG.md
4. Ensure CI passes
5. Get review from two team members
6. Squash commits before merging

## Release Process

1. Update version in setup.py
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Deploy to PyPI

## Getting Help

- Check existing issues and discussions
- Join our community chat
- Ask in pull request comments
- Tag maintainers when needed

## Code of Conduct

This project follows the [Contributor Covenant](https://www.contributor-covenant.org/version/2/0/code_of_conduct/) Code of Conduct.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.