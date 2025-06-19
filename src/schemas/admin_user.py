from pydantic import BaseModel, EmailStr
from typing import List, Optional

class AdminUserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    is_superuser: Optional[bool] = False
    merchant_ids: Optional[List[int]] = []
    permissions: Optional[List[str]] = []

class AdminUserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool
    merchant_ids: List[int]
    permissions: List[str]

    class Config:
        orm_mode = True

from pydantic import BaseModel, EmailStr
from typing import List

class AdminUserMeResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool
    merchant_ids: List[int]
    permissions: List[str]

    class Config:
        orm_mode = True
