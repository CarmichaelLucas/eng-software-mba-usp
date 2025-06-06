from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from todo.repositories.todo_repository import TodoRepository
from todo.schemas.todo_dto import (
    TodoCreateDTO,
    TodoDTO,
    TodoFilterDTO,
)


class TodoService:
    def __init__(self, session: AsyncSession):
        self.repository = TodoRepository(session=session)

    async def get_all(self, filters: TodoFilterDTO) -> List[Optional[TodoDTO]]:
        return await self.repository.get_all(filters=filters)

    async def get_by_id(self, id: int) -> Optional[TodoDTO]:
        todo = await self.repository.get_by_id(id=id)

        if not todo:
            raise Exception('Todo não encontrado.')

        return todo

    async def create(self, todo: TodoCreateDTO) -> TodoDTO:
        return await self.repository.create(todo=todo)

    async def update(self, id: int, new_state: str):
        todo = await self.get_by_id(id=id)
        return await self.repository.update(id=todo.id, new_state=new_state)

    async def delete(self, id: int):
        todo = await self.get_by_id(id=id)
        return await self.repository.delete(id=todo.id)
