from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import transaction_router
from scalar_fastapi import get_scalar_api_reference


app = FastAPI(
    title="iKash API",
    description="Système de gestion de transactions Mobile Money",
    version="1.0.0",
    docs_url=None, 
    redoc_url=None,  
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(
    transaction_router.router
)
@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )
