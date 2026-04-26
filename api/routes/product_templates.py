from fastapi import APIRouter, Depends, status
from api.db.main import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from api.services.product_templates import ProductTemplateService
from api.schemas.product_templates import ProductTemplateCreate, ProductTemplateRead, ProductTemplateUpdate, ProductTemplateDelete


router = APIRouter()
product_template_service = ProductTemplateService()

@router.get("/", status_code = status.HTTP_200_OK)
async def get_product_templates(db : AsyncSession = Depends(get_db)):
    templates = await product_template_service.get_all_product_templates(db = db)

    return {
        "message" : "All templates are ",
        "templates" : templates
    }

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_template(new_template_data: ProductTemplateCreate, db : AsyncSession = Depends(get_db)):
    new_template_data_dict = new_template_data.model_dump(exclude_unset=True)

    new_template = await product_template_service.create_product_template(db=db, template_data=new_template_data_dict)
    
    return {
        "message": "Product template created", 
        "new_template": new_template
    }

@router.put("/{template_id}")
async def update_product_template(template_id: int, updated_template_data: ProductTemplateUpdate, db : AsyncSession = Depends(get_db)):
    updated_template_data_dict = updated_template_data.model_dump(exclude_unset=True)
    
    template = await product_template_service.update_product_template(db=db, template_id=template_id, template_data=updated_template_data_dict)
    
    return {
        "message": f"Product template with id {template_id} updated", 
        "template": template
    }

@router.delete("/{template_id}")
async def delete_product_template(template_id: int, db : AsyncSession = Depends(get_db)):
    result = await product_template_service.delete_product_template(db=db, template_id=template_id)
    
    return {
        "message": f"Product template with id {template_id} deleted",
        "result": result
    }


