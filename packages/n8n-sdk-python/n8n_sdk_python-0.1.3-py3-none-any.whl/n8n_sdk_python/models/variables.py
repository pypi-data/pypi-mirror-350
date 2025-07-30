"""
n8n variables data models.
Define workflow variables related data structures.
"""

from enum import Enum
from datetime import datetime
from typing import Optional, Any

from pydantic import Field

from .base import N8nBaseModel


class VariableType(str, Enum):
    """Variable type enum, defines the variable data types supported by the system"""
    STRING = "string"  # String type, the most commonly used variable type
    NUMBER = "number"  # Number type, used for numerical calculations
    BOOLEAN = "boolean"  # Boolean type, represents true/false values
    JSON = "json"  # JSON type, used for complex data structures


class Variable(N8nBaseModel):
    """Variable data model, represents an environment variable in the system
    
    Corresponds to the response data item of GET /variables
    """
    id: str = Field(..., description="Unique identifier of the variable")
    key: str = Field(..., description="Variable key name, used in workflows")
    value: Any = Field(..., description="Variable value, can be any type depending on 'type'")
    type: Optional[VariableType] = Field(VariableType.STRING, description="Variable data type, default is string")
    description: Optional[str] = Field(None, description="Variable description, helps understand the variable's purpose")
    createdAt: Optional[datetime] = Field(None, description="Variable creation time")
    updatedAt: Optional[datetime] = Field(None, description="Variable last update time")


class VariableCreate(N8nBaseModel):
    """Create variable request model
    
    Corresponds to the request body of POST /variables
    """
    key: str = Field(..., description="Variable key name, must be unique, used for reference in workflows")
    value: str = Field(..., description="Initial value of the variable, API requires string type")


class VariableUpdate(N8nBaseModel):
    """Update variable request model
    
    Corresponds to the request body of variable update API (although not explicitly defined in API docs)
    """
    key: Optional[str] = Field(None, description="New key name for the variable")
    value: Optional[Any] = Field(None, description="New value for the variable")
    type: Optional[VariableType] = Field(None, description="New type for the variable")
    description: Optional[str] = Field(None, description="New description for the variable")


class VariablesList(N8nBaseModel):
    """Variables list response model
    
    Corresponds to the complete response of GET /variables
    """
    data: list[Variable] = Field(..., description="List of variables")
    nextCursor: Optional[str] = Field(None, description="Pagination cursor, used to get the next page of data")
    count: Optional[int] = Field(None, description="Total number of variables") 