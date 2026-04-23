from api.db.models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid


class ProductService:
    @staticmethod
    async def create_product(db: AsyncSession, product_data):

        product = Product(**product_data)
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    

    async def get_all_products(self, db):
        result = await db.execute(select(Product))
        return result.scalars().all()

    @staticmethod
    async def get_product_by_id(db: AsyncSession, product_uid : uuid.UUID ):
        result = await db.execute(select(Product).filter(Product.uid == product_uid))
        return result.scalars().first()
    
    @staticmethod
    async def get_product_by_barcode(db:AsyncSession, barcode : str):
        result = await db.execute(select(Product).filter(Product.barcode == barcode))

        return result.scalars().first()
    
   
    
    @staticmethod
    async def update_product(db: AsyncSession, product_id: uuid.UUID, update_data):
        product = await db.query(Product).filter(Product.uid == product_id).first()
        if not product:
            return None
        for key, value in update_data.items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete_product(db: AsyncSession, product_id: uuid.UUID):
        product = await db.query(Product).filter(Product.uid == product_id).first()
        if not product:
            return None
        await db.delete(product)
        await db.commit()
        return True