from fastapi import APIRouter

from todo.controllers.todo_controller import (
    router as todo_router,
)

main_router = APIRouter()


main_router.include_router(todo_router, tags=['ToDo'])
