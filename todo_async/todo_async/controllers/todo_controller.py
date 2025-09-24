from fastapi import APIRouter, Depends, HTTPException, status

from todo_async import settings
from todo_async.schemas.todo_dto import (
    TodoCreateDTO,
)

from ..middleware import (
    validate_token_messaging,
)

from opentelemetry.trace import get_tracer
from opentelemetry.trace import Status, StatusCode

tracer = get_tracer('todo_async')
router = APIRouter()


@router.post(
    '/todos/async',
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    description='Criar Todo Async',
)
async def create_async(
    params: TodoCreateDTO,
    token: dict = Depends(validate_token_messaging),
):
    with tracer.start_as_current_span("todo_async.controller.create") as span:
        try:
            from todo_async.app import kafka_service
            await kafka_service.produce(
                topic=settings.token_validation_request_topic,
                msg={
                    'token': token,
                    'todo': {
                        'title': params.title,
                        'description': params.description,
                        'state': params.state,
                    },
                },
            )
            span.set_status(Status(StatusCode.OK))
            return {'message': 'ToDo sendo criado. Aguarde alguns segundos!'}
        except (Exception, ValueError) as e:
            span.set_status(Status(StatusCode.ERROR, str(e)))
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
            )
