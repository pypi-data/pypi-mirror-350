"""Teams client for ReZEN API."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from .base_client import BaseClient


class SortDirection(Enum):
    """Sort direction options."""

    ASC = "ASC"
    DESC = "DESC"


class SortField(Enum):
    """Sort field options for teams."""

    ID = "ID"
    NAME = "NAME"
    STATUS = "STATUS"
    TEAM_TYPE = "TEAM_TYPE"
    LEADER_NAME = "LEADER_NAME"
    CREATED_AT = "CREATED_AT"


class TeamStatus(Enum):
    """Team status options."""

    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"


class TeamType(Enum):
    """Team type options."""

    NORMAL = "NORMAL"
    PLATINUM = "PLATINUM"
    GROUP = "GROUP"
    DOMESTIC = "DOMESTIC"
    PRO = "PRO"


class TeamsClient(BaseClient):
    """Client for teams API endpoints.

    This client provides access to team search functionality and team details.
    Note: This uses a different base URL than the main ReZEN API.
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the teams client.

        Args:
            api_key: API key for authentication. If None, will look for REZEN_API_KEY env var
            base_url: Base URL for the teams API. Defaults to yenta production URL
        """
        # Use the yenta base URL for teams API
        teams_base_url = base_url or "https://yenta.therealbrokerage.com/api/v1"
        super().__init__(api_key=api_key, base_url=teams_base_url)

    def search_teams(
        self,
        page_number: Optional[int] = None,
        page_size: Optional[int] = None,
        sort_direction: Optional[Union[SortDirection, str]] = None,
        sort_by: Optional[
            Union[List[Union[SortField, str]], Union[SortField, str]]
        ] = None,
        team_id: Optional[str] = None,
        name: Optional[str] = None,
        search_text: Optional[str] = None,
        status: Optional[Union[TeamStatus, str]] = None,
        created_at_start: Optional[Union[date, str]] = None,
        created_at_end: Optional[Union[date, str]] = None,
        team_type: Optional[Union[TeamType, str]] = None,
    ) -> Dict[str, Any]:
        """Search teams given a set of criteria.

        Args:
            page_number: Page number for pagination (default: 0)
            page_size: Number of results per page (default: 20, min: 1)
            sort_direction: Sort direction (ASC or DESC, default: ASC)
            sort_by: Fields to sort by (default: ["NAME"])
            team_id: Filter by team UUID
            name: Filter by team name
            search_text: General search text
            status: Filter by team status (ACTIVE or INACTIVE)
            created_at_start: Filter by creation date start (YYYY-MM-DD format)
            created_at_end: Filter by creation date end (YYYY-MM-DD format)
            team_type: Filter by team type (NORMAL, PLATINUM, GROUP, DOMESTIC, PRO)

        Returns:
            Dictionary containing team search results with pagination information

        Example:
            ```python
            # Search for active teams
            teams = client.teams.search_teams(
                status=TeamStatus.ACTIVE,
                team_type=TeamType.PLATINUM,
                page_size=50
            )

            # Search by name
            teams = client.teams.search_teams(
                name="Sales Team",
                sort_by=[SortField.NAME, SortField.CREATED_AT],
                sort_direction=SortDirection.DESC
            )

            # Search with text query
            teams = client.teams.search_teams(
                search_text="marketing",
                page_number=2
            )
            ```
        """
        params: Dict[str, Any] = {}

        # Add pagination parameters
        if page_number is not None:
            params["pageNumber"] = page_number
        if page_size is not None:
            params["pageSize"] = page_size

        # Add sorting parameters
        if sort_direction is not None:
            if isinstance(sort_direction, SortDirection):
                params["sortDirection"] = sort_direction.value
            else:
                params["sortDirection"] = sort_direction

        if sort_by is not None:
            if isinstance(sort_by, list):
                # Handle list of sort fields
                sort_values = []
                for field in sort_by:
                    if isinstance(field, SortField):
                        sort_values.append(field.value)
                    else:
                        sort_values.append(field)
                params["sortBy"] = sort_values
            else:
                # Handle single sort field
                if isinstance(sort_by, SortField):
                    params["sortBy"] = [sort_by.value]
                else:
                    params["sortBy"] = [sort_by]

        # Add filter parameters
        if team_id is not None:
            params["id"] = team_id
        if name is not None:
            params["name"] = name
        if search_text is not None:
            params["searchText"] = search_text

        if status is not None:
            if isinstance(status, TeamStatus):
                params["status"] = status.value
            else:
                params["status"] = status

        if team_type is not None:
            if isinstance(team_type, TeamType):
                params["teamType"] = team_type.value
            else:
                params["teamType"] = team_type

        # Add date range parameters
        if created_at_start is not None:
            if isinstance(created_at_start, date):
                params["createdAtStart"] = created_at_start.isoformat()
            else:
                params["createdAtStart"] = created_at_start

        if created_at_end is not None:
            if isinstance(created_at_end, date):
                params["createdAtEnd"] = created_at_end.isoformat()
            else:
                params["createdAtEnd"] = created_at_end

        return self.get("teams", params=params)

    def get_team_without_agents(self, team_id: str) -> Dict[str, Any]:
        """Get team by ID without agents information.

        Args:
            team_id: UUID of the team to retrieve

        Returns:
            Dictionary containing team details without agent information

        Example:
            ```python
            team = client.teams.get_team_without_agents("550e8400-e29b-41d4-a716-446655440000")
            print(f"Team name: {team['name']}")
            print(f"Team status: {team['status']}")
            ```
        """
        return self.get(f"teams/{team_id}/without-agents")
