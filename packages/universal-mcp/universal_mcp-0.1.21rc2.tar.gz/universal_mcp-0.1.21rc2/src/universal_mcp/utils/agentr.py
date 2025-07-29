import os

import httpx
from loguru import logger

from universal_mcp.config import AppConfig
from universal_mcp.exceptions import NotAuthorizedError


class AgentrClient:
    """Helper class for AgentR API operations.

    This class provides utility methods for interacting with the AgentR API,
    including authentication, authorization, and credential management.

    Args:
        api_key (str, optional): AgentR API key. If not provided, will look for AGENTR_API_KEY env var
        base_url (str, optional): Base URL for AgentR API. Defaults to https://api.agentr.dev
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        if api_key:
            self.api_key = api_key
        elif os.getenv("AGENTR_API_KEY"):
            self.api_key = os.getenv("AGENTR_API_KEY")
        else:
            logger.error(
                "API key for AgentR is missing. Please visit https://agentr.dev to create an API key, then set it as AGENTR_API_KEY environment variable."
            )
            raise ValueError("AgentR API key required - get one at https://agentr.dev")
        self.base_url = (base_url or os.getenv("AGENTR_BASE_URL", "https://api.agentr.dev")).rstrip("/")
        self.client = httpx.Client(
            base_url=self.base_url, headers={"X-API-KEY": self.api_key}, timeout=30, follow_redirects=True
        )

    def get_credentials(self, integration_name: str) -> dict:
        """Get credentials for an integration from the AgentR API.

        Args:
            integration_name (str): Name of the integration to get credentials for

        Returns:
            dict: Credentials data from API response

        Raises:
            NotAuthorizedError: If credentials are not found (404 response)
            HTTPError: For other API errors
        """
        response = self.client.get(
            f"/api/{integration_name}/credentials/",
        )
        if response.status_code == 404:
            logger.warning(f"No credentials found for {integration_name}. Requesting authorization...")
            action = self.get_authorization_url(integration_name)
            raise NotAuthorizedError(action)
        response.raise_for_status()
        return response.json()

    def get_authorization_url(self, integration_name: str) -> str:
        """Get authorization URL for an integration.

        Args:
            integration_name (str): Name of the integration to get authorization URL for

        Returns:
            str: Message containing authorization URL

        Raises:
            HTTPError: If API request fails
        """
        response = self.client.get(
            f"/api/{integration_name}/authorize/",
        )
        response.raise_for_status()
        url = response.json()
        return f"Please ask the user to visit the following url to authorize the application: {url}. Render the url in proper markdown format with a clickable link."

    def fetch_apps(self) -> list[AppConfig]:
        """Fetch available apps from AgentR API.

        Returns:
            List of application configurations

        Raises:
            httpx.HTTPError: If API request fails
        """
        response = self.client.get("/api/apps/")
        response.raise_for_status()
        data = response.json()
        return [AppConfig.model_validate(app) for app in data]
