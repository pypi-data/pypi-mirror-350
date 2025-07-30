"""Base client for the 1Shot API."""

from datetime import datetime
from typing import Dict, Optional

from pydantic import BaseModel

class TokenResponse(BaseModel):
    """Response from the token endpoint."""

    access_token: str
    token_type: str
    expires_in: int
    scope: str


class BaseClient:
    """Base client for the 1Shot API."""

    def __init__(
        self,
        api_key: str,
        api_secret: str,
        base_url: str = "https://api.1shotapi.com/v0",
    ) -> None:
        """Initialize the client.

        Args:
            api_key: Your API key
            api_secret: Your API secret
            base_url: Base URL for the API
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

    def _get_token_url(self) -> str:
        """Get the token URL.

        Returns:
            The token URL
        """
        return f"{self.base_url}/token"

    def _get_token_data(self) -> Dict[str, str]:
        """Get the token request data.

        Returns:
            The token request data
        """
        return {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.api_secret,
        }

    def _get_headers(self) -> Dict[str, str]:
        """Get the request headers.

        Returns:
            The request headers
        """
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Content-Type": "application/json",
        }

    def _get_url(self, path: str) -> str:
        """Get the full URL for a path.

        Args:
            path: The API path

        Returns:
            The full URL
        """
        return f"{self.base_url}{path}" 