from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from project.database import get_session
from project.schemas.auth_dto import (
    AuthLoginDTO,
    AuthResponseDTO,
)
from project.services.auth_service import AuthService

router = APIRouter()


@router.post(
    '/login',
    response_model=AuthResponseDTO,
    status_code=status.HTTP_201_CREATED,
    description='Login Usuários',
)
async def login(
    params: AuthLoginDTO, session: AsyncSession = Depends(get_session)
):
    try:
        service = AuthService(session=session)
        return await service.token(data=params)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
