import logging

from todo_async.instrumentation.tracing import *
from todo_async.instrumentation.metrics import *

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider

from todo_async.controllers import main_router
from todo_async.messaging.kafka_service import KafkaService
from todo_async.database import engine

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

add_pagination(app)
app.include_router(main_router, prefix='/api/v1')
