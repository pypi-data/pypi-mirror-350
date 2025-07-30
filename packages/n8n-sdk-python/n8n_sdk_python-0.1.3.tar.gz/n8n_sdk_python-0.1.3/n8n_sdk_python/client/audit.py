"""
N8n Audit API client for generating security audit reports.

This module provides a client for interacting with the n8n Audit API,
enabling the generation of security audit reports for n8n instances.
These reports help identify potential security risks and best practices.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.audit import AuditAdditionalOptions, AuditResponse


class AuditClient(BaseClient):
    """
    Client for interacting with the n8n Audit API.
    
    Provides methods for generating security audit reports that analyze
    various security aspects of an n8n instance, including credentials,
    databases, filesystem access, nodes, and instance configuration.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def generate_audit_report(
        self,
        options: Optional[AuditAdditionalOptions | dict[str, Any]] = None
    ) -> AuditResponse:
        """
        Generate a comprehensive security audit report for the n8n instance.
        
        The audit report analyzes various security aspects including credentials,
        database queries, filesystem access, node usage, and instance configuration
        to identify potential security risks and best practices.
        
        Args:
            options: Optional configuration for the audit report generation,
                    either as an AuditAdditionalOptions instance or a dictionary.
                    Can include settings like abandoned workflow threshold days
                    or specific categories to audit.
                    
        Returns:
            An AuditResponse object containing the detailed audit report findings
            
        Raises:
            TypeError: If options parameter is not of the expected format
            N8nAPIError: If the API request fails
            
        API Docs: https://docs.n8n.io/api/v1/audit/#generate-an-audit
        """
        _options: Optional[AuditAdditionalOptions] = None
        if options is not None:
            if isinstance(options, dict):
                _options = AuditAdditionalOptions(**options)
            elif isinstance(options, AuditAdditionalOptions):
                _options = options
            else:
                raise TypeError(
                    "Parameter 'options' must be of type AuditAdditionalOptions or dict, "
                    f"got {type(options).__name__}"
                )

        payload: Optional[dict[str, Any]] = None
        if _options:
            # The N8N-API.md example payload is: { "additionalOptions": { "daysAbandonedWorkflow": 0, ... } }
            # So we need to wrap the options model.
            payload = {"additionalOptions": _options.model_dump(exclude_none=True)}
        
        response_data = await self.post(endpoint="/v1/audit", json=payload)
        return AuditResponse(**response_data) 