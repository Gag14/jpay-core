from fastapi import FastAPI
from src.models.enums.network_type import NetworkType
from src.db.engine import engine
from src.db.base import Base
from src.models import merchant, balance, transaction, wallet, coin
from src.models.enums import transaction_status
from src.routes.core import merchant
from src.routes import admin

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(merchant.router, prefix="/api/v1/core/merchants", tags=["Merchants"])
# app.include_router(admin.router, prefix="/api/v1/admin")

@app.get("/")
def root():
    return {"status": "OK"}
