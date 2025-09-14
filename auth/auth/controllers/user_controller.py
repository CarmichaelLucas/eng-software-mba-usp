from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_session
from auth.schemas.user_dto import (
    UserDTO,
    UserPublicRequest,
    UserPublicResponse,
)
from auth.services.user_service import UserService

router = APIRouter()


@router.post(
    '/users/',
    response_model=UserPublicResponse,
    status_code=status.HTTP_201_CREATED,
    description='Criar Usuários',
)
async def create(
    params: UserPublicRequest, session: AsyncSession = Depends(get_session)
):
    try:
        user = UserDTO(**dict(params))
        service = UserService(session=session)
        return await service.create(user=user)
    except (Exception, ValueError) as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(e)
        )
