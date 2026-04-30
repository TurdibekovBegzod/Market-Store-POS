from pydantic import BaseModel, Field
from uuid import UUID
from decimal import Decimal

class Product(BaseModel):
    uid: UUID

    barcode: str
    name: str

    description: str | None = None

    price: Decimal
    quantity: int

    currency_id: int | None = None
    template_id: int | None = None

    attributes: list[str] = Field(default_factory=list)

    class Config:
        from_attributes = True

class ProductCreate(BaseModel):
    barcode: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str | None = None

    price: Decimal = Field(gt=0)
    quantity: int = Field(ge=0)

    currency_id: int = Field(gt=0)
    template_id: int | None = Field(default=None, gt=0)

    attributes: list[str] = Field(default_factory=list)

class ProductRead(Product):
    pass

class ProductUpdate(BaseModel):
    barcode : str | None = None
    name : str | None = None
    description : str | None = None
    price : Decimal | None = None
    quantity : int | None = None

    currency_id : int | None = None
    template_id : int | None = None

    attributes : list[str] | None = None


