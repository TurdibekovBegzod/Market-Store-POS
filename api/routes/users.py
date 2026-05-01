from fastapi import APIRouter, Depends, status, HTTPException
from api.services.users import UserService
from api.schemas.users  import UserCreate, UserEmail, UserRead, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from api.db.main import get_db 
from api.security.hash import hash_password, verify_password
from pydantic import EmailStr
import uuid

router = APIRouter()

user_service = UserService()
@router.get("/", response_model=list[UserRead], status_code=status.HTTP_200_OK)
async def get_all_user(db : AsyncSession = Depends(get_db)):
    users = await user_service.get_all_user(db = db)

    return users

@router.get("/by-email", response_model = UserRead, status_code=status.HTTP_200_OK)
async def get_user_by_email(user_email: str, db: AsyncSession = Depends(get_db)):
    user = await user_service.get_user_by_email(user_email=user_email, db=db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.get("/{user_uid}", response_model=UserRead, status_code=status.HTTP_200_OK)
async def get_user_by_uid(user_uid : uuid.UUID, db : AsyncSession = Depends(get_db)):
    user = await user_service.get_user_by_uid(user_uid=user_uid, db = db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):

    existing_user = await user_service.get_user_by_email(
        user_email=user_data.email.lower(),
        db=db
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user_data.email} already exists"
        )

    user_dict = user_data.model_dump()
    password_hash = hash_password(user_dict.pop("password"))

    user_dict["email"] = user_dict["email"].lower()
    user_dict["password_hash"] = password_hash

    return await user_service.create_user(user_data=user_dict, db=db)

@router.delete("/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_uid : uuid.UUID, db : AsyncSession = Depends(get_db)):
    existing_user = await user_service.get_user_by_uid(
        user_uid=user_uid,
        db=db
    )
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await user_service.delete_user(user_uid=user_uid, db = db)

    return {
        "message" : "User deleted successfully",
        'status': result
    } 

@router.put("/", response_model=UserRead)
async def update_user(
    email: EmailStr,
    password: str,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user = await user_service.get_user_by_email(user_email=email, db=db)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    user_dict = user_data.model_dump(exclude_unset=True)

    if not user_dict:
        raise HTTPException(status_code=400, detail="No data to update")

    if "password" in user_dict:
        user_dict["password_hash"] = hash_password(user_dict.pop("password"))

    updated_user = await user_service.update_user(
        user_data=user_dict,
        user_email=email,
        db=db
    )

    return updated_user
    
    





