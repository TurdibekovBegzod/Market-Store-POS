from fastapi import APIRouter, Depends, HTTPException, status
from api.db.main import get_db
from api.services.currencies import CurrencyService
from api.schemas.currencies import CurrencyCreate, CurrencyRead, CurrencyUpdate, CurrencyDelete
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
currencies_service = CurrencyService()

@router.get("/", response_model=list[CurrencyRead], status_code=status.HTTP_200_OK)
async def get_currencies(db: AsyncSession = Depends(get_db)):
    return await currencies_service.get_all_currencies(db=db)

@router.post("/", response_model=CurrencyRead, status_code=status.HTTP_201_CREATED)
async def create_currency(currency: CurrencyCreate, db: AsyncSession = Depends(get_db)):
    currency_data = currency.model_dump(exclude_unset=True)
    return await currencies_service.create_currency(db=db, currency_data=currency_data)


@router.get("/{currency_id}", response_model=CurrencyRead, status_code=status.HTTP_200_OK)
async def get_currency_by_id(currency_id: int, db: AsyncSession = Depends(get_db)):
    result = await currencies_service.get_currency_by_id(db=db, currency_id=currency_id)

    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Currency with id {currency_id} not found"
        )
    return result

@router.put("/{currency_id}", response_model=CurrencyRead, status_code=status.HTTP_200_OK)
async def update_currency(currency_id: int, currency_update: CurrencyUpdate, db: AsyncSession = Depends(get_db)):
    update_data = currency_update.model_dump(exclude_unset=True)
    result = await currencies_service.update_currency(db=db, currency_id=currency_id, update_data=update_data)

    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Currency with id {currency_id} not found"
        )
    return result

@router.delete("/{currency_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_currency(currency_id: int, db: AsyncSession = Depends(get_db)):
    result = await currencies_service.delete_currency(db=db, currency_id=currency_id)

    if not result:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"Currency with id {currency_id} not found or could not be deleted"
        )   
    return None