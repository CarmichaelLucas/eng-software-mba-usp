from sqlalchemy.ext.asyncio import AsyncSession

from auth.schemas.auth_dto import (
    AuthPublicRequest,
    AuthPublicResponse,
    AuthPublicUserResponse,
)

from auth.services.user_service import UserService
from auth.utils.jwt_util import JWTUtil

from opentelemetry.trace import get_tracer

tracer = get_tracer('auth')


class AuthService:
    def __init__(self, session: AsyncSession):
        self.user_service = UserService(session=session)
        self.jwt = JWTUtil()

    async def token(self, data: AuthPublicRequest) -> AuthPublicResponse:
        user = await self.user_service.get_by_email(email=data.email)
        is_password_valid = await self.user_service.verify_password(
            email=data.email, password=data.password
        )

        if not is_password_valid:
            raise ValueError('Credenciais inválidas')

        access_token, expire_in = self.jwt.token(entity_uuid=user.uuid)

        return AuthPublicResponse(
            access_token=access_token, expire_in=int(expire_in.strftime('%s'))
        )

    async def validate(self, token: str) -> AuthPublicUserResponse:
        with tracer.start_as_current_span("auth.service.validate") as span:
            user_uuid = self.jwt.verify(token=token)

            user = await self.user_service.get_by_uuid(uuid=user_uuid)

            if user is None:
                raise Exception('Usuário não encontrado')

            return AuthPublicUserResponse(
                allowed=True,
                user_uuid=user.uuid,
            )
