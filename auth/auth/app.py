import logging

from auth.instrumentation.tracing import *
from auth.instrumentation.metrics import *

from contextlib import asynccontextmanager
from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider

from auth.controllers import main_router
from auth.database import engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@asynccontextmanager
async def lifespan(app):
    yield
    
    if engine:
        await engine.dispose()
        logger.info("Engine fechada.")

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app, meter_provider=get_meter_provider())

app.include_router(main_router, prefix='/api/v1')
