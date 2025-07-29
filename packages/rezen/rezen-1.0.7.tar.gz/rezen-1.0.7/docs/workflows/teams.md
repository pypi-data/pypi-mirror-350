# Team Management Workflows

This guide covers finding and managing teams using the ReZEN Teams API.

## 👥 Overview

The Teams API allows you to:
- Search for teams by name, status, or type
- Get detailed team information
- Find teams for agent assignment
- Filter teams by various criteria

## 🚀 Quick Start

```python
from rezen import RezenClient, TeamStatus, TeamType

client = RezenClient()

# Search for active teams
teams = client.teams.search_teams(status=TeamStatus.ACTIVE)

# Find a specific team
perry_teams = client.teams.search_teams(name="The Perry Group Standard Team")

# Get team details
team_id = "ab45fb68-3f2a-4985-8ec6-73d1b409ea33"
team_details = client.teams.get_team_without_agents(team_id)
```

## 🔍 Search Workflows

### Workflow 1: Find Team by Exact Name

```python
# Search for exact team name
teams_response = client.teams.search_teams(
    name="The Perry Group Standard Team"
)

teams = teams_response.get('results', [])
if teams:
    team = teams[0]
    print(f"Found team: {team['name']} (ID: {team['id']})")
else:
    print("Team not found")
```

### Workflow 2: Search Teams by Text

```python
# Search for teams containing specific text
teams_response = client.teams.search_teams(
    search_text="Perry Group",
    page_size=20
)

teams = teams_response.get('results', [])
for team in teams:
    if "Perry Group" in team.get('name', ''):
        print(f"🎯 Match: {team['name']} (ID: {team['id']})")
```

### Workflow 3: Filter Teams by Status and Type

```python
from rezen.teams import TeamStatus, TeamType, SortField, SortDirection

# Find active platinum teams
platinum_teams = client.teams.search_teams(
    status=TeamStatus.ACTIVE,
    team_type=TeamType.PLATINUM,
    sort_by=[SortField.NAME],
    sort_direction=SortDirection.ASC,
    page_size=50
)

print(f"Found {len(platinum_teams.get('results', []))} active platinum teams")
```

### Workflow 4: Advanced Search with Pagination

```python
# Search with full pagination and sorting
search_params = {
    "search_text": "Group",
    "status": TeamStatus.ACTIVE,
    "team_type": TeamType.NORMAL,
    "page_number": 0,
    "page_size": 25,
    "sort_by": [SortField.NAME, SortField.CREATED_AT],
    "sort_direction": SortDirection.DESC
}

teams_response = client.teams.search_teams(**search_params)

print(f"Page {teams_response.get('pageNumber', 0) + 1}")
print(f"Total teams: {teams_response.get('totalCount', 0)}")
print(f"Teams on this page: {len(teams_response.get('results', []))}")
```

## 📊 Team Information Workflows

### Get Team Details

```python
# Get team without agent details (faster)
team_id = "ab45fb68-3f2a-4985-8ec6-73d1b409ea33"
team_info = client.teams.get_team_without_agents(team_id)

print(f"Team Name: {team_info.get('name')}")
print(f"Status: {team_info.get('status')}")
print(f"Type: {team_info.get('type')}")
print(f"Created: {team_info.get('createdAt')}")
```

### Extract Team Information from Search

```python
def extract_team_info(team_data):
    """Extract key information from team search results."""
    return {
        'id': team_data.get('id'),
        'name': team_data.get('name'),
        'status': team_data.get('status'),
        'type': team_data.get('type'),
        'created_date': team_data.get('createdAt'),
        'agent_count': len(team_data.get('agents', []))
    }

# Use with search results
teams_response = client.teams.search_teams(search_text="Perry")
teams = teams_response.get('results', [])

for team_data in teams:
    team_info = extract_team_info(team_data)
    print(f"Team: {team_info['name']} ({team_info['agent_count']} agents)")
```

## 🏗️ Integration Workflows

### Workflow 1: Find Team for Agent Assignment

```python
def find_team_for_agent(team_name_or_search):
    """Find team ID for agent assignment in transactions."""
    
    # Try exact name first
    teams_response = client.teams.search_teams(name=team_name_or_search)
    teams = teams_response.get('results', [])
    
    if teams:
        return teams[0]
    
    # Try text search
    teams_response = client.teams.search_teams(search_text=team_name_or_search)
    teams = teams_response.get('results', [])
    
    # Look for exact matches in search results
    for team in teams:
        if team_name_or_search.lower() in team.get('name', '').lower():
            return team
    
    return None

# Usage
team = find_team_for_agent("The Perry Group Standard Team")
if team:
    team_id = team['id']
    print(f"✅ Found team ID: {team_id}")
    
    # Use in transaction builder
    agent_data = {
        "firstName": "Agent",
        "lastName": "Name", 
        "email": "agent@email.com",
        "teamId": team_id  # Assign to found team
    }
else:
    print("❌ Team not found")
```

### Workflow 2: Validate Team Assignment

```python
def validate_team_assignment(team_id):
    """Validate that a team exists and is active."""
    try:
        team_info = client.teams.get_team_without_agents(team_id)
        
        if team_info.get('status') != 'ACTIVE':
            return False, f"Team is not active: {team_info.get('status')}"
        
        return True, f"Team valid: {team_info.get('name')}"
        
    except Exception as e:
        return False, f"Team not found or error: {e}"

# Usage
team_id = "ab45fb68-3f2a-4985-8ec6-73d1b409ea33"
is_valid, message = validate_team_assignment(team_id)

if is_valid:
    print(f"✅ {message}")
else:
    print(f"❌ {message}")
```

### Workflow 3: Team Discovery for New Users

```python
def discover_available_teams(search_criteria=None):
    """Discover teams available for assignment."""
    
    search_params = {
        "status": TeamStatus.ACTIVE,
        "page_size": 100,
        "sort_by": [SortField.NAME],
        "sort_direction": SortDirection.ASC
    }
    
    if search_criteria:
        search_params["search_text"] = search_criteria
    
    teams_response = client.teams.search_teams(**search_params)
    teams = teams_response.get('results', [])
    
    # Group by team type
    team_groups = {}
    for team in teams:
        team_type = team.get('type', 'UNKNOWN')
        if team_type not in team_groups:
            team_groups[team_type] = []
        team_groups[team_type].append(team)
    
    return team_groups

# Usage
all_teams = discover_available_teams()

for team_type, teams in all_teams.items():
    print(f"\n{team_type} Teams ({len(teams)}):")
    for team in teams[:5]:  # Show first 5
        print(f"  - {team['name']} (ID: {team['id']})")
```

## 📋 Enumeration Reference

### Team Status Options
```python
from rezen.teams import TeamStatus

TeamStatus.ACTIVE     # Active teams
TeamStatus.INACTIVE   # Inactive teams
```

### Team Type Options  
```python
from rezen.teams import TeamType

TeamType.NORMAL       # Standard teams
TeamType.PLATINUM     # Platinum level teams
TeamType.GROUP        # Group teams
TeamType.DOMESTIC     # Domestic teams  
TeamType.PRO          # Professional teams
```

### Sort Field Options
```python
from rezen.teams import SortField

SortField.ID          # Sort by team ID
SortField.NAME        # Sort by team name
SortField.STATUS      # Sort by status
SortField.TEAM_TYPE   # Sort by team type
SortField.LEADER_NAME # Sort by leader name
SortField.CREATED_AT  # Sort by creation date
```

### Sort Direction Options
```python
from rezen.teams import SortDirection

SortDirection.ASC     # Ascending order
SortDirection.DESC    # Descending order
```

## ✅ Best Practices

### 1. Efficient Team Search
```python
# Start with exact name search (fastest)
teams = client.teams.search_teams(name="Exact Team Name")

# Fall back to text search if needed
if not teams.get('results'):
    teams = client.teams.search_teams(search_text="Partial Name")
```

### 2. Cache Team Information
```python
# Cache frequently used team IDs
KNOWN_TEAMS = {
    "perry_group": "ab45fb68-3f2a-4985-8ec6-73d1b409ea33",
    "other_team": "other-team-id-here"
}

def get_team_id(team_key):
    if team_key in KNOWN_TEAMS:
        return KNOWN_TEAMS[team_key]
    
    # Search if not cached
    teams_response = client.teams.search_teams(search_text=team_key)
    teams = teams_response.get('results', [])
    return teams[0]['id'] if teams else None
```

### 3. Error Handling
```python
from rezen.exceptions import NotFoundError, ValidationError

try:
    team_info = client.teams.get_team_without_agents(team_id)
except NotFoundError:
    print(f"Team not found: {team_id}")
except ValidationError as e:
    print(f"Invalid team ID format: {e}")
```

### 4. Pagination for Large Results
```python
def get_all_teams(search_text=None):
    """Get all teams with pagination."""
    all_teams = []
    page_number = 0
    page_size = 100
    
    while True:
        response = client.teams.search_teams(
            search_text=search_text,
            page_number=page_number,
            page_size=page_size
        )
        
        teams = response.get('results', [])
        all_teams.extend(teams)
        
        # Check if there are more pages
        if not response.get('hasNext', False):
            break
            
        page_number += 1
    
    return all_teams
```

## 🚨 Common Issues

### Issue: No Teams Found
**Causes:**
- API key doesn't have team access permissions
- Search criteria too restrictive
- Team name misspelled

**Solutions:**
```python
# Try broader search
teams = client.teams.search_teams()  # Get all teams

# Check total count
print(f"Total teams available: {teams.get('totalCount', 0)}")
```

### Issue: Team ID Not Working in Transaction Builder
**Cause:** Team might be inactive or ID incorrect

**Solution:**
```python
# Validate team before use
team_info = client.teams.get_team_without_agents(team_id)
if team_info.get('status') != 'ACTIVE':
    print(f"⚠️  Team is {team_info.get('status')}, not ACTIVE")
```

### Issue: Search Returns Too Many Results
**Solution:** Use more specific criteria
```python
# More specific search
teams = client.teams.search_teams(
    name="Exact Team Name",           # Exact match
    status=TeamStatus.ACTIVE,         # Only active
    team_type=TeamType.NORMAL,        # Specific type
    page_size=10                      # Limit results
)
```

## 🔗 Related Workflows

- **[Transaction Builder](transaction-builder.md)** - Using team IDs in transactions
- **[Authentication](authentication.md)** - Setting up API access
- **[Error Handling](error-handling.md)** - Troubleshooting team issues

## 📚 API Response Reference

### Search Response Structure
```python
{
    "pageNumber": 0,
    "pageSize": 100,
    "hasNext": true,
    "totalCount": 4481,
    "results": [
        {
            "id": "team-uuid",
            "name": "Team Name",
            "type": "NORMAL",
            "status": "ACTIVE",
            "createdAt": 1646692557474,
            "agents": [...]  # Agent details if included
        }
    ]
}
```

### Team Details Response
```python
{
    "id": "team-uuid",
    "name": "Team Name", 
    "type": "NORMAL",
    "status": "ACTIVE",
    "createdAt": 1646692557474,
    "updatedAt": 1646692557474,
    # Additional team details without agent list
}
``` 