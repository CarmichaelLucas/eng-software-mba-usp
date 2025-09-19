import logging

from sqlalchemy.ext.asyncio import AsyncSession

from todo_async.repositories.todo_repository import TodoRepository
from todo_async.schemas.todo_dto import (
    TodoCreateDTO,
    TodoDTO
)

from opentelemetry.trace import get_tracer

tracer = get_tracer('todo_async')


class TodoService:
    def __init__(self, session: AsyncSession):
        self.repository = TodoRepository(session=session)

    async def create(self, todo: TodoCreateDTO, user_uuid: str) -> TodoDTO:
        with tracer.start_as_current_span("todo_async.service.create"):
            return await self.repository.create(todo=todo, user_uuid=user_uuid)

    async def consume(self, msg):
        with tracer.start_as_current_span("todo_async.service.consumer"):
            try:
                if msg['allowed']:
                    todo = TodoCreateDTO(
                        title=msg['title'],
                        description=msg['description'],
                        state=msg['state'],
                    )

                    await self.create(todo=todo, user_uuid=msg['user_uuid'])
                else:
                    raise Exception('Não autorizado a inclusão do ToDo.')
            except Exception as e:
                logging.error(f'Erro ao processar consumo: {e}')
                raise
