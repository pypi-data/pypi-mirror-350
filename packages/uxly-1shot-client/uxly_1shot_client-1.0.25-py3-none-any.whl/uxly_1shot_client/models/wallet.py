"""Wallet models for the 1Shot API."""

from typing import Dict, List, Optional

from pydantic import BaseModel, Field, validator


class AccountBalanceDetails(BaseModel):
    """Account balance details model."""

    type: int = Field(..., description="The chain technology type")
    ticker: str = Field(..., description="The token ticker")
    chain_id: int = Field(..., alias="chainId", description="The chain ID")
    token_address: str = Field(..., alias="tokenAddress", description="The token address")
    account_address: str = Field(..., alias="accountAddress", description="The account address")
    balance: str = Field(..., description="The balance of the token as a Big Number String")
    decimals: int = Field(..., description="The number of decimals in the balance. Determined by the token type.")


class EscrowWallet(BaseModel):
    """Escrow wallet stored by chain service"""

    id: str = Field(..., description="internal ID of the escrowWallet object")
    account_address: str = Field(..., alias="accountAddress", description="string address of a wallet insight platform holds keys for")
    business_id: Optional[str] = Field(None, alias="businessId", description="The business ID that owns this wallet. Admin escrow wallets will not have this value. An escrow wallet will have either a user ID or a business ID.")
    user_id: Optional[str] = Field(None, alias="userId", description="The User ID of the person that owns this wallet. Admin escrow wallets will not have this value. An escrow wallet will have either a user ID or a business ID.")
    chain_id: int = Field(..., alias="chainId", description="The chain ID")
    name: str = Field(..., description="The name of the escrow wallet.")
    description: Optional[str] = Field(None, description="Optional description of the escrow wallet, can be used to describe it's purpose.")
    is_admin: bool = Field(..., alias="isAdmin", description="Whether or not the escrow wallet is an admin escrow wallet, used for internal purposes.")
    account_balance_details: Optional[AccountBalanceDetails] = Field(
        None, 
        alias="accountBalanceDetails", 
        description="The account balance details"
    )
    updated: int = Field(..., description="The last update timestamp")
    created: int = Field(..., description="The creation timestamp")


class WalletListParams(BaseModel):
    """Parameters for listing wallets."""

    chain_id: Optional[int] = Field(None, alias="chainId", description="The specific chain to get the wallets for")
    page_size: Optional[int] = Field(None, alias="pageSize", description="The size of the page to return. Defaults to 25")
    page: Optional[int] = Field(None, description="Which page to return. This is 1 indexed, and default to the first page, 1")
    name: Optional[str] = Field(None, description="Filters on the name of the escrow wallet.")

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


class WalletCreateParams(BaseModel):
    """Parameters for creating a wallet."""

    chain: int = Field(..., description="The chain ID to create the wallet on")
    name: str = Field(..., description="The name of the escrow wallet")
    description: Optional[str] = Field(None, description="A description of the escrow wallet, such as it's intended use. This is for reference only.")


class WalletUpdateParams(BaseModel):
    """Parameters for updating a wallet."""

    name: Optional[str] = Field(None, description="The name of the escrow wallet")
    description: Optional[str] = Field(None, description="Optional description of the escrow wallet, can be used to describe it's purpose") 