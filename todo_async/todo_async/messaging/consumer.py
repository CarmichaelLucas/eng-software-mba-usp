import json
import logging

from todo_async import settings
from todo_async.database import AsyncSessionLocal
from todo_async.messaging import TOPICS

from opentelemetry.trace import get_tracer
from opentelemetry.trace import Status, StatusCode

tracer = get_tracer("todo_async")

class Consumer:
    @classmethod
    async def call(self, msg):
        async with AsyncSessionLocal() as session:
            with tracer.start_as_current_span("consumer.dispatch", attributes={
                "messaging.topic": msg.topic,
                "messaging.message_length": len(msg.value),
            }) as span:
                try:
                    data = json.loads(msg.value.decode('utf-8'))
                    service = TOPICS[msg.topic](session=session)
                    await service.consume(msg=data)
                    span.set_status(Status(StatusCode.OK))
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    logging.error(f'Enviando para DLQ: {msg}, Erro: {e}')

                    dlq_payload = {
                        "original_topic": msg.topic,
                        "partition": msg.partition,
                        "offset": msg.offset,
                        "error": str(e),
                        "value": msg.value.decode("utf-8"),
                    }

                    # envia para DLQ
                    from todo_async.consume import kafka_service
                    await kafka_service.produce(
                        topic=settings.todo_dlq_topic, 
                        msg=dlq_payload
                    )
                finally:
                    await session.close()
