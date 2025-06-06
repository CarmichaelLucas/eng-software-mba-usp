from fastapi import FastAPI
from fastapi_pagination import add_pagination

from todo.controllers import main_router

app = FastAPI(title='Project ToDo', description='API para gerir tarefas')

add_pagination(app)

app.include_router(main_router, prefix='/api/v1')
