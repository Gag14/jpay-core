from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.utils.security import decrypt_api_key, hash_api_key
from src.repositories.merchant_repository import MerchantRepository
from src.db.session import get_db

class APIKeyAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.merchant_repo = MerchantRepository()
        
        

    async def dispatch(self, request: Request, call_next) -> Response:
        print(1)
        open_routes = ["/docs", "/openapi.json", "/api/v1/core/merchants/register", "/api/v1/core/deposits/trigger-monitor", "/api/v1/test/webhook/test"]
        if request.url.path in open_routes:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

        encrypted_key = auth_header.split(" ")[1]

        try:
            raw_key = decrypt_api_key(encrypted_key)
            hashed_key = hash_api_key(raw_key)
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid or corrupted API key")

        # Use FastAPI dependency-injection pattern manually
        db = next(get_db())
        merchant = self.merchant_repo.get_by_api_key(db, hashed_key)
        if not merchant or not merchant.is_active:
            raise HTTPException(status_code=401, detail="Unauthorized: merchant not found or inactive")

        request.state.merchant = merchant  # Pass it to downstream
        return await call_next(request)
