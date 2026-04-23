from pydantic import BaseModel
from uuid import UUID

class User(BaseModel):
    firstname : str
    lastname : str
    email  : str

class UserCreate(User):
    password_hash : str

class UserRead(User):
    id : UUID

class UserUpdate(BaseModel):
    firstname : str | None = None
    lastname : str | None = None
    email  : str | None = None
    password_hash : str | None = None


class UserDelete(BaseModel):
    id : UUID

class UserLogin(BaseModel):
    email : str
    password_hash : str

