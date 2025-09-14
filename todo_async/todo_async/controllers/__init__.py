from fastapi import APIRouter

from todo_async.controllers.todo_controller import (
    router as todo_async_router,
)

main_router = APIRouter()


main_router.include_router(todo_async_router, tags=['ToDo'])
