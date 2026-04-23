from pydantic import BaseModel
from uuid import UUID

class Product(BaseModel):
    id : UUID
    barcode : str
    name : str
    description : str | None = None
    price : float
    quantity : int

    currency_id : int
    template_id : int | None = None

    metadata : dict | None = None

class ProductCreate(BaseModel):
    barcode : str
    name : str
    description : str | None = None
    price : float
    quantity : int

    currency_id : int
    template_id : int | None = None

    metadata : dict | None = None

class ProductRead(Product):
    pass

class ProductUpdate(BaseModel):
    barcode : str | None = None
    name : str | None = None
    description : str | None = None
    price : float | None = None
    quantity : int | None = None

    currency_id : int | None = None
    template_id : int | None = None

    metadata : dict | None = None
class ProductDelete(BaseModel):
    uid : UUID

