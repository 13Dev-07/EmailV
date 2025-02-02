# Email Validator Development Guide

## Project Structure
```
app/
├── api/              # API endpoints and models
├── caching/          # Redis caching components
├── config/           # Configuration management
├── monitoring/       # Prometheus metrics
├── tests/           # Test suites
├── validators/       # Core validation logic
└── main.py          # Application entry point
```

## Development Setup

1. Set up development environment
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
```

2. Install pre-commit hooks
```bash
pre-commit install
```

3. Configure environment for development
```bash
cp .env.example .env.dev
# Edit .env.dev with development settings
```

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest app/tests/test_validators.py
```

### Test Categories
1. Unit Tests
   - Email validation logic
   - DNS resolution
   - SMTP verification
   - Redis operations

2. Integration Tests
   - API endpoints
   - Component interaction
   - Caching behavior

3. Performance Tests
   - Load testing
   - Concurrency testing
   - Cache efficiency

## Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document public interfaces
- Write descriptive commit messages

## Adding Features

1. Create feature branch
```bash
git checkout -b feature/your-feature-name
```

2. Implement feature
   - Add tests first
   - Implement functionality
   - Update documentation
   - Add metrics if needed

3. Run quality checks
```bash
# Run linter
flake8 app

# Run type checker
mypy app

# Run tests
pytest
```

4. Submit pull request
   - Describe changes
   - Link related issues
   - Include test results
   - Add migration steps if needed

## Documentation

### Updating Docs
1. API changes: Update `docs/api.md`
2. Configuration: Update `docs/configuration.md`
3. Deployment: Update `docs/deployment.md`

### Building Documentation
```bash
# Generate API docs
python scripts/generate_api_docs.py

# Build documentation site
mkdocs build
```

## Performance Optimization

### Profiling
```bash
# Run profiler
python -m cProfile -o profile.stats app/main.py

# Analyze results
snakeviz profile.stats
```

### Benchmarking
```bash
# Run benchmark suite
pytest benchmark/
```

## Debugging

### Logging
```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Detailed information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
```

### Development Server
```bash
# Run with reload
uvicorn app.main:app --reload --log-level debug

# Run with debugger
python -m debugpy --listen 5678 -m uvicorn app.main:app
```