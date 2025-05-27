from sqlalchemy.ext.asyncio import AsyncSession

from project.schemas.auth_dto import (
    AuthLoginDTO,
    AuthResponseDTO,
)
from project.services.user_service import UserService
from project.utils.jwt_util import JWTUtil


class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_service = UserService(session=session)
        self.jwt = JWTUtil()

    async def token(self, data: AuthLoginDTO) -> AuthResponseDTO:
        entity = await self.user_service.get_by_email(email=data.email)

        is_password_valid = await self.user_service.verify_password(
            email=data.email, password=data.password
        )

        if not entity and not is_password_valid:
            raise ValueError('Credenciais inválidas')

        auth = AuthResponseDTO(
            access_token=self.jwt.token(entity_id=entity.id),
            refresh_token=self.jwt.refresh(entity_id=entity.id),
        )

        return auth
