"""Structs module for the 1Shot API."""

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from uxly_1shot_client.models.common import PagedResponse
from uxly_1shot_client.models.struct import SolidityStruct, StructCreateParams, StructListParams, StructUpdateParams
if TYPE_CHECKING:
    from uxly_1shot_client.async_client import AsyncClient
    from uxly_1shot_client.sync_client import Client

class BaseStructs:
    """Base class for structs module."""

    def _get_list_url(self, business_id: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Get the URL for listing structs.

        Args:
            business_id: The business ID
            params: Optional filter parameters

        Returns:
            The URL for listing structs
        """
        url = f"/business/{business_id}/structs"
        if params:
            query_params = []
            for key, value in params.items():
                if value is not None:
                    query_params.append(f"{key}={value}")
            if query_params:
                url += "?" + "&".join(query_params)
        return url

    def _get_create_url(self, business_id: str) -> str:
        """Get the URL for creating a struct.

        Args:
            business_id: The business ID

        Returns:
            The URL for creating a struct
        """
        return f"/business/{business_id}/structs"

    def _get_get_url(self, struct_id: str) -> str:
        """Get the URL for getting a struct.

        Args:
            struct_id: The struct ID

        Returns:
            The URL for getting a struct
        """
        return f"/structs/{struct_id}"

    def _get_update_url(self, struct_id: str) -> str:
        """Get the URL for updating a struct.

        Args:
            struct_id: The struct ID

        Returns:
            The URL for updating a struct
        """
        return f"/structs/{struct_id}"

    def _get_delete_url(self, struct_id: str) -> str:
        """Get the URL for deleting a struct.

        Args:
            struct_id: The struct ID

        Returns:
            The URL for deleting a struct
        """
        return f"/structs/{struct_id}"


class SyncStructs(BaseStructs):
    """Synchronous structs module for the 1Shot API."""

    def __init__(self, client: "Client") -> None:
        """Initialize the structs module.

        Args:
            client: The synchronous client instance
        """
        self._client = client

    def list(
        self, business_id: str, params: Optional[Union[StructListParams, Dict[str, Any]]] = None
    ) -> PagedResponse[SolidityStruct]:
        """List structs for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or StructListParams instance

        Returns:
            A paged response of structs
        """
        if params is not None and not isinstance(params, StructListParams):
            params = StructListParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_list_url(business_id, params.model_dump(by_alias=True) if params else None)
        response = self._client._request("GET", url)
        return PagedResponse[SolidityStruct].model_validate(response)

    def create(
        self, business_id: str, params: Union[StructCreateParams, Dict[str, Any]]
    ) -> SolidityStruct:
        """Create a new struct for a business.

        Args:
            business_id: The business ID
            params: Parameters for creating the struct, either as a dict or StructCreateParams instance

        Returns:
            The created struct
        """
        if not isinstance(params, StructCreateParams):
            params = StructCreateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_create_url(business_id)
        response = self._client._request("POST", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return SolidityStruct.model_validate(response)

    def get(self, struct_id: str) -> SolidityStruct:
        """Get a struct by ID.

        Args:
            struct_id: The struct ID

        Returns:
            The struct
        """
        url = self._get_get_url(struct_id)
        response = self._client._request("GET", url)
        return SolidityStruct.model_validate(response)

    def update(
        self, struct_id: str, params: Union[StructUpdateParams, Dict[str, Any]]
    ) -> SolidityStruct:
        """Update a struct.

        Args:
            struct_id: The struct ID
            params: Update parameters, either as a dict or StructUpdateParams instance

        Returns:
            The updated struct
        """
        if not isinstance(params, StructUpdateParams):
            params = StructUpdateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_update_url(struct_id)
        response = self._client._request("PUT", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return SolidityStruct.model_validate(response)

    def delete(self, struct_id: str) -> None:
        """Delete a struct.

        Args:
            struct_id: The struct ID

        Returns:
            A dictionary with a success flag
        """
        url = self._get_delete_url(struct_id)
        self._client._request("DELETE", url)


class AsyncStructs(BaseStructs):
    """Asynchronous structs module for the 1Shot API."""

    def __init__(self, client: "AsyncClient") -> None:
        """Initialize the structs module.

        Args:
            client: The asynchronous client instance
        """
        self._client = client

    async def list(
        self, business_id: str, params: Optional[Union[StructListParams, Dict[str, Any]]] = None
    ) -> PagedResponse[SolidityStruct]:
        """List structs for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or StructListParams instance

        Returns:
            A paged response of structs
        """
        if params is not None and not isinstance(params, StructListParams):
            params = StructListParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_list_url(business_id, params.model_dump(by_alias=True) if params else None)
        response = await self._client._request("GET", url)
        return PagedResponse[SolidityStruct].model_validate(response)

    async def create(
        self, business_id: str, params: Union[StructCreateParams, Dict[str, Any]]
    ) -> SolidityStruct:
        """Create a new struct for a business.

        Args:
            business_id: The business ID
            params: Parameters for creating the struct, either as a dict or StructCreateParams instance

        Returns:
            The created struct
        """
        if not isinstance(params, StructCreateParams):
            params = StructCreateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_create_url(business_id)
        response = await self._client._request("POST", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return SolidityStruct.model_validate(response)

    async def get(self, struct_id: str) -> SolidityStruct:
        """Get a struct by ID.

        Args:
            struct_id: The struct ID

        Returns:
            The struct
        """
        url = self._get_get_url(struct_id)
        response = await self._client._request("GET", url)
        return SolidityStruct.model_validate(response)

    async def update(
        self, struct_id: str, params: Union[StructUpdateParams, Dict[str, Any]]
    ) -> SolidityStruct:
        """Update a struct.

        Args:
            struct_id: The struct ID
            params: Update parameters, either as a dict or StructUpdateParams instance

        Returns:
            The updated struct
        """
        if not isinstance(params, StructUpdateParams):
            params = StructUpdateParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_update_url(struct_id)
        response = await self._client._request("PUT", url, data=params.model_dump(exclude_none=True, by_alias=True))
        return SolidityStruct.model_validate(response)

    async def delete(self, struct_id: str) -> None:
        """Delete a struct.

        Args:
            struct_id: The struct ID

        Returns:
            A dictionary with a success flag
        """
        url = self._get_delete_url(struct_id)
        await self._client._request("DELETE", url) 