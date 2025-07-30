from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field

class Log(BaseModel):
    type: str = Field(..., alias="_type")
    address: str
    block_hash: str = Field(..., alias="blockHash")
    block_number: int = Field(..., alias="blockNumber")
    data: str
    index: int
    topics: List[str]
    transaction_hash: str = Field(..., alias="transactionHash")
    transaction_index: int = Field(..., alias="transactionIndex")

class TransactionReceipt(BaseModel):
    type: str = Field(..., alias="_type")
    blob_gas_price: Optional[str] = Field(None, alias="blobGasPrice")
    blob_gas_used: Optional[str] = Field(None, alias="blobGasUsed")
    block_hash: str = Field(..., alias="blockHash")
    block_number: int = Field(..., alias="blockNumber")
    contract_address: Optional[str] = Field(None, alias="contractAddress")
    cumulative_gas_used: str = Field(..., alias="cumulativeGasUsed")
    from_: str = Field(..., alias="from")
    gas_price: str = Field(..., alias="gasPrice")
    gas_used: str = Field(..., alias="gasUsed")
    hash: str
    index: int
    logs: List[Log]
    logs_bloom: str = Field(..., alias="logsBloom")
    status: int
    to: str

class FragmentInput(BaseModel):
    array_children: Optional[None] = Field(None, alias="arrayChildren")  # Matches null in JSON
    array_length: Optional[None] = Field(None, alias="arrayLength")
    base_type: str = Field(..., alias="baseType")
    components: Optional[None]
    indexed: bool
    name: str
    type: str

class Fragment(BaseModel):
    anonymous: bool
    inputs: List[FragmentInput]
    name: str
    type: str

class ParsedLogEntry(BaseModel):
    args: List[Union[str, None]]  # Some values might be null
    fragment: Fragment
    name: str
    signature: str
    topic: str

class Data(BaseModel):
    business_id: str = Field(..., alias="businessId")
    chain: int
    logs: Optional[List[ParsedLogEntry]] = None
    transaction_execution_id: str = Field(..., alias="transactionExecutionId")
    transaction_execution_memo: Optional[str] = Field(None, alias="transactionExecutionMemo")
    transaction_id: str = Field(..., alias="transactionId")
    transaction_receipt: Optional[TransactionReceipt] = Field(None, alias="transactionReceipt")
    user_id: Optional[str] = Field(None, alias="userId")

class WebhookPayload(BaseModel):
    event_name: str = Field(..., alias="eventName")
    data: Data
    timestamp: int
    api_version: int = Field(..., alias="apiVersion")
    signature: str