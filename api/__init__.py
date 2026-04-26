from fastapi import FastAPI
from api.routes.users import router as users_router
from api.routes.products import router as products_router
from api.routes.currencies import router as currencies_router
from api.routes.product_templates import router as product_templates_router

from api.db.main import init_db
from fastapi.openapi.models import Contact


# app = FastAPI()

# @app.on_event("startup")
# async def on_startup():
#     await init_db()
async def life_span(app : FastAPI):
    print("server is starting ... ")
    await init_db()
    yield 
    print("Server has been stopped")


version = "v1"

app = FastAPI(
    title="Market Store POS API",
    description="API for managing products, users, and transactions in a market store point-of-sale system.",
    version=version,
    lifespan=life_span,
    docs_url=f"/api/{version}/docs",
    redoc_url=f"/api/{version}/redoc",
    contact=Contact(
        name = "Begzod Turdibekov",
        email="begzodasidev@gmail.com"
    )
) 

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(products_router, prefix="/products", tags=["Products"])
app.include_router(currencies_router, prefix="/currencies", tags=["Currencies"])
app.include_router(product_templates_router, prefix="/product-templates", tags=["Product Templates"])



