import asyncio
import json
import logging

from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)

from todo_async import settings
from todo_async.messaging.consumer import Consumer

from opentelemetry.instrumentation.aiokafka import AIOKafkaInstrumentor
from opentelemetry.propagate import extract
from opentelemetry.context import attach, detach
from opentelemetry.propagate import inject
from opentelemetry.trace import get_tracer

AIOKafkaInstrumentor().instrument()

tracer = get_tracer('todo_async')


class KafkaService:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def producer(self, topic: str, msg: dict):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers
            )
            await producer.start()

            try:
                headers = {}
                inject(headers)
                kafka_headers = [(k, v.encode()) for k, v in headers.items()]

                with tracer.start_as_current_span("kafka_produce", attributes={
                    "messaging.system": "kafka",
                    "messaging.destination": topic,
                    "messaging.operation": "send"
                }):
                    await producer.send_and_wait(
                        topic,
                        json.dumps(msg).encode(),
                        headers=kafka_headers
                    )
            finally:
                await producer.stop()

        except Exception as e:
            logging.error(f'Erro ao produzir mensagem no Kafka: {e}')

    async def consumer(self, topic: str, service: Consumer):
        consumer = AIOKafkaConsumer(
            topic,
            loop=self.loop,
            bootstrap_servers=settings.kafka_bootstrap_servers,
        )

        try:
            await consumer.start()

        except Exception as e:
            logging.error(f'Erro Kafka: {e}')
            return

        try:
            async for msg in consumer:
                headers = {k: v.decode() for k, v in msg.headers or []}
                ctx = extract(headers)
                token = attach(ctx)
                try:
                    with tracer.start_as_current_span("kafka_consume", attributes={
                        "messaging.system": "kafka",
                        "messaging.destination": topic,
                        "messaging.operation": "receive",
                        "messaging.kafka.partition": msg.partition,
                        "messaging.kafka.offset": msg.offset,
                    }):
                        await service.call(msg)
                finally:
                    detach(token)
        except Exception as e:
            logging.error(f'Erro consumir mensagem Kafka: {e}')
        finally:
            await consumer.stop()
