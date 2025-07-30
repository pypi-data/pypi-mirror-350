"""Struct models for the 1Shot API."""

from typing import Any, Dict, List, Optional, Union
from enum import Enum

from pydantic import BaseModel, Field, validator


class ESolidityAbiParameterType(str, Enum):
    """Valid Solidity ABI parameter types."""
    ADDRESS = "address"
    BOOL = "bool"
    BYTES = "bytes"
    BYTES_FIXED = "bytes<M>"
    INT = "int"
    INT_FIXED = "int<M>"
    UINT = "uint"
    UINT_FIXED = "uint<M>"
    STRING = "string"
    STRUCT = "struct"
    TUPLE = "tuple"


class SolidityStructParam(BaseModel):
    """A single defined parameter for a transaction after it has been created."""

    id: str = Field(..., description="Internal ID of the parameter.")
    struct_id: str = Field(..., alias="structId", description="Internal ID struct that owns this parameter.")
    name: str = Field(..., description="The parameter name")
    description: Optional[str] = Field(None, description="Description of the parameter")
    type: ESolidityAbiParameterType = Field(..., description="The parameter type")
    index: int = Field(..., description="This is the relative index in the contract function. It should start at 0, and must not skip any numbers.")
    value: Optional[str] = Field(None, description="This is an optional, static value for the parameter. If you set this, you will never be required or able to pass a value for this parameter when you execute the transaction, it will use the set value. This is useful for creating dedicated endpoints with specific functionalities, particularly when tied to API Credentials that can only execute specific transactions. For example, you can have a 'transfer' transaction that is hardcoded to a specific amount, or to a specific receiver address.")
    type_size: Optional[int] = Field(None, alias="typeSize", description="This is an optional field that specifies the main size of the Solidity type. For example, if your type is uint, by default it is a uint256. If you want a uint8 instead, set this value to 8. It works for int, uint, fixed, ufixed, and bytes types. Valid values for bytes are 1 to 32, for others it is 256 % 8")
    type_size2: Optional[int] = Field(None, alias="typeSize2", description="This is identical to typeSize but only used for fixed and ufixed sizes. This is the second size of the fixed field, for example, fixed(typeSize)x(typeSize2).")
    is_array: bool = Field(..., alias="isArray", description="If this parameter is an array type set this to true. By default, arrays can be of any size so you don't need to set arraySize.")
    array_size: Optional[int] = Field(None, alias="arraySize", description="If the parameter is a fixed size array, set this value.")
    type_struct_id: Optional[str] = Field(None, alias="typeStructId", description="The ID of the sub-struct if the type is 'struct'. When creating a param, you must set only one of either typeStructId (to re-use an existing Solidity Struct) or typeStruct (creates a new struct for the param)")
    type_struct: Optional["SolidityStruct"] = Field(None, alias="typeStruct", description="The sub-struct if the type is 'struct', which will be created for use by this parameter. When creating a param, you must set only one of either typeStructId (to re-use an existing Solidity Struct) or typeStruct (creates a new struct for the param)")
    is_optional: bool = Field(False, alias="isOptional", description="Whether the parameter is optional")
    default_value: Optional[str] = Field(None, alias="defaultValue", description="The default value if optional")

    @validator('type_size')
    def validate_type_size(cls, v, values):
        if v is not None:
            if values.get('type') == ESolidityAbiParameterType.BYTES:
                if not 1 <= v <= 32:
                    raise ValueError('For bytes type, typeSize must be between 1 and 32')
            elif values.get('type') in [ESolidityAbiParameterType.INT, ESolidityAbiParameterType.UINT]:
                if v % 8 != 0 or v > 256:
                    raise ValueError('For int/uint types, typeSize must be a multiple of 8 and not exceed 256')
        return v

    @validator('type_struct_id', 'type_struct')
    def validate_struct_reference(cls, v, values):
        if values.get('type') == ESolidityAbiParameterType.STRUCT:
            if not (values.get('type_struct_id') or values.get('type_struct')):
                raise ValueError('For struct type, either typeStructId or typeStruct must be provided')
            if values.get('type_struct_id') and values.get('type_struct'):
                raise ValueError('For struct type, only one of typeStructId or typeStruct can be provided')
        return v


class SolidityStruct(BaseModel):
    """A struct object as defined in solidity ABI"""

    id: str = Field(..., description="Internal ID of the struct.")
    business_id: str = Field(..., alias="businessId", description="Internal ID of the business that owns this struct")
    name: str = Field(..., description="The name of the struct. Structs are used to define the parameters of a transaction, but these structs don't have names.")
    params: List[SolidityStructParam] = Field(..., description="The struct parameters")
    updated: int = Field(..., description="The last update timestamp")
    created: int = Field(..., description="The creation timestamp")
    deleted: bool = Field(..., description="Whether the struct is deleted")


class NewSolidityStructParam(BaseModel):
    """Parameters for creating a new struct parameter."""

    name: str = Field(..., description="The parameter name")
    description: Optional[str] = Field(None, description="Description of the parameter")
    type: ESolidityAbiParameterType = Field(..., description="The parameter type")
    index: int = Field(..., description="This is the relative index in the contract function. It should start at 0, and must not skip any numbers.")
    value: Optional[str] = Field(None, description="This is an optional, static value for the parameter. If you set this, you will never be required or able to pass a value for this parameter when you execute the transaction, it will use the set value.")
    type_size: Optional[int] = Field(None, alias="typeSize", description="This is an optional field that specifies the main size of the Solidity type.")
    type_size2: Optional[int] = Field(None, alias="typeSize2", description="This is identical to typeSize but only used for fixed and ufixed sizes.")
    is_array: bool = Field(..., alias="isArray", description="If this parameter is an array type set this to true.")
    array_size: Optional[int] = Field(None, alias="arraySize", description="If the parameter is a fixed size array, set this value.")
    type_struct_id: Optional[str] = Field(None, alias="typeStructId", description="The ID of the sub-struct if the type is 'struct'.")
    type_struct: Optional[Dict[str, Any]] = Field(None, alias="typeStruct", description="The sub-struct if the type is 'struct'.")

    @validator('type_size')
    def validate_type_size(cls, v, values):
        if v is not None:
            if values.get('type') == ESolidityAbiParameterType.BYTES:
                if not 1 <= v <= 32:
                    raise ValueError('For bytes type, typeSize must be between 1 and 32')
            elif values.get('type') in [ESolidityAbiParameterType.INT, ESolidityAbiParameterType.UINT]:
                if v % 8 != 0 or v > 256:
                    raise ValueError('For int/uint types, typeSize must be a multiple of 8 and not exceed 256')
        return v

    @validator('type_struct_id', 'type_struct')
    def validate_struct_reference(cls, v, values):
        if values.get('type') == ESolidityAbiParameterType.STRUCT:
            if not (values.get('type_struct_id') or values.get('type_struct')):
                raise ValueError('For struct type, either typeStructId or typeStruct must be provided')
            if values.get('type_struct_id') and values.get('type_struct'):
                raise ValueError('For struct type, only one of typeStructId or typeStruct can be provided')
        return v


class StructUpdateParams(BaseModel):
    """Parameters for updating a struct."""

    name: str = Field(..., description="The new name for the struct")


class StructParamUpdateRequest(BaseModel):
    """Parameters for updating a struct parameter."""

    id: str = Field(..., description="The parameter ID")
    name: Optional[str] = Field(None, description="The parameter name")
    description: Optional[str] = Field(None, description="The parameter description")
    type: Optional[ESolidityAbiParameterType] = Field(None, description="The parameter type")
    index: Optional[int] = Field(None, description="The parameter index")
    value: Optional[str] = Field(None, description="The parameter value")
    type_size: Optional[int] = Field(None, alias="typeSize", description="The parameter type size")
    type_size2: Optional[int] = Field(None, alias="typeSize2", description="The parameter type size 2")
    is_array: Optional[bool] = Field(None, alias="isArray", description="Whether the parameter is an array")
    array_size: Optional[int] = Field(None, alias="arraySize", description="The array size")
    type_struct_id: Optional[str] = Field(None, alias="typeStructId", description="The type struct ID")
    type_struct: Optional[Dict[str, Any]] = Field(None, alias="typeStruct", description="The type struct")

    @validator('type_size')
    def validate_type_size(cls, v, values):
        if v is not None and values.get('type'):
            if values.get('type') == ESolidityAbiParameterType.BYTES:
                if not 1 <= v <= 32:
                    raise ValueError('For bytes type, typeSize must be between 1 and 32')
            elif values.get('type') in [ESolidityAbiParameterType.INT, ESolidityAbiParameterType.UINT]:
                if v % 8 != 0 or v > 256:
                    raise ValueError('For int/uint types, typeSize must be a multiple of 8 and not exceed 256')
        return v

    @validator('type_struct_id', 'type_struct')
    def validate_struct_reference(cls, v, values):
        if values.get('type') == ESolidityAbiParameterType.STRUCT:
            if not (values.get('type_struct_id') or values.get('type_struct')):
                raise ValueError('For struct type, either typeStructId or typeStruct must be provided')
            if values.get('type_struct_id') and values.get('type_struct'):
                raise ValueError('For struct type, only one of typeStructId or typeStruct can be provided')
        return v


class StructListParams(BaseModel):
    """Parameters for listing structs."""

    page_size: Optional[int] = Field(None, alias="pageSize", description="The size of the page to return. Defaults to 25")
    page: Optional[int] = Field(None, description="Which page to return. This is 1 indexed, and default to the first page, 1")

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


class StructCreateParams(BaseModel):
    """Parameters for creating a struct."""

    name: str = Field(..., description="The name of the struct")
    description: Optional[str] = Field(None, description="A description of the struct")
    params: List[SolidityStructParam] = Field(..., description="The parameters of the struct")


# Update the forward reference
SolidityStructParam.model_rebuild() 