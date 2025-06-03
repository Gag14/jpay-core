from pydantic import BaseModel, EmailStr


class MerchantRegisterRequest(BaseModel):
    name: str
    contact_email: EmailStr


class MerchantRegisterResponse(BaseModel):
    api_key: str
