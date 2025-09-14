from fastapi import APIRouter

from auth.controllers.auth_controller import router as auth_router
from auth.controllers.user_controller import router as user_router

main_router = APIRouter()


main_router.include_router(auth_router, tags=['Auth'])
main_router.include_router(user_router, tags=['Users'])
