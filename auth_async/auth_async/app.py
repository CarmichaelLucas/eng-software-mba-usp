import logging

from auth_async.instrumentation.tracing import *
from auth_async.instrumentation.metrics import *

from contextlib import asynccontextmanager
from fastapi import FastAPI

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider

from auth_async.controllers import main_router
from auth_async.messaging.kafka_service import KafkaService
from auth_async.database import engine

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

kafka_service: KafkaService | None = None

@asynccontextmanager
async def lifespan(app):
    global kafka_service
    kafka_service = KafkaService()
    await kafka_service.start()
    yield
    await kafka_service.stop()

    if engine:
        await engine.dispose()
        logger.info("Engine fechada.")

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app, meter_provider=get_meter_provider())

app.include_router(main_router, prefix='/api/v1')
