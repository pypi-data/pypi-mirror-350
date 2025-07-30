"""
n8n Credentials API data models.
Defines the data structures for credentials, including credential types, data, and other related information.
"""

from datetime import datetime
from typing import Any, Optional, Union

from pydantic import Field, validator, RootModel

from .base import N8nBaseModel


class CredentialType(N8nBaseModel):
    """Credential type basic information, describes available credential types and their properties"""
    id: str = Field(..., description="Unique identifier of the credential type, usually corresponding to node type name")
    name: str = Field(..., description="Name of the credential type, such as 'github', 'slack', etc.")
    displayName: Optional[str] = Field(None, description="Friendly display name of the credential type, used in the user interface")

class CredentialDataSchemaResponse(N8nBaseModel):
    """Credential data structure description, used for automatically generating credential forms and validating data
    
    Corresponds to the response of GET /credentials/schema/{credentialTypeName}
    """
    type: str = Field("object", description="Schema data type, usually 'object'")
    properties: dict[str, Any] = Field(..., description="Defines credential properties and their data types, constraints, etc.")
    required: Optional[list[str]] = Field(None, description="List of property names that must be provided")
    additionalProperties: Optional[Union[bool, dict[str, Any]]] = Field(False, description="Whether additional properties are allowed, or schema definition for additional properties")

class CredentialTransferRequest(N8nBaseModel):
    """Credential transfer request model, used to transfer credential to another project
    
    Corresponds to the request body of PUT /credentials/{id}/transfer
    """
    destinationProjectId: str = Field(..., description="Unique identifier of the destination project, credential will be transferred to this project")

class NodeAccess(N8nBaseModel):
    """Node access configuration, defines which node types can use this credential"""
    nodeType: str = Field(..., description="Node type name that can access this credential")
    date: Optional[Union[str, datetime]] = Field(None, description="Date when access permission was granted")

class CredentialTypeProperty(N8nBaseModel):
    """Credential type property definition, describes each configuration item of a credential type"""
    name: str = Field(..., description="Technical name of the property, such as 'apiKey'")
    displayName: str = Field(..., description="Display name of the property, such as 'API Key'")
    type: str = Field(..., description="Data type of the property, such as 'string', 'number', 'boolean'")
    default: Optional[Any] = Field(None, description="Default value of the property, if user doesn't provide one")
    required: Optional[bool] = Field(False, description="Whether this property is required")
    description: Optional[str] = Field(None, description="Detailed description of the property, typically used for tooltips")
    placeholder: Optional[str] = Field(None, description="Placeholder text displayed in the input field")
    options: Optional[list[dict[str, Any]]] = Field(None, description="List of possible values for the property, used for dropdown selection")
    typeOptions: Optional[dict[str, Any]] = Field(None, description="Type-specific options, such as input validation rules")

class CredentialTypeDescription(N8nBaseModel):
    """Complete credential type description, contains all metadata related to a credential type"""
    name: str = Field(..., description="Technical name of the credential type")
    displayName: str = Field(..., description="Display name of the credential type")
    description: Optional[str] = Field(None, description="Detailed description of the credential type")
    icon: Optional[str] = Field(None, description="Icon of the credential type")
    documentationUrl: Optional[str] = Field(None, description="Documentation URL for the credential type")
    properties: list[CredentialTypeProperty] = Field(default_factory=list, description="All configurable properties of the credential type")
    required: Optional[list[str]] = Field(None, description="List of property names that must be provided")
    authenticate: Optional[dict[str, Any]] = Field(None, description="Authentication configuration for the credential type")

class CredentialData(N8nBaseModel, RootModel[dict[str, Any]]):
    """Credential data, stores actual authentication information such as API keys, usernames/passwords, etc.
    
    Structure varies by credential type, typically encrypted by the system
    """
    pass

class CredentialListItem(N8nBaseModel):
    """Credential list item, represents a single item in a credential list"""
    id: str = Field(..., description="Unique identifier of the credential")
    name: str = Field(..., description="Friendly name of the credential, named by the user")
    type: str = Field(..., description="Type of the credential, such as 'github', 'slack'")
    nodesAccess: list[NodeAccess] = Field(default_factory=list, description="List of node types allowed to use this credential")
    createdAt: Union[str, datetime] = Field(..., description="Time when the credential was created")
    updatedAt: Union[str, datetime] = Field(..., description="Time when the credential was last updated")
    sharedWith: Optional[list[dict[str, Any]]] = Field(None, description="List of users this credential is shared with")

class CredentialDetail(CredentialListItem):
    """Credential details, contains full credential information and its data"""
    data: Optional[CredentialData] = Field(None, description="Actual data of the credential, may be partially masked")

class CredentialTestResult(N8nBaseModel):
    """Credential test result, represents the result of testing a credential's validity"""
    status: str = Field(..., description="Status of the test, such as 'success' or 'error'")
    message: Optional[str] = Field(None, description="Detailed explanation of the test result or error message")

class CredentialSharing(N8nBaseModel):
    """Credential sharing settings, defines how to share credential with other users"""
    user: Optional[dict[str, Any]] = Field(None, description="Information about the shared user, including ID and name")
    role: Optional[str] = Field(None, description="User's role and permissions for this credential")
    date: Optional[Union[str, datetime]] = Field(None, description="Date when the sharing setting was created or updated")

class CredentialShort(N8nBaseModel):
    """Brief credential information, used for list display, doesn't include sensitive data
    
    This model corresponds to the response of POST /credentials
    """
    id: str = Field(..., description="Unique identifier of the credential")
    name: str = Field(..., description="Friendly name of the credential")
    type: str = Field(..., description="Type name of the credential")
    nodesAccess: Optional[list[NodeAccess]] = Field(None, description="Node types that can use this credential")
    createdAt: Union[str, datetime] = Field(..., description="Credential creation time")
    updatedAt: Union[str, datetime] = Field(..., description="Credential update time")
    sharedWith: Optional[list[CredentialSharing]] = Field(None, description="Sharing configuration of the credential")

class Credential(CredentialShort):
    """Complete credential model, contains all credential-related information
    
    This model may be used for internal or detailed views
    """
    data: dict[str, Any] = Field(default_factory=dict, description="Actual data of the credential, typically masked")
    ownedBy: Optional[dict[str, Any]] = Field(None, description="Owner information of the credential")

class CredentialCreate(N8nBaseModel):
    """Create credential request model
    
    Corresponds to the request body of POST /credentials
    """
    name: str = Field(..., description="Name of the new credential, used for identification and display")
    type: str = Field(..., description="Type of the credential, such as 'github', 'slack'")
    data: dict[str, Any] = Field(default_factory=dict, description="Actual data of the credential, such as API keys, usernames/passwords, etc.")
    nodesAccess: Optional[list[NodeAccess]] = Field(None, description="Node types allowed to use this credential")
    sharedWith: Optional[list[dict[str, Any]]] = Field(None, description="Initial sharing settings")

class CredentialUpdate(N8nBaseModel):
    """Update credential request model"""
    name: Optional[str] = Field(None, description="New name for the credential")
    data: Optional[dict[str, Any]] = Field(None, description="Updated credential data")
    nodesAccess: Optional[list[NodeAccess]] = Field(None, description="Updated node access configuration")
    sharedWith: Optional[list[dict[str, Any]]] = Field(None, description="Updated sharing settings")

class CredentialTest(N8nBaseModel):
    """Credential test request and result model"""
    credential_id: str = Field(..., description="ID of the credential to test")
    success: bool = Field(..., description="Test result, true indicates success, false indicates failure")
    message: Optional[str] = Field(None, description="Detailed explanation of the test result")
    details: Optional[dict[str, Any]] = Field(None, description="Detailed information about the test, such as error stack")

class CredentialTypeList(N8nBaseModel):
    """Credential type list model, used to get all available credential types"""
    count: int = Field(..., description="Total number of credential types")
    types: dict[str, CredentialTypeDescription] = Field(default_factory=dict, description="Dictionary of credential types, key is type name")