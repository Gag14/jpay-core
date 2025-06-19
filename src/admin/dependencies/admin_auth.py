from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError
from src.admin.jwtauth import decode_access_token
from src.db.session import get_db
from src.models.admin_user import AdminUser
from src.repositories.admin_user_repository import AdminUserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/auth/login")

def get_current_admin_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> AdminUser:
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")

    repo = AdminUserRepository()
    user = repo.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
