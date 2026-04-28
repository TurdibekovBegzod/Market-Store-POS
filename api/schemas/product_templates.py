from pydantic import BaseModel, Field
from typing import Any, List, Optional




class ProductTemplate(BaseModel):

    id: int
    name: str
    description: Optional[str] = None
    
    attributes: list[str] = Field(default_factory=list)

class ProductTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    attributes: list[str] = Field(default_factory=list)

class ProductTemplateRead(ProductTemplate):
    pass

class ProductTemplateCreate(BaseModel):
    name: str
    description: Optional[str] = None
    attributes: list[str] = Field(default_factory=list)

class ProductTemplateRead(ProductTemplate):
    pass

class ProductTemplateUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    attributes: Optional[list['str']] = list()

class ProductTemplateDelete(BaseModel):
    id: int

