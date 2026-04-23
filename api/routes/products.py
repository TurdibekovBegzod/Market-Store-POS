from fastapi import APIRouter, Depends, HTTPException, status
from api.services.products import ProductService
from api.db.models import Product
from api.db.main import get_db
from api.schemas.products import ProductCreate, ProductUpdate, ProductRead, ProductDelete
import uuid
router = APIRouter()

product_service = ProductService()

@router.get("/", response_model=list[ProductRead])
async def get_products(db=Depends(get_db)):
    return await product_service.get_all_products(db=db)

@router.get("/{product_uid}", response_model=ProductRead)
async def get_product_by_uid(product_uid: uuid.UUID, db=Depends(get_db)):
    result = await product_service.get_product_by_id(db=db, product_uid=product_uid)

    if not result:
        raise HTTPException(
            status_code = 404,
            detail = f"Product with id {product_uid} not found"
        )
    return result

@router.get("/barcode/{barcode}", response_model=ProductRead)
async def get_product_by_barcode(barcode: str, db=Depends(get_db)):
    result = await product_service.get_product_by_barcode(db=db, barcode=barcode)

    if not result:
        raise HTTPException(
            status_code = 404,
            detail = f"Product with barcode {barcode} not found"
        )
    return result 

@router.post("/", response_model=ProductRead, status_code = status.HTTP_201_CREATED)
async def create_product(product_data: ProductCreate, db=Depends(get_db)):
    data = product_data.model_dump(exclude_unset=True)
    return await product_service.create_product(db=db, product_data=data)
