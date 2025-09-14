from functools import lru_cache

from todo_async.messaging.consumer import Consumer
from todo_async.messaging.kafka_service import (
    KafkaService as PubSubService,
)


@lru_cache()
class ProducerService:
    def __init__(self):
        self.messaging = PubSubService()

    async def call(self, topic: str, msg: dict):
        return await self.messaging.producer(topic=topic, msg=msg)


@lru_cache()
class ConsumerService:
    def __init__(self):
        self.messaging = PubSubService()

    async def call(self, topic: str):
        return await self.messaging.consumer(topic=topic, service=Consumer())
