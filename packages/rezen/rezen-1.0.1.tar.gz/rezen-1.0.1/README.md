# ReZEN API Python Client

A comprehensive Python wrapper for the ReZEN (Real Estate) API, providing easy access to transaction builder, transactions, teams, and related real estate services.

## 🚀 Quick Start

```python
from rezen import RezenClient

# Initialize client (uses REZEN_API_KEY environment variable)
client = RezenClient()

# Or provide API key directly
client = RezenClient(api_key="your_api_key_here")

# Create a transaction builder
response = client.transaction_builder.create_transaction_builder({
    "type": "PURCHASE",
    "property": {
        "address": "123 Main St",
        "city": "Anytown",
        "state": "CA",
        "zipCode": "12345"
    }
})

# Search for teams
teams = client.teams.search_teams(status="ACTIVE")

# Get transaction details
transaction = client.transactions.get_transaction("transaction-id")
```

## 📦 Installation

```bash
pip install rezen

# Or for development:
git clone <repository-url>
cd rezen
pip install -r requirements-dev.txt
```

## 🔧 Setup

1. **Get your API key** from the ReZEN platform
2. **Set environment variable**:
   ```bash
   export REZEN_API_KEY="your_api_key_here"
   ```
3. **Or create a `.env` file**:
   ```
   REZEN_API_KEY=your_api_key_here
   ```

## 🔄 Main Workflows

### 🏗️ Transaction Builder Workflows
- **Create transactions** from scratch
- **Import existing transactions** 
- **Manage participants** (buyers, sellers, agents)
- **Submit transactions** for processing
- **Update transaction details** and contracts

### 📋 Transaction Management Workflows  
- **Retrieve transaction details** and status
- **Manage participants** and their information
- **Handle financial operations** (payments, fees)
- **Escrow management** (deposits, documentation)
- **Generate reports** and summaries

### 👥 Team Management Workflows
- **Search teams** by name, status, or type
- **Get team details** and member information
- **Filter by team types** (Normal, Platinum, Group, etc.)

### 🧪 Testing & Development Workflows
- **Unit testing** with mocked responses
- **Live API testing** with real endpoints
- **Error handling** and validation
- **Coverage reporting**

## 📖 Detailed Documentation

For comprehensive workflow documentation, see:

- **[Transaction Builder Workflows](docs/workflows/transaction-builder.md)** - Creating and managing transaction builders
- **[Transaction Management Workflows](docs/workflows/transactions.md)** - Working with existing transactions
- **[Team Management Workflows](docs/workflows/teams.md)** - Finding and managing teams
- **[Authentication & Setup](docs/workflows/authentication.md)** - API key setup and configuration
- **[Testing Workflows](docs/workflows/testing.md)** - Development and testing procedures
- **[Error Handling](docs/workflows/error-handling.md)** - Common errors and solutions

## 🏗️ Client Structure

The ReZEN client provides access to different API sections:

```python
client = RezenClient()

# Transaction Builder API (89 endpoints)
client.transaction_builder.create_transaction_builder()
client.transaction_builder.add_buyer()
client.transaction_builder.submit_transaction()

# Transactions API (49 endpoints) 
client.transactions.get_transaction()
client.transactions.create_participant()
client.transactions.get_summary_pdf()

# Teams API (2 endpoints)
client.teams.search_teams()
client.teams.get_team_without_agents()
```

## 🎯 Key Features

- **✅ 140+ endpoints** implemented with full coverage
- **🔒 Type-safe** with comprehensive type hints
- **🧪 100% test coverage** with pytest
- **📝 Complete documentation** with examples
- **🔧 Easy configuration** with environment variables
- **🚨 Robust error handling** with custom exceptions
- **🔄 Async support** planned for future versions

## 🛠️ Development

```bash
# Clone and setup
git clone <repository-url>
cd rezen
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements-dev.txt

# Run tests
pytest

# Run tests with coverage
pytest --cov=rezen --cov-report=html

# Format code
black rezen tests
isort rezen tests

# Type checking
mypy rezen
```

## 📄 API Coverage

| API Section | Endpoints | Status |
|-------------|-----------|--------|
| Transaction Builder | 89 | ✅ Complete |
| Transactions | 49 | ✅ Complete |  
| Teams | 2 | ✅ Complete |
| **Total** | **140** | **✅ Complete** |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure 100% test coverage
5. Submit a pull request

See [STYLE_GUIDE.md](STYLE_GUIDE.md) for coding standards.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 The Perry Group

## 🆘 Support

- **Documentation**: [docs/](docs/)
- **Issues**: [Create an issue](../../issues)
- **API Reference**: [docs/api-reference/](docs/api-reference/) 