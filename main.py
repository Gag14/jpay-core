from fastapi import FastAPI
from src.core.middleware.api_key_auth import APIKeyAuthMiddleware
from src.models.enums.network_type import NetworkType
from src.db.engine import engine
from src.db.base import Base
from src.models import merchant, balance, transaction, wallet, coin, fiat_currency, admin_user
from src.models.enums import transaction_status, wallet_type
from src.routes.core import merchant, deposit, test
from src.routes import admin, core

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.add_middleware(APIKeyAuthMiddleware)  

app.include_router(merchant.router, prefix="/api/v1/core/merchants", tags=["Merchants"])
app.include_router(deposit.router, prefix="/api/v1/core/deposits", tags=["Deposits"])
app.include_router(test.router, prefix="/api/v1/test", tags=["Webhook Test"])

# app.include_router(admin.router, prefix="/api/v1/admin")

@app.get("/")
def root():
    return {"status": "OK"}
