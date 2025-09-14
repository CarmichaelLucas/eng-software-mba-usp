import logging

from auth_async.instrumentation.tracing import *
from auth_async.instrumentation.metrics import *

from contextlib import asynccontextmanager
from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider

from auth_async.controllers import main_router

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


@asynccontextmanager
async def lifespan(app):
    yield

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app, meter_provider=get_meter_provider())

app.include_router(main_router, prefix='/api/v1')
