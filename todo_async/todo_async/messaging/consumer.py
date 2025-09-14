import json
import logging

from todo_async.database import AsyncSessionLocal
from todo_async.messaging import TOPICS


class Consumer:
    @classmethod
    async def call(self, msg):
        async with AsyncSessionLocal() as session:
            try:
                data = json.loads(msg.value.decode('utf-8'))
                service = TOPICS[msg.topic](session=session)
                await service.consume(msg=data)
            except Exception as e:
                # TODO: DQL
                logging.error(f'Enviando para DLQ: {msg}, Erro: {e}')
            finally:
                await session.close()
