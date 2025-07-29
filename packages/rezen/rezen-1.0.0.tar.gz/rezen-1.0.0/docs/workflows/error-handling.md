# Error Handling Workflows

This guide covers common errors, troubleshooting, and error handling patterns for the ReZEN API.

## 🚨 Overview

The ReZEN API client provides structured error handling through custom exception classes that help you understand and respond to different types of errors.

## 🏗️ Exception Hierarchy

```python
from rezen.exceptions import (
    RezenError,          # Base exception
    AuthenticationError, # 401 errors
    ValidationError,     # 400 errors
    NotFoundError,       # 404 errors
    RateLimitError,      # 429 errors
    ServerError,         # 5xx errors
    NetworkError,        # Connection issues
)
```

## 🚀 Quick Error Handling

```python
from rezen import RezenClient
from rezen.exceptions import AuthenticationError, ValidationError, NotFoundError

client = RezenClient()

try:
    result = client.transaction_builder.create_transaction_builder({
        "type": "PURCHASE"
    })
except AuthenticationError as e:
    print(f"🔑 Authentication issue: {e}")
    # Check API key
except ValidationError as e:
    print(f"📝 Validation issue: {e}")
    print(f"Details: {e.response_data}")
    # Fix input data
except NotFoundError as e:
    print(f"🔍 Resource not found: {e}")
    # Check IDs
except Exception as e:
    print(f"❌ Unexpected error: {e}")
```

## 📋 Error Handling Workflows

### Workflow 1: Comprehensive Error Handling

```python
from rezen import RezenClient
from rezen.exceptions import (
    AuthenticationError, ValidationError, NotFoundError,
    RateLimitError, ServerError, NetworkError, RezenError
)
import time

def safe_api_call(func, *args, **kwargs):
    """Safely execute an API call with comprehensive error handling."""
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
            
        except AuthenticationError as e:
            print(f"🔑 Authentication failed: {e}")
            # Don't retry auth errors
            raise
            
        except ValidationError as e:
            print(f"📝 Validation error: {e}")
            print(f"Response data: {e.response_data}")
            # Don't retry validation errors
            raise
            
        except NotFoundError as e:
            print(f"🔍 Resource not found: {e}")
            # Don't retry not found errors
            raise
            
        except RateLimitError as e:
            print(f"⏱️  Rate limit exceeded: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (2 ** attempt)  # Exponential backoff
                print(f"   Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
                continue
            raise
            
        except ServerError as e:
            print(f"🔧 Server error: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (attempt + 1)
                print(f"   Retrying in {wait_time}s... (attempt {attempt + 1})")
                time.sleep(wait_time)
                continue
            raise
            
        except NetworkError as e:
            print(f"🌐 Network error: {e}")
            if attempt < max_retries - 1:
                wait_time = retry_delay * (attempt + 1)
                print(f"   Retrying in {wait_time}s... (attempt {attempt + 1})")
                time.sleep(wait_time)
                continue
            raise
            
        except RezenError as e:
            print(f"⚠️  ReZEN API error: {e}")
            raise
            
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            raise

# Usage
client = RezenClient()

result = safe_api_call(
    client.teams.search_teams,
    name="The Perry Group Standard Team"
)
```

### Workflow 2: Transaction-Specific Error Handling

```python
def create_transaction_with_error_handling(transaction_data):
    """Create transaction with detailed error handling."""
    
    client = RezenClient()
    
    try:
        # Step 1: Create transaction builder
        response = client.transaction_builder.create_transaction_builder(transaction_data)
        builder_id = response.get('message')
        
        if not builder_id:
            raise ValueError("No builder ID returned from API")
        
        print(f"✅ Transaction builder created: {builder_id}")
        return builder_id
        
    except ValidationError as e:
        print(f"❌ Transaction data validation failed:")
        
        # Parse validation details
        response_data = e.response_data
        if isinstance(response_data, dict):
            if 'errors' in response_data:
                for field, error in response_data['errors'].items():
                    print(f"   {field}: {error}")
            elif 'message' in response_data:
                print(f"   {response_data['message']}")
        
        # Suggest fixes
        print("\n🔧 Suggested fixes:")
        print("   - Check required fields: type, property details")
        print("   - Verify data formats (dates, emails, phone numbers)")
        print("   - Ensure numeric fields are valid")
        
        raise
        
    except AuthenticationError:
        print("❌ Authentication failed")
        print("🔧 Check your API key in environment variables")
        raise
        
    except Exception as e:
        print(f"❌ Unexpected error creating transaction: {e}")
        raise

# Usage
transaction_data = {
    "type": "PURCHASE",
    "property": {
        "address": "123 Main St",
        "city": "Los Angeles",
        "state": "CA",
        "zipCode": "90210"
    }
}

try:
    builder_id = create_transaction_with_error_handling(transaction_data)
except Exception as e:
    print(f"Failed to create transaction: {e}")
```

### Workflow 3: Batch Operation Error Handling

```python
def batch_operation_with_error_handling(operations):
    """Execute multiple operations with individual error handling."""
    
    results = []
    errors = []
    
    for i, operation in enumerate(operations):
        try:
            result = operation()
            results.append({
                'index': i,
                'status': 'success',
                'result': result
            })
            
        except ValidationError as e:
            error_info = {
                'index': i,
                'status': 'validation_error',
                'error': str(e),
                'details': e.response_data
            }
            errors.append(error_info)
            results.append(error_info)
            
        except NotFoundError as e:
            error_info = {
                'index': i,
                'status': 'not_found',
                'error': str(e)
            }
            errors.append(error_info)
            results.append(error_info)
            
        except Exception as e:
            error_info = {
                'index': i,
                'status': 'unexpected_error',
                'error': str(e)
            }
            errors.append(error_info)
            results.append(error_info)
    
    # Summary
    success_count = len([r for r in results if r['status'] == 'success'])
    print(f"Batch operation complete: {success_count}/{len(operations)} successful")
    
    if errors:
        print(f"❌ {len(errors)} errors occurred:")
        for error in errors:
            print(f"   Operation {error['index']}: {error['status']} - {error['error']}")
    
    return results, errors

# Usage
client = RezenClient()

operations = [
    lambda: client.teams.search_teams(name="Team 1"),
    lambda: client.teams.search_teams(name="Team 2"),
    lambda: client.teams.get_team_without_agents("invalid-id"),  # Will cause error
]

results, errors = batch_operation_with_error_handling(operations)
```

## 🔍 Specific Error Scenarios

### Authentication Errors (401)

```python
# Common causes and solutions
try:
    client = RezenClient()
    teams = client.teams.search_teams()
except AuthenticationError as e:
    print("🔑 Authentication Error Troubleshooting:")
    print("1. Check REZEN_API_KEY environment variable")
    print("2. Verify API key format (should start with 'real_')")
    print("3. Confirm API key is not expired")
    print("4. Test with explicit API key:")
    print("   client = RezenClient(api_key='your_key_here')")
```

### Validation Errors (400)

```python
# Parse validation details
try:
    client.transaction_builder.add_buyer(builder_id, {
        "firstName": "",  # Empty required field
        "email": "invalid-email"  # Invalid format
    })
except ValidationError as e:
    print("📝 Validation Error Details:")
    
    response_data = e.response_data
    if 'errors' in response_data:
        for field, messages in response_data['errors'].items():
            print(f"   {field}: {messages}")
    
    # Suggest fixes based on common issues
    common_fixes = {
        'email': 'Ensure valid email format (user@domain.com)',
        'phoneNumber': 'Use format: +1234567890 or (123) 456-7890',
        'firstName': 'Cannot be empty',
        'lastName': 'Cannot be empty',
        'zipCode': 'Must be 5 digits',
        'state': 'Use 2-letter state code (CA, NY, etc.)'
    }
    
    for field in response_data.get('errors', {}):
        if field in common_fixes:
            print(f"   💡 {field}: {common_fixes[field]}")
```

### Not Found Errors (404)

```python
# Handle missing resources
def safe_get_team(team_id):
    try:
        return client.teams.get_team_without_agents(team_id)
    except NotFoundError:
        print(f"🔍 Team not found: {team_id}")
        print("   Possible causes:")
        print("   - Team ID is incorrect")
        print("   - Team was deleted")
        print("   - No permission to access team")
        
        # Try to find similar teams
        print("   Searching for similar teams...")
        try:
            teams = client.teams.search_teams(search_text="Perry")
            if teams.get('results'):
                print("   Found similar teams:")
                for team in teams['results'][:3]:
                    print(f"     - {team['name']} (ID: {team['id']})")
        except Exception:
            pass
        
        return None
```

### Rate Limiting (429)

```python
import time
import random

def handle_rate_limiting(func, *args, **kwargs):
    """Handle rate limiting with exponential backoff."""
    
    max_retries = 5
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
            
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise  # Final attempt failed
            
            # Exponential backoff with jitter
            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
            print(f"⏱️  Rate limited. Waiting {delay:.1f}s before retry {attempt + 1}/{max_retries}")
            time.sleep(delay)
            
    return None  # Should not reach here
```

### Server Errors (5xx)

```python
def handle_server_errors(func, *args, **kwargs):
    """Handle server errors with retry logic."""
    
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
            
        except ServerError as e:
            print(f"🔧 Server error (attempt {attempt + 1}): {e}")
            
            if attempt == max_retries - 1:
                print("❌ Max retries reached. Server may be experiencing issues.")
                print("💡 Try again later or contact support if issue persists.")
                raise
            
            wait_time = retry_delay * (attempt + 1)
            print(f"   Retrying in {wait_time}s...")
            time.sleep(wait_time)
```

## 🛡️ Defensive Programming Patterns

### Pattern 1: Validate Before API Calls

```python
def validate_transaction_data(data):
    """Validate transaction data before API call."""
    
    errors = []
    
    # Required fields
    if not data.get('type'):
        errors.append("Transaction type is required")
    
    # Property validation
    property_data = data.get('property', {})
    required_property_fields = ['address', 'city', 'state', 'zipCode']
    
    for field in required_property_fields:
        if not property_data.get(field):
            errors.append(f"Property {field} is required")
    
    # State validation
    if property_data.get('state') and len(property_data['state']) != 2:
        errors.append("State must be 2-letter code (e.g., 'CA')")
    
    # ZIP code validation
    zip_code = property_data.get('zipCode')
    if zip_code and not zip_code.isdigit():
        errors.append("ZIP code must contain only digits")
    
    if errors:
        raise ValueError(f"Validation failed: {'; '.join(errors)}")
    
    return True

# Usage
try:
    transaction_data = {"type": "PURCHASE", "property": {...}}
    validate_transaction_data(transaction_data)
    
    result = client.transaction_builder.create_transaction_builder(transaction_data)
except ValueError as e:
    print(f"❌ Pre-validation failed: {e}")
except ValidationError as e:
    print(f"❌ API validation failed: {e}")
```

### Pattern 2: Circuit Breaker Pattern

```python
import time
from typing import Callable, Any

class CircuitBreaker:
    """Circuit breaker for API calls."""
    
    def __init__(self, failure_threshold=5, recovery_timeout=60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = 'CLOSED'  # CLOSED, OPEN, HALF_OPEN
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        
        if self.state == 'OPEN':
            if time.time() - self.last_failure_time < self.recovery_timeout:
                raise Exception("Circuit breaker is OPEN")
            else:
                self.state = 'HALF_OPEN'
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        self.failure_count = 0
        self.state = 'CLOSED'
    
    def _on_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = 'OPEN'

# Usage
circuit_breaker = CircuitBreaker()

try:
    result = circuit_breaker.call(
        client.teams.search_teams,
        name="Team Name"
    )
except Exception as e:
    print(f"Circuit breaker protected call failed: {e}")
```

## 📊 Error Monitoring and Logging

```python
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('rezen_api')

def log_api_error(operation, error, **context):
    """Log API errors with context."""
    
    error_data = {
        'operation': operation,
        'error_type': type(error).__name__,
        'error_message': str(error),
        'timestamp': datetime.utcnow().isoformat(),
        **context
    }
    
    if hasattr(error, 'status_code'):
        error_data['status_code'] = error.status_code
    
    if hasattr(error, 'response_data'):
        error_data['response_data'] = error.response_data
    
    logger.error(f"API Error: {error_data}")
    
    # Could also send to monitoring service
    # send_to_monitoring_service(error_data)

# Usage
try:
    result = client.teams.search_teams(name="Team Name")
except Exception as e:
    log_api_error(
        operation='teams.search_teams',
        error=e,
        team_name="Team Name",
        user_id="user123"
    )
    raise
```

## ✅ Best Practices

### 1. Always Use Specific Exception Handling
```python
# ✅ Good: Specific exceptions
try:
    result = api_call()
except ValidationError as e:
    handle_validation_error(e)
except AuthenticationError as e:
    handle_auth_error(e)

# ❌ Bad: Catch-all
try:
    result = api_call()
except Exception as e:
    print(f"Something went wrong: {e}")
```

### 2. Provide Actionable Error Messages
```python
# ✅ Good: Actionable message
except ValidationError as e:
    print(f"❌ Email validation failed: {e}")
    print("💡 Please use format: user@domain.com")

# ❌ Bad: Generic message
except ValidationError as e:
    print("Error occurred")
```

### 3. Log Errors with Context
```python
# ✅ Good: Context included
try:
    client.transaction_builder.add_buyer(builder_id, buyer_data)
except ValidationError as e:
    logger.error(f"Failed to add buyer to {builder_id}: {e}", extra={
        'builder_id': builder_id,
        'buyer_data': buyer_data,
        'response': e.response_data
    })

# ❌ Bad: No context
except ValidationError as e:
    logger.error(f"Validation error: {e}")
```

### 4. Implement Retry Logic for Appropriate Errors
```python
# Retry on: ServerError, NetworkError, RateLimitError
# Don't retry: AuthenticationError, ValidationError, NotFoundError
```

## 🔗 Related Workflows

- **[Authentication](authentication.md)** - Solving authentication errors
- **[Transaction Builder](transaction-builder.md)** - Transaction-specific error handling
- **[Teams](teams.md)** - Team-related error scenarios
- **[Testing](testing.md)** - Testing error scenarios 