from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.repositories.admin_user_repository import AdminUserRepository
from src.admin.jwtauth import create_access_token
from src.db.session import get_db
from fastapi import Body
from src.schemas.admin_user import AdminUserCreate, AdminUserResponse, AdminUserMeResponse
from src.admin.dependencies.admin_auth import get_current_admin_user
from src.models.admin_user import AdminUser

router = APIRouter()

@router.post("/register", response_model=AdminUserResponse)
def register_admin_user(
    payload: AdminUserCreate = Body(...),
    db: Session = Depends(get_db)
):
    repo = AdminUserRepository()
    existing = repo.get_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = repo.hash_password(payload.password)
    user_data = payload.dict(exclude={"password"})
    user_data["password_hash"] = hashed_password
    try:
        new_user = repo.create(db, user_data)
        return new_user
    except IntegrityError as e:
        db.rollback()  # important to reset session state
        if 'admin_users_email_key' in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Integrity error occurred"
        )
    return new_user

@router.post("/login")
def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    repo = AdminUserRepository()
    user = repo.get_by_username(db, form_data.username)
    if not user or not repo.verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({
        "sub": str(user.id),
        "username": user.username,
        "is_superuser": user.is_superuser,
    })
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=AdminUserMeResponse)
def get_current_admin_user_info(
    user: AdminUser = Depends(get_current_admin_user)
):
    return user