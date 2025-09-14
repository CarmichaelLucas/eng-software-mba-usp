import asyncio
import logging

from auth_async.instrumentation.tracing import *
from auth_async.instrumentation.metrics import *

from contextlib import asynccontextmanager
from fastapi import FastAPI

from auth_async import settings
from auth_async.services.messaging_service import ConsumerService

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

@asynccontextmanager
async def lifespan(app):
    consumer = ConsumerService()
    asyncio.create_task(
        consumer.call(topic=settings.token_validation_request_topic)
    )
    yield

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app, meter_provider=get_meter_provider())
