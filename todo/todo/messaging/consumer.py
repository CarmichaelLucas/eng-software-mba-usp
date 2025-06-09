import json
import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from todo.database import get_session
from todo.messaging import TOPICS


class Consumer:
    def __init__(
        self,
        session: AsyncSession = Depends(get_session)
    ):
        self.session = session

    async def call(self, msg):
        try:
            service = TOPICS[msg.topic](session=self.session)
            await service.consume(msg=self._encode_json(msg))
        except Exception as e:
            # TODO: DQL
            logging.error(f'Enviando para DLQ: {msg}, Erro: {e}')

    def _encode_json(msg):
        to_load = msg.value.decode('utf-8')
        return json.loads(to_load)
