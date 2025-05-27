from pydantic import BaseModel, EmailStr


class UserDTO(BaseModel):
    id: int = None
    username: str = None
    email: EmailStr


class UserCreateDTO(BaseModel):
    username: str = None
    email: EmailStr
    password: str
