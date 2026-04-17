from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    uid : UUID
    firstname : str
    lastname : str
    email  : str
    password_hash: str