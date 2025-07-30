"""Validation utilities for the 1Shot API."""

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator


class UUID(str):
    """A UUID string."""

    @classmethod
    def __get_validators__(cls):
        """Get validators for the UUID type."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> str:
        """Validate a UUID string.

        Args:
            v: The value to validate

        Returns:
            The validated UUID string

        Raises:
            ValueError: If the value is not a valid UUID
        """
        if not isinstance(v, str):
            raise ValueError("UUID must be a string")
        if not v.isalnum() or len(v) != 32:
            raise ValueError("Invalid UUID format")
        return v


class ChainID(int):
    """A chain ID."""

    @classmethod
    def __get_validators__(cls):
        """Get validators for the chain ID type."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> int:
        """Validate a chain ID.

        Args:
            v: The value to validate

        Returns:
            The validated chain ID

        Raises:
            ValueError: If the value is not a valid chain ID
        """
        if not isinstance(v, int):
            raise ValueError("Chain ID must be an integer")
        if v <= 0:
            raise ValueError("Chain ID must be positive")
        return v


class StateMutability(str):
    """A state mutability value."""

    VALID_VALUES = ["nonpayable", "payable", "view", "pure"]

    @classmethod
    def __get_validators__(cls):
        """Get validators for the state mutability type."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> str:
        """Validate a state mutability value.

        Args:
            v: The value to validate

        Returns:
            The validated state mutability value

        Raises:
            ValueError: If the value is not a valid state mutability
        """
        if not isinstance(v, str):
            raise ValueError("State mutability must be a string")
        if v not in cls.VALID_VALUES:
            raise ValueError(f"State mutability must be one of {cls.VALID_VALUES}")
        return v


class ParameterType(str):
    """A parameter type."""

    VALID_VALUES = ["address", "bool", "bytes", "int", "string", "uint", "struct"]

    @classmethod
    def __get_validators__(cls):
        """Get validators for the parameter type."""
        yield cls.validate

    @classmethod
    def validate(cls, v: Any) -> str:
        """Validate a parameter type.

        Args:
            v: The value to validate

        Returns:
            The validated parameter type

        Raises:
            ValueError: If the value is not a valid parameter type
        """
        if not isinstance(v, str):
            raise ValueError("Parameter type must be a string")
        if v not in cls.VALID_VALUES:
            raise ValueError(f"Parameter type must be one of {cls.VALID_VALUES}")
        return v


class BaseParams(BaseModel):
    """Base class for parameter validation."""

    def validate_all(self) -> None:
        """Validate all fields in the model."""
        self.model_validate(self.model_dump()) 