"""
N8n Credential API client for managing authentication credentials.

This module provides a client for interacting with the n8n Credential API,
enabling operations such as creating, retrieving, updating, testing, and
deleting credentials, as well as retrieving credential type information.
"""

from typing import Any, Optional
from pydantic import ValidationError

from ..client.base import BaseClient
from ..models.credentials import (
    CredentialListItem,
    CredentialDetail,
    CredentialTestResult,
    CredentialTypeDescription,
    CredentialTypeList,
    CredentialShort,
    CredentialDataSchemaResponse,
    CredentialCreate
)
from ..models.base import N8nBaseModel
from ..utils.logger import log


class CredentialClient(BaseClient):
    """
    Client for interacting with the n8n Credential API.
    
    Provides methods for credential management, including creating, retrieving,
    updating, testing, and deleting credentials, as well as retrieving credential
    type information and schemas.
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize the credential client.
        
        Args:
            base_url: Base URL for the n8n API, defaults to environment variable or localhost
            api_key: Authentication key for n8n API, defaults to environment variable
        """
        super().__init__(base_url=base_url, api_key=api_key)
        self._credential_types_cache = None
    
    async def get_credentials(self, credential_type: Optional[str] = None) -> list[CredentialListItem]:
        """
        Retrieve a list of credentials from the n8n instance.
        
        Args:
            credential_type: Optional filter to retrieve credentials of a specific type
            
        Returns:
            A list of credential objects containing basic credential information
            
        Note:
            This method catches exceptions and returns an empty list on error
        """
        params: dict[str, Any] = {}
        if credential_type:
            params["type"] = credential_type
        
        try:
            response = await self.get("/v1/credentials", params=params)
            credentials = []
            for item in response.get("data", []):
                credentials.append(CredentialListItem(**item))
            return credentials
        except Exception as e:
            log.error(f"Failed to retrieve credentials list: {str(e)}")
            return []
    
    async def get_credential(self, credential_id: str) -> Optional[CredentialDetail]:
        """
        Retrieve detailed information about a specific credential.
        
        Args:
            credential_id: The ID of the credential to retrieve
            
        Returns:
            A credential detail object if found, None otherwise
            
        Note:
            This method catches exceptions and returns None on error
        """
        try:
            response = await self.get(f"/v1/credentials/{credential_id}")
            if response:
                return CredentialDetail(**response)
            return None
        except Exception as e:
            log.error(f"Failed to retrieve credential {credential_id}: {str(e)}")
            return None
    
    async def create_credential(
        self,
        name: str,
        credential_type: str,
        data: dict[str, Any]
    ) -> CredentialShort:
        """
        Create a new credential in the n8n instance.
        
        Args:
            name: The name for the credential
            credential_type: The type of credential to create
            data: The credential data containing authentication information
            
        Returns:
            A credential object representing the created credential
            
        Raises:
            N8nAPIError: If the API request fails
            
        API Docs: https://docs.n8n.io/api/v1/credentials/#create-a-credential
        """
        payload = CredentialCreate(name=name, type=credential_type, data=data).model_dump()
        response_data = await self.post(endpoint="/v1/credentials", json=payload)
        return CredentialShort(**response_data)
    
    async def update_credential(self, credential_id: str, credential_data: dict[str, Any]) -> Optional[CredentialDetail]:
        """
        Update an existing credential in the n8n instance.
        
        Args:
            credential_id: The ID of the credential to update
            credential_data: The updated credential data
            
        Returns:
            An updated credential detail object if successful, None otherwise
            
        Note:
            This method catches exceptions and returns None on error
        """
        try:
            response = await self.patch(f"/v1/credentials/{credential_id}", json=credential_data)
            if response:
                return CredentialDetail(**response)
            return None
        except Exception as e:
            log.error(f"Failed to update credential {credential_id}: {str(e)}")
            return None
    
    async def delete_credential(
        self,
        credential_id: str
    ) -> CredentialShort:
        """
        Delete a credential from the n8n instance.
        
        Args:
            credential_id: The ID of the credential to delete
            
        Returns:
            A credential object representing the deleted credential
            
        Raises:
            N8nAPIError: If the credential is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/credentials/#delete-credential-by-id
        """
        response_data = await self.delete(endpoint=f"/v1/credentials/{credential_id}")
        return CredentialShort(**response_data)
    
    async def test_credential(self, credential_id: str) -> Optional[CredentialTestResult]:
        """
        Test if a credential is valid and can authenticate successfully.
        
        Args:
            credential_id: The ID of the credential to test
            
        Returns:
            A test result object indicating success or failure with a message
            
        Note:
            This method catches exceptions and returns a failure result on error
        """
        try:
            response = await self.post(f"/v1/credentials/{credential_id}/test")
            if response:
                return CredentialTestResult(
                    status="success" if response.get("status", "").lower() != "error" else "error",
                    message=response.get("message")
                )
            return None
        except Exception as e:
            log.error(f"Failed to test credential {credential_id}: {str(e)}")
            return CredentialTestResult(status="error", message=str(e))
    
    async def get_credential_types(self, use_cache: bool = True) -> dict[str, CredentialTypeDescription]:
        """
        Retrieve all available credential types from the n8n instance.
        
        Args:
            use_cache: Whether to use cached results if available
            
        Returns:
            A dictionary mapping credential type names to their descriptions
            
        Note:
            This method catches exceptions and returns an empty dictionary on error
        """
        if use_cache and self._credential_types_cache is not None:
            return self._credential_types_cache
        
        try:
            response = await self.get("/v1/credentials/types")
            credential_types = {}
            
            for type_name, type_data in response.items():
                credential_types[type_name] = CredentialTypeDescription(
                    name=type_name,
                    displayName=type_data.get("displayName", type_name),
                    properties=type_data.get("properties", []),
                    authenticate=type_data.get("authenticate")
                )
            
            self._credential_types_cache = credential_types
            return credential_types
        except Exception as e:
            log.error(f"Failed to retrieve credential types: {str(e)}")
            return {}
    
    async def get_credential_type(self, type_name: str) -> Optional[CredentialTypeDescription]:
        """
        Retrieve information about a specific credential type.
        
        Args:
            type_name: The name of the credential type to retrieve
            
        Returns:
            A credential type description if found, None otherwise
        """
        types = await self.get_credential_types()
        return types.get(type_name)

    async def get_credential_schema(
        self,
        credential_type_name: str
    ) -> CredentialDataSchemaResponse:
        """
        Retrieve the schema for a specific credential type.
        
        The schema describes the data structure required for creating
        credentials of the specified type.
        
        Args:
            credential_type_name: The name of the credential type to get the schema for
            
        Returns:
            A schema response object containing the credential data schema
            
        Raises:
            N8nAPIError: If the credential type is not found or the request fails
            
        API Docs: https://docs.n8n.io/api/v1/credentials/#show-credential-data-schema
        """
        response_data = await self.get(endpoint=f"/v1/credentials/schema/{credential_type_name}")
        return CredentialDataSchemaResponse(**response_data)

    async def transfer_credential_to_project(
        self,
        credential_id: str,
        destination_project_id: str
    ) -> N8nBaseModel:
        """
        Transfer a credential to another project in the n8n instance.
        
        This operation moves a credential from its current project to a different project,
        maintaining all credential configurations.
        
        Args:
            credential_id: The ID of the credential to transfer
            destination_project_id: The ID of the destination project
            
        Returns:
            A basic response object indicating success
            
        Raises:
            N8nAPIError: If the credential or project is not found, or if the request fails
            
        API Docs: https://docs.n8n.io/api/v1/workflows/#transfer-a-credential-to-another-project
        """
        _payload = {"destinationProjectId": destination_project_id}
        response_data = await self.put(endpoint=f"/v1/credentials/{credential_id}/transfer", json=_payload)
        return N8nBaseModel() 