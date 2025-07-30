"""Wallets module for the 1Shot API."""

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from uxly_1shot_client.models.common import PagedResponse
from uxly_1shot_client.models.wallet import (
    EscrowWallet,
    WalletListParams,
    WalletCreateParams,
    WalletUpdateParams,
)
if TYPE_CHECKING:
    from uxly_1shot_client.async_client import AsyncClient
    from uxly_1shot_client.sync_client import Client

class BaseWallets:
    """Base class for wallets module."""

    def _get_list_url(self, business_id: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Get the URL for listing wallets.

        Args:
            business_id: The business ID
            params: Optional filter parameters

        Returns:
            The URL for listing wallets
        """
        url = f"/business/{business_id}/wallets"
        if params:
            query_params = []
            for key, value in params.items():
                if value is not None:
                    query_params.append(f"{key}={value}")
            if query_params:
                url += "?" + "&".join(query_params)
        return url

    def _get_create_url(self, business_id: str) -> str:
        """Get the URL for creating a wallet.

        Args:
            business_id: The business ID

        Returns:
            The URL for creating a wallet
        """
        return f"/business/{business_id}/wallets"

    def _get_get_url(self, escrow_wallet_id: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Get the URL for getting a wallet.

        Args:
            escrow_wallet_id: The wallet ID
            params: Optional query parameters

        Returns:
            The URL for getting a wallet
        """
        url = f"/wallets/{escrow_wallet_id}"
        if params:
            query_params = []
            for key, value in params.items():
                if value is not None:
                    query_params.append(f"{key}={value}")
            if query_params:
                url += "?" + "&".join(query_params)
        return url

    def _get_update_url(self, escrow_wallet_id: str) -> str:
        """Get the URL for updating a wallet.

        Args:
            escrow_wallet_id: The wallet ID

        Returns:
            The URL for updating a wallet
        """
        return f"/wallets/{escrow_wallet_id}"

    def _get_delete_url(self, escrow_wallet_id: str) -> str:
        """Get the URL for deleting a wallet.

        Args:
            escrow_wallet_id: The wallet ID

        Returns:
            The URL for deleting a wallet
        """
        return f"/wallets/{escrow_wallet_id}"


class SyncWallets(BaseWallets):
    """Synchronous wallets module for the 1Shot API."""

    def __init__(self, client: "Client") -> None:
        """Initialize the wallets module.

        Args:
            client: The synchronous client instance
        """
        self._client = client

    def list(
        self, business_id: str, params: Optional[Union[WalletListParams, Dict[str, Any]]] = None
    ) -> PagedResponse[EscrowWallet]:
        """List escrow wallets for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or WalletListParams instance

        Returns:
            A paged response of wallets
        """
        if params is not None and not isinstance(params, WalletListParams):
            params = WalletListParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_list_url(business_id, params.model_dump(by_alias=True) if params else None)
        response = self._client._request("GET", url)
        return PagedResponse[EscrowWallet].model_validate(response)

    def create(
        self, business_id: str, params: Union[WalletCreateParams, Dict[str, Any]]
    ) -> EscrowWallet:
        """Create a new escrow wallet for a business.

        Args:
            business_id: The business ID
            params: Parameters for creating the wallet, either as a dict or WalletCreateParams instance

        Returns:
            The created wallet
        """
        if not isinstance(params, WalletCreateParams):
            params = WalletCreateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_create_url(business_id)
        response = self._client._request("POST", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return EscrowWallet.model_validate(response)

    def get(
        self, escrow_wallet_id: str, include_balances: Optional[bool] = None
    ) -> EscrowWallet:
        """Get an escrow wallet by ID.

        Args:
            escrow_wallet_id: The wallet ID
            include_balances: Whether to include balance information

        Returns:
            The wallet
        """
        params = {"includeBalances": str(include_balances).lower()} if include_balances is not None else None
        url = self._get_get_url(escrow_wallet_id, params)
        response = self._client._request("GET", url)
        return EscrowWallet.model_validate(response)

    def update(
        self, escrow_wallet_id: str, params: Union[WalletUpdateParams, Dict[str, Any]]
    ) -> EscrowWallet:
        """Update an escrow wallet.

        Args:
            escrow_wallet_id: The wallet ID
            params: Update parameters, either as a dict or WalletUpdateParams instance

        Returns:
            The updated wallet
        """
        if not isinstance(params, WalletUpdateParams):
            params = WalletUpdateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_update_url(escrow_wallet_id)
        response = self._client._request("PUT", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return EscrowWallet.model_validate(response)

    def delete(self, escrow_wallet_id: str) -> None:
        """Delete an escrow wallet.

        Args:
            escrow_wallet_id: The wallet ID

        Returns:
            A dictionary with a success flag
        """
        url = self._get_delete_url(escrow_wallet_id)
        self._client._request("DELETE", url)


class AsyncWallets(BaseWallets):
    """Asynchronous wallets module for the 1Shot API."""

    def __init__(self, client: "AsyncClient") -> None:
        """Initialize the wallets module.

        Args:
            client: The asynchronous client instance
        """
        self._client = client

    async def list(
        self, business_id: str, params: Optional[Union[WalletListParams, Dict[str, Any]]] = None
    ) -> PagedResponse[EscrowWallet]:
        """List escrow wallets for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or WalletListParams instance

        Returns:
            A paged response of wallets
        """
        if params is not None and not isinstance(params, WalletListParams):
            params = WalletListParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_list_url(business_id, params.model_dump(by_alias=True) if params else None)
        response = await self._client._request("GET", url)
        return PagedResponse[EscrowWallet].model_validate(response)

    async def create(
        self, business_id: str, params: Union[WalletCreateParams, Dict[str, Any]]
    ) -> EscrowWallet:
        """Create a new escrow wallet for a business.

        Args:
            business_id: The business ID
            params: Parameters for creating the wallet, either as a dict or WalletCreateParams instance

        Returns:
            The created wallet
        """
        if not isinstance(params, WalletCreateParams):
            params = WalletCreateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_create_url(business_id)
        response = await self._client._request("POST", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return EscrowWallet.model_validate(response)

    async def get(
        self, escrow_wallet_id: str, include_balances: Optional[bool] = None
    ) -> EscrowWallet:
        """Get an escrow wallet by ID.

        Args:
            escrow_wallet_id: The wallet ID
            include_balances: Whether to include balance information

        Returns:
            The wallet
        """
        params = {"includeBalances": str(include_balances).lower()} if include_balances is not None else None
        url = self._get_get_url(escrow_wallet_id, params)
        response = await self._client._request("GET", url)
        return EscrowWallet.model_validate(response)

    async def update(
        self, escrow_wallet_id: str, params: Union[WalletUpdateParams, Dict[str, Any]]
    ) -> EscrowWallet:
        """Update an escrow wallet.

        Args:
            escrow_wallet_id: The wallet ID
            params: Update parameters, either as a dict or WalletUpdateParams instance

        Returns:
            The updated wallet
        """
        if not isinstance(params, WalletUpdateParams):
            params = WalletUpdateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_update_url(escrow_wallet_id)
        response = await self._client._request("PUT", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return EscrowWallet.model_validate(response)

    async def delete(self, escrow_wallet_id: str) -> Dict[str, bool]:
        """Delete an escrow wallet.

        Args:
            escrow_wallet_id: The wallet ID

        Returns:
            A dictionary with a success flag
        """
        url = self._get_delete_url(escrow_wallet_id)
        return await self._client._request("DELETE", url) 