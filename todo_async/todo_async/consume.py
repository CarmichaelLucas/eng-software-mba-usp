import asyncio
import logging

from todo_async.instrumentation.tracing import *
from todo_async.instrumentation.metrics import *

from contextlib import asynccontextmanager
from fastapi import FastAPI

from todo_async import settings
from todo_async.messaging.kafka_service import KafkaService

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.metrics import get_meter_provider

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

kafka_service: KafkaService | None = None

@asynccontextmanager
async def lifespan(app):
    global kafka_service
    kafka_service = KafkaService()
    await kafka_service.start()

    from todo_async.messaging.consumer import Consumer
    asyncio.create_task(
        kafka_service.consume(
            topic=settings.token_validation_response_topic,
            service=Consumer()
        )
    )

    yield

    await kafka_service.stop()

app = FastAPI(lifespan=lifespan)
FastAPIInstrumentor.instrument_app(app, meter_provider=get_meter_provider())
