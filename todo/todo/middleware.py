from fastapi import HTTPException, Request, status

from todo import settings
from todo.integrations.request import (
    Request as RequestHTTP,
)

from opentelemetry.trace import get_tracer

tracer = get_tracer('todo')

async def validate_token(request: Request):
    with tracer.start_as_current_span("todo.middleware.validate_token"):
        authorization: str = request.headers.get('Authorization')

        if not authorization or not authorization.startswith('Bearer '):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token ausente ou inválido.',
            )

        token = authorization.split(' ')[1]
        request = RequestHTTP(
            base_url=f'{settings.auth_base_url}/api/v1/oauth/validate-token'
        )
        response = await request.get(headers=_auth_headers(token=token))

        if response['allowed']:
            return response['user_uuid']

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Sem permissão para executar a ação.',
        )


def _auth_headers(token: str) -> dict:
    return {'Authorization': f'Bearer {token}'}
