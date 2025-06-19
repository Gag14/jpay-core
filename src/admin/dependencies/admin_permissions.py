from fastapi import Depends
from src.models.admin_user import AdminUser
from src.admin.dependencies.admin_auth import get_current_admin_user

def get_allowed_merchant_ids(admin: AdminUser = Depends(get_current_admin_user)) -> list[int] | None:
    if admin.is_superuser:
        return None
    return admin.merchant_ids
