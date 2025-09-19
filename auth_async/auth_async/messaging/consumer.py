import json
import logging

from auth_async.database import AsyncSessionLocal
from auth_async.messaging import TOPICS

from auth_async import settings


class Consumer:
    @classmethod
    async def call(self, msg):
        async with AsyncSessionLocal() as session:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                service = TOPICS[msg.topic](session=session)
                await service.consume(msg=data)
            except Exception as e:
                logging.error(f'Enviando para DLQ: {msg}, Erro: {e}')

                dlq_payload = {
                    "original_topic": msg.topic,
                    "partition": msg.partition,
                    "offset": msg.offset,
                    "error": str(e),
                    "value": msg.value.decode("utf-8"),
                }

                # envia para DLQ
                from auth_async.app import kafka_service
                await kafka_service.produce(
                    topic=settings.auth_dlq_topic, 
                    msg=dlq_payload
                )
            finally:
                await session.close()
