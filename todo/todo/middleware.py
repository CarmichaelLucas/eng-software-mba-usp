from fastapi import HTTPException, Request, status
import logging

from opentelemetry.trace import Status, StatusCode
from opentelemetry.trace import get_tracer

tracer = get_tracer('todo')

async def validate_token(request: Request):
    with tracer.start_as_current_span("todo.middleware.validate_token") as span:
        try:
            authorization: str = request.headers.get('Authorization')

            if not authorization or not authorization.startswith('Bearer '):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Token ausente ou inválido.',
                )

            token = authorization.split(' ')[1]
            
            from todo.app import request_client
            response = await request_client.get(headers=_auth_headers(token=token))

            if not response['allowed']:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Sem permissão para executar a ação.',
                )

            span.set_status(Status(StatusCode.OK))
            return response['user_uuid']
        except Exception as e:
            logging.error(f'Erro ao validar token: {e}')
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise

def _auth_headers(token: str) -> dict:
    return {'Authorization': f'Bearer {token}'}
