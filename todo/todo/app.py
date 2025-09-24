import logging

from todo.instrumentation.tracing import *
from todo.instrumentation.metrics import *

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider

from todo.controllers import main_router
from todo.integrations.request import Request as RequestHTTP
from todo import settings
from todo.database import engine


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

request_client: RequestHTTP | None = None

@asynccontextmanager
async def lifespan(app):
    global request_client

    # --- Startup ---
    request_client = RequestHTTP(base_url=f'{settings.auth_base_url}/api/v1/oauth/validate-token')
    logger.info("Request client inicializado.")

    yield  # --- aqui roda a aplicação ---

    # --- Shutdown ---
    if request_client:
        await request_client.close()
        logger.info("Request client fechado.")
    
    if engine:
        await engine.dispose()
        logger.info("Engine fechada.")

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app, meter_provider=get_meter_provider())

add_pagination(app)

app.include_router(main_router, prefix='/api/v1')
