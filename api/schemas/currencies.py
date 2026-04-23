from pydantic import BaseModel


class Currency(BaseModel):
    id: int
    code: str
    name: str
    symbol: str


class CurrencyCreate(BaseModel):
    code: str
    name: str
    symbol: str

class CurrencyRead(Currency):
    pass

class CurrencyUpdate(BaseModel):
    code: str | None = None
    name: str | None = None
    symbol: str | None = None

class CurrencyDelete(BaseModel):
    id: int
