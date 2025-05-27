from fastapi import FastAPI

from project.controllers import main_router

app = FastAPI(
    title='Project A', description='API para autenticar e autorizar Usuários'
)


app.include_router(main_router, prefix='/api/v1')
