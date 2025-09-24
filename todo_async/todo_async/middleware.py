from fastapi import HTTPException, Request, status

from opentelemetry.trace import get_tracer
from opentelemetry.trace import Status, StatusCode

tracer = get_tracer('todo_async')


async def validate_token_messaging(request: Request):
    with tracer.start_as_current_span("todo_async.middleware.extract_token") as span:
        try:
            authorization: str = request.headers.get('Authorization')

            if not authorization or not authorization.startswith('Bearer '):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Token ausente ou inválido.',
                )

            token = authorization.split(' ')[1]
            span.set_status(Status(StatusCode.OK))
            return token
        except Exception as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token ausente ou inválido.',
            )
