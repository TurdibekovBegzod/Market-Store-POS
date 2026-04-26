from pydantic import BaseModel, Field
from typing import Any, List, Optional




class ProductTemplate(BaseModel):

    id: int
    name: str
    description: Optional[str] = None
    
    attributes: dict[str, Any] = Field(default_factory=dict)

class ProductTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    attributes: dict[str, Any] = Field(default_factory=dict)

class ProductTemplateRead(ProductTemplate):
    pass

class ProductTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    attributes: dict[str, Any] = Field(default_factory=dict)

class ProductTemplateRead(ProductTemplate):
    pass

class ProductTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[dict[str, Any]] = None

class ProductTemplateDelete(BaseModel):
    id: int

