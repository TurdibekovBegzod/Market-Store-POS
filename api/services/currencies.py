from api.db.models import Currency
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

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
    
    @staticmethod
    async def update_currency(db: AsyncSession, currency_id: int, update_data):
        currency = await CurrencyService.get_currency_by_id(db=db, currency_id=currency_id)

        if not currency:
            return None
        

        for key, value in update_data.items():
            setattr(currency, key, value)
        await db.commit()
        await db.refresh(currency)
        return currency
    
    @staticmethod
    async def delete_currency(db: AsyncSession, currency_id: int):
        currency = await CurrencyService.get_currency_by_id(db=db, currency_id=currency_id)

        if not currency:
            return None
        
        await db.delete(currency)
        await db.commit()
        return True