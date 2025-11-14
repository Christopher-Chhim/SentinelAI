# Comprehensive Testing Guide for SentinelAI

This document provides a complete guide for running and understanding the test suite for the SentinelAI emergency response system.

## Overview

The SentinelAI project includes extensive unit and integration tests covering:
- Python backend services (FastAPI, LLM agent)
- Machine learning model (scream detection)
- TypeScript/React frontend (Next.js, Three.js)
- Database schema validation

**Total Test Count**: 150+ tests across all modules

## Quick Start

### Running All Tests

```bash
# Frontend tests
cd sentinelai_db && npm install && npm test

# Backend server tests
cd server && pip install -r tests/requirements.txt && pytest tests/ -v

# Model tests
cd model && pip install -r tests/requirements.txt && pytest tests/ -v
```

## Detailed Test Execution

### 1. Python Server Tests

```bash
cd server

# Install test dependencies
pip install -r tests/requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test files
pytest tests/test_adjacencyList.py -v
pytest tests/test_zone_traversal.py -v
pytest tests/test_custom_types.py -v
pytest tests/test_prompts.py -v
pytest tests/test_agent.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html --cov-report=term

# Run tests matching a pattern
pytest tests/ -k "test_bfs" -v

# Run tests with output
pytest tests/ -v -s
```

**Test Files:**
- `test_adjacencyList.py`: Graph adjacency list conversion (13 tests)
- `test_zone_traversal.py`: BFS pathfinding algorithm (15 tests)
- `test_custom_types.py`: Pydantic model validation (40+ tests)
- `test_prompts.py`: LLM prompt validation (25+ tests)
- `test_agent.py`: LLM client logic (25+ tests)

### 2. Model Tests

```bash
cd model

# Install test dependencies
pip install -r tests/requirements.txt

# Run all model tests
pytest tests/ -v

# Run specific test
pytest tests/test_live_scream_detector.py -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html
```

**Test Files:**
- `test_live_scream_detector.py`: Scream detection model (20+ tests)

### 3. TypeScript/React Tests

```bash
cd sentinelai_db

# Install dependencies (includes test libraries)
npm install

# Run all tests
npm test

# Run in watch mode (great for development)
npm run test:watch

# Run with coverage
npm run test:coverage

# Run specific test file
npm test -- utils.test.ts

# Run tests matching a pattern
npm test -- --testNamePattern="should merge"
```

**Test Files:**
- `utils.test.ts`: className utility function (50+ tests)
- `schema-validation.test.ts`: Database schema validation (9+ tests)
- `env-config.test.ts`: Environment configuration (3+ tests)
- `mall-data-structures.test.ts`: Mall visualization logic (15+ tests)

## Test Categories

### Pure Function Tests
Tests for functions without side effects:
- `calculate_adjacency_list()` - Graph conversion
- `bfs()` - Pathfinding algorithm
- `cn()` - className merging
- Status determination functions

### Data Model Tests
Tests for data structures and validation:
- Pydantic models (Utterance, ResponseRequiredRequest, etc.)
- Type safety and validation
- JSON serialization

### Configuration Tests
Tests for system configuration:
- Prompt templates and content
- Environment variable validation
- Database schema structure

### Mock-Based Tests
Tests with mocked dependencies:
- LLM agent methods (mocked Cerebras API)
- Model loading (mocked TensorFlow)
- Component rendering (mocked Three.js)

## Coverage Reports

### Python Coverage

After running tests with coverage:
```bash
# View HTML coverage report
cd server
pytest tests/ --cov=. --cov-report=html
open htmlcov/index.html
```

### TypeScript Coverage

After running tests with coverage:
```bash
cd sentinelai_db
npm run test:coverage
open coverage/lcov-report/index.html
```

## Test Assertions

### Python (pytest)
```python
assert result == expected
assert len(result) > 0
assert "text" in result
assert result is not None
with pytest.raises(ValidationError):
    create_invalid_object()
```

### TypeScript (Jest)
```typescript
expect(result).toBe(expected)
expect(result).toContain('text')
expect(result).toHaveLength(5)
expect(result).toBeDefined()
expect(result).toBeInTheDocument()
```

## Test Naming Conventions

### Python
```python
def test_function_name_condition():
    """Test that function_name does X when condition Y"""
    pass
```

### TypeScript
```typescript
it('should do X when Y', () => {
  // test code
})
```

## Mocking Strategies

### Python - Mocking async functions
```python
from unittest.mock import AsyncMock, patch

@patch('module.async_function')
async def test_with_async_mock(mock_func):
    mock_func.return_value = AsyncMock(return_value="result")
    result = await function_under_test()
    assert result == "result"
```

### TypeScript - Mocking modules
```typescript
jest.mock('@/lib/module', () => ({
  function: jest.fn(() => 'mocked result')
}))
```

## Debugging Tests

### Python
```bash
# Run with print statements visible
pytest tests/ -v -s

# Run with debugger
pytest tests/ --pdb

# Stop on first failure
pytest tests/ -x

# Show local variables on failure
pytest tests/ -l
```

### TypeScript
```bash
# Run with console output
npm test -- --verbose

# Debug in VS Code
# Add breakpoint and use "Debug Jest Tests" configuration
```

## Common Issues and Solutions

### Issue: Import errors in Python tests
**Solution**: Tests add parent directory to path:
```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

### Issue: Module not found in TypeScript tests
**Solution**: Check `jest.config.js` moduleNameMapper:
```javascript
moduleNameMapper: {
  '^@/(.*)$': '<rootDir>/$1',
}
```

### Issue: Async tests timing out
**Solution**: Increase timeout in pytest:
```python
@pytest.mark.timeout(10)
async def test_slow_function():
    pass
```

### Issue: Canvas/WebGL errors in React tests
**Solution**: Mocked in `jest.setup.js`:
```javascript
HTMLCanvasElement.prototype.getContext = jest.fn()
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests

on: [push, pull_request]

jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: |
          cd server
          pip install -r requirements.txt -r tests/requirements.txt
      - name: Run tests
        run: |
          cd server
          pytest tests/ --cov=. --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  test-typescript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '18'
      - name: Install dependencies
        run: |
          cd sentinelai_db
          npm install
      - name: Run tests
        run: |
          cd sentinelai_db
          npm test -- --coverage
```

## Performance Considerations

- Use `pytest-xdist` for parallel Python test execution
- Use `jest --maxWorkers=4` for parallel TypeScript tests
- Mock expensive operations (API calls, ML model loading)
- Use fixtures for reusable test data

## Writing New Tests

### Checklist for New Tests
- [ ] Test describes a specific behavior
- [ ] Test name is clear and descriptive
- [ ] Test covers happy path
- [ ] Test covers edge cases
- [ ] Test covers error conditions
- [ ] Mocks are used appropriately
- [ ] Test is independent (no side effects)
- [ ] Test is deterministic (no random failures)

### Test Template - Python
```python
class TestNewFeature:
    """Test suite for new_feature"""

    def test_happy_path(self):
        """Test basic functionality works"""
        result = new_feature(valid_input)
        assert result == expected_output

    def test_edge_case(self):
        """Test handling of edge case"""
        result = new_feature(edge_case_input)
        assert result is not None

    def test_error_handling(self):
        """Test error is raised for invalid input"""
        with pytest.raises(ValueError):
            new_feature(invalid_input)
```

### Test Template - TypeScript
```typescript
describe('NewFeature', () => {
  describe('Happy path', () => {
    it('should work with valid input', () => {
      const result = newFeature(validInput)
      expect(result).toBe(expectedOutput)
    })
  })

  describe('Edge cases', () => {
    it('should handle empty input', () => {
      const result = newFeature(emptyInput)
      expect(result).toBeDefined()
    })
  })

  describe('Error handling', () => {
    it('should throw error for invalid input', () => {
      expect(() => newFeature(invalidInput)).toThrow()
    })
  })
})
```

## Test Maintenance

- Run tests before committing code
- Update tests when modifying code
- Remove obsolete tests
- Refactor tests as needed
- Keep test dependencies updated
- Review test coverage regularly

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Jest Documentation](https://jestjs.io/)
- [Testing Library](https://testing-library.com/)
- [Testing Best Practices](https://testingjavascript.com/)

## Summary

This test suite provides comprehensive coverage of the SentinelAI application with 150+ tests covering Python backend, ML models, and TypeScript frontend. Tests are designed to be:
- **Fast**: Most tests run in milliseconds
- **Reliable**: Deterministic and well-mocked
- **Maintainable**: Clear naming and structure
- **Comprehensive**: Cover happy paths, edge cases, and errors

For questions or contributions, please refer to the project's main README.