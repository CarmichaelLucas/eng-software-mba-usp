from fastapi import HTTPException, Request, status

from opentelemetry.trace import get_tracer

tracer = get_tracer('todo_async')


async def validate_token_messaging(request: Request):
    with tracer.start_as_current_span(
        "todo_async.kafka_create_todo_middleware",
        attributes={
            "messaging.system": "kafka",
            "messaging.destination": "token_validation_request",
            "messaging.operation": "consume"
        }
    ):
        authorization: str = request.headers.get('Authorization')

        if not authorization or not authorization.startswith('Bearer '):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Token ausente ou inválido.',
            )

        token = authorization.split(' ')[1]
        return token
