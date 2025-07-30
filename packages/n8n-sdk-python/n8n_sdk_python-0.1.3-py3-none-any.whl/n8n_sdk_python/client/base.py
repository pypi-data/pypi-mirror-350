"""
Base client for n8n SDK providing HTTP communication with n8n API.

This module contains the base class for all n8n API clients, offering
standard HTTP methods and error handling for API communication.
"""

import os
from typing import Any, Optional

import httpx

from ..utils.logger import log
from ..utils.errors import N8nAPIError


class BaseClient:
    """
    Base client class for n8n API communication.
    
    Provides fundamental HTTP methods and request handling for interacting
    with the n8n API, including error handling and response processing.
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None, timeout: int = 30):
        """
        Initialize the n8n base API client.
        
        Args:
            base_url: Base URL for the n8n API, defaults to environment variable or localhost
            api_key: Authentication key for n8n API, defaults to environment variable
            timeout: Request timeout in seconds, defaults to 30
        """
        self.base_url = base_url or os.getenv("N8N_BASE_URL", "http://localhost:5678")
        self.api_key = api_key or os.getenv("N8N_API_KEY")
        self.headers = {"X-N8N-API-KEY": self.api_key} if self.api_key else {}
        self.timeout = timeout
    
    async def _request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[dict[str, Any]] = None,
        json_payload: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None,
        timeout: Optional[int] = None
    ) -> Any:
        """
        Execute an HTTP request to the n8n API.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH, DELETE)
            endpoint: API endpoint path
            params: Optional URL query parameters
            json_payload: Optional JSON data for request body
            headers: Optional additional HTTP headers
            timeout: Optional request timeout in seconds
            
        Returns:
            Response data (typically a dictionary or list)
            
        Raises:
            N8nApiError: When the API request fails
        """
        url = f"{self.base_url}/api/{endpoint.lstrip('/')}"
        request_headers = {**self.headers, **(headers or {})}
        
        log.debug(f"Requesting {method} {url} with payload: {json_payload}")
        
        try:
            async with httpx.AsyncClient() as client:
                request_kwargs = {
                    "method": method,
                    "url": url,
                    "params": params,
                    "headers": request_headers,
                    "timeout": timeout or self.timeout
                }
                if json_payload is not None:
                    request_kwargs["json"] = json_payload
                elif method in ["POST", "PUT", "PATCH"]:
                    request_kwargs["content"] = b''
                
                response = await client.request(**request_kwargs)
                
                log.debug(f"Response status: {response.status_code}")
                
                # Try to parse response as JSON
                if response.content:
                    try:
                        response_data = response.json()
                    except ValueError:
                        response_data = response.text
                else:
                    response_data = None
                
                # Check for errors
                if response.is_error:
                    error_msg = f"n8n API error: {response.status_code}"
                    if isinstance(response_data, dict) and "message" in response_data:
                        error_msg = f"{error_msg} - {response_data['message']}"
                    
                    raise N8nAPIError(
                        message=error_msg,
                        status_code=response.status_code,
                        response_body=response.text,
                        details={"endpoint": endpoint, "method": method}
                    )
                
                return response_data
                
        except httpx.RequestError as e:
            error_msg = f"Request error: {str(e)}"
            log.error(error_msg)
            raise N8nAPIError(
                message=error_msg,
                details={"endpoint": endpoint, "method": method}
            )
    
    async def get(
        self, 
        endpoint: str, 
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """
        Execute a GET request to the n8n API.
        
        Args:
            endpoint: API endpoint path
            params: Optional URL query parameters
            headers: Optional additional HTTP headers
            
        Returns:
            Response data from the API
            
        Raises:
            N8nApiError: When the API request fails
        """
        return await self._request("GET", endpoint, params=params, headers=headers)
    
    async def put(
        self,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """
        Execute a PUT request to the n8n API.
        
        Args:
            endpoint: API endpoint path
            json: Optional JSON payload for the request body
            params: Optional URL query parameters
            headers: Optional additional HTTP headers
            
        Returns:
            Response data from the API
            
        Raises:
            N8nApiError: When the API request fails
        """
        return await self._request("PUT", endpoint, json_payload=json, params=params, headers=headers)
    
    async def post(
        self, 
        endpoint: str, 
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """
        Execute a POST request to the n8n API.
        
        Args:
            endpoint: API endpoint path
            json: Optional JSON payload for the request body
            params: Optional URL query parameters
            headers: Optional additional HTTP headers
            
        Returns:
            Response data from the API
            
        Raises:
            N8nApiError: When the API request fails
        """
        return await self._request("POST", endpoint, json_payload=json, params=params, headers=headers)
    
    async def patch(
        self, 
        endpoint: str, 
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """
        Execute a PATCH request to the n8n API.
        
        Args:
            endpoint: API endpoint path
            json: Optional JSON payload for the request body
            params: Optional URL query parameters
            headers: Optional additional HTTP headers
            
        Returns:
            Response data from the API
            
        Raises:
            N8nApiError: When the API request fails
        """
        return await self._request("PATCH", endpoint, json_payload=json, params=params, headers=headers)
    
    async def delete(
        self, 
        endpoint: str, 
        params: Optional[dict[str, Any]] = None,
        headers: Optional[dict[str, str]] = None
    ) -> Any:
        """
        Execute a DELETE request to the n8n API.
        
        Args:
            endpoint: API endpoint path
            params: Optional URL query parameters
            headers: Optional additional HTTP headers
            
        Returns:
            Response data from the API
            
        Raises:
            N8nApiError: When the API request fails
        """
        return await self._request("DELETE", endpoint, params=params, headers=headers) 