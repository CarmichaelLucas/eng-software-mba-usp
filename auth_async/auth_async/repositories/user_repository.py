import logging
from typing import Optional
from uuid import uuid4

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from auth_async.models.user_model import User
from auth_async.schemas.user_dto import UserDTO
from auth_async.utils.encode_util import EncodeUtil

from opentelemetry.trace import get_tracer

tracer = get_tracer('auth_async')


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.encode = EncodeUtil()

    async def create(self, user: UserDTO) -> UserDTO:
        try:
            db_user = User(
                email=user.email,
                name=user.name,
                username=user.username,
                password=self.encode.crypt(user.password),
                uuid=uuid4(),
            )
            self.session.add(db_user)
            await self.session.commit()
            await self.session.refresh(db_user)
            return UserDTO(
                id=db_user.id,
                name=db_user.name,
                username=db_user.username,
                email=db_user.email,
                uuid=str(db_user.uuid),
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
                    id=user.id,
                    name=user.name,
                    username=user.username,
                    email=user.email,
                    password=user.password,
                    uuid=str(user.uuid),
                )

            return None
        except Exception as e:
            logging.error(f'Erro ao buscar usuário por email: {e}')
            raise

    async def get_by_uuid(self, uuid: str) -> Optional[UserDTO]:
        with tracer.start_as_current_span("db.auth_async.select", attributes={
            "db.system": "postgresql",
            "db.operation": "SELECT",
            "db.sql.table": "auth_async",
            "enduser.id": uuid,
        }):       
            try:
                result = await self.session.execute(
                    select(User).where(User.uuid == uuid)
                )
                user = result.scalar()

                if user:
                    return UserDTO(
                        id=user.id,
                        name=user.name,
                        username=user.username,
                        email=user.email,
                        uuid=str(user.uuid),
                    )

                return None
            except Exception as e:
                logging.error(f'Erro ao buscar usuário por email: {e}')
                raise
