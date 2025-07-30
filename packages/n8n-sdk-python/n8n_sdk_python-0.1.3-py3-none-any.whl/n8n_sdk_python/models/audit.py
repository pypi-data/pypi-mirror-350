"""
n8n audit log data models.
Define audit log related data structures.
"""

from typing import Optional, Any
from pydantic import Field
from .base import N8nBaseModel

class AuditAdditionalOptions(N8nBaseModel):
    """Additional options for audit requests"""
    daysAbandonedWorkflow: Optional[int] = Field(None, description="Number of days for abandoned workflows")
    categories: Optional[list[str]] = Field(None, description="Audit categories")

class AuditReportLocationItem(N8nBaseModel):
    """Audit report location item, identify the location of the audit finding
    
    The kind field determines the type of the item, and then uses different field combinations based on the type.
    """
    kind: str = Field(..., description="Problem type, such as 'credential', 'node', 'community'")
    id: Optional[str] = Field(None, description="The unique identifier of the item")
    name: Optional[str] = Field(None, description="The name or label of the item")
    workflowId: Optional[str] = Field(None, description="The ID of the related workflow, only applicable when kind is 'node'")
    workflowName: Optional[str] = Field(None, description="The name of the related workflow, only applicable when kind is 'node'")
    nodeId: Optional[str] = Field(None, description="The ID of the related node, only applicable when kind is 'node'")
    nodeName: Optional[str] = Field(None, description="The name of the related node, only applicable when kind is 'node'")
    nodeType: Optional[str] = Field(None, description="The type of the related node, only applicable when kind is 'node'")
    packageUrl: Optional[str] = Field(None, description="The package URL of the community node, only applicable when kind is 'community'")

class AuditReportSection(N8nBaseModel):
    """Audit report section, contains specific audit findings
    
    Each section includes title, description, recommendation and problem location.
    """
    title: str = Field(..., description="Section title, describes the type of audit findings")
    description: str = Field(..., description="Detailed description of the problem, including risks and potential impacts")
    recommendation: str = Field(..., description="Recommended actions to resolve or mitigate the problem")
    # NOTE: N8N API has a "or validating the input of the expression in the "Query" field.": null,
    # This is not a valid Python identifier, Pydantic may not be able to handle it directly.
    # We can treat it as additional_details or a similar generic dict.
    additional_details: Optional[dict[str, Optional[str]]] = Field(None, alias="or validating the input of the expression in the \"Query\" field.", description="Additional details or suggestions, possibly as an alternative to the main recommendation")
    location: list[AuditReportLocationItem] = Field(..., description="List of problem locations, indicating where the problem was found in the system")

class AuditRiskReport(N8nBaseModel):
    """Audit risk report base class"""
    risk: str
    sections: list[AuditReportSection]

class AuditResponse(N8nBaseModel):
    """Audit API response model"""
    CredentialsRiskReport: Optional[AuditRiskReport] = Field(None, alias="Credentials Risk Report")
    DatabaseRiskReport: Optional[AuditRiskReport] = Field(None, alias="Database Risk Report")
    FilesystemRiskReport: Optional[AuditRiskReport] = Field(None, alias="Filesystem Risk Report")
    NodesRiskReport: Optional[AuditRiskReport] = Field(None, alias="Nodes Risk Report")
    InstanceRiskReport: Optional[AuditRiskReport] = Field(None, alias="Instance Risk Report") 