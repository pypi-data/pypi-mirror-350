"""Transaction models for the 1Shot API."""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, validator, constr
from datetime import datetime

# Valid chain IDs from the spec
VALID_CHAIN_IDS = [
    1, 11155111, 42, 137, 43114, 43113, 80002, 100, 56, 1284, 42161, 10, 592, 81, 97, 324, 8453, 84532, 88888, 11297108109, 42220, 130, 480, 81457
]

# Valid state mutability values
VALID_STATE_MUTABILITIES = ['nonpayable', 'payable', 'view', 'pure']

# Valid status values
VALID_STATUSES = ['live', 'archived', 'both']

class ListTransactionsParams(BaseModel):
    """Parameters for listing transactions.
    
    Args:
        page_size: The size of the page to return. Defaults to 25
        page: Which page to return. This is 1 indexed, and defaults to the first page, 1
        chain_id: The specific chain to get transactions for
        name: Filter transactions by name
        status: Filter by deletion status - 'live', 'archived', or 'both'
        contract_address: Filter by contract address
    """
    
    page_size: Optional[int] = Field(None, alias="pageSize", description="The size of the page to return. Defaults to 25")
    page: Optional[int] = Field(None, description="Which page to return. This is 1 indexed, and defaults to the first page, 1")
    chain_id: Optional[int] = Field(None, alias="chainId", description="The specific chain to get transactions for")
    name: Optional[str] = Field(None, description="Filter transactions by name")
    status: Optional[str] = Field(None, description="Filter by deletion status - 'live', 'archived', or 'both'")
    contract_address: Optional[str] = Field(None, alias="contractAddress", description="Filter by contract address")

    @validator('status')
    def validate_status(cls, v):
        if v is not None and v not in VALID_STATUSES:
            raise ValueError(f'Status must be one of {VALID_STATUSES}')
        return v

    @validator('page')
    def validate_page(cls, v):
        if v is not None and v < 1:
            raise ValueError('Page must be greater than or equal to 1')
        return v

    @validator('page_size')
    def validate_page_size(cls, v):
        if v is not None and v < 1:
            raise ValueError('Page size must be greater than or equal to 1')
        return v

    @validator('chain_id')
    def validate_chain_id(cls, v):
        if v is not None and v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v):
        if v is not None:
            if not v.startswith('0x'):
                raise ValueError('Contract address must start with 0x')
            if len(v) != 42:
                raise ValueError('Contract address must be 42 characters long (including 0x)')
        return v


class Transaction(BaseModel):
    """A transaction model representing a single defined transaction, corresponding to a method call on a smart contract on a chain."""

    id: str = Field(..., description="Internal ID of the transaction object. Transactions are sometimes referred to as Endpoints. A Transaction is a single method on a smart contract")
    business_id: str = Field(..., alias="businessId", description="The internal ID of the business. Every object in the API is ultimately scoped to a single Business")
    chain: int = Field(..., description="The ChainId of a supported chain on 1Shot API")
    contract_address: str = Field(..., alias="contractAddress", description="string address of contract")
    escrow_wallet_id: str = Field(..., alias="escrowWalletId", description="The default escrow wallet that will execute this Transaction")
    name: str = Field(..., description="Name of transaction")
    description: str = Field(..., description="Description of transaction")
    function_name: str = Field(..., alias="functionName", description="Name of the function on the contract")
    state_mutability: str = Field(..., alias="stateMutability", description="The state mutability of a Solidity function")
    inputs: List[Dict[str, Any]] = Field(..., description="The input parameters for the transaction function")
    outputs: List[Dict[str, Any]] = Field(..., description="The output parameters for the transaction function")
    callback_url: Optional[str] = Field(None, alias="callbackUrl", description="The current destination for webhooks to be sent when this transaction is executed. Will be null if no webhook is assigned")
    public_key: Optional[str] = Field(None, alias="publicKey", description="The current public key for verifying the integrity of the webhook when this transaction is executed. 1Shot will sign its webhooks with a private key and provide a signature for the webhook that can be validated with this key. It will be null if there is no webhook destination specified")
    updated: int = Field(..., description="Unix timestamp of when the transaction was last updated")
    created: int = Field(..., description="Unix timestamp of when the transaction was created")
    deleted: bool = Field(..., description="Whether the transaction is deleted")

    @validator('chain')
    def validate_chain(cls, v):
        if v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v):
        if not v.startswith('0x'):
            raise ValueError('Contract address must start with 0x')
        if len(v) != 42:
            raise ValueError('Contract address must be 42 characters long (including 0x)')
        return v

    @validator('state_mutability')
    def validate_state_mutability(cls, v):
        if v not in VALID_STATE_MUTABILITIES:
            raise ValueError(f'State mutability must be one of {VALID_STATE_MUTABILITIES}')
        return v

    @validator('callback_url')
    def validate_callback_url(cls, v):
        if v is not None:
            if not v.startswith(('http://', 'https://')):
                raise ValueError('Callback URL must start with http:// or https://')
        return v


class TransactionEstimate(BaseModel):
    """A summary of values required to estimate the cost of executing a transaction."""

    chain: int = Field(..., description="The ChainId of a supported chain on 1Shot API")
    contract_address: str = Field(..., alias="contractAddress", description="string address of contract")
    function_name: str = Field(..., alias="functionName", description="The name of the function on the contract")
    gas_amount: str = Field(..., alias="gasAmount", description="The amount of gas units it will use")
    max_fee_per_gas: Optional[str] = Field(None, alias="maxFeePerGas")
    max_priority_fee_per_gas: Optional[str] = Field(None, alias="maxPriorityFeePerGas")
    gas_price: Optional[str] = Field(None, alias="gasPrice")

    @validator('chain')
    def validate_chain(cls, v):
        if v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v):
        if not v.startswith('0x'):
            raise ValueError('Contract address must start with 0x')
        if len(v) != 42:
            raise ValueError('Contract address must be 42 characters long (including 0x)')
        return v


class TransactionTestResult(BaseModel):
    """The result of running /test on a transaction."""

    success: bool = Field(..., description="Whether or not the transaction would run successfully")
    result: Optional[Dict[str, Any]] = Field(None, description="The result returned by the transaction, if it was successful. When running a test, no changes are made on the blockchain, so these results are hypothetical")
    error: Optional[Dict[str, Any]] = Field(None, description="The error that occurred, if the transaction was not successful")


class ERC7702Authorization(BaseModel):
    """A single authorization for an ERC-7702 transaction. It represents a single potential delegation from an EOA to a contract."""

    address: str = Field(..., description="The contract address that is being authorized to act on behalf of the EOA")
    nonce: str = Field(..., description="The delegation nonce. This starts at 0 and must be positive. The EOA must keep track of this nonce itself")
    chain_id: int = Field(..., alias="chainId", description="The chain ID where the authorization is valid")
    signature: str = Field(..., description="The signature of the authorization, from the EOA that is delegating the authorization to the contract at address")

    @validator('address')
    def validate_address(cls, v):
        if not v.startswith('0x'):
            raise ValueError('Address must start with 0x')
        if len(v) != 42:
            raise ValueError('Address must be 42 characters long (including 0x)')
        return v

    @validator('chain_id')
    def validate_chain_id(cls, v):
        if v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('signature')
    def validate_signature(cls, v):
        if not v.startswith('0x'):
            raise ValueError('Signature must start with 0x')
        if not all(c in '0123456789abcdefABCDEF' for c in v[2:]):
            raise ValueError('Signature must contain only hex characters')
        return v


class TransactionCreateParams(BaseModel):
    """Parameters for creating a new Transaction. A Transaction is sometimes referred to as an Endpoint. A Transaction corresponds to a single method on a smart contract."""
    
    chain: int = Field(..., description="The ChainId of a supported chain on 1Shot API")
    contract_address: str = Field(..., alias="contractAddress", description="string address of contract")
    escrow_wallet_id: str = Field(..., alias="escrowWalletId", description="The ID of the escrow wallet that will execute the transaction")
    name: str = Field(..., description="Name of transaction")
    description: str = Field(..., description="Description of transaction")
    function_name: str = Field(..., alias="functionName", description="Name of the function on the contract")
    state_mutability: str = Field(..., alias="stateMutability", description="The state mutability of a Solidity function")
    inputs: List[Dict[str, Any]] = Field(..., description="The input parameters for the transaction function")
    outputs: List[Dict[str, Any]] = Field(..., description="The output parameters for the transaction function")
    callback_url: Optional[str] = Field(None, alias="callbackUrl", description="The URL to send webhooks to when this transaction is executed. This must be a valid HTTP or HTTPS URL and include the protocol")

    @validator('chain')
    def validate_chain(cls, v):
        if v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v):
        if not v.startswith('0x'):
            raise ValueError('Contract address must start with 0x')
        if len(v) != 42:
            raise ValueError('Contract address must be 42 characters long (including 0x)')
        return v

    @validator('state_mutability')
    def validate_state_mutability(cls, v):
        if v not in VALID_STATE_MUTABILITIES:
            raise ValueError(f'State mutability must be one of {VALID_STATE_MUTABILITIES}')
        return v

    @validator('callback_url')
    def validate_callback_url(cls, v):
        if v is not None:
            if not v.startswith(('http://', 'https://')):
                raise ValueError('Callback URL must start with http:// or https://')
        return v


class TransactionUpdateParams(BaseModel):
    """Parameters for updating a transaction. Allows modification of transaction properties while maintaining its core functionality."""
    
    chain: Optional[int] = Field(None, description="The ChainId of a supported chain on 1Shot API")
    contract_address: Optional[str] = Field(None, alias="contractAddress", description="string address of contract")
    escrow_wallet_id: Optional[str] = Field(None, alias="escrowWalletId", description="The ID of the escrow wallet that will execute the transaction")
    name: Optional[str] = Field(None, description="Name of transaction")
    description: Optional[str] = Field(None, description="Description of transaction")
    function_name: Optional[str] = Field(None, alias="functionName", description="Name of the function on the contract")
    state_mutability: Optional[str] = Field(None, alias="stateMutability", description="The state mutability of a Solidity function")
    callback_url: Optional[str] = Field(None, alias="callbackUrl", description="The URL to send webhooks to when this transaction is executed. This must be a valid HTTP or HTTPS URL and include the protocol")

    @validator('chain')
    def validate_chain(cls, v):
        if v is not None and v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v):
        if v is not None:
            if not v.startswith('0x'):
                raise ValueError('Contract address must start with 0x')
            if len(v) != 42:
                raise ValueError('Contract address must be 42 characters long (including 0x)')
        return v

    @validator('state_mutability')
    def validate_state_mutability(cls, v):
        if v is not None and v not in VALID_STATE_MUTABILITIES:
            raise ValueError(f'State mutability must be one of {VALID_STATE_MUTABILITIES}')
        return v

    @validator('callback_url')
    def validate_callback_url(cls, v):
        if v is not None:
            if not v.startswith(('http://', 'https://')):
                raise ValueError('Callback URL must start with http:// or https://')
        return v


class ContractFunctionParamDescription(BaseModel):
    """A description of a function parameter. This may be an input or an output parameter."""

    index: int = Field(..., description="The index of the parameter. Starts at 0")
    name: str = Field(..., description="The name of the parameter, as defined in the Solidity contract. Input parameters are required to have names; this may be blank for output parameters")
    description: str = Field(..., description="A description of the parameter and its purpose. These descriptions are provided by either humans or AI and are intended for AI agent consumption")
    tags: List[str] = Field(..., description="An array of tag names associated with the function parameter")


class ContractFunctionDescription(BaseModel):
    """The description of a single function on a contract."""

    name: str = Field(..., description="The name of the function. This has to exactly match the name of the function in the Solidity contract, including the case and whitespace")
    description: str = Field(..., description="A human provided description of the function, what it does, and a basic overview of its parameters")
    tags: List[str] = Field(..., description="An array of tag names provided to the contract function")
    inputs: List[ContractFunctionParamDescription] = Field(..., description="An array of input parameters for the function. All inputs are required to be named")
    outputs: List[ContractFunctionParamDescription] = Field(..., description="An array of input parameters for the function. All inputs are required to be named")


class ContractDescription(BaseModel):
    """A description of a contract, designed to be used for contract discovery by AI agents."""

    id: str = Field(..., description="Internal ID of the contract description")
    user_id: str = Field(..., alias="userId", description="ID of the user that created")
    chain: int = Field(..., description="The ChainId of a supported chain on 1Shot API")
    contract_address: str = Field(..., alias="contractAddress", description="string address of contract")
    name: str = Field(..., description="The name of the contract. This is human provided and has no technical significance")
    description: str = Field(..., description="The human provided description of what the contract is and does, and the top level")
    tags: List[str] = Field(..., description="An array of tag names provided to the contract")
    updated: int = Field(..., description="Unix timestamp of when the contract description was last updated")
    created: int = Field(..., description="Unix timestamp of when the contract description was created")

    @validator('chain')
    def validate_chain(cls, v):
        if v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v):
        if not v.startswith('0x'):
            raise ValueError('Contract address must start with 0x')
        if len(v) != 42:
            raise ValueError('Contract address must be 42 characters long (including 0x)')
        return v


class FullContractDescription(ContractDescription):
    """A description of a smart contract, including all functions and parameters."""

    functions: List[ContractFunctionDescription] = Field(..., description="An array of Contract Function Descriptions, describing each function on the contract")


class ContractSearchParams(BaseModel):
    """Parameters for searching contract descriptions."""

    query: str = Field(..., description="A free-form query to search for contracts. This uses semantic search to find the most relevant contracts")
    chain: Optional[int] = Field(None, description="The ChainId of a supported chain on 1Shot API")

    @validator('chain')
    def validate_chain(cls, v):
        if v is not None and v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v


class ContractTransactionsParams(BaseModel):
    """Parameters for creating transactions from a contract description."""

    chain: int = Field(..., description="The ChainId of a supported chain on 1Shot API")
    contract_address: str = Field(..., alias="contractAddress", description="string address of contract")
    escrow_wallet_id: str = Field(..., alias="escrowWalletId", description="The ID of the escrow wallet that will execute the transactions")

    @validator('chain')
    def validate_chain(cls, v):
        if v not in VALID_CHAIN_IDS:
            raise ValueError(f'Chain ID must be one of {VALID_CHAIN_IDS}')
        return v

    @validator('contract_address')
    def validate_contract_address(cls, v):
        if not v.startswith('0x'):
            raise ValueError('Contract address must start with 0x')
        if len(v) != 42:
            raise ValueError('Contract address must be 42 characters long (including 0x)')
        return v 