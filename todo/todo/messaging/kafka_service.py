import asyncio
import json
import logging
from typing import List

from fastapi import Depends

from aiokafka import (
    AIOKafkaConsumer,
    AIOKafkaProducer,
)

from todo import settings
from todo.messaging.consumer import Consumer


class KafkaService:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def producer(
        self,
        topic: str,
        msg: dict
    ):
        try:
            producer = AIOKafkaProducer(
                bootstrap_servers=settings.kafka_bootstrap_servers
            )
            await producer.start()

            try:
                await producer.send_and_wait(
                    topic,
                    self._serializer(msg)
                )
            finally:
                await producer.stop()

        except Exception as e:
            logging.error(f'Erro ao produzir mensagem no Kafka: {e}')

    async def consumer(
        self,
        service: object = Depends(Consumer)
    ):
        consumer = AIOKafkaConsumer(
            self.topic,
            loop=self.loop,
            bootstrap_servers=settings.kafka_bootstrap_servers,
        )

        try:
            await consumer.start()

        except Exception as e:
            logging.error(f'Erro ao consumir mensagem do Kafka: {e}')
            return

        try:
            async for msg in consumer:
                await service.call(msg)

        finally:
            await consumer.stop()

    def _serializer(msg: List):
        return json.dumps(msg).encode()
