import logging

from sqlalchemy.ext.asyncio import AsyncSession

from auth_async import settings
from auth_async.schemas.auth_dto import (
    AuthPublicRequest,
    AuthPublicResponse,
    AuthPublicUserResponse,
)

from auth_async.services.user_service import UserService
from auth_async.utils.jwt_util import JWTUtil

from opentelemetry.trace import get_tracer

tracer = get_tracer('auth_async')


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
        with tracer.start_as_current_span("auth_async.validate_token") as span:
            user_uuid = self.jwt.verify(token=token)

            user = await self.user_service.get_by_uuid(uuid=user_uuid)

            if user is None:
                raise Exception('Usuário não encontrado')

            return AuthPublicUserResponse(
                allowed=True,
                user_uuid=user.uuid,
            )

    async def consume(self, msg: dict):
        with tracer.start_as_current_span("auth_async.consume") as span:
            try:
                auth = await self.validate(token=msg['token'])

                if auth.allowed:
                    await self.produce(
                        topic=settings.token_validation_response_topic,
                        msg={
                            'allowed': auth.allowed,
                            'user_uuid': auth.user_uuid,
                            'title': msg['todo']['title'],
                            'description': msg['todo']['description'],
                            'state': msg['todo']['state'],
                        },
                    )

            except Exception as e:
                logging.error(f'Erro ao validar token: {e}')
                raise

    @classmethod
    async def produce(self, topic: str, msg: dict):
        from auth_async.services.messaging_service import ProducerService
        try:
            await ProducerService().call(topic=topic, msg=msg)
        except Exception as e:
            logging.error(f'Erro ao produzir mensagem: {e}')
            raise
