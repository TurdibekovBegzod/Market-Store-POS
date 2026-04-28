
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from datetime import datetime, timezone

from api.db.models import ProductTemplate   

class ProductTemplateService:
    @staticmethod
    async def create_product_template(db: AsyncSession, template_data):
        template = ProductTemplate(**template_data)
        template.updated_at = datetime.now(timezone.utc)
        db.add(template)
        await db.commit()
        await db.refresh(template)
        return template
    
    @staticmethod
    async def get_all_product_templates(db: AsyncSession):
        result = await db.execute(select(ProductTemplate))
        return result.scalars().all()
    
    @staticmethod
    async def get_product_template_by_id(db: AsyncSession, template_id: int):
        result = await db.execute(select(ProductTemplate).filter(ProductTemplate.id == template_id))
        template = result.scalars().first()
        if not template:
            raise HTTPException(
                status_code = 404,
                detail = f"Product template with id {template_id} not found")
        return template
    
    @staticmethod
    async def update_product_template(db: AsyncSession, template_id: int, template_data : dict):
        template = await ProductTemplateService.get_product_template_by_id(db=db, template_id=template_id)

        template.updated_at = datetime.now(timezone.utc)
        if not template:
            raise HTTPException(
                status_code = 404,
                detail = f"Product template with id {template_id} not found")

        for key, value in template_data.items():
            setattr(template, key, value)
        await db.commit()
        await db.refresh(template)
        return template
    
    @staticmethod
    async def delete_product_template(db: AsyncSession, template_id: int):
        template = await ProductTemplateService.get_product_template_by_id(db=db, template_id=template_id)

        if not template:
            raise HTTPException(
                status_code = 404,
                detail = f"Product template with id {template_id} not found")
        
        await db.delete(template)
        await db.commit()
        return True
