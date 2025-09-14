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
