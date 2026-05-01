
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime, timezone
import uuid
from api.db.models import User


class UserService:
    @staticmethod
    async def create_user(user_data : dict, db : AsyncSession):
        new_user = User(**user_data)

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        return new_user

    @staticmethod
    async def get_user_by_email(user_email : str, db : AsyncSession):
        result = await db.execute(select(User).where(User.email == user_email))
        
        user = result.scalar_one_or_none()

        return user
    
    @staticmethod
    async def get_all_user(db : AsyncSession):
        users = await db.execute(select(User))

        return users.scalars().all()
    
    @staticmethod
    async def get_user_by_uid(user_uid : uuid.UUID, db : AsyncSession):
        user = await db.execute(select(User).where(User.uid == user_uid))

        return user.scalar_one_or_none()
    
    @staticmethod
    async def delete_user(user_uid : uuid.UUID, db : AsyncSession):
        user = await UserService.get_user_by_uid(user_uid=user_uid, db = db)

        await db.delete(user)
        await db.commit()

        return True
    
    @staticmethod
    async def update_user(db : AsyncSession,user_email : str, user_data : dict):
        user_email = user_email

        user = await UserService.get_user_by_email(
            user_email=user_email,
            db = db
        )

        for key, value in user_data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)

        return user


