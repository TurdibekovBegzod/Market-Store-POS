from api.db.models import Product
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid
from fastapi import HTTPException, status


class ProductService:
    @staticmethod
    async def create_product(db: AsyncSession, product_data):
        barcode = product_data['barcode']

        existing = await ProductService.get_product_by_barcode(db = db, barcode=barcode)
        if existing:
            raise HTTPException(status_code=400, detail=f"Barcode `{barcode}` already exists")
        
        product = Product(**product_data)
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product
    

    async def get_all_products(self, db):
        result = await db.execute(select(Product))
        return result.scalars().all()

    @staticmethod
    async def get_product_by_uid(db: AsyncSession, product_uid : uuid.UUID ):
        result = await db.execute(select(Product).filter(Product.uid == product_uid))
        return result.scalars().first()
    
    @staticmethod
    async def get_product_by_barcode(db:AsyncSession, barcode : str):
        result = await db.execute(select(Product).filter(Product.barcode == barcode))

        return result.scalar_one_or_none()
    
   
    
    @staticmethod
    async def update_product(db: AsyncSession, product_uid: uuid.UUID, product_data : dict):
        product = await ProductService.get_product_by_uid(db=db, product_uid=product_uid)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with uid {product_uid} is not found!"
            )
        
        for key, value in product_data.items():
            setattr(product, key, value)
        await db.commit()
        await db.refresh(product)
        return product

    @staticmethod
    async def delete_product(db: AsyncSession, product_uid: uuid.UUID):
        product = await ProductService.get_product_by_uid(product_uid=product_uid, db = db)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with uid {product_uid} not found"
            )
        
        await db.delete(product)
        await db.commit()
        return True