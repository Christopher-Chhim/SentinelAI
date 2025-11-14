# SentinelAI Test Suite

This directory contains comprehensive unit and integration tests for the SentinelAI application.

## Test Structure

### TypeScript/React Tests (`__tests__/`)

- **utils.test.ts**: Tests for the `cn` utility function used for className merging
- **schema-validation.test.ts**: Integration tests validating database schema structure
- **env-config.test.ts**: Tests for environment configuration validation
- **mall-data-structures.test.ts**: Tests for mall visualization data structures and zone logic

## Running Tests

### Frontend (TypeScript/React)

```bash
cd sentinelai_db

# Install dependencies (if not already installed)
npm install

# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Backend (Python)

```bash
cd server

# Install test dependencies
pip install pytest pytest-asyncio pytest-cov

# Run all server tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# Run specific test file
pytest tests/test_agent.py -v
```

```bash
cd model

# Run model tests
pytest tests/ -v
```

## Test Coverage

### Python Tests

- **server/tests/test_adjacencyList.py**: 13 tests for graph adjacency list conversion
- **server/tests/test_zone_traversal.py**: 15 tests for BFS pathfinding algorithm
- **server/tests/test_custom_types.py**: 40+ tests for Pydantic models
- **server/tests/test_prompts.py**: 25+ tests for LLM prompt validation
- **server/tests/test_agent.py**: 25+ tests for LLM agent logic
- **model/tests/test_live_scream_detector.py**: 20+ tests for scream detection model

### TypeScript Tests

- **utils.test.ts**: 50+ tests for className utility function
- **schema-validation.test.ts**: Database schema validation tests
- **env-config.test.ts**: Environment configuration tests
- **mall-data-structures.test.ts**: 15+ tests for mall data structures and zone logic

## Test Categories

### Unit Tests
- Pure function tests (adjacencyList, zone_traversal, utils)
- Data model validation (custom_types)
- Configuration tests (prompts, env-config)

### Integration Tests
- Database schema validation
- Component interaction tests
- API endpoint tests (future)

### Mock-Based Tests
- LLM client tests with mocked dependencies
- Model loading tests with mocked TensorFlow
- React component tests with mocked Three.js

## Best Practices

1. **Descriptive Test Names**: Each test clearly describes what it tests
2. **Arrange-Act-Assert**: Tests follow the AAA pattern
3. **Edge Cases**: Tests cover edge cases, error conditions, and boundary values
4. **Mocking**: External dependencies are properly mocked
5. **Coverage**: Aim for >80% code coverage on testable code

## Adding New Tests

### Python Tests

Create a new test file in `tests/` directory:

```python
"""
Unit tests for my_module.py
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from my_module import my_function


class TestMyFunction:
    """Test suite for my_function"""

    def test_basic_functionality(self):
        """Test basic functionality"""
        result = my_function(input_data)
        assert result == expected_output
```

### TypeScript Tests

Create a new test file in `__tests__/` directory:

```typescript
/**
 * Unit tests for myComponent.tsx
 */

import { render, screen } from '@testing-library/react'
import MyComponent from '@/components/MyComponent'

describe('MyComponent', () => {
  it('should render correctly', () => {
    render(<MyComponent />)
    expect(screen.getByText('Expected Text')).toBeInTheDocument()
  })
})
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Python Tests
  run: |
    cd server
    pytest tests/ --cov=. --cov-report=xml

- name: Run TypeScript Tests
  run: |
    cd sentinelai_db
    npm test -- --coverage
```

## Test Maintenance

- Update tests when code changes
- Add tests for new features
- Remove tests for deprecated features
- Keep test dependencies up-to-date
- Review and refactor tests periodically

## Known Limitations

- Three.js canvas rendering is mocked in tests
- Supabase real-time subscriptions require manual mocking
- ML model tests use mocked TensorFlow operations
- WebSocket tests require async handling

## Future Improvements

- [ ] Add E2E tests with Playwright
- [ ] Add visual regression tests
- [ ] Add performance benchmarks
- [ ] Add mutation testing
- [ ] Increase integration test coverage
- [ ] Add API contract tests

## Support

For questions or issues with tests, please:
1. Check existing test examples
2. Review Jest/Pytest documentation
3. Open an issue in the repository