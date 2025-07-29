# Transaction Builder Workflows

This guide covers all workflows for creating and managing transaction builders using the ReZEN API.

## 🏗️ Overview

Transaction builders are the primary way to create new transactions in the ReZEN system. They allow you to:
- Create transactions from scratch
- Import from existing transactions
- Add and manage participants (buyers, sellers, agents)
- Update property and contract information
- Submit completed transactions for processing

## 🚀 Quick Start Workflow

```python
from rezen import RezenClient

client = RezenClient()

# 1. Create a transaction builder
response = client.transaction_builder.create_transaction_builder({
    "type": "PURCHASE"
})
builder_id = response.get('message')

# 2. Add property information
client.transaction_builder.update_location_info(builder_id, {
    "address": "123 Main St",
    "city": "Los Angeles", 
    "state": "CA",
    "zipCode": "90210"
})

# 3. Add participants
client.transaction_builder.add_seller(builder_id, {
    "firstName": "John",
    "lastName": "Seller", 
    "email": "john@example.com"
})

client.transaction_builder.add_buyer(builder_id, {
    "firstName": "Jane",
    "lastName": "Buyer",
    "email": "jane@example.com" 
})

# 4. Submit the transaction
result = client.transaction_builder.submit_transaction(builder_id)
```

## 📋 Complete Workflows

### Workflow 1: Create Transaction from Scratch

**Step 1: Initialize Transaction Builder**
```python
# Create new builder
response = client.transaction_builder.create_transaction_builder({
    "type": "PURCHASE"  # or "SALE", "LEASE", etc.
})
builder_id = response.get('message')
```

**Step 2: Add Property Information**
```python
# Required property details
property_info = {
    "address": "123 Main Street",
    "city": "Los Angeles",
    "state": "CA", 
    "zipCode": "90210",
    "county": "Los Angeles County",
    "propertyType": "SINGLE_FAMILY",
    "purchasePrice": 500000
}

client.transaction_builder.update_location_info(builder_id, property_info)
```

**Step 3: Add Title Information**
```python
title_info = {
    "titleCompany": "ABC Title Company",
    "titleOfficer": "John Title Officer",
    "titleCompanyPhone": "555-123-4567",
    "titleCompanyEmail": "title@abctitle.com"
}

client.transaction_builder.update_title_info(builder_id, title_info)
```

**Step 4: Add Participants**

Add Listing Agent:
```python
listing_agent = {
    "firstName": "Sarah",
    "lastName": "Agent",
    "email": "sarah@realty.com",
    "phoneNumber": "555-987-6543",
    "licenseNumber": "12345678",
    "brokerageName": "Best Realty",
    "teamId": "ab45fb68-3f2a-4985-8ec6-73d1b409ea33"  # The Perry Group Standard Team
}

client.transaction_builder.add_listing_agent(builder_id, listing_agent)
```

Add Seller:
```python
seller = {
    "firstName": "John",
    "lastName": "Seller",
    "email": "john.seller@email.com",
    "phoneNumber": "555-111-2222",
    "address": "123 Current Address",
    "city": "Los Angeles", 
    "state": "CA",
    "zipCode": "90210"
}

client.transaction_builder.add_seller(builder_id, seller)
```

Add Buying Agent:
```python
buying_agent = {
    "firstName": "Mike", 
    "lastName": "BuyerAgent",
    "email": "mike@realty.com",
    "phoneNumber": "555-444-5555",
    "licenseNumber": "87654321",
    "brokerageName": "Great Realty"
}

client.transaction_builder.add_buying_agent(builder_id, buying_agent)
```

Add Buyer:
```python
buyer = {
    "firstName": "Jane",
    "lastName": "Buyer", 
    "email": "jane.buyer@email.com",
    "phoneNumber": "555-333-4444",
    "address": "456 Future Address",
    "city": "Los Angeles",
    "state": "CA", 
    "zipCode": "90211"
}

client.transaction_builder.add_buyer(builder_id, buyer)
```

**Step 5: Add Contract Details**
```python
contract_info = {
    "contractDate": "2024-01-15",
    "closingDate": "2024-02-15", 
    "purchasePrice": 500000,
    "earnestMoney": 10000,
    "inspectionPeriod": 10,
    "financingType": "CONVENTIONAL"
}

client.transaction_builder.update_contract_info(builder_id, contract_info)
```

**Step 6: Validate and Submit**
```python
# Optional: Get transaction builder to verify information
builder_details = client.transaction_builder.get_transaction_builder(builder_id)

# Submit the transaction
try:
    result = client.transaction_builder.submit_transaction(builder_id)
    transaction_id = result.get('transactionId')
    print(f"✅ Transaction submitted successfully: {transaction_id}")
except Exception as e:
    print(f"❌ Submission failed: {e}")
```

### Workflow 2: Import from Existing Transaction

```python
# Create builder from existing transaction
existing_transaction_id = "existing-txn-123"

response = client.transaction_builder.create_builder_from_transaction({
    "transactionId": existing_transaction_id,
    "copyType": "FULL"  # or "MINIMAL"
})

builder_id = response.get('message')

# Modify as needed, then submit
client.transaction_builder.submit_transaction(builder_id)
```

### Workflow 3: Managing Multiple Participants

**Add Multiple Buyers**
```python
buyers = [
    {"firstName": "John", "lastName": "Buyer1", "email": "john@email.com"},
    {"firstName": "Jane", "lastName": "Buyer2", "email": "jane@email.com"}
]

for buyer in buyers:
    client.transaction_builder.add_buyer(builder_id, buyer)
```

**Add Co-Agents**
```python
co_agent = {
    "firstName": "Assistant",
    "lastName": "Agent", 
    "email": "assistant@realty.com",
    "role": "CO_LISTING_AGENT"
}

client.transaction_builder.add_co_agent(builder_id, co_agent)
```

**Add Other Participants**
```python
lender = {
    "firstName": "Bank",
    "lastName": "Officer",
    "email": "loan@bank.com", 
    "role": "LENDER",
    "company": "Big Bank Lending"
}

client.transaction_builder.add_other_participant(builder_id, lender)
```

## 🔍 Management Workflows

### Get Transaction Builders
```python
# Get all builders for a user
builders = client.transaction_builder.get_transaction_builders(
    limit=50,
    offset=0, 
    yenta_id="user-id"
)

# Get paginated results
paginated = client.transaction_builder.get_transaction_builders_paged(
    page_number=0,
    page_size=20,
    sort_by="created_date",
    sort_direction="DESC"
)
```

### Update Existing Builder
```python
# Update property information
new_property_info = {
    "purchasePrice": 550000,  # Price increase
    "closingDate": "2024-03-01"  # Date change
}

client.transaction_builder.update_location_info(builder_id, new_property_info)

# Update participant information
updated_buyer = {
    "firstName": "Jane Updated",
    "lastName": "Buyer",
    "email": "jane.updated@email.com"
}

client.transaction_builder.update_buyer(builder_id, buyer_id, updated_buyer)
```

### Delete Participants
```python
# Remove a buyer
client.transaction_builder.delete_buyer(builder_id, buyer_id)

# Remove a seller  
client.transaction_builder.delete_seller(builder_id, seller_id)

# Remove other participant
client.transaction_builder.delete_other_participant(builder_id, participant_id)
```

### Delete Transaction Builder
```python
# Delete the entire transaction builder
client.transaction_builder.delete_transaction_builder(builder_id)
```

## ✅ Best Practices

### 1. Data Validation
- Always validate required fields before submission
- Use proper date formats (YYYY-MM-DD)
- Ensure email addresses are valid
- Verify phone number formats

### 2. Error Handling
```python
from rezen.exceptions import ValidationError, NotFoundError

try:
    result = client.transaction_builder.submit_transaction(builder_id)
except ValidationError as e:
    print(f"Validation failed: {e.response_data}")
    # Fix validation issues and retry
except NotFoundError as e:
    print(f"Builder not found: {builder_id}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 3. Required vs Optional Fields

**Required for Submission:**
- Property address, city, state, zip
- At least one buyer
- At least one seller  
- Purchase price
- Contract date

**Highly Recommended:**
- Listing agent with team assignment
- Buying agent
- Title company information
- Closing date

### 4. Team Assignment
Always assign agents to teams for proper commission tracking:
```python
agent_data = {
    "firstName": "Agent",
    "lastName": "Name",
    "email": "agent@email.com",
    "teamId": "ab45fb68-3f2a-4985-8ec6-73d1b409ea33"  # Your team ID
}
```

## 🚨 Common Issues

### Issue: Submission Fails with Validation Errors
**Solution:** Check that all required fields are populated and in correct format

### Issue: Agent Not Associated with Team
**Solution:** Use the teams API to find the correct team ID and assign it to the agent

### Issue: Duplicate Participants
**Solution:** Use the participant management endpoints to update existing participants instead of adding new ones

### Issue: Permission Denied
**Solution:** Ensure your API key has transaction builder permissions

## 📊 Monitoring Progress

```python
# Check builder status before submission
builder = client.transaction_builder.get_transaction_builder(builder_id)
print(f"Builder status: {builder.get('status')}")
print(f"Required fields complete: {builder.get('validation', {}).get('isComplete')}")

# Get validation details
validation = builder.get('validation', {})
if not validation.get('isComplete'):
    missing_fields = validation.get('missingFields', [])
    print(f"Missing required fields: {missing_fields}")
```

## 🔗 Related Workflows

- **[Transaction Management](transactions.md)** - Working with submitted transactions
- **[Team Management](teams.md)** - Finding and assigning teams
- **[Error Handling](error-handling.md)** - Troubleshooting common issues 