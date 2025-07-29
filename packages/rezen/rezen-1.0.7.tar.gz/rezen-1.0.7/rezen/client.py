"""Main ReZEN API client."""

from typing import Optional

from .agents import AgentsClient
from .teams import TeamsClient
from .transaction_builder import TransactionBuilderClient
from .transactions import TransactionsClient


class RezenClient:
    """Main client for the ReZEN API.

    This is the primary interface for interacting with the ReZEN API.
    It provides access to different API sections through client properties.

    Example:
        ```python
        from rezen import RezenClient

        # Initialize with API key from environment variable
        client = RezenClient()

        # Or provide API key directly
        client = RezenClient(api_key="your_api_key_here")

        # Use transaction builder endpoints
        response = client.transaction_builder.update_title_info(
            transaction_id="12345",
            title_info={"title": "New Title Information"}
        )

        # Use transactions endpoints
        response = client.transactions.get_transaction("tx-12345")

        # Use teams endpoints
        teams = client.teams.search_teams(status="ACTIVE")

        # Use agents endpoints
        agents = client.agents.search_active_agents(name="John")
        ```
    """

    def __init__(
        self, api_key: Optional[str] = None, base_url: Optional[str] = None
    ) -> None:
        """Initialize the ReZEN client.

        Args:
            api_key: API key for authentication. If None, will look for REZEN_API_KEY env var
            base_url: Base URL for the API. Defaults to production URL
        """
        self._api_key = api_key
        self._base_url = base_url
        self._transaction_builder: Optional[TransactionBuilderClient] = None
        self._transactions: Optional[TransactionsClient] = None
        self._teams: Optional[TeamsClient] = None
        self._agents: Optional[AgentsClient] = None

    @property
    def transaction_builder(self) -> TransactionBuilderClient:
        """Access to transaction builder endpoints.

        Returns:
            TransactionBuilderClient instance
        """
        if self._transaction_builder is None:
            self._transaction_builder = TransactionBuilderClient(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._transaction_builder

    @property
    def transactions(self) -> TransactionsClient:
        """Access to transactions endpoints.

        Returns:
            TransactionsClient instance
        """
        if self._transactions is None:
            self._transactions = TransactionsClient(
                api_key=self._api_key, base_url=self._base_url
            )
        return self._transactions

    @property
    def teams(self) -> TeamsClient:
        """Access to teams endpoints.

        Returns:
            TeamsClient instance
        """
        if self._teams is None:
            self._teams = TeamsClient(
                api_key=self._api_key
                # Note: teams uses a different base URL, handled in TeamsClient
            )
        return self._teams

    @property
    def agents(self) -> AgentsClient:
        """Access to agents endpoints.

        Returns:
            AgentsClient instance
        """
        if self._agents is None:
            self._agents = AgentsClient(
                api_key=self._api_key
                # Note: agents uses a different base URL, handled in AgentsClient
            )
        return self._agents
