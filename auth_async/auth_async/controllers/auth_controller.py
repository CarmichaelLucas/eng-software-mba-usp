from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth_async.database import get_session
from auth_async.schemas.auth_dto import (
    AuthPublicRequest,
    AuthPublicResponse,
    AuthPublicUserResponse,
)
from auth_async.services.auth_service import AuthService

router = APIRouter()


@router.post(
    '/oauth/login',
    response_model=AuthPublicResponse,
    status_code=status.HTTP_201_CREATED,
    description='Login Usuários',
)
async def login(
    params: Annotated[AuthPublicRequest, Depends()],
    session: AsyncSession = Depends(get_session),
):
    try:
        service = AuthService(session=session)
        return await service.token(data=params)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)
        )


@router.get(
    '/oauth/validate-token',
    response_model=AuthPublicUserResponse,
    description='Validar TOKEN de acesso',
)
async def validate_token(
    token: Annotated[str, Depends(OAuth2PasswordBearer(tokenUrl='token'))],
    session: AsyncSession = Depends(get_session),
):
    try:
        service = AuthService(session=session)
        return await service.validate(token=token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Credenciais inválida. Realize o login!',
            headers={'WWW-Authenticate': 'Bearer'},
        )
