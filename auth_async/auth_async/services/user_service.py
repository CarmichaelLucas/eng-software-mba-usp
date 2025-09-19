import logging

from sqlalchemy.ext.asyncio import AsyncSession

from auth_async.repositories.user_repository import UserRepository
from auth_async.schemas.user_dto import (
    UserDTO,
)
from auth_async.utils.encode_util import EncodeUtil

from opentelemetry.trace import get_tracer

tracer = get_tracer('todo_async')


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session=session)
        self.encode = EncodeUtil()

    async def get_by_email(self, email: str) -> UserDTO:
        return await self.repository.get_by_email(email=email)

    async def get_by_uuid(self, uuid: str) -> UserDTO:
        with tracer.start_as_current_span("auth_async.service.select") as span:
            return await self.repository.get_by_uuid(uuid=uuid)

    async def verify_password(self, email: str, password: str) -> bool:
        user = await self.get_by_email(email=email)

        if not user:
            return False

        if not self.encode.verify(
            password=password, password_hash=user.password
        ):
            return False

        return True

    async def create(self, user: UserDTO) -> UserDTO:
        try:
            if await self.get_by_email(email=user.email):
                raise ValueError('Usuário já existe')

            return await self.repository.create(user=user)
        except Exception as e:
            logging.error(f'Erro ao criar Usuário: {e}')
            raise e
