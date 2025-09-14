from pydantic import BaseModel, EmailStr


class UserPublicResponse(BaseModel):
    id: int
    name: str
    username: str
    email: EmailStr
    uuid: str


class UserPublicRequest(BaseModel):
    username: str
    name: str
    email: EmailStr
    password: str


class UserDTO(BaseModel):
    id: int = None
    name: str = None
    username: str = None
    email: EmailStr = None
    uuid: str = None
    password: str = None
