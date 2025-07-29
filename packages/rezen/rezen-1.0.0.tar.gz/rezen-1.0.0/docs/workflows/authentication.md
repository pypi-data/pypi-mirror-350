# Authentication & Setup Workflows

This guide covers setting up authentication and configuring the ReZEN API client.

## 🔑 Overview

The ReZEN API uses API key authentication. You need:
- A valid ReZEN API key
- Proper environment configuration
- Network access to ReZEN endpoints

## 🚀 Quick Setup

```python
from rezen import RezenClient

# Method 1: Environment variable (recommended)
client = RezenClient()

# Method 2: Direct API key
client = RezenClient(api_key="your_api_key_here")

# Method 3: Custom base URL (for testing)
client = RezenClient(
    api_key="your_api_key_here",
    base_url="https://staging.example.com/api/v1"
)
```

## 📋 Setup Workflows

### Workflow 1: Environment Variable Setup

**Step 1: Create .env file**
```bash
# In your project root
echo "REZEN_API_KEY=your_actual_api_key_here" > .env
```

**Step 2: Use in Python**
```python
from rezen import RezenClient
import os

# Option A: Load automatically (recommended)
client = RezenClient()

# Option B: Load manually
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("REZEN_API_KEY")
client = RezenClient(api_key=api_key)
```

### Workflow 2: System Environment Variable

**Linux/macOS:**
```bash
# Set for current session
export REZEN_API_KEY="your_api_key_here"

# Set permanently (add to ~/.bashrc or ~/.zshrc)
echo 'export REZEN_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows:**
```cmd
# Set for current session
set REZEN_API_KEY=your_api_key_here

# Set permanently
setx REZEN_API_KEY "your_api_key_here"
```

**Python usage:**
```python
import os
from rezen import RezenClient

# Verify environment variable is set
api_key = os.getenv("REZEN_API_KEY")
if not api_key:
    raise ValueError("REZEN_API_KEY environment variable not set")

client = RezenClient()  # Will use environment variable
```

### Workflow 3: Configuration File Setup

**config.py:**
```python
import os
from typing import Optional

class RezenConfig:
    """Configuration management for ReZEN API."""
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.base_url = self._get_base_url()
    
    def _get_api_key(self) -> str:
        """Get API key from environment or config."""
        api_key = os.getenv("REZEN_API_KEY")
        if not api_key:
            raise ValueError(
                "REZEN_API_KEY not found. Set environment variable or pass directly."
            )
        return api_key
    
    def _get_base_url(self) -> Optional[str]:
        """Get custom base URL if specified."""
        return os.getenv("REZEN_BASE_URL")  # Optional override

# Usage
config = RezenConfig()
client = RezenClient(api_key=config.api_key, base_url=config.base_url)
```

## 🔧 Validation Workflows

### Workflow 1: Test Authentication

```python
from rezen import RezenClient
from rezen.exceptions import AuthenticationError

def test_authentication():
    """Test if authentication is working."""
    try:
        client = RezenClient()
        
        # Try a simple API call
        teams = client.teams.search_teams(page_size=1)
        print("✅ Authentication successful")
        print(f"   Total teams accessible: {teams.get('totalCount', 0)}")
        return True
        
    except AuthenticationError as e:
        print(f"❌ Authentication failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

# Test authentication
if test_authentication():
    print("🎉 Ready to use ReZEN API!")
else:
    print("🔧 Please check your API key configuration")
```

### Workflow 2: Validate API Key Format

```python
import re

def validate_api_key_format(api_key: str) -> bool:
    """Validate API key format (adjust pattern as needed)."""
    if not api_key:
        return False
    
    # Example pattern - adjust based on actual ReZEN API key format
    pattern = r'^real_v2[A-Za-z0-9]{32,}$'
    return bool(re.match(pattern, api_key))

# Usage
api_key = "real_v2neAIGs2QEYJ14ck8uypMsBqOquT9TgmMzf"
if validate_api_key_format(api_key):
    print("✅ API key format looks valid")
else:
    print("❌ API key format appears invalid")
```

### Workflow 3: Test All Client Features

```python
def comprehensive_auth_test():
    """Test authentication across all client features."""
    client = RezenClient()
    
    tests = [
        ("Teams API", lambda: client.teams.search_teams(page_size=1)),
        ("Transaction Builder API", lambda: client.transaction_builder.get_transaction_builders(1, 0, "test")),
        ("Transactions API", lambda: client.transactions.get_participant_transactions("test-id"))
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            test_func()
            results[test_name] = "✅ Success"
        except AuthenticationError:
            results[test_name] = "❌ Auth Failed"
        except Exception as e:
            results[test_name] = f"⚠️  Other Error: {str(e)[:50]}..."
    
    print("Authentication Test Results:")
    for test_name, result in results.items():
        print(f"  {test_name}: {result}")
    
    return all("Success" in result for result in results.values())
```

## 🏗️ Client Configuration Workflows

### Workflow 1: Multiple Client Instances

```python
# Different environments
production_client = RezenClient(api_key="prod_key")
staging_client = RezenClient(
    api_key="staging_key",
    base_url="https://staging.example.com/api/v1"
)

# Different API keys for different users
user1_client = RezenClient(api_key="user1_api_key")
user2_client = RezenClient(api_key="user2_api_key")
```

### Workflow 2: Client Factory Pattern

```python
from typing import Dict, Optional
from rezen import RezenClient

class RezenClientFactory:
    """Factory for creating configured ReZEN clients."""
    
    _instances: Dict[str, RezenClient] = {}
    
    @classmethod
    def get_client(
        cls, 
        name: str = "default",
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> RezenClient:
        """Get or create a client instance."""
        
        if name not in cls._instances:
            cls._instances[name] = RezenClient(
                api_key=api_key,
                base_url=base_url
            )
        
        return cls._instances[name]
    
    @classmethod
    def clear_instances(cls):
        """Clear all cached instances."""
        cls._instances.clear()

# Usage
client = RezenClientFactory.get_client("production")
test_client = RezenClientFactory.get_client(
    "testing", 
    base_url="https://test.example.com"
)
```

## 🔍 Troubleshooting Workflows

### Workflow 1: Debug Authentication Issues

```python
import os
from rezen import RezenClient

def debug_authentication():
    """Debug common authentication issues."""
    
    print("🔍 Debugging ReZEN Authentication\n")
    
    # Check 1: Environment variable
    api_key_env = os.getenv("REZEN_API_KEY")
    if api_key_env:
        print(f"✅ REZEN_API_KEY found in environment")
        print(f"   Key starts with: {api_key_env[:10]}...")
    else:
        print("❌ REZEN_API_KEY not found in environment")
    
    # Check 2: .env file
    env_file_exists = os.path.exists(".env")
    print(f"📄 .env file exists: {env_file_exists}")
    
    # Check 3: Client creation
    try:
        client = RezenClient()
        print("✅ Client created successfully")
        
        # Check 4: API call
        try:
            response = client.teams.search_teams(page_size=1)
            print("✅ API call successful")
            print(f"   Response keys: {list(response.keys())}")
        except Exception as e:
            print(f"❌ API call failed: {e}")
            
    except Exception as e:
        print(f"❌ Client creation failed: {e}")

# Run debug
debug_authentication()
```

### Workflow 2: Network Connectivity Test

```python
import requests
from urllib.parse import urlparse

def test_network_connectivity():
    """Test network connectivity to ReZEN endpoints."""
    
    endpoints = [
        "https://arrakis.therealbrokerage.com/api/v1",  # Main API
        "https://yenta.therealbrokerage.com/api/v1"     # Teams API
    ]
    
    for endpoint in endpoints:
        try:
            # Parse domain for testing
            domain = urlparse(endpoint).netloc
            
            # Test basic connectivity (without auth)
            response = requests.get(f"https://{domain}", timeout=10)
            print(f"✅ {domain} is reachable (status: {response.status_code})")
            
        except requests.exceptions.Timeout:
            print(f"❌ {domain} - Timeout (network issue)")
        except requests.exceptions.ConnectionError:
            print(f"❌ {domain} - Connection failed (firewall/DNS)")
        except Exception as e:
            print(f"⚠️  {domain} - Other error: {e}")

test_network_connectivity()
```

## 🚨 Common Issues

### Issue 1: "API key is required" Error

**Causes:**
- Environment variable not set
- .env file not loaded
- Wrong variable name

**Solutions:**
```python
# Check current environment
import os
print("Current REZEN_API_KEY:", os.getenv("REZEN_API_KEY"))

# Force load .env file
from dotenv import load_dotenv
load_dotenv(override=True)

# Set manually for testing
os.environ["REZEN_API_KEY"] = "your_key_here"
```

### Issue 2: "Authentication failed" Error

**Causes:**
- Invalid API key
- API key expired
- Wrong API endpoint

**Solutions:**
```python
# Test with explicit API key
client = RezenClient(api_key="your_actual_key")

# Check API key format
api_key = "your_key"
if not api_key.startswith("real_"):
    print("⚠️ API key might be incorrect format")
```

### Issue 3: Network/Connectivity Issues

**Causes:**
- Firewall blocking requests
- VPN issues
- DNS problems

**Solutions:**
```python
# Test with custom timeout
import requests
session = requests.Session()
session.timeout = 30

# Use custom session (advanced)
# Note: ReZEN client doesn't expose session config directly
# Contact support for custom networking needs
```

## ✅ Best Practices

### 1. Secure API Key Storage
```python
# ✅ Good: Environment variables
client = RezenClient()

# ❌ Bad: Hardcoded in source
client = RezenClient(api_key="real_v2hardcodedkey123")
```

### 2. Environment-Specific Configuration
```python
import os

ENV = os.getenv("ENVIRONMENT", "production")

if ENV == "development":
    client = RezenClient(base_url="https://dev.example.com")
elif ENV == "staging":
    client = RezenClient(base_url="https://staging.example.com")
else:
    client = RezenClient()  # Production
```

### 3. Error Handling
```python
from rezen.exceptions import AuthenticationError, NetworkError

try:
    client = RezenClient()
    result = client.teams.search_teams()
except AuthenticationError:
    print("Check your API key")
except NetworkError:
    print("Check your internet connection")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 4. Health Checks
```python
def health_check():
    """Simple health check for monitoring."""
    try:
        client = RezenClient()
        client.teams.search_teams(page_size=1)
        return {"status": "healthy", "api": "accessible"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

## 🔗 Related Workflows

- **[Transaction Builder](transaction-builder.md)** - Using authenticated client for transactions
- **[Teams](teams.md)** - Team search requires authentication
- **[Error Handling](error-handling.md)** - Authentication error troubleshooting
- **[Testing](testing.md)** - Authentication in test environments 