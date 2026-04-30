from fastapi import APIRouter, Depends, HTTPException, status
from api.services.products import ProductService
from api.db.models import Product
from api.db.main import get_db
from api.schemas.products import ProductCreate, ProductUpdate, ProductRead
import uuid
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

router = APIRouter()

product_service = ProductService()

@router.get("/", response_model=list[ProductRead])
async def get_products(db=Depends(get_db)):
    return await product_service.get_all_products(db=db)

@router.get("/{product_uid}", response_model=ProductRead)
async def get_product_by_uid(product_uid: uuid.UUID, db=Depends(get_db)):
    result = await product_service.get_product_by_uid(db=db, product_uid=product_uid)

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

# @router.delete("/")
# async def delete_product(product_uid : uuid.UUID)

@router.put("/{product_uid}", status_code=status.HTTP_200_OK)
async def update_product(product_uid : uuid.UUID, product_data : ProductUpdate, db = Depends(get_db)):

    product_data_dict= product_data.model_dump(exclude_unset=True)

    product = await product_service.update_product(
        product_uid=product_uid,
        product_data = product_data_dict,
        db = db
    )

    return JSONResponse(
        content = jsonable_encoder(product)
    )

@router.delete("/{product_uid}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_product(product_uid : uuid.UUID, db = Depends(get_db)):

    result = await product_service.delete_product(product_uid=product_uid, db = db)

    return JSONResponse(
        content = {
            'message' : f"Product with uid {product_uid} successfully deleted.",
            'status' : result
        }
    )

    


