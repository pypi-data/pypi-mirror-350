"""Models for transaction executions."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class TransactionExecution(BaseModel):
    """A single execution of a transaction- ie, a function call"""

    id: str = Field(..., description="internal ID of the transaction execution")
    transaction_id: str = Field(..., alias="transactionId", description="internal ID of the transaction")
    api_credential_id: Optional[str] = Field(
        None, 
        alias="apiCredentialId", 
        description="ID of the API Credential used to execute the transaction. Note, this is not the API Key itself. This will be null if a user initiated the execution and not an API Credential"
    )
    api_key: Optional[str] = Field(
        None,
        alias="apiKey",
        description="The actual API key used"
    )
    user_id: Optional[str] = Field(
        None, 
        alias="userId", 
        description="The User ID that executed the transaction. This will be null if an API key was used instead of a user token."
    )
    status: str = Field(
        ...,
        description="Current status of the execution",
        pattern="^(Pending|Submitted|Completed|Retrying|Failed)$",
    )
    chain_transaction_id: Optional[str] = Field(
        None, 
        alias="chainTransactionId", 
        description="The ID of the actual chain transaction in the internal chain service."
    )
    transaction_hash: Optional[str] = Field(
        None, 
        alias="transactionHash", 
        description="The hash of the transaction. Only calculated once the status is Submitted."
    )
    name: str = Field(
        ...,
        description="the name of the associated Transaction. Included as a convienience."
    )
    function_name: str = Field(
        ...,
        alias="functionName",
        description="The functionName of the associated Transaction. Included as a convienience."
    )
    chain: int = Field(
        ...,
        description="The chain ID"
    )
    memo: Optional[str] = Field(
        None, 
        description="Optional text supplied when the transaction is executed. This can be a note to the user about why the execution was done, or formatted information such as JSON that can be used by the user's system."
    )
    completed: Optional[int] = Field(
        None,
        description="The completion timestamp"
    )
    updated: int = Field(..., description="The last update timestamp")
    created: int = Field(..., description="The creation timestamp")
    deleted: bool = Field(..., description="Whether the execution is deleted")


class ExecutionListParams(BaseModel):
    """Parameters for listing executions."""

    page_size: Optional[int] = Field(None, alias="pageSize", description="The size of the page to return. Defaults to 25")
    page: Optional[int] = Field(None, description="Which page to return. This is 1 indexed, and default to the first page, 1")
    chain_id: Optional[int] = Field(None, alias="chainId", description="The specific chain to get the executions for")
    status: Optional[str] = Field(None, description="The status of the executions to return")
    escrow_wallet_id: Optional[str] = Field(None, alias="escrowWalletId", description="The escrow wallet ID to get the executions for")
    transaction_id: Optional[str] = Field(None, alias="transactionId", description="The transaction ID to get the executions for")
    api_credential_id: Optional[str] = Field(None, alias="apiCredentialId", description="The API credential ID to get the executions for")
    user_id: Optional[str] = Field(None, alias="userId", description="The user ID to get the executions for")

    @validator('page')
    def validate_page(cls, v):
        if v is not None and v < 1:
            raise ValueError('Page number must be greater than or equal to 1')
        return v

    @validator('page_size')
    def validate_page_size(cls, v):
        if v is not None and v < 1:
            raise ValueError('Page size must be greater than or equal to 1')
        return v
