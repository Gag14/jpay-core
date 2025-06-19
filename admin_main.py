from fastapi import FastAPI
from src.routes.admin.auth import auth, merchants
from src.db.engine import engine
from src.db.base import Base
from src.routes.admin.transactions import transactions
from src.routes.admin.wallets import wallets

from src.models import admin_user  # ensure model is registered

app = FastAPI(title="Admin API")

Base.metadata.create_all(bind=engine)

# Add all admin routers from __init__.py

app.include_router(auth.router, prefix="/api/v1/admin/auth", tags=["Admin Auth"])
app.include_router(merchants.router, prefix="/api/v1/admin/merchants", tags=["Admin Merchants"])
app.include_router(transactions.router, prefix="/api/v1/admin/transactions", tags=["Admin Transactions"])
app.include_router(wallets.router, prefix="/api/v1/admin/wallets", tags=["Admin Wallets"])


@app.get("/")
def root():
    return {"admin_status": "OK"}
