import logging

from sqlalchemy.ext.asyncio import AsyncSession

from todo_async.models.todo_model import Todo
from todo_async.schemas.todo_dto import (
    TodoCreateDTO,
    TodoDTO,
)

from opentelemetry.trace import get_tracer

tracer = get_tracer('todo_async')


class TodoRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, todo: TodoCreateDTO, user_uuid: str) -> TodoDTO:
        with tracer.start_as_current_span("db.todo_async.insert", attributes={
            "db.system": "postgresql",
            "db.operation": "INSERT",
            "db.sql.table": "todo_async",
            "enduser.id": user_uuid,
        }):
            try:
                todo_db = Todo(
                    title=todo.title,
                    description=todo.description,
                    state=todo.state,
                    user_uuid=user_uuid,
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
