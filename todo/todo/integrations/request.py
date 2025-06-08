import aiohttp

from fastapi import HTTPException


class Request():
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def get(
        self,
        params: dict = None,
        headers: dict = None
    ) -> dict:

        async with aiohttp.ClientSession() as session:
            async with session.get(
                self.base_url,
                headers=headers,
                params=params
            ) as response:
                if response.status != 200:
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Erro ao buscar dados: {await response.text()}"
                    )

                data = await response.json()
    
        return data
