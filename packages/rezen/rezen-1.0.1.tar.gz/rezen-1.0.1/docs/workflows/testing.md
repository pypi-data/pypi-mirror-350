# Testing Workflows

This guide covers testing strategies, patterns, and best practices for the ReZEN API client.

## 🧪 Overview

Testing the ReZEN API wrapper involves:
- Unit testing with mocked responses
- Integration testing with live API
- Error scenario testing
- Performance and reliability testing

## 🚀 Quick Testing Setup

```python
# Install testing dependencies
pip install pytest pytest-cov responses pytest-mock

# Run tests
pytest

# Run with coverage
pytest --cov=rezen --cov-report=html
```

## 📋 Testing Frameworks

### Framework 1: Unit Testing with Responses

```python
import responses
import pytest
from rezen import RezenClient
from rezen.exceptions import ValidationError, NotFoundError

class TestRezenClient:
    """Test ReZEN client with mocked responses."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = RezenClient(api_key="test_key")
    
    @responses.activate
    def test_search_teams_success(self):
        """Test successful team search."""
        # Mock API response
        mock_response = {
            "pageNumber": 0,
            "pageSize": 10,
            "totalCount": 1,
            "results": [
                {
                    "id": "team-123",
                    "name": "Test Team",
                    "status": "ACTIVE",
                    "type": "NORMAL"
                }
            ]
        }
        
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams",
            json=mock_response,
            status=200
        )
        
        # Execute test
        result = self.client.teams.search_teams(name="Test Team")
        
        # Assertions
        assert result == mock_response
        assert len(result["results"]) == 1
        assert result["results"][0]["name"] == "Test Team"
    
    @responses.activate 
    def test_search_teams_validation_error(self):
        """Test validation error handling."""
        # Mock validation error response
        error_response = {
            "message": "Validation failed",
            "errors": {
                "name": ["Name is required"]
            }
        }
        
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams",
            json=error_response,
            status=400
        )
        
        # Test that exception is raised
        with pytest.raises(ValidationError) as exc_info:
            self.client.teams.search_teams(name="")
        
        # Verify error details
        assert exc_info.value.status_code == 400
        assert "Validation failed" in str(exc_info.value)
```

### Framework 2: Integration Testing

```python
import pytest
from rezen import RezenClient

class TestLiveAPI:
    """Integration tests with live API."""
    
    @pytest.fixture(scope="class")
    def client(self):
        """Create live API client."""
        return RezenClient()  # Uses environment API key
    
    @pytest.mark.integration
    def test_authentication(self, client):
        """Test that authentication works."""
        try:
            result = client.teams.search_teams(page_size=1)
            assert "results" in result
            assert "totalCount" in result
        except Exception as e:
            pytest.fail(f"Authentication failed: {e}")
    
    @pytest.mark.integration
    def test_teams_search(self, client):
        """Test team search functionality."""
        result = client.teams.search_teams(
            name="The Perry Group Standard Team"
        )
        
        assert result is not None
        assert "results" in result
        
        # Should find at least one team
        teams = result.get("results", [])
        assert len(teams) > 0
        
        # Verify team structure
        team = teams[0]
        required_fields = ["id", "name", "status", "type"]
        for field in required_fields:
            assert field in team
    
    @pytest.mark.integration
    def test_transaction_builder_lifecycle(self, client):
        """Test complete transaction builder lifecycle."""
        # Create transaction builder
        response = client.transaction_builder.create_transaction_builder({
            "type": "PURCHASE"
        })
        
        builder_id = response.get("message")
        assert builder_id is not None
        
        try:
            # Add property info
            property_info = {
                "address": "123 Test Street",
                "city": "Test City",
                "state": "CA",
                "zipCode": "90210"
            }
            client.transaction_builder.update_location_info(
                builder_id, property_info
            )
            
            # Verify builder exists
            builder = client.transaction_builder.get_transaction_builder(
                builder_id
            )
            assert builder is not None
            
        finally:
            # Cleanup - delete builder
            try:
                client.transaction_builder.delete_transaction_builder(builder_id)
            except Exception:
                pass  # Ignore cleanup errors
```

### Framework 3: Error Scenario Testing

```python
class TestErrorScenarios:
    """Test error handling scenarios."""
    
    def setup_method(self):
        """Set up test client."""
        self.client = RezenClient(api_key="test_key")
    
    @responses.activate
    def test_authentication_error(self):
        """Test authentication error handling."""
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams",
            json={"message": "Unauthorized"},
            status=401
        )
        
        with pytest.raises(AuthenticationError):
            self.client.teams.search_teams()
    
    @responses.activate
    def test_not_found_error(self):
        """Test not found error handling."""
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams/invalid-id",
            json={"message": "Team not found"},
            status=404
        )
        
        with pytest.raises(NotFoundError):
            self.client.teams.get_team_without_agents("invalid-id")
    
    @responses.activate
    def test_rate_limit_error(self):
        """Test rate limit error handling."""
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams",
            json={"message": "Rate limit exceeded"},
            status=429,
            headers={"Retry-After": "60"}
        )
        
        with pytest.raises(RateLimitError):
            self.client.teams.search_teams()
    
    @responses.activate
    def test_server_error_retry(self):
        """Test server error retry logic."""
        # First call fails, second succeeds
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams",
            json={"message": "Internal server error"},
            status=500
        )
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams",
            json={"results": []},
            status=200
        )
        
        # Should retry and succeed
        result = self.client.teams.search_teams()
        assert result == {"results": []}
```

## 🛠️ Test Utilities

### Utility 1: Test Data Factories

```python
from typing import Dict, Any

class TestDataFactory:
    """Factory for creating test data."""
    
    @staticmethod
    def team_data(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create team test data."""
        data = {
            "id": "test-team-123",
            "name": "Test Team",
            "status": "ACTIVE",
            "type": "NORMAL",
            "createdAt": 1640995200000
        }
        
        if overrides:
            data.update(overrides)
        
        return data
    
    @staticmethod
    def transaction_builder_data(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create transaction builder test data."""
        data = {
            "type": "PURCHASE",
            "property": {
                "address": "123 Test Street",
                "city": "Test City",
                "state": "CA",
                "zipCode": "90210"
            }
        }
        
        if overrides:
            data.update(overrides)
        
        return data
    
    @staticmethod
    def buyer_data(overrides: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create buyer test data."""
        data = {
            "firstName": "John",
            "lastName": "Buyer",
            "email": "john.buyer@example.com",
            "phoneNumber": "555-123-4567"
        }
        
        if overrides:
            data.update(overrides)
        
        return data

# Usage in tests
def test_create_buyer():
    buyer_data = TestDataFactory.buyer_data({
        "firstName": "Jane",
        "email": "jane@example.com"
    })
    
    # Use in test...
```

### Utility 2: Response Mock Helper

```python
import responses
from typing import Dict, Any, Optional

class ResponseMocker:
    """Helper for mocking API responses."""
    
    @staticmethod
    def add_teams_search_response(
        teams: list = None,
        status: int = 200,
        total_count: int = None
    ):
        """Add mocked teams search response."""
        if teams is None:
            teams = [TestDataFactory.team_data()]
        
        if total_count is None:
            total_count = len(teams)
        
        mock_response = {
            "pageNumber": 0,
            "pageSize": len(teams),
            "totalCount": total_count,
            "results": teams
        }
        
        responses.add(
            responses.GET,
            "https://yenta.therealbrokerage.com/api/v1/teams",
            json=mock_response,
            status=status
        )
    
    @staticmethod
    def add_error_response(
        url: str,
        status: int,
        message: str = "Error occurred",
        errors: Dict[str, Any] = None
    ):
        """Add mocked error response."""
        error_data = {"message": message}
        
        if errors:
            error_data["errors"] = errors
        
        responses.add(
            responses.GET,
            url,
            json=error_data,
            status=status
        )

# Usage in tests
@responses.activate
def test_teams_with_helper():
    ResponseMocker.add_teams_search_response(
        teams=[TestDataFactory.team_data({"name": "Special Team"})],
        total_count=1
    )
    
    client = RezenClient(api_key="test")
    result = client.teams.search_teams()
    
    assert result["results"][0]["name"] == "Special Team"
```

### Utility 3: Test Configuration

```python
import os
import pytest
from unittest.mock import patch

class TestConfig:
    """Test configuration management."""
    
    @staticmethod
    @pytest.fixture
    def mock_api_key():
        """Mock API key for testing."""
        with patch.dict(os.environ, {"REZEN_API_KEY": "test_api_key"}):
            yield "test_api_key"
    
    @staticmethod
    @pytest.fixture  
    def test_client(mock_api_key):
        """Create test client with mocked API key."""
        return RezenClient()
    
    @staticmethod
    def skip_if_no_api_key():
        """Skip test if no API key available."""
        return pytest.mark.skipif(
            not os.getenv("REZEN_API_KEY"),
            reason="No API key available for integration testing"
        )

# Usage
class TestWithConfig:
    @TestConfig.skip_if_no_api_key()
    def test_integration_feature(self):
        """This test requires API key."""
        client = RezenClient()
        # Test implementation...
```

## 📊 Testing Workflows

### Workflow 1: Test-Driven Development

```python
# 1. Write failing test first
def test_new_feature_that_does_not_exist():
    """Test for feature that doesn't exist yet."""
    client = RezenClient(api_key="test")
    
    # This should work when implemented
    result = client.new_feature.do_something("param")
    assert result["status"] == "success"

# 2. Run test (it fails)
# pytest test_new_feature.py -v

# 3. Implement minimum code to pass
# ... implement new_feature ...

# 4. Run test again (it passes)
# 5. Refactor and improve
```

### Workflow 2: Coverage-Driven Testing

```python
# Run coverage analysis
# pytest --cov=rezen --cov-report=html

# Identify uncovered lines
# open htmlcov/index.html

# Write tests for uncovered code
def test_edge_case_not_covered():
    """Test edge case found in coverage report."""
    # Test implementation for uncovered line...
    pass
```

### Workflow 3: Performance Testing

```python
import time
import pytest

class TestPerformance:
    """Performance testing for API calls."""
    
    @pytest.mark.performance
    def test_teams_search_performance(self):
        """Test team search response time."""
        client = RezenClient()
        
        start_time = time.time()
        result = client.teams.search_teams(page_size=100)
        end_time = time.time()
        
        response_time = end_time - start_time
        
        # Should respond within 2 seconds
        assert response_time < 2.0, f"Response too slow: {response_time:.2f}s"
        
        # Should return data
        assert len(result["results"]) > 0
    
    @pytest.mark.performance
    def test_concurrent_requests(self):
        """Test concurrent API requests."""
        import concurrent.futures
        
        client = RezenClient()
        
        def make_request():
            return client.teams.search_teams(page_size=1)
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # All should succeed
        assert len(results) == 10
        for result in results:
            assert "results" in result
```

## 🔧 Testing Configuration

### Configuration 1: pytest.ini

```ini
[tool:pytest]
markers =
    integration: marks tests as integration tests (deselect with '-m "not integration"')
    performance: marks tests as performance tests
    slow: marks tests as slow running
    unit: marks tests as unit tests

testpaths = tests

python_files = test_*.py *_test.py
python_classes = Test*
python_functions = test_*

addopts = 
    --strict-markers
    --disable-warnings
    -v
    --tb=short
    --cov=rezen
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=95
```

### Configuration 2: Test Environment Setup

```python
# conftest.py
import pytest
import os
from unittest.mock import patch

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Set up test environment."""
    # Set test environment variables
    test_env = {
        "REZEN_API_KEY": "test_api_key_for_mocking",
        "ENVIRONMENT": "test"
    }
    
    with patch.dict(os.environ, test_env):
        yield

@pytest.fixture
def mock_responses():
    """Enable responses mocking for test."""
    import responses
    with responses.RequestsMock() as rsps:
        yield rsps
```

### Configuration 3: CI/CD Pipeline Testing

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, "3.10", "3.11"]
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        pip install -r requirements-dev.txt
    
    - name: Run unit tests
      run: |
        pytest -m "not integration" --cov=rezen
    
    - name: Run integration tests
      if: matrix.python-version == '3.9'
      env:
        REZEN_API_KEY: ${{ secrets.REZEN_API_KEY }}
      run: |
        pytest -m integration
    
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## ✅ Best Practices

### 1. Test Structure (AAA Pattern)
```python
def test_feature():
    # Arrange
    client = RezenClient(api_key="test")
    mock_data = {"key": "value"}
    
    # Act
    result = client.feature.method(mock_data)
    
    # Assert
    assert result["status"] == "success"
```

### 2. Descriptive Test Names
```python
# ✅ Good: Descriptive
def test_search_teams_returns_empty_list_when_no_teams_match_criteria():
    pass

# ❌ Bad: Vague
def test_search_teams():
    pass
```

### 3. Independent Tests
```python
# ✅ Good: Independent test
def test_create_transaction_builder():
    client = RezenClient(api_key="test")
    # Test creates its own data
    
# ❌ Bad: Dependent on other tests
def test_update_transaction_builder():
    # Assumes builder from previous test exists
```

### 4. Test One Thing
```python
# ✅ Good: Tests one specific behavior
def test_search_teams_with_invalid_status_raises_validation_error():
    pass

# ❌ Bad: Tests multiple things
def test_teams_functionality():
    # Tests search, create, update, delete all in one
```

## 🚨 Common Testing Issues

### Issue: Flaky Tests

**Cause:** Tests depend on external state or timing

**Solution:**
```python
# Use deterministic test data
@responses.activate
def test_with_mocked_data():
    # Mock all external calls
    responses.add(...)
    
    # Test with predictable data
```

### Issue: Slow Test Suite

**Cause:** Too many integration tests

**Solution:**
```python
# Separate unit and integration tests
pytest -m "not integration"  # Fast unit tests
pytest -m integration        # Slower integration tests
```

### Issue: Low Test Coverage

**Cause:** Missing edge case tests

**Solution:**
```python
# Test error conditions
def test_error_scenarios():
    with pytest.raises(ValidationError):
        client.method(invalid_data)
```

## 🔗 Related Workflows

- **[Error Handling](error-handling.md)** - Testing error scenarios
- **[Authentication](authentication.md)** - Testing auth configurations
- **[Transaction Builder](transaction-builder.md)** - Testing transaction workflows
- **[Teams](teams.md)** - Testing team operations 