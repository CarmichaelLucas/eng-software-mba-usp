from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_session
from auth.schemas.auth_dto import (
    AuthPublicRequest,
    AuthPublicResponse,
    AuthPublicUserResponse,
)
from auth.services.auth_service import AuthService
from opentelemetry.trace import get_tracer

tracer = get_tracer('auth')
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
    with tracer.start_as_current_span("auth.controller.validate_token"):
        try:
            service = AuthService(session=session)
            return await service.validate(token=token)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Credenciais inválida. Realize o login!',
                headers={'WWW-Authenticate': 'Bearer'},
            )
