import aiohttp
import logging
from fastapi import HTTPException, status
from tenacity import retry, wait_exponential, stop_after_attempt

from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from opentelemetry.trace import get_tracer
from opentelemetry.trace import Status, StatusCode

AioHttpClientInstrumentor().instrument()
tracer = get_tracer('todo')


class Request:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        # timeout = aiohttp.ClientTimeout(total=60)  # 5s para tudo
        # connector = aiohttp.TCPConnector(limit=100, ttl_dns_cache=300)
        self.session = aiohttp.ClientSession()
        #     timeout=timeout, connector=connector
        # )

    @retry(wait=wait_exponential(multiplier=0.5), stop=stop_after_attempt(3))
    async def get(self, params: dict = None, headers: dict = None) -> dict:
        with tracer.start_as_current_span("todo.integration.get") as span:
            async with self.session.get(
                self.base_url, headers=headers, params=params
            ) as response:
                try:
                    if response.status != status.HTTP_200_OK:
                        raise HTTPException(
                            status_code=response.status,
                            detail=f'Erro: {await response.text()}',
                        )

                    span.set_status(Status(StatusCode.OK))
                    return await response.json()
                except Exception as e:
                    span.set_status(Status(StatusCode.ERROR, str(e)))
                    logging.error(f'Erro ao buscar ToDo: {e}')
                    raise

    async def close(self):
        await self.session.close()
