# Agent Management Workflows

This guide covers finding and managing agents using the ReZEN Agents API.

## 🤝 Overview

The Agents API allows you to:
- Search for agents by name, email, or location
- Get detailed agent information and profiles
- Access agent network hierarchies (sponsor trees, downlines)
- Manage agent financial information and tax forms
- Work with agent plans and commission structures
- Integrate agents with transaction workflows

## 🚀 Quick Start

```python
from rezen import RezenClient, AgentStatus, Country, StateOrProvince

client = RezenClient()

# Search for active agents
agents = client.agents.search_active_agents(name="Perry")

# Get agent by email
agent = client.agents.get_agents_by_email("michael@theperry.group")

# Get current user info
me = client.agents.get_me()

# Get agent's network info
agent_id = "bd465129-b224-43e3-b92f-524ea5f53783"
network = client.agents.get_front_line_agents_info(agent_id)
```

## 🔍 Agent Discovery Workflows

### Workflow 1: Find Agent by Email

```python
# Search for agent by exact email address
def find_agent_by_email(email_address):
    """Find agent by their email address."""
    try:
        agents = client.agents.get_agents_by_email(email_address)
        
        if agents and len(agents) > 0:
            agent = agents[0]
            return {
                'id': agent.get('id'),
                'name': f"{agent.get('firstName', '')} {agent.get('lastName', '')}",
                'email': agent.get('emailAddress'),
                'status': agent.get('status'),
                'phone': agent.get('phoneNumber')
            }
        return None
        
    except Exception as e:
        print(f"Error finding agent: {e}")
        return None

# Usage
agent_info = find_agent_by_email("michael@theperry.group")
if agent_info:
    print(f"✅ Found: {agent_info['name']} (ID: {agent_info['id']})")
```

### Workflow 2: Search Agents by Name

```python
from rezen.agents import AgentSortField, AgentSortDirection

def search_agents_by_name(name, limit=10):
    """Search for agents by name with sorting."""
    try:
        response = client.agents.search_active_agents(
            name=name,
            page_size=limit,
            sort_by=[AgentSortField.FIRST_NAME, AgentSortField.LAST_NAME],
            sort_direction=AgentSortDirection.ASC
        )
        
        agents = response.get('results', [])
        total_count = response.get('totalCount', 0)
        
        print(f"Found {total_count} agents matching '{name}'")
        
        agent_list = []
        for agent in agents:
            agent_info = {
                'id': agent.get('id'),
                'name': f"{agent.get('firstName', '')} {agent.get('lastName', '')}",
                'email': agent.get('emailAddress'),
                'state': agent.get('administrativeAreas', [{}])[0].get('stateOrProvince'),
                'status': agent.get('status')
            }
            agent_list.append(agent_info)
            
        return agent_list
        
    except Exception as e:
        print(f"Error searching agents: {e}")
        return []

# Usage
perry_agents = search_agents_by_name("Perry", limit=5)
for agent in perry_agents:
    print(f"  - {agent['name']} ({agent['state']}) - {agent['email']}")
```

### Workflow 3: Search Agents by Location

```python
from rezen.agents import Country, StateOrProvince

def find_agents_by_location(state=None, country=None, limit=20):
    """Find agents by geographic location."""
    try:
        search_params = {
            'page_size': limit,
            'sort_by': [AgentSortField.LAST_NAME, AgentSortField.FIRST_NAME],
            'sort_direction': AgentSortDirection.ASC
        }
        
        if country:
            search_params['country'] = [country]
        
        if state:
            search_params['state_or_province'] = [state]
        
        response = client.agents.search_active_agents(**search_params)
        
        agents = response.get('results', [])
        print(f"Found {len(agents)} agents in specified location")
        
        return agents
        
    except Exception as e:
        print(f"Error searching by location: {e}")
        return []

# Usage - Find agents in Utah
utah_agents = find_agents_by_location(
    state=StateOrProvince.UTAH,
    country=Country.UNITED_STATES,
    limit=10
)

for agent in utah_agents:
    print(f"Utah Agent: {agent.get('firstName')} {agent.get('lastName')}")
```

### Workflow 4: Get Multiple Agents by IDs

```python
def get_agents_bulk(agent_ids):
    """Get multiple agents by their IDs (max 20)."""
    if len(agent_ids) > 20:
        print("⚠️  Maximum 20 agent IDs allowed per request")
        agent_ids = agent_ids[:20]
    
    try:
        response = client.agents.get_agents_by_ids(agent_ids)
        agents = response.get('agents', [])
        
        agent_details = {}
        for agent in agents:
            agent_id = agent.get('id')
            agent_details[agent_id] = {
                'name': f"{agent.get('firstName', '')} {agent.get('lastName', '')}",
                'email': agent.get('emailAddress'),
                'status': agent.get('status'),
                'phone': agent.get('phoneNumber')
            }
        
        return agent_details
        
    except Exception as e:
        print(f"Error getting agents by IDs: {e}")
        return {}

# Usage
agent_ids = [
    "bd465129-b224-43e3-b92f-524ea5f53783",  # Michael Perry
    "be696b5d-6845-41f5-8440-8d8bef15f361"   # Jack Perry
]

agents_info = get_agents_bulk(agent_ids)
for agent_id, info in agents_info.items():
    print(f"{info['name']}: {info['email']}")
```

## 🏗️ Agent Network Workflows

### Workflow 1: Analyze Agent's Network Hierarchy

```python
def analyze_agent_network(agent_id):
    """Get comprehensive network information for an agent."""
    network_info = {}
    
    try:
        # Get front-line agents (direct recruits)
        front_line = client.agents.get_front_line_agents_info(agent_id)
        network_info['front_line_agents'] = front_line.get('frontLineAgentInfos', [])
        
        # Get network size by tier
        network_sizes = client.agents.get_network_size_by_tier(agent_id)
        network_info['network_sizes'] = network_sizes
        
        # Get sponsor tree (upline)
        sponsor_tree = client.agents.get_sponsor_tree(agent_id)
        network_info['sponsor_tree'] = sponsor_tree
        
        return network_info
        
    except Exception as e:
        print(f"Error analyzing network for {agent_id}: {e}")
        return {}

def display_network_summary(agent_id, agent_name=None):
    """Display a summary of agent's network."""
    network = analyze_agent_network(agent_id)
    
    if not network:
        print(f"❌ Could not retrieve network info for {agent_name or agent_id}")
        return
    
    print(f"\n🌟 Network Summary for {agent_name or agent_id}")
    print("=" * 50)
    
    # Front-line agents summary
    front_line = network.get('front_line_agents', [])
    if front_line:
        print(f"👥 Direct Team: {len(front_line)} agents")
        
        # Active vs inactive
        active_count = sum(1 for agent in front_line if agent.get('status') == 'ACTIVE')
        inactive_count = len(front_line) - active_count
        print(f"   ✅ Active: {active_count}")
        print(f"   ❌ Inactive: {inactive_count}")
        
        # Total network size from front-line
        total_network = sum(agent.get('sizeOfNetwork', 0) for agent in front_line)
        print(f"   🌐 Total Network: {total_network} agents")
        
        # Top performers
        top_performers = sorted(front_line, 
                              key=lambda x: x.get('sizeOfNetwork', 0), 
                              reverse=True)[:3]
        
        print(f"\n   🏆 Top Network Builders:")
        for i, agent in enumerate(top_performers, 1):
            name = f"{agent.get('firstName', '')} {agent.get('lastName', '')}"
            network_size = agent.get('sizeOfNetwork', 0)
            print(f"      {i}. {name}: {network_size} agents")

# Usage
michael_perry_id = "bd465129-b224-43e3-b92f-524ea5f53783"
display_network_summary(michael_perry_id, "Michael Perry")
```

### Workflow 2: Get Downline Agents by Tier

```python
from datetime import date, timedelta

def get_downline_by_tier(agent_id, tier, include_recent_only=False):
    """Get agents in specific tier of network."""
    search_params = {
        'tier': tier,
        'page_size': 50,
        'status_in': [AgentStatus.ACTIVE]  # Only active agents
    }
    
    # Optional: Only agents updated in last 30 days
    if include_recent_only:
        thirty_days_ago = date.today() - timedelta(days=30)
        search_params['updated_at_from'] = thirty_days_ago
    
    try:
        response = client.agents.get_down_line_agents(agent_id, **search_params)
        
        agents = response.get('agents', [])
        total_count = response.get('totalCount', 0)
        
        print(f"Tier {tier} Network: {total_count} agents")
        
        return {
            'tier': tier,
            'total_count': total_count,
            'agents': agents,
            'has_more': response.get('hasNext', False)
        }
        
    except Exception as e:
        print(f"Error getting tier {tier} agents: {e}")
        return None

# Usage - Get multiple tiers
def analyze_network_tiers(agent_id, max_tier=3):
    """Analyze multiple tiers of agent's network."""
    print(f"🔍 Analyzing network tiers for agent {agent_id}")
    
    tier_data = {}
    for tier in range(1, max_tier + 1):
        tier_info = get_downline_by_tier(agent_id, tier)
        if tier_info:
            tier_data[tier] = tier_info
    
    # Summary
    total_network = sum(data['total_count'] for data in tier_data.values())
    print(f"\n📊 Network Summary:")
    print(f"   Total Network Size: {total_network} agents")
    
    for tier, data in tier_data.items():
        print(f"   Tier {tier}: {data['total_count']} agents")
    
    return tier_data

# Usage
michael_perry_id = "bd465129-b224-43e3-b92f-524ea5f53783"
network_analysis = analyze_network_tiers(michael_perry_id, max_tier=3)
```

## 💼 Agent Financial Information

### Workflow 1: Get Agent Payment Information

```python
def get_agent_payment_info(agent_id):
    """Get agent's payment and financial information."""
    payment_info = {}
    
    try:
        # Get payment details (if accessible)
        try:
            payment_details = client.agents.get_payment_details(agent_id)
            payment_info['payment_details'] = payment_details
        except Exception:
            payment_info['payment_details'] = "Access restricted"
        
        # Get masked payment methods
        try:
            masked_methods = client.agents.get_masked_payment_methods(agent_id)
            payment_info['payment_methods'] = masked_methods
        except Exception:
            payment_info['payment_methods'] = "Access restricted"
        
        # Get payment settings history
        try:
            settings_history = client.agents.search_payment_settings(
                agent_id, 
                page_size=10
            )
            payment_info['settings_history'] = settings_history
        except Exception:
            payment_info['settings_history'] = "Access restricted"
        
        return payment_info
        
    except Exception as e:
        print(f"Error getting payment info: {e}")
        return {}

# Usage
agent_id = "bd465129-b224-43e3-b92f-524ea5f53783"
payment_info = get_agent_payment_info(agent_id)

for info_type, data in payment_info.items():
    if data == "Access restricted":
        print(f"⚠️  {info_type}: Access restricted (privacy protection)")
    else:
        print(f"✅ {info_type}: Available")
```

### Workflow 2: Get Agent Tax Information

```python
def get_agent_tax_info(agent_id):
    """Get agent's tax form information."""
    tax_info = {}
    
    try:
        # Get tax forms summary
        try:
            tax_summary = client.agents.get_tax_forms_summary(agent_id)
            tax_info['summary'] = tax_summary
        except Exception:
            tax_info['summary'] = "Access restricted"
        
        # Get masked tax forms
        try:
            masked_forms = client.agents.get_masked_tax_forms_lite(agent_id)
            tax_info['masked_forms'] = masked_forms
        except Exception:
            tax_info['masked_forms'] = "Access restricted"
        
        # Get latest personal tax form
        try:
            latest_form = client.agents.get_latest_personal_tax_form_lite(agent_id)
            tax_info['latest_personal'] = latest_form
        except Exception:
            tax_info['latest_personal'] = "Access restricted"
        
        return tax_info
        
    except Exception as e:
        print(f"Error getting tax info: {e}")
        return {}

# Usage
tax_info = get_agent_tax_info(agent_id)
print("📄 Tax Information Access:")
for info_type, data in tax_info.items():
    status = "✅ Available" if data != "Access restricted" else "⚠️  Restricted"
    print(f"   {info_type}: {status}")
```

## 📋 Agent Plans & Commission Workflows

### Workflow 1: Get Commission Plan Information

```python
def get_commission_plans():
    """Get available commission plan information."""
    plans_info = {}
    
    try:
        # Get official commission plan
        official_plan = client.agents.get_official_commission_plan()
        plans_info['official'] = official_plan
        
        # Get commission plan basic info
        basic_info = client.agents.get_commission_plan_basic_info()
        plans_info['basic_info'] = basic_info
        
        return plans_info
        
    except Exception as e:
        print(f"Error getting commission plans: {e}")
        return {}

def display_commission_info():
    """Display commission plan information."""
    plans = get_commission_plans()
    
    if plans:
        print("💰 Commission Plan Information:")
        
        if 'official' in plans:
            print("   ✅ Official commission plan available")
        
        if 'basic_info' in plans:
            basic = plans['basic_info']
            print(f"   📊 Basic Info: {len(basic)} plan details")
    else:
        print("❌ No commission plan information available")

# Usage
display_commission_info()
```

### Workflow 2: Get Specific Agent Plans

```python
def get_agent_plan_details(plan_id, plan_type):
    """Get specific plan details by ID and type."""
    try:
        if plan_type == "revenue_share":
            return client.agents.get_revenue_share_plan(plan_id)
        elif plan_type == "equity_purchase":
            return client.agents.get_equity_purchase_plan(plan_id)
        elif plan_type == "equity_award":
            return client.agents.get_equity_award_plan(plan_id)
        elif plan_type == "elite_equity_award":
            return client.agents.get_elite_equity_award_plan(plan_id)
        elif plan_type == "commission":
            return client.agents.get_commission_plan(plan_id)
        else:
            print(f"Unknown plan type: {plan_type}")
            return None
            
    except Exception as e:
        print(f"Error getting {plan_type} plan {plan_id}: {e}")
        return None

# Usage (requires valid plan IDs)
# plan_details = get_agent_plan_details("plan-uuid", "revenue_share")
```

## 🛠️ Utility Workflows

### Workflow 1: Agent Profile Validation

```python
def validate_agent_profile(agent_id):
    """Validate agent profile completeness."""
    validation_results = {}
    
    try:
        # Get profile score
        profile_score = client.agents.get_profile_score(agent_id)
        validation_results['profile_score'] = profile_score
        
        # Check if slug is being used
        # Note: We'd need the agent's slug to check availability
        
        return validation_results
        
    except Exception as e:
        print(f"Error validating profile: {e}")
        return {}

def check_slug_availability(slug):
    """Check if a slug is available for use."""
    try:
        result = client.agents.is_slug_available(slug)
        is_available = result.get('available', False)
        
        if is_available:
            print(f"✅ Slug '{slug}' is available")
        else:
            print(f"❌ Slug '{slug}' is not available")
        
        return is_available
        
    except Exception as e:
        print(f"Error checking slug: {e}")
        return False

# Usage
check_slug_availability("test-agent-slug")
```

### Workflow 2: Get Agent License Information

```python
def get_agent_license_info(license_id):
    """Get agent license images and information."""
    try:
        license_images = client.agents.get_license_images(license_id)
        
        print(f"📄 License Information:")
        print(f"   License ID: {license_id}")
        
        if license_images:
            images = license_images.get('images', [])
            print(f"   📸 Images: {len(images)} available")
            
            for i, image in enumerate(images):
                print(f"      {i+1}. {image.get('filename', 'Unknown')}")
        
        return license_images
        
    except Exception as e:
        print(f"Error getting license info: {e}")
        return None

# Usage (requires valid license ID)
# license_info = get_agent_license_info("license-uuid")
```

### Workflow 3: Get Service Integration Information

```python
def get_service_integrations():
    """Get information about external service integrations."""
    integrations = {}
    
    try:
        # Get Tipalti URL for payment processing
        tipalti_info = client.agents.get_tipalti_url()
        integrations['tipalti'] = tipalti_info
        
        # Get OpCity information
        opcity_info = client.agents.get_opcity_info()
        integrations['opcity'] = opcity_info
        
        return integrations
        
    except Exception as e:
        print(f"Error getting service integrations: {e}")
        return {}

def display_service_integrations():
    """Display available service integrations."""
    integrations = get_service_integrations()
    
    print("🔗 Service Integrations:")
    
    if 'tipalti' in integrations:
        tipalti = integrations['tipalti']
        tipalti_url = tipalti.get('url', 'Not available')
        print(f"   💳 Tipalti Payment: {tipalti_url}")
    
    if 'opcity' in integrations:
        print(f"   🏠 OpCity: Integration available")

# Usage
display_service_integrations()
```

## 🔗 Integration with Transaction Workflows

### Find Agent for Transaction Assignment

```python
def find_agent_for_transaction(agent_identifier):
    """Find agent for assignment to transaction."""
    agent_info = None
    
    # Try email first
    if '@' in agent_identifier:
        agents = client.agents.get_agents_by_email(agent_identifier)
        if agents and len(agents) > 0:
            agent_info = agents[0]
    
    # Try name search
    if not agent_info:
        search_result = client.agents.search_active_agents(
            name=agent_identifier,
            page_size=5
        )
        
        agents = search_result.get('results', [])
        if agents:
            # Look for exact name match
            for agent in agents:
                full_name = f"{agent.get('firstName', '')} {agent.get('lastName', '')}"
                if agent_identifier.lower() in full_name.lower():
                    agent_info = agent
                    break
            
            # Use first result if no exact match
            if not agent_info:
                agent_info = agents[0]
    
    if agent_info:
        return {
            'id': agent_info.get('id'),
            'firstName': agent_info.get('firstName'),
            'lastName': agent_info.get('lastName'),
            'email': agent_info.get('emailAddress'),
            'phone': agent_info.get('phoneNumber'),
            'status': agent_info.get('status')
        }
    
    return None

# Usage in transaction context
def assign_agent_to_transaction(transaction_builder, agent_identifier, role="LISTING_AGENT"):
    """Assign agent to transaction using various identifier types."""
    
    agent = find_agent_for_transaction(agent_identifier)
    
    if not agent:
        print(f"❌ Could not find agent: {agent_identifier}")
        return False
    
    if agent['status'] != 'ACTIVE':
        print(f"⚠️  Agent {agent['firstName']} {agent['lastName']} is {agent['status']}")
        return False
    
    # Add to transaction builder
    agent_data = {
        "firstName": agent['firstName'],
        "lastName": agent['lastName'],
        "email": agent['email'],
        "phoneNumber": agent['phone'],
        "role": role
    }
    
    # Use appropriate transaction builder method
    # transaction_builder.add_listing_agent(agent_data)
    print(f"✅ Agent assigned: {agent['firstName']} {agent['lastName']} as {role}")
    return True

# Usage
# assign_agent_to_transaction(builder, "michael@theperry.group", "LISTING_AGENT")
# assign_agent_to_transaction(builder, "Michael Perry", "BUYER_AGENT")
```

## 📋 Enumeration Reference

### Agent Status Options
```python
from rezen.agents import AgentStatus

AgentStatus.CANDIDATE     # Candidate agents
AgentStatus.ACTIVE        # Active agents
AgentStatus.INACTIVE      # Inactive agents
AgentStatus.REJECTED      # Rejected applications
AgentStatus.RESURRECTING  # Reactivating agents
```

### Sort Direction Options
```python
from rezen.agents import AgentSortDirection

AgentSortDirection.ASC    # Ascending order
AgentSortDirection.DESC   # Descending order
```

### Sort Field Options
```python
from rezen.agents import AgentSortField

AgentSortField.ID               # Sort by agent ID
AgentSortField.FIRST_NAME       # Sort by first name
AgentSortField.LAST_NAME        # Sort by last name
AgentSortField.EMAIL_ADDRESS    # Sort by email
AgentSortField.ACCOUNT_COUNTRY  # Sort by country
```

### Country Options
```python
from rezen.agents import Country

Country.UNITED_STATES     # United States
Country.CANADA            # Canada
```

### State/Province Options
```python
from rezen.agents import StateOrProvince

# US States (examples)
StateOrProvince.CALIFORNIA
StateOrProvince.TEXAS
StateOrProvince.FLORIDA
StateOrProvince.NEW_YORK
StateOrProvince.UTAH

# Canadian Provinces (examples) 
StateOrProvince.ONTARIO
StateOrProvince.BRITISH_COLUMBIA
StateOrProvince.ALBERTA
StateOrProvince.QUEBEC

# All 50 US states + DC + Puerto Rico + 10 Canadian provinces available
```

## ✅ Best Practices

### 1. Efficient Agent Search
```python
# Start with email search (most specific)
agents = client.agents.get_agents_by_email("agent@email.com")

# Fall back to name search
if not agents:
    search_result = client.agents.search_active_agents(name="Agent Name")
    agents = search_result.get('results', [])
```

### 2. Handle Privacy Restrictions
```python
# Many agent endpoints are privacy-protected
def safe_agent_call(func, *args, **kwargs):
    """Safely call agent endpoints that may be privacy-restricted."""
    try:
        return func(*args, **kwargs)
    except Exception as e:
        if "Unauthorized" in str(e) or "Forbidden" in str(e):
            return {"error": "Access restricted for privacy"}
        raise e

# Usage
payment_info = safe_agent_call(client.agents.get_payment_details, agent_id)
```

### 3. Cache Frequently Used Agent Data
```python
# Cache agent lookups to reduce API calls
AGENT_CACHE = {}

def get_cached_agent(email):
    if email in AGENT_CACHE:
        return AGENT_CACHE[email]
    
    agents = client.agents.get_agents_by_email(email)
    if agents and len(agents) > 0:
        AGENT_CACHE[email] = agents[0]
        return agents[0]
    
    return None
```

### 4. Validate Agent Status
```python
def validate_agent_for_transaction(agent_id):
    """Validate agent can be used in transactions."""
    try:
        # Get agent info from search or other methods
        search_result = client.agents.get_agents_by_ids([agent_id])
        agents = search_result.get('agents', [])
        
        if not agents:
            return False, "Agent not found"
        
        agent = agents[0]
        status = agent.get('status')
        
        if status != 'ACTIVE':
            return False, f"Agent status is {status}, not ACTIVE"
        
        return True, "Agent is valid"
        
    except Exception as e:
        return False, f"Error validating agent: {e}"

# Usage
is_valid, message = validate_agent_for_transaction(agent_id)
if not is_valid:
    print(f"⚠️  {message}")
```

## 🚨 Common Issues

### Issue: Agent Search Returns No Results
**Causes:**
- Agent name misspelled
- Agent not in active status
- Search criteria too restrictive

**Solutions:**
```python
# Try broader search
all_agents = client.agents.search_active_agents(page_size=100)
print(f"Total active agents: {all_agents.get('totalCount', 0)}")

# Try different search terms
variations = ["Michael Perry", "Perry", "Michael", "mike perry"]
for term in variations:
    result = client.agents.search_active_agents(name=term)
    if result.get('results'):
        print(f"✅ Found results for: {term}")
        break
```

### Issue: Access Denied for Agent Information
**Cause:** Privacy restrictions on sensitive agent data

**Solution:** Expected behavior - only public information accessible
```python
# These endpoints are privacy-protected:
# - Payment details
# - Tax forms  
# - Profile scores
# - Downline details (if not your network)

# These endpoints are generally accessible:
# - Public agent search
# - Basic agent information
# - Your own agent information (get_me)
```

### Issue: Network Information Not Available
**Cause:** Agent network data is restricted to authorized users

**Solution:**
```python
# You can only access network information for:
# 1. Your own agent account
# 2. Agents in your downline (if you're their upline)

# Check your access level
me = client.agents.get_me()
my_agent_id = me.get('id')

# You can always access your own network
my_network = client.agents.get_front_line_agents_info(my_agent_id)
```

### Issue: Bulk Agent Lookup Fails
**Cause:** Too many agent IDs in single request

**Solution:**
```python
def get_agents_in_batches(agent_ids, batch_size=20):
    """Get agents in batches to avoid limits."""
    all_agents = {}
    
    for i in range(0, len(agent_ids), batch_size):
        batch = agent_ids[i:i + batch_size]
        try:
            result = client.agents.get_agents_by_ids(batch)
            agents = result.get('agents', [])
            
            for agent in agents:
                all_agents[agent['id']] = agent
                
        except Exception as e:
            print(f"Error in batch {i//batch_size + 1}: {e}")
    
    return all_agents
```

## 🔗 Related Workflows

- **[Transaction Builder](transaction-builder.md)** - Using agent IDs in transactions
- **[Teams](teams.md)** - Finding team IDs for agent assignment  
- **[Authentication](authentication.md)** - Setting up API access
- **[Error Handling](error-handling.md)** - Troubleshooting agent issues

## 📚 API Response Reference

### Search Active Agents Response
```python
{
    "pageNumber": 0,
    "pageSize": 20,
    "hasNext": true,
    "totalCount": 21,
    "results": [
        {
            "id": "agent-uuid",
            "firstName": "Michael",
            "lastName": "Perry", 
            "emailAddress": "michael@theperry.group",
            "phoneNumber": "18015889964",
            "status": "ACTIVE",
            "administrativeAreas": [
                {
                    "stateOrProvince": "UTAH",
                    "country": "UNITED_STATES"
                }
            ]
        }
    ]
}
```

### Agent Network Response
```python
{
    "frontLineAgentInfos": [
        {
            "id": "agent-uuid",
            "firstName": "Agent",
            "lastName": "Name",
            "emailAddress": "agent@email.com",
            "phoneNumber": "phone",
            "status": "ACTIVE",
            "sizeOfNetwork": 15,
            "sponsorSplit": 100.0
        }
    ]
}
```

### Get Me Response
```python
{
    "id": "your-agent-uuid",
    "firstName": "Your",
    "lastName": "Name",
    "emailAddress": "your@email.com", 
    "phoneNumber": "your-phone",
    "status": "ACTIVE"
}
``` 