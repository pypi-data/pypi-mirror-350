"""Transactions module for the 1Shot API."""

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union


from uxly_1shot_client.models.common import PagedResponse
from uxly_1shot_client.models.execution import TransactionExecution
if TYPE_CHECKING:
    from uxly_1shot_client.async_client import AsyncClient
    from uxly_1shot_client.sync_client import Client
from uxly_1shot_client.models.transaction import (
    TransactionEstimate,
    TransactionTestResult,
    Transaction,
    ListTransactionsParams,
    TransactionCreateParams,
    TransactionUpdateParams,
    ContractDescription,
    FullContractDescription,
    ContractSearchParams,
    ContractTransactionsParams,
    ERC7702Authorization,
)

class BaseTransactions:
    """Base class for transactions module."""

    def _get_test_url(self, transaction_id: str) -> str:
        """Get the URL for testing a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for testing a transaction
        """
        return f"/transactions/{transaction_id}/test"

    def _get_estimate_url(self, transaction_id: str) -> str:
        """Get the URL for estimating a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for estimating a transaction
        """
        return f"/transactions/{transaction_id}/estimate"

    def _get_execute_url(self, transaction_id: str) -> str:
        """Get the URL for executing a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for executing a transaction
        """
        return f"/transactions/{transaction_id}/execute"

    def _get_read_url(self, transaction_id: str) -> str:
        """Get the URL for reading a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for reading a transaction
        """
        return f"/transactions/{transaction_id}/read"

    def _get_get_url(self, transaction_id: str) -> str:
        """Get the URL for getting a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for getting a transaction
        """
        return f"/transactions/{transaction_id}"

    def _get_list_url(self, business_id: str, params: Optional[Dict[str, Any]] = None) -> str:
        """Get the URL for listing transactions.

        Args:
            business_id: The business ID
            params: Optional filter parameters

        Returns:
            The URL for listing transactions
        """
        url = f"/business/{business_id}/transactions"
        if params:
            query_params = []
            for key, value in params.items():
                if value is not None:
                    query_params.append(f"{key}={value}")
            if query_params:
                url += "?" + "&".join(query_params)
        return url

    def _get_create_url(self, business_id: str) -> str:
        """Get the URL for creating a transaction.

        Args:
            business_id: The business ID

        Returns:
            The URL for creating a transaction
        """
        return f"/business/{business_id}/transactions"

    def _get_import_from_abi_url(self, business_id: str) -> str:
        """Get the URL for importing transactions from an ABI.

        Args:
            business_id: The business ID

        Returns:
            The URL for importing transactions from an ABI
        """
        return f"/business/{business_id}/transactions/abi"

    def _get_contract_transactions_url(self, business_id: str) -> str:
        """Get the URL for creating transactions from a contract description.

        Args:
            business_id: The business ID

        Returns:
            The URL for creating transactions from a contract description
        """
        return f"/business/{business_id}/transactions/contract"

    def _get_contract_search_url(self) -> str:
        """Get the URL for searching contract descriptions.

        Returns:
            The URL for searching contract descriptions
        """
        return "/contracts/descriptions/search"

    def _get_update_url(self, transaction_id: str) -> str:
        """Get the URL for updating a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for updating a transaction
        """
        return f"/transactions/{transaction_id}"

    def _get_delete_url(self, transaction_id: str) -> str:
        """Get the URL for deleting a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for deleting a transaction
        """
        return f"/transactions/{transaction_id}"

    def _get_restore_url(self, transaction_id: str) -> str:
        """Get the URL for restoring a transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The URL for restoring a transaction
        """
        return f"/transactions/{transaction_id}/restore"


class SyncTransactions(BaseTransactions):
    """Synchronous transactions module for the 1Shot API."""

    def __init__(self, client: "Client") -> None:
        """Initialize the transactions module.

        Args:
            client: The synchronous client instance
        """
        self._client = client

    def test(self, transaction_id: str, params: Dict[str, Any]) -> TransactionTestResult:
        """Test a transaction execution. This method simulates the execution of a transaction. No gas will be spent and nothing on chain will change, but it will let you know whether or not an execution would succeed.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction

        Returns:
            The test result, including success status and potential error information

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        response = self._client._request(
            "POST",
            self._get_test_url(transaction_id),
            data={"params": params},
        )
        return TransactionTestResult.model_validate(response)

    def estimate(self, transaction_id: str, params: Dict[str, Any], escrow_wallet_id: Optional[str] = None) -> TransactionEstimate:
        """Estimate the cost of executing a transaction. Returns data about the fees and amount of gas.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction
            escrow_wallet_id: Optional ID of the escrow wallet to use for the estimate

        Returns:
            The cost estimate, including gas amount and fees

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        data: Dict[str, Any] = {"params": params}
        if escrow_wallet_id is not None:
            data["escrowWalletId"] = escrow_wallet_id

        response = self._client._request(
            "POST",
            self._get_estimate_url(transaction_id),
            data=data,
        )
        return TransactionEstimate.model_validate(response)

    def execute(
        self,
        transaction_id: str,
        params: Dict[str, Any],
        escrow_wallet_id: Optional[str] = None,
        memo: Optional[str] = None,
        authorization_list: Optional[List[ERC7702Authorization]] = None,
    ) -> TransactionExecution:
        """Execute a transaction. You can only execute transactions that are payable or nonpayable. Use /read for view and pure transactions.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction
            escrow_wallet_id: Optional ID of the escrow wallet to use
            memo: Optional memo for the execution. You may include any text you like when you execute a transaction, as a note to yourself about why it was done. This text can be JSON or similar if you want to store formatted data.
            authorization_list: Optional list of ERC-7702 authorizations. If you are using ERC-7702, you must provide at least one authorization.

        Returns:
            The execution result

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        data: Dict[str, Any] = {"params": params}
        if escrow_wallet_id is not None:
            data["escrowWalletId"] = escrow_wallet_id
        if memo is not None:
            data["memo"] = memo
        if authorization_list is not None:
            data["authorizationList"] = [auth.model_dump(by_alias=True) for auth in authorization_list]

        response = self._client._request(
            "POST",
            self._get_execute_url(transaction_id),
            data=data,
        )
        return TransactionExecution.model_validate(response)

    def read(self, transaction_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read the result of a view or pure function. This will error on payable and nonpayable transactions.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction

        Returns:
            The function result

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        response = self._client._request(
            "POST",
            self._get_read_url(transaction_id),
            data={"params": params},
        )
        return response

    def get(self, transaction_id: str) -> Transaction:
        """Get a single Transaction via its TransactionId.

        Args:
            transaction_id: The transaction ID

        Returns:
            The transaction

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        response = self._client._request(
            "GET",
            self._get_get_url(transaction_id),
        )
        return Transaction.model_validate(response)

    def list(
        self,
        business_id: str,
        params: Optional[Union[ListTransactionsParams, Dict[str, Any]]] = None,
    ) -> PagedResponse[Transaction]:
        """List transactions for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or ListTransactionsParams instance

        Returns:
            A paged response of transactions

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        if params is not None and not isinstance(params, ListTransactionsParams):
            params = ListTransactionsParams.model_validate(params, by_alias=True, by_name=True)
        dumped_params = params.model_dump(mode='json', by_alias=True) if params else None
        url = self._get_list_url(business_id, dumped_params)
        response = self._client._request("GET", url)
        return PagedResponse[Transaction].model_validate(response)

    def create(
        self,
        business_id: str,
        params: Union[TransactionCreateParams, Dict[str, Any]],
    ) -> Transaction:
        """Create a new Transaction. A Transaction is sometimes referred to as an Endpoint. A Transaction corresponds to a single method on a smart contract.

        Args:
            business_id: The business ID
            params: Transaction creation parameters, either as a dict or TransactionCreateParams instance

        Returns:
            The created transaction

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        if not isinstance(params, TransactionCreateParams):
            params = TransactionCreateParams.model_validate(params, by_alias=True, by_name=True)
        response = self._client._request(
            "POST",
            self._get_create_url(business_id),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return Transaction.model_validate(response)

    def import_from_abi(
        self,
        business_id: str,
        params: Dict[str, Any],
    ) -> List[Transaction]:
        """Import a complete ethereum ABI and creates Transactions for each "function" type entry. Every transaction will be associated with the same Escrow Wallet.

        Args:
            business_id: The business ID
            params: ABI import parameters including:
                - chain: The chain ID
                - contractAddress: The contract address
                - escrowWalletId: The escrow wallet ID
                - abi: The Ethereum ABI
                - name: Optional name of the smart contract
                - description: Optional description of the smart contract
                - tags: Optional array of tags for the smart contract

        Returns:
            The imported transactions

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        response = self._client._request(
            "POST",
            self._get_import_from_abi_url(business_id),
            data=params,
        )
        return [Transaction.model_validate(tx) for tx in response]

    def create_from_contract(
        self,
        business_id: str,
        params: Union[ContractTransactionsParams, Dict[str, Any]],
    ) -> List[Transaction]:
        """Assures that Transactions exist for a given contract. This is based on the verified contract ABI and the highest-ranked Contract Description. If Transactions already exist, they are not modified. If they do not exist, any methods that are in the Contract Description will be created with the details from the Contract Description.

        Args:
            business_id: The business ID
            params: Contract transactions parameters, either as a dict or ContractTransactionsParams instance

        Returns:
            The created transactions

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        if not isinstance(params, ContractTransactionsParams):
            params = ContractTransactionsParams.model_validate(params, by_alias=True, by_name=True)
        response = self._client._request(
            "POST",
            self._get_contract_transactions_url(business_id),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return [Transaction.model_validate(tx) for tx in response]

    def search_contracts(
        self,
        params: Union[ContractSearchParams, Dict[str, Any]],
    ) -> List[FullContractDescription]:
        """Performs a semantic search on contract descriptions to find the most relevant contracts.

        Args:
            params: Search parameters, either as a dict or ContractSearchParams instance

        Returns:
            A list of contract descriptions matching the search query

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        if not isinstance(params, ContractSearchParams):
            params = ContractSearchParams.model_validate(params, by_alias=True, by_name=True)
        response = self._client._request(
            "POST",
            self._get_contract_search_url(),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return [FullContractDescription.model_validate(desc) for desc in response]

    def update(
        self,
        transaction_id: str,
        params: Union[TransactionUpdateParams, Dict[str, Any]],
    ) -> Transaction:
        """Update a Transaction. You can update most of the properties of a transaction via this method, but you can't change the inputs or outputs. Use the Struct API calls for that instead.

        Args:
            transaction_id: The transaction ID
            params: Update parameters, either as a dict or TransactionUpdateParams instance

        Returns:
            The updated transaction

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        if not isinstance(params, TransactionUpdateParams):
            params = TransactionUpdateParams.model_validate(params, by_alias=True, by_name=True)
        response = self._client._request(
            "PUT",
            self._get_update_url(transaction_id),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return Transaction.model_validate(response)

    def delete(self, transaction_id: str) -> None:
        """Delete a transaction.

        Args:
            transaction_id: The transaction ID

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        self._client._request(
            "DELETE",
            self._get_delete_url(transaction_id),
        )

    def restore(self, transaction_id: str) -> Transaction:
        """Restore a deleted transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The restored transaction

        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        response = self._client._request(
            "PUT",
            self._get_restore_url(transaction_id),
        )
        return Transaction.model_validate(response)


class AsyncTransactions(BaseTransactions):
    """Asynchronous transactions module for the 1Shot API."""

    def __init__(self, client: "AsyncClient") -> None:
        """Initialize the transactions module.

        Args:
            client: The asynchronous client instance
        """
        self._client = client

    async def test(self, transaction_id: str, params: Dict[str, Any]) -> TransactionTestResult:
        """Test a transaction execution. This method simulates the execution of a transaction. No gas will be spent and nothing on chain will change, but it will let you know whether or not an execution would succeed.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction

        Returns:
            The test result, including success status and potential error information

        Raises:
            aiohttp.ClientError: If the request fails
        """
        response = await self._client._request(
            "POST",
            self._get_test_url(transaction_id),
            data={"params": params},
        )
        return TransactionTestResult.model_validate(response)

    async def estimate(self, transaction_id: str, params: Dict[str, Any], escrow_wallet_id: Optional[str] = None) -> TransactionEstimate:
        """Estimate the cost of executing a transaction. Returns data about the fees and amount of gas.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction
            escrow_wallet_id: Optional ID of the escrow wallet to use for the estimate

        Returns:
            The cost estimate, including gas amount and fees

        Raises:
            aiohttp.ClientError: If the request fails
        """
        data: Dict[str, Any] = {"params": params}
        if escrow_wallet_id is not None:
            data["escrowWalletId"] = escrow_wallet_id

        response = await self._client._request(
            "POST",
            self._get_estimate_url(transaction_id),
            data=data,
        )
        return TransactionEstimate.model_validate(response)

    async def execute(
        self,
        transaction_id: str,
        params: Dict[str, Any],
        escrow_wallet_id: Optional[str] = None,
        memo: Optional[str] = None,
        authorization_list: Optional[List[ERC7702Authorization]] = None,
    ) -> TransactionExecution:
        """Execute a transaction. You can only execute transactions that are payable or nonpayable. Use /read for view and pure transactions.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction
            escrow_wallet_id: Optional ID of the escrow wallet to use
            memo: Optional memo for the execution. You may include any text you like when you execute a transaction, as a note to yourself about why it was done. This text can be JSON or similar if you want to store formatted data.
            authorization_list: Optional list of ERC-7702 authorizations. If you are using ERC-7702, you must provide at least one authorization.

        Returns:
            The execution result

        Raises:
            aiohttp.ClientError: If the request fails
        """
        data: Dict[str, Any] = {"params": params}
        if escrow_wallet_id is not None:
            data["escrowWalletId"] = escrow_wallet_id
        if memo is not None:
            data["memo"] = memo
        if authorization_list is not None:
            data["authorizationList"] = [auth.model_dump(by_alias=True) for auth in authorization_list]

        response = await self._client._request(
            "POST",
            self._get_execute_url(transaction_id),
            data=data,
        )
        return TransactionExecution.model_validate(response)

    async def read(self, transaction_id: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Read the result of a view or pure function. This will error on payable and nonpayable transactions.

        Args:
            transaction_id: The transaction ID
            params: Parameters for the transaction

        Returns:
            The function result

        Raises:
            aiohttp.ClientError: If the request fails
        """
        response = await self._client._request(
            "POST",
            self._get_read_url(transaction_id),
            data={"params": params},
        )
        return response

    async def get(self, transaction_id: str) -> Transaction:
        """Get a single Transaction via its TransactionId.

        Args:
            transaction_id: The transaction ID

        Returns:
            The transaction

        Raises:
            aiohttp.ClientError: If the request fails
        """
        response = await self._client._request(
            "GET",
            self._get_get_url(transaction_id),
        )
        return Transaction.model_validate(response)

    async def list(
        self,
        business_id: str,
        params: Optional[Union[ListTransactionsParams, Dict[str, Any]]] = None,
    ) -> PagedResponse[Transaction]:
        """List transactions for a business.

        Args:
            business_id: The business ID
            params: Optional filter parameters, either as a dict or ListTransactionsParams instance

        Returns:
            A paged response of transactions

        Raises:
            aiohttp.ClientError: If the request fails
        """
        if params is not None and not isinstance(params, ListTransactionsParams):
            params = ListTransactionsParams.model_validate(params, by_alias=True, by_name=True)
        dumped_params = params.model_dump(mode='json', by_alias=True) if params else None
        url = self._get_list_url(business_id, dumped_params)
        response = await self._client._request("GET", url)
        return PagedResponse[Transaction].model_validate(response)

    async def create(
        self,
        business_id: str,
        params: Union[TransactionCreateParams, Dict[str, Any]],
    ) -> Transaction:
        """Create a new Transaction. A Transaction is sometimes referred to as an Endpoint. A Transaction corresponds to a single method on a smart contract.

        Args:
            business_id: The business ID
            params: Transaction creation parameters, either as a dict or TransactionCreateParams instance

        Returns:
            The created transaction

        Raises:
            aiohttp.ClientError: If the request fails
        """
        if not isinstance(params, TransactionCreateParams):
            params = TransactionCreateParams.model_validate(params, by_alias=True, by_name=True)
        response = await self._client._request(
            "POST",
            self._get_create_url(business_id),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return Transaction.model_validate(response)

    async def import_from_abi(
        self,
        business_id: str,
        params: Dict[str, Any],
    ) -> List[Transaction]:
        """Import a complete ethereum ABI and creates Transactions for each "function" type entry. Every transaction will be associated with the same Escrow Wallet.

        Args:
            business_id: The business ID
            params: ABI import parameters including:
                - chain: The chain ID
                - contractAddress: The contract address
                - escrowWalletId: The escrow wallet ID
                - abi: The Ethereum ABI
                - name: Optional name of the smart contract
                - description: Optional description of the smart contract
                - tags: Optional array of tags for the smart contract

        Returns:
            The imported transactions

        Raises:
            aiohttp.ClientError: If the request fails
        """
        response = await self._client._request(
            "POST",
            self._get_import_from_abi_url(business_id),
            data=params,
        )
        return [Transaction.model_validate(tx) for tx in response]

    async def create_from_contract(
        self,
        business_id: str,
        params: Union[ContractTransactionsParams, Dict[str, Any]],
    ) -> List[Transaction]:
        """Assures that Transactions exist for a given contract. This is based on the verified contract ABI and the highest-ranked Contract Description. If Transactions already exist, they are not modified. If they do not exist, any methods that are in the Contract Description will be created with the details from the Contract Description.

        Args:
            business_id: The business ID
            params: Contract transactions parameters, either as a dict or ContractTransactionsParams instance

        Returns:
            The created transactions

        Raises:
            aiohttp.ClientError: If the request fails
        """
        if not isinstance(params, ContractTransactionsParams):
            params = ContractTransactionsParams.model_validate(params, by_alias=True, by_name=True)
        response = await self._client._request(
            "POST",
            self._get_contract_transactions_url(business_id),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return [Transaction.model_validate(tx) for tx in response]

    async def search_contracts(
        self,
        params: Union[ContractSearchParams, Dict[str, Any]],
    ) -> List[FullContractDescription]:
        """Performs a semantic search on contract descriptions to find the most relevant contracts.

        Args:
            params: Search parameters, either as a dict or ContractSearchParams instance

        Returns:
            A list of contract descriptions matching the search query

        Raises:
            aiohttp.ClientError: If the request fails
        """
        if not isinstance(params, ContractSearchParams):
            params = ContractSearchParams.model_validate(params, by_alias=True, by_name=True)
        response = await self._client._request(
            "POST",
            self._get_contract_search_url(),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return [FullContractDescription.model_validate(desc) for desc in response]

    async def update(
        self,
        transaction_id: str,
        params: Union[TransactionUpdateParams, Dict[str, Any]],
    ) -> Transaction:
        """Update a Transaction. You can update most of the properties of a transaction via this method, but you can't change the inputs or outputs. Use the Struct API calls for that instead.

        Args:
            transaction_id: The transaction ID
            params: Update parameters, either as a dict or TransactionUpdateParams instance

        Returns:
            The updated transaction

        Raises:
            aiohttp.ClientError: If the request fails
        """
        if not isinstance(params, TransactionUpdateParams):
            params = TransactionUpdateParams.model_validate(params, by_alias=True, by_name=True)
        response = await self._client._request(
            "PUT",
            self._get_update_url(transaction_id),
            data=params.model_dump(exclude_none=True, by_alias=True),
        )
        return Transaction.model_validate(response)

    async def delete(self, transaction_id: str) -> None:
        """Delete a transaction.

        Args:
            transaction_id: The transaction ID

        Raises:
            aiohttp.ClientError: If the request fails
        """
        await self._client._request(
            "DELETE",
            self._get_delete_url(transaction_id),
        )

    async def restore(self, transaction_id: str) -> Transaction:
        """Restore a deleted transaction.

        Args:
            transaction_id: The transaction ID

        Returns:
            The restored transaction

        Raises:
            aiohttp.ClientError: If the request fails
        """
        response = await self._client._request(
            "PUT",
            self._get_restore_url(transaction_id),
        )
        return Transaction.model_validate(response) 