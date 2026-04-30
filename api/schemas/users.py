from pydantic import BaseModel, EmailStr
from uuid import UUID

class UserCreate(BaseModel):
    password : str
    firstname : str
    lastname : str
    email  : EmailStr

class UserRead(BaseModel):
    uid : UUID
    firstname : str
    lastname : str
    email  : EmailStr
    password_hash : str

class UserUpdate(BaseModel):
    firstname : str | None = None
    lastname : str | None = None
    email  : EmailStr | None = None
    password : str | None = None


class UserDelete(BaseModel):
    uid : UUID

class UserLogin(BaseModel):
    email : str
    password_hash : str

class UserEmail(BaseModel):
    email : EmailStr

