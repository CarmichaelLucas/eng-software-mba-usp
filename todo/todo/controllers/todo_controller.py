from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from todo.database import get_session
from todo.schemas.todo_dto import (
    TodoCreateDTO,
    TodoDTO,
    TodoFilterDTO,
)
from todo.services.todo_service import TodoService

from ..middleware import validate_token

router = APIRouter()


@router.post(
    '/todos/',
    response_model=TodoDTO,
    status_code=status.HTTP_201_CREATED,
    description='Criar Todo',
)
async def create(
    params: TodoCreateDTO,
    session: AsyncSession = Depends(get_session),
    user_uuid: dict = Depends(validate_token)
):
    try:
        service = TodoService(session=session)
        return await service.create(todo=params, user_uuid=user_uuid)
    except (Exception, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.get(
    '/todos/',
    response_model=Page[TodoDTO],
    status_code=status.HTTP_200_OK,
    description='Listar Todos',
)
async def get_all(
    filters: Annotated[TodoFilterDTO, Query()],
    session: AsyncSession = Depends(get_session)
):
    try:
        service = TodoService(session=session)
        todos = await service.get_all(filters=filters)
        return paginate(todos)
    except (Exception, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.put(
    '/todos/{id}',
    response_model=dict,
    status_code=status.HTTP_200_OK,
    description='Atualizar Todo',
)
async def update(
    id: int, state: str, session: AsyncSession = Depends(get_session)
):
    try:
        service = TodoService(session=session)
        await service.update(id=id, new_state=state)
        return {'message': 'ToDo atualizado com sucesso.'}
    except (Exception, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )


@router.delete(
    '/todos/{id}',
    status_code=status.HTTP_204_NO_CONTENT,
    description='Atualizar Todo',
)
async def delete(id: int, session: AsyncSession = Depends(get_session)):
    try:
        service = TodoService(session=session)
        return await service.delete(id=id)
    except (Exception, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
