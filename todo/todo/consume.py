from fastapi import FastAPI
import asyncio

from todo.services.messaging_service import ConsumerService

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    consumer = ConsumerService()
    asyncio.create_task(consumer.call())
