import aiohttp
from fastapi import HTTPException, status

from opentelemetry.instrumentation.aiohttp_client import (
    AioHttpClientInstrumentor
)
from opentelemetry.trace import get_tracer

AioHttpClientInstrumentor().instrument()

tracer = get_tracer('todo')


class Request:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def get(self, params: dict = None, headers: dict = None) -> dict:
        with tracer.start_as_current_span("todo.integration.get"):
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.base_url, headers=headers, params=params
                ) as response:
                    if response.status != status.HTTP_200_OK:
                        raise HTTPException(
                            status_code=response.status,
                            detail=f'Erro: {await response.text()}',
                        )

                    data = await response.json()

            return data
