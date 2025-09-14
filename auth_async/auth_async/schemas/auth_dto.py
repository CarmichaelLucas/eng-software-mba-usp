from pydantic import BaseModel, EmailStr


class AuthPublicResponse(BaseModel):
    token_type: str = 'bearer'
    access_token: str
    expire_in: int = None


class AuthPublicRequest(BaseModel):
    email: EmailStr
    password: str


class AuthPublicUserResponse(BaseModel):
    allowed: bool
    user_uuid: str
