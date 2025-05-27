import logging

from sqlalchemy.ext.asyncio import AsyncSession

from project.repositories.user_repository import UserRepository
from project.schemas.user_dto import (
    UserCreateDTO,
    UserDTO,
)


class UserService:
    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session=session)

    async def get_by_email(self, email: str) -> UserDTO:
        return await self.repository.get_by_email(email=email)

    async def verify_password(self, email: str, password: str) -> bool:
        return await self.repository.verify_password(
            email=email, password=password
        )

    async def create(self, user: UserCreateDTO) -> UserDTO:
        try:
            if await self.get_by_email(email=user.email):
                raise ValueError('Usuário já existe')

            entity = await self.repository.create(user=user)
            return entity
        except Exception as e:
            logging.error(f'Erro ao criar Usuário: {e}')
            raise e
