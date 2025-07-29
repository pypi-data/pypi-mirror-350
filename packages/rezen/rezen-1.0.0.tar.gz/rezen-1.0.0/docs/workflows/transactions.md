# Transaction Management Workflows

This guide covers working with submitted transactions using the ReZEN API.

## 📋 Overview

The Transactions API allows you to work with live, submitted transactions including:
- Retrieving transaction details and status
- Managing participants and their information
- Handling financial operations (payments, fees)
- Escrow management (deposits, documentation)
- Generating reports and summaries

## 🚀 Quick Start

```python
from rezen import RezenClient

client = RezenClient()

# Get transaction details
transaction = client.transactions.get_transaction("transaction-id")

# Get participants
participants = client.transactions.get_transaction_participant_lite_info("transaction-id")

# Create new participant
new_participant = client.transactions.create_participant("transaction-id", {
    "firstName": "John",
    "lastName": "Participant",
    "email": "john@example.com",
    "role": "INSPECTOR"
})

# Get summary PDF
summary = client.transactions.get_summary_pdf("transaction-id")
```

## 📋 Core Workflows

### Workflow 1: Transaction Information Retrieval

```python
def get_transaction_overview(transaction_id: str):
    """Get comprehensive transaction overview."""
    client = RezenClient()
    
    try:
        # Basic transaction details
        transaction = client.transactions.get_transaction(transaction_id)
        print(f"Transaction: {transaction.get('id')}")
        print(f"Status: {transaction.get('status')}")
        print(f"Type: {transaction.get('type')}")
        
        # Get participants summary
        participants = client.transactions.get_transaction_participant_lite_info(transaction_id)
        print(f"Participants: {len(participants)}")
        
        # Get transaction features/permissions
        features = client.transactions.get_transaction_features(transaction_id)
        print(f"Available features: {list(features.keys())}")
        
        # Get process information
        process_info = client.transactions.get_transaction_process(transaction_id)
        print(f"Current process stage: {process_info.get('currentStage')}")
        
        return {
            'transaction': transaction,
            'participants': participants,
            'features': features,
            'process': process_info
        }
        
    except Exception as e:
        print(f"Error retrieving transaction overview: {e}")
        return None

# Usage
overview = get_transaction_overview("your-transaction-id")
```

### Workflow 2: Participant Management

```python
def manage_transaction_participants(transaction_id: str):
    """Comprehensive participant management."""
    client = RezenClient()
    
    # Get existing participants
    participants = client.transactions.get_transaction_participant_lite_info(transaction_id)
    print(f"Current participants: {len(participants)}")
    
    for participant in participants:
        print(f"  - {participant.get('firstName')} {participant.get('lastName')} ({participant.get('role')})")
    
    # Add new participant (e.g., inspector)
    inspector_data = {
        "firstName": "John",
        "lastName": "Inspector", 
        "email": "john.inspector@example.com",
        "phoneNumber": "555-123-4567",
        "role": "INSPECTOR",
        "company": "Inspection Services LLC"
    }
    
    try:
        new_participant = client.transactions.create_participant(transaction_id, inspector_data)
        participant_id = new_participant.get('id')
        print(f"✅ Added inspector: {participant_id}")
        
        # Update participant information
        updated_info = {
            "email": "john.inspector.updated@example.com",
            "phoneNumber": "555-987-6543"
        }
        
        client.transactions.update_participant(transaction_id, participant_id, updated_info)
        print(f"✅ Updated participant information")
        
        # Get detailed participant info
        detailed_info = client.transactions.get_participant_info(transaction_id, participant_id)
        print(f"Participant details: {detailed_info.get('firstName')} {detailed_info.get('lastName')}")
        
    except Exception as e:
        print(f"❌ Error managing participants: {e}")

# Usage
manage_transaction_participants("your-transaction-id")
```

### Workflow 3: Financial Operations

```python
def handle_transaction_finances(transaction_id: str, agent_id: str):
    """Handle financial operations for a transaction."""
    client = RezenClient()
    
    try:
        # Get payment information for agent
        payment_info = client.transactions.get_payment_info(transaction_id, agent_id)
        print(f"Payment info: {payment_info}")
        
        # Get money transfers
        transfers = client.transactions.get_money_transfers(transaction_id)
        print(f"Money transfers: {len(transfers)}")
        
        # Get attached fees
        fees = client.transactions.get_attached_fees(transaction_id)
        print(f"Attached fees: {len(fees)}")
        
        # Get paid at closing information
        paid_at_closing = client.transactions.get_paid_at_closing(transaction_id)
        print(f"Paid at closing items: {len(paid_at_closing)}")
        
        # Update payment information
        updated_payment = {
            "commissionPercentage": 3.0,
            "commissionAmount": 15000,
            "paymentMethod": "DIRECT_DEPOSIT"
        }
        
        client.transactions.update_payment_info(transaction_id, agent_id, updated_payment)
        print("✅ Updated payment information")
        
        return {
            'payment_info': payment_info,
            'transfers': transfers,
            'fees': fees,
            'paid_at_closing': paid_at_closing
        }
        
    except Exception as e:
        print(f"❌ Error handling finances: {e}")
        return None

# Usage
finances = handle_transaction_finances("transaction-id", "agent-id")
```

### Workflow 4: Escrow Management

```python
def manage_escrow_operations(transaction_id: str):
    """Manage escrow-related operations."""
    client = RezenClient()
    
    try:
        # Create escrow account
        escrow_data = {
            "escrowCompany": "Secure Escrow LLC",
            "escrowOfficer": "Jane Escrow",
            "escrowPhone": "555-ESCROW",
            "escrowEmail": "jane@secureescrow.com",
            "escrowNumber": "ESC-12345"
        }
        
        escrow_result = client.transactions.create_escrow(transaction_id, escrow_data)
        print(f"✅ Created escrow: {escrow_result}")
        
        # Create deposit
        deposit_data = {
            "amount": 10000,
            "depositType": "EARNEST_MONEY",
            "depositDate": "2024-01-15",
            "description": "Initial earnest money deposit"
        }
        
        deposit_result = client.transactions.create_escrow_deposits(transaction_id, deposit_data)
        print(f"✅ Created deposit: {deposit_result}")
        
        # Get check deposits with upload URLs
        check_deposits = client.transactions.get_check_deposits_with_upload_urls(transaction_id)
        print(f"Check deposits available: {len(check_deposits)}")
        
        # Get download URLs for existing deposits
        download_urls = client.transactions.get_check_deposits_with_download_urls(transaction_id)
        print(f"Download URLs available: {len(download_urls)}")
        
        return {
            'escrow': escrow_result,
            'deposit': deposit_result,
            'check_deposits': check_deposits,
            'download_urls': download_urls
        }
        
    except Exception as e:
        print(f"❌ Error managing escrow: {e}")
        return None

# Usage
escrow_info = manage_escrow_operations("transaction-id")
```

### Workflow 5: Banking Operations

```python
def manage_banking_operations(transaction_id: str):
    """Manage banking operations for transaction."""
    client = RezenClient()
    
    try:
        # Create US bank account
        us_bank_data = {
            "bankName": "First National Bank",
            "accountType": "CHECKING",
            "routingNumber": "123456789",
            "accountNumber": "987654321",
            "accountHolderName": "John Account Holder"
        }
        
        us_bank = client.transactions.create_bank_account_us(transaction_id, us_bank_data)
        print(f"✅ Created US bank account: {us_bank}")
        
        # Create Canadian bank account (if applicable)
        canada_bank_data = {
            "bankName": "Royal Bank of Canada",
            "branchNumber": "12345",
            "institutionNumber": "003",
            "accountNumber": "1234567890",
            "accountHolderName": "John Canadian Account"
        }
        
        try:
            canada_bank = client.transactions.create_bank_account_canada(transaction_id, canada_bank_data)
            print(f"✅ Created Canadian bank account: {canada_bank}")
        except Exception as e:
            print(f"⚠️  Canadian bank account not applicable: {e}")
        
        return {
            'us_bank': us_bank,
            'canada_bank': canada_bank if 'canada_bank' in locals() else None
        }
        
    except Exception as e:
        print(f"❌ Error managing banking: {e}")
        return None

# Usage
banking_info = manage_banking_operations("transaction-id")
```

## 🔍 Advanced Workflows

### Workflow 1: Batch Transaction Processing

```python
def process_multiple_transactions(transaction_ids: list):
    """Process multiple transactions efficiently."""
    client = RezenClient()
    
    # Use batch endpoint for lite information
    try:
        batch_results = client.transactions.get_transactions_lite_batch_get({
            "transactionIds": transaction_ids
        })
        
        print(f"Batch processing {len(transaction_ids)} transactions")
        
        results = []
        for transaction_data in batch_results:
            transaction_id = transaction_data.get('id')
            
            try:
                # Get additional details for each transaction
                detailed_info = {
                    'basic_info': transaction_data,
                    'participants': client.transactions.get_transaction_participant_lite_info(transaction_id),
                    'features': client.transactions.get_transaction_features(transaction_id)
                }
                
                results.append(detailed_info)
                print(f"✅ Processed transaction: {transaction_id}")
                
            except Exception as e:
                print(f"❌ Error processing {transaction_id}: {e}")
                results.append({'id': transaction_id, 'error': str(e)})
        
        return results
        
    except Exception as e:
        print(f"❌ Batch processing failed: {e}")
        return []

# Usage
transaction_ids = ["txn-1", "txn-2", "txn-3"]
batch_results = process_multiple_transactions(transaction_ids)
```

### Workflow 2: Rolling Transaction Analysis

```python
def analyze_rolling_transactions():
    """Analyze transactions with rolling pagination."""
    client = RezenClient()
    
    all_transactions = []
    page = 0
    page_size = 100
    
    try:
        while True:
            # Get rolling transactions with pagination
            response = client.transactions.get_rolling_transactions(
                page=page,
                size=page_size,
                sort_by="createdDate",
                sort_direction="DESC"
            )
            
            transactions = response.get('content', [])
            if not transactions:
                break
            
            all_transactions.extend(transactions)
            print(f"Retrieved page {page + 1}: {len(transactions)} transactions")
            
            # Analysis for this page
            page_stats = {
                'total_count': len(transactions),
                'by_status': {},
                'by_type': {}
            }
            
            for txn in transactions:
                status = txn.get('status', 'UNKNOWN')
                txn_type = txn.get('type', 'UNKNOWN')
                
                page_stats['by_status'][status] = page_stats['by_status'].get(status, 0) + 1
                page_stats['by_type'][txn_type] = page_stats['by_type'].get(txn_type, 0) + 1
            
            print(f"  Status breakdown: {page_stats['by_status']}")
            print(f"  Type breakdown: {page_stats['by_type']}")
            
            # Check if we have more pages
            if not response.get('hasNext', False):
                break
            
            page += 1
        
        print(f"\n📊 Total transactions analyzed: {len(all_transactions)}")
        return all_transactions
        
    except Exception as e:
        print(f"❌ Error analyzing rolling transactions: {e}")
        return []

# Usage
analysis_results = analyze_rolling_transactions()
```

### Workflow 3: Participant Transaction Insights

```python
def get_participant_insights(agent_id: str):
    """Get insights about participant's transactions."""
    client = RezenClient()
    
    try:
        # Get participant transactions by lifecycle group
        lifecycle_groups = ['PENDING', 'ACTIVE', 'CLOSING', 'CLOSED']
        insights = {}
        
        for group in lifecycle_groups:
            try:
                transactions = client.transactions.get_participant_transactions_by_lifecycle_group(
                    agent_id, group
                )
                insights[group] = {
                    'count': len(transactions),
                    'transactions': transactions
                }
                print(f"{group}: {len(transactions)} transactions")
            except Exception as e:
                print(f"⚠️  Could not get {group} transactions: {e}")
                insights[group] = {'count': 0, 'transactions': []}
        
        # Get current transactions count
        current_count = client.transactions.get_participant_transactions_count(agent_id)
        insights['current_count'] = current_count
        print(f"Current active transactions: {current_count}")
        
        # Get current transactions list
        current_transactions = client.transactions.get_participant_current_transactions(agent_id)
        insights['current_transactions'] = current_transactions
        print(f"Current transaction details: {len(current_transactions)}")
        
        # Get transaction listings
        listings = client.transactions.get_participant_transactions_listings(agent_id)
        insights['listings'] = listings
        print(f"Participant listings: {len(listings)}")
        
        return insights
        
    except Exception as e:
        print(f"❌ Error getting participant insights: {e}")
        return {}

# Usage
agent_insights = get_participant_insights("agent-id")
```

## 📊 Reporting Workflows

### Workflow 1: Transaction Summary Generation

```python
def generate_transaction_summary(transaction_id: str):
    """Generate comprehensive transaction summary."""
    client = RezenClient()
    
    try:
        # Get summary PDF
        summary_pdf = client.transactions.get_summary_pdf(transaction_id)
        
        # Get transaction explanation
        explanation = client.transactions.explain_transaction(transaction_id)
        
        # Basic transaction info
        transaction = client.transactions.get_transaction(transaction_id)
        participants = client.transactions.get_transaction_participant_lite_info(transaction_id)
        
        summary_data = {
            'transaction_id': transaction_id,
            'status': transaction.get('status'),
            'type': transaction.get('type'),
            'participant_count': len(participants),
            'summary_pdf': summary_pdf,
            'explanation': explanation,
            'generated_at': datetime.utcnow().isoformat()
        }
        
        print(f"📋 Transaction Summary Generated")
        print(f"   ID: {transaction_id}")
        print(f"   Status: {summary_data['status']}")
        print(f"   Type: {summary_data['type']}")
        print(f"   Participants: {summary_data['participant_count']}")
        
        return summary_data
        
    except Exception as e:
        print(f"❌ Error generating summary: {e}")
        return None

# Usage
summary = generate_transaction_summary("transaction-id")
```

### Workflow 2: Title Operations

```python
def handle_title_operations(transaction_id: str):
    """Handle title-related operations."""
    client = RezenClient()
    
    try:
        # Update title information
        title_data = {
            "titleCompany": "Premier Title Services",
            "titleOfficer": "Sarah Title",
            "titlePhone": "555-TITLE-1",
            "titleEmail": "sarah@premiertitle.com",
            "policyNumber": "POL-789456"
        }
        
        client.transactions.update_transaction_title(transaction_id, title_data)
        print("✅ Updated title information")
        
        # Update title system user
        system_user_data = {
            "systemUserId": "user-12345",
            "accessLevel": "FULL"
        }
        
        client.transactions.update_title_system_user(transaction_id, system_user_data)
        print("✅ Updated title system user")
        
        # Update title order
        order_data = {
            "orderNumber": "ORDER-98765",
            "orderDate": "2024-01-15",
            "orderStatus": "PENDING"
        }
        
        client.transactions.update_title_order(transaction_id, order_data)
        print("✅ Updated title order")
        
        # Check title placement eligibility
        eligibility = client.transactions.get_title_placement_eligibility(transaction_id)
        print(f"Title placement eligible: {eligibility.get('eligible', False)}")
        
        return {
            'title_updated': True,
            'system_user_updated': True,
            'order_updated': True,
            'placement_eligibility': eligibility
        }
        
    except Exception as e:
        print(f"❌ Error handling title operations: {e}")
        return None

# Usage
title_info = handle_title_operations("transaction-id")
```

## ✅ Best Practices

### 1. Error Handling for Live Transactions
```python
from rezen.exceptions import NotFoundError, ValidationError

def safe_transaction_operation(transaction_id, operation_func):
    try:
        return operation_func(transaction_id)
    except NotFoundError:
        print(f"Transaction {transaction_id} not found or no access")
        return None
    except ValidationError as e:
        print(f"Validation error: {e.response_data}")
        return None
```

### 2. Participant Management Best Practices
```python
# Always check existing participants before adding new ones
def add_participant_safely(transaction_id, participant_data):
    client = RezenClient()
    
    # Check existing participants
    existing = client.transactions.get_transaction_participant_lite_info(transaction_id)
    
    # Check for duplicates by email
    existing_emails = [p.get('email') for p in existing]
    if participant_data.get('email') in existing_emails:
        print("⚠️  Participant with this email already exists")
        return None
    
    return client.transactions.create_participant(transaction_id, participant_data)
```

### 3. Financial Data Validation
```python
def validate_payment_data(payment_data):
    """Validate payment data before updating."""
    required_fields = ['commissionPercentage', 'commissionAmount']
    
    for field in required_fields:
        if field not in payment_data:
            raise ValueError(f"Missing required field: {field}")
    
    # Validate percentage
    if not 0 <= payment_data['commissionPercentage'] <= 100:
        raise ValueError("Commission percentage must be between 0 and 100")
    
    return True
```

### 4. Batch Operations Efficiency
```python
# Use batch endpoints when possible
def get_multiple_transaction_info(transaction_ids):
    client = RezenClient()
    
    # Prefer batch endpoint over individual calls
    return client.transactions.get_transactions_lite_batch_get({
        "transactionIds": transaction_ids
    })
```

## 🚨 Common Issues

### Issue: Transaction Not Found
**Solution:** Verify transaction ID and user permissions
```python
try:
    transaction = client.transactions.get_transaction(transaction_id)
except NotFoundError:
    print("Check transaction ID and user access permissions")
```

### Issue: Participant Update Failures
**Solution:** Validate participant data and check constraints
```python
# Ensure participant exists before updating
participants = client.transactions.get_transaction_participant_lite_info(transaction_id)
participant_ids = [p.get('id') for p in participants]

if participant_id not in participant_ids:
    print("Participant not found in transaction")
```

### Issue: Payment Information Inconsistencies
**Solution:** Always validate financial calculations
```python
# Cross-check commission calculations
if payment_data['commissionAmount'] != (purchase_price * payment_data['commissionPercentage'] / 100):
    print("⚠️  Commission amount doesn't match percentage calculation")
```

## 🔗 Related Workflows

- **[Transaction Builder](transaction-builder.md)** - Creating transactions that become live transactions
- **[Teams](teams.md)** - Finding teams for transaction participants
- **[Error Handling](error-handling.md)** - Handling transaction-specific errors
- **[Authentication](authentication.md)** - Setting up access to transaction data 