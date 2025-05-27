import logging
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from project.models.user_model import User
from project.schemas.user_dto import UserCreateDTO, UserDTO
from project.utils.encode_util import EncodeUtil


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.encode = EncodeUtil()

    async def create(self, user: UserCreateDTO) -> UserDTO:
        try:
            db_user = User(
                email=user.email,
                username=user.username,
                password=self.encode.crypt(user.password),
            )
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return UserDTO(
                id=db_user.id, username=db_user.username, email=db_user.email
            )
        except Exception as e:
            logging.error(f'Erro ao criar Usuário: {e}')
            raise

    async def get_by_email(self, email: str) -> Optional[UserDTO]:
        try:
            result = await self.session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar()

            if user:
                return UserDTO(
                    id=user.id, username=user.username, email=user.email
                )

            return None
        except Exception as e:
            logging.error(f'Erro ao buscar usuário por email: {e}')
            raise

    async def verify_password(self, email: str, password: str) -> bool:
        try:
            result = await self.session.execute(
                select(User).where(User.email == email)
            )
            user = result.scalar()

            if user:
                return self.encode.verify(
                    password=password, password_hash=user.password
                )

            return False
        except Exception as e:
            logging.error(f'Erro de credenciais inválida: {e}')
            raise
