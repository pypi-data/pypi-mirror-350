"""Executions module for the 1Shot API."""

from typing import TYPE_CHECKING, Any, Dict, Optional, Union

from uxly_1shot_client.models.common import PagedResponse
from uxly_1shot_client.models.execution import ExecutionListParams, TransactionExecution
if TYPE_CHECKING:
    from uxly_1shot_client.async_client import AsyncClient
    from uxly_1shot_client.sync_client import Client


class BaseExecutions:
    """Base class for executions module."""

    def _get_list_url(self, business_id: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Get the URL for listing executions.

        Args:
            business_id: The business ID
            params: Optional filter parameters

        Returns:
            The URL for listing executions
        """
        url = f"/business/{business_id}/transactions/executions"
        if params:
            query_params = []
            for key, value in params.items():
                if value is not None:
                    query_params.append(f"{key}={value}")
            if query_params:
                url += "?" + "&".join(query_params)
        return url

    def _get_get_url(self, execution_id: str) -> str:
        """Get the URL for getting an execution.

        Args:
            execution_id: The execution ID

        Returns:
            The URL for getting an execution
        """
        return f"/executions/{execution_id}"


class SyncExecutions(BaseExecutions):
    """Synchronous executions module for the 1Shot API."""

    def __init__(self, client: "Client") -> None:
        """Initialize the executions module.

        Args:
            client: The synchronous client instance
        """
        self._client = client

    def list(
        self, business_id: str, params: Optional[Union[ExecutionListParams, Dict[str, Any]]] = None
    ) -> PagedResponse[TransactionExecution]:
        """List executions for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or ExecutionListParams instance

        Returns:
            A paged response of executions
        """
        if params is not None and not isinstance(params, ExecutionListParams):
            params = ExecutionListParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_list_url(business_id, params.model_dump(by_alias=True) if params else None)
        response = self._client._request("GET", url)
        return PagedResponse[TransactionExecution].model_validate(response)

    def get(self, execution_id: str) -> TransactionExecution:
        """Get an execution by ID.

        Args:
            execution_id: The execution ID

        Returns:
            The execution
        """
        url = self._get_get_url(execution_id)
        response = self._client._request("GET", url)
        return TransactionExecution.model_validate(response)


class AsyncExecutions(BaseExecutions):
    """Asynchronous executions module for the 1Shot API."""

    def __init__(self, client: "AsyncClient") -> None:
        """Initialize the executions module.

        Args:
            client: The asynchronous client instance
        """
        self._client = client

    async def list(
        self, business_id: str, params: Optional[Union[ExecutionListParams, Dict[str, Any]]] = None
    ) -> PagedResponse[TransactionExecution]:
        """List executions for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or ExecutionListParams instance

        Returns:
            A paged response of executions
        """
        if params is not None and not isinstance(params, ExecutionListParams):
            params = ExecutionListParams.model_validate(params, by_alias=True, by_name=True)
        url = self._get_list_url(business_id, params.model_dump(by_alias=True) if params else None)
        response = await self._client._request("GET", url)
        return PagedResponse[TransactionExecution].model_validate(response)

    async def get(self, execution_id: str) -> TransactionExecution:
        """Get an execution by ID.

        Args:
            execution_id: The execution ID

        Returns:
            The execution
        """
        url = self._get_get_url(execution_id)
        response = await self._client._request("GET", url)
        return TransactionExecution.model_validate(response)