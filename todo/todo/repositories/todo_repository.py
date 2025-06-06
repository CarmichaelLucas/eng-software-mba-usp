import logging
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from todo.models.todo_model import Todo
from todo.schemas.todo_dto import (
    TodoCreateDTO,
    TodoDTO,
    TodoFilterDTO,
)


class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self, filters: TodoFilterDTO) -> List[Optional[TodoDTO]]:
        try:
            query = select(Todo)

            if filters.title:
                query = query.filter(Todo.title == filters.title)

            if filters.state:
                query = query.filter(Todo.state == filters.state)

            result = await self.session.scalars(
                query.offset(filters.offset).limit(filters.limit)
            )

            todos = result.all()

            if todos:
                return [
                    TodoDTO(
                        id=todo.id,
                        title=todo.title,
                        description=todo.description,
                        state=todo.state,
                    )
                    for todo in todos
                ]

            return []
        except Exception as e:
            logging.error(f'Erro ao buscar ToDos: {e}')
            raise

    async def get_by_id(self, id: int) -> Optional[TodoDTO]:
        try:
            result = await self.session.execute(
                select(Todo).where(Todo.id == id)
            )
            todo = result.scalar()

            if todo:
                return TodoDTO(
                    id=todo.id,
                    title=todo.title,
                    description=todo.description,
                    state=todo.state,
                )

            return None
        except Exception as e:
            logging.error(f'Erro ao buscar ToDo: {e}')
            raise

    async def create(self, todo: TodoCreateDTO) -> TodoDTO:
        try:
            todo_db = Todo(
                title=todo.title,
                description=todo.description,
                state=todo.state,
                user_uuid=str(uuid4()),
            )

            self.session.add(todo_db)
            await self.session.commit()
            await self.session.refresh(todo_db)

            return TodoDTO(
                id=todo_db.id,
                title=todo_db.title,
                description=todo_db.description,
                state=todo_db.state,
            )
        except Exception as e:
            logging.error(f'Erro ao criar ToDo: {e}')
            raise

    async def update(self, id: int, new_state: str):
        try:
            await self.session.execute(
                update(Todo).where(Todo.id == id).values(state=new_state)
            )
            await self.session.commit()
        except Exception as e:
            logging.error(f'Erro ao atualizar ToDo: {e}')
            raise

    async def delete(self, id: int):
        try:
            await self.session.execute(delete(Todo).where(Todo.id == id))
            await self.session.commit()
        except Exception as e:
            logging.error(f'Erro ao deletar ToDo: {e}')
            raise
