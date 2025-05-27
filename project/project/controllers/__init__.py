from fastapi import APIRouter

from project.controllers.auth_controller import router as auth_router
from project.controllers.user_controller import router as user_router

main_router = APIRouter()


main_router.include_router(auth_router, tags=['Auth'])
main_router.include_router(user_router, tags=['Users'])
