"""
n8n projects data models.
Define project-related data structures.
"""

from datetime import datetime
from typing import Optional

from pydantic import Field

from .base import N8nBaseModel


class Project(N8nBaseModel):
    """Project data model"""
    id: str
    name: str
    type: Optional[str] = Field(None, description="Project type, this field exists in API examples but is not detailed") # Field present in GET /projects response examples
    createdAt: Optional[datetime] = Field(None, description="Creation time (inferred)")
    updatedAt: Optional[datetime] = Field(None, description="Update time (inferred)")

class ProjectCreate(N8nBaseModel):
    """Create project request model (POST /projects)"""
    name: str

class ProjectUpdate(N8nBaseModel):
    """Update project request model (PUT /projects/{projectId})"""
    name: str

class ProjectList(N8nBaseModel):
    """Project list response model (GET /projects)"""
    data: list[Project]
    nextCursor: Optional[str] = None