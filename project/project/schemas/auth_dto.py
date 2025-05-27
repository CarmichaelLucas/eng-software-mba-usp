from pydantic import BaseModel, EmailStr


class AuthResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = 'bearer'


class AuthLoginDTO(BaseModel):
    email: EmailStr
    password: str
