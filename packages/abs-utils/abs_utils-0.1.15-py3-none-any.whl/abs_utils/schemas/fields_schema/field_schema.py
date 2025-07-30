from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from .common_schema import BaseFieldSchema, ValidationRules, FieldType

class Validation(ValidationRules):
    unique: Optional[bool] = Field(default=False)
    index: Optional[bool] = Field(default=False)

class Reference(BaseModel):
    entity_id: str
    field_id: str
    alias: str

    @model_validator(mode='after')
    def validate_reference(self) -> 'Reference':
        if self.entity_id is None or self.field_id is None:
            raise ValueError("entity_id and field_id are required")
        
        if self.entity_id.strip() == "" or self.field_id.strip() == "":
            raise ValueError("entity_id and field_id cannot be empty")
        
        if self.alias.strip() == "":
            raise ValueError("alias cannot be empty")
        
        return self
    
class FieldSchema(BaseFieldSchema):
    is_protected: bool = Field(default=False)
    entity_id: str
    description: Optional[str] = None
    validations: Optional[Validation] = None
    reference: Optional[Reference] = None

    model_config = ConfigDict(extra="ignore")
        
