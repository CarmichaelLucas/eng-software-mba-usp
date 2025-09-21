import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import jwt
from jwt.exceptions import InvalidTokenError

from auth import settings
from opentelemetry.trace import get_tracer

tracer = get_tracer('auth')

class JWTUtil:
    @staticmethod
    def _create_access_token(
        data: dict, expires_delta: timedelta | None = None
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)

        to_encode.update({'exp': expire})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key, algorithm=settings.algorithm
        )

        return encoded_jwt, to_encode['exp']

    @staticmethod
    def token(entity_uuid: str) -> str:
        data = {'sub': str(entity_uuid)}
        access_token_expire = timedelta(
            minutes=settings.access_token_expire_minutes
        )

        return JWTUtil._create_access_token(
            data=data, expires_delta=access_token_expire
        )

    @staticmethod
    def refresh(entity_id: str) -> str:
        expire = timedelta(days=settings.refresh_token_expire_days)

        payload = {
            'sub': str(entity_id),
            'exp': datetime.utcnow() + expire,
        }

        return jwt.encode(payload, settings.secret_key, settings.algorithm)

    @staticmethod
    def verify(token: str) -> Optional[str]:
        with tracer.start_as_current_span("auth.util.verify"):
            try:
                payload = jwt.decode(
                    token, settings.secret_key, algorithms=[settings.algorithm]
                )

                return payload.get('sub')
            except InvalidTokenError as e:
                logging.error(f'Erro ao decidificar TOKEN: {e}')
                raise
