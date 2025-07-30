import json
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, validator


class N8nBaseModel(BaseModel):
    """Base model class for n8n API, all other models inherit from this class"""
    
    class Config:
        """Pydantic configuration"""
        validate_assignment = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
    
    def to_json(self) -> str:
        """Convert model to JSON string"""
        return json.dumps(self.model_dump(), default=str)
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        """Create model instance from dictionary"""
        return cls(**data)
    
    def update_from_dict(self, data: dict[str, Any]) -> None:
        """Update model fields from dictionary"""
        for field_name, field_value in data.items():
            if hasattr(self, field_name):
                setattr(self, field_name, field_value) 