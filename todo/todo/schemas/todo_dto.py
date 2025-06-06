from pydantic import BaseModel


class TodoDTO(BaseModel):
    id: int = None
    title: str
    description: str
    state: str


class TodoCreateDTO(BaseModel):
    title: str
    description: str
    state: str


class TodoFilterDTO(BaseModel):
    title: str = None
    state: str = None
    offset: int = 0
    limit: int = 20
