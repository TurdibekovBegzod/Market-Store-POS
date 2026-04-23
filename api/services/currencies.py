from api.db.models import Currency
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class CurrencyService:
    @staticmethod
    async def create_currency(db: AsyncSession, currency_data):
        currency = Currency(**currency_data)
        db.add(currency)
        await db.commit()
        await db.refresh(currency)
        return currency
    
    @staticmethod
    async def get_all_currencies(db: AsyncSession):
        result = await db.execute(select(Currency))
        return result.scalars().all()
    
    @staticmethod
    async def get_currency_by_id(db: AsyncSession, currency_id: int):
        result = await db.execute(select(Currency).filter(Currency.id == currency_id))
        return result.scalars().first()